import boto3
import aws_lambda.dynamodb as dynamodb
import json
import logging
import os
FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
deserializer = boto3.dynamodb.types.TypeDeserializer()


def display_selected_entries(ddb, event):
    results, count = ddb.scan(os.environ['DDBTable'])
    results = [{k: deserializer.deserialize(v) for k,v in item.items()} for item in results['Items']]
    return aws_lambda.generate_return(200, results)

def display_all_entries(ddb, event):
    try:
        int(event['pathParameters']['id_number'])
    except ValueError:
        return aws_lambda.generate_return(400, {'error': 'Must provide integer for id_number'})
    results = ddb.get(os.environ['DDBTable'], int(event['pathParameters']['id_number']))
    return aws_lambda.generate_return(200, results)

def main(event, context):
    resp = aws_lambda.generate_return(
        400, {'error': 'Invalid resource', 'resource': event['resource']})
    func_calls = {
        '/id/{id_number}': {'func': display_selected_entries},
        '/id': {'func': display_all_entries},
    }
    if event['resource'] in list(func_calls.keys()):
        ddb = dynamodb.DynamoDB()
        resp = func_calls[event['resource']]['func'](ddb, event)

    LOGGER.debug(resp)
    return resp
