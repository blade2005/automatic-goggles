import decimal
import boto3
import boto3.dynamodb.types
import json
import logging
import os
import pickle
import json
from json import JSONEncoder
import datetime

FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
deserializer = boto3.dynamodb.types.TypeDeserializer()

RESPONSE_DEFAULT_HEADERS = {"Content-Type": "application/json"}

class PythonObjectEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, (decimal.Decimal,)):
            return float(obj)
        elif isinstance(
            obj, (list, dict, str, int, float, bool, type, type(None), bytes)
        ):
            return JSONEncoder.default(self, obj)
        else:
            logging.warning(
                "Unable to find matching encoder for type %s. Using pickle",
                str(type(obj)),
            )
        return {"_python_object": pickle.dumps(obj)}

def generate_response(status, data, headers=None):
    if not headers:
        headers = RESPONSE_DEFAULT_HEADERS
    return {
        "statusCode": status,
        "headers": headers,
        "body": json.dumps(data, cls=PythonObjectEncoder, sort_keys=True),
    }

def display_selected_entries(table, event):
    try:
        int(event['pathParameters']['id_number'])
    except ValueError:
        return generate_response(400, {'error': 'Must provide integer for id_number'})
    results = table.get_item(Key={'id': int(event['pathParameters']['id_number'])})
    data = results['Item']
    data['id'] = int(data['id'])
    return generate_response(200, data)

def display_all_entries(table, event):
    results = table.scan()
    LOGGER.info(results['Items'])
    return generate_response(200, [int(r['id']) for r in results['Items']])

def main(event, context):
    resp = generate_response(
        400, {'error': 'Invalid resource', 'resource': event['resource']})
    func_calls = {
        '/id/{id_number}': {'func': display_selected_entries},
        '/id': {'func': display_all_entries},
    }
    LOGGER.info('Hanlding request for %s', event['resource'])
    if event['resource'] in list(func_calls.keys()):
        ddb = boto3.resource('dynamodb')
        table = ddb.Table(os.environ['DDBTable'])
        resp = func_calls[event['resource']]['func'](table, event)

    LOGGER.debug(resp)
    return resp
