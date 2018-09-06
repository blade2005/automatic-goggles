automatic-goggles
=================

Onica Approach 1
================

VPC with private / public subnets and all required dependent infrastructure (DO NOT USE THE DEFAULT VPC)

ELB to be used to register web server instances

- Include a simple health check to make sure the web servers are responding
- The health check should automatically replace instances if they are unhealthy, and the instances should come back into service on their own

Auto Scaling Group and Launch Configuration that launches EC2 instances and registers them to the ELB

- Establish a minimum, maximum, and desired server count that scales up/down based on a metric of your choice (and be able to demonstrate a scaling event)
- Security Group allowing HTTP traffic to load balancer from anywhere (not directly to the instance(s))

Security Group allowing only HTTP traffic from the load balancer to the instance(s)

Remote management ports such as SSH and RDP must not be open to the world

Some kind of automation or scriptin gthat achieves the following:

- Install a web server (your choice – Apache and Nginx are common examples)
- Deploys a simple “hello world” page for the web server to serve up
- May be written in the language of your choice (HTML, PHP, etc)
- May be sourced from the location of your choice (S3, cookbook file/ template, etc)
- Must include the server’s hostname in the “hello world” presented to the user

All AWS resources must be created using Terraform or CloudFormation

No resources may be created or managed by hand other than EC2 SSH keys


Deploy
======
You can deploy by:

	stack=helloworld;aws cloudformation create-stack --cli-input-json file://approach1.conf --template-body file://approach1.cft.yaml --stack-name $stack && aws cloudformation wait stack-create-complete --stack-name $stack; aws cloudformation describe-stacks

Delete the stack by:

	stack=helloworld;aws cloudformation delete-stack --stack-name $stack && aws cloudformation wait stack-delete-complete --stack-name $stack

Update stack by:

    stack=helloworld;aws cloudformation update-stack --stack-name $stack --template-body file://approach1.cft.yaml --cli-input-json file://update-approach1.conf && aws cloudformation wait stack-update-complete --stack $stack


Onica Approach 2
================

Objective: Launch a simple API utilizing automation and AWS best practices.

DynamoDB table

- Must contain multiple unique records (sample structure provided below, you may determine your own schema as desired)

Lambda Function

- Must be written in language supported natively by AWS (Node.js, Java, C#, Go, Python – NO SHIMS)
- Must log execution output to CloudWatch Logs

API Gateway with two stages (dev and prod) exposing endpoints for the Lambda function

- Must have a path to expose all DynamoDB records as well as a single record

§ Example:

/id should return a list of all records
1
2
3
45

/id/5 should return the details of record #5 in DynamoDB
{
“id”: “5”,
“details” {
“firstName”: “Onica”,
“lastName”: “Test”
}
}

CloudWatch Logs

- Must have a retention policy of 30 days

IAM roles and policies must be created in a least permissive model (AVOID USING AWS MANAGED POLICIES)

All AWS resources must be created using Serverless Framework, Terraform, or CloudFormation

No resources may be created or managed by hand other than EC2 SSH keys