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

	aws cloudformation create-stack --cli-input-json file://approach1.conf --template-body file://approach1.cft.yaml
