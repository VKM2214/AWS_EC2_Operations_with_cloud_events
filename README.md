# Sample web application (Python Flask) invoking a Lambda function

This sample web application invokes a AWS Lambda function for schedule the Start and Stop of Ec2 instance based on the given schedule date and time. 
All the backend logic is implemented in a Lambda function.



## Features of the Start_stop_ec2 application

1. This app takes Instance id and schedule data and time(UTC or GMT) in cron or rate format as inputs

2. It invokes a Lambda function to schedule Start/Stop of the EC2 Instance based on Instance id and schedule data/time.



## Setup


*Prerequisites:*

1) Need to have a AWS account with console access.
2) Clone the repo 
3) Update the conf/credentials.py file with the aws credentials(access_key and secret_key) and region(For eg:- If your region is "US-east-1", enter 'us-east-1' in the region field)
4) Create a two AWS Lambda function with name 'start_stop_ec2' & 'stop_ec2' and paste the below code in inline editor. Update the conf/credentials.py file with the lambda function name details and accesskey details. 
5) To Create IAM policy using JSON policy editor:-
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Start*",
        "ec2:Stop*"
      ],
      "Resource": "*"
    }
  ]
}


## 'start_stop_ec2'

import boto3
region = 'us-east-1'
instances = ['instance name here']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))

## 'stop_ec2'

import boto3
region = 'us-east-1'
instances = ['instance name here']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('Stopped your instances: ' + str(instances))

Follow this setup if you want to use a local copy of this application. 

1. `pip install requirements.txt`

## How to run the start_stop_ec2 application

To start the application, 

1. Run `python 'start_stop_ec2.py' from the console.
2. Visit `localhost` which is generated on your Command line in your browser. 
3. Give the inputs and click on the 'Start/Stop' button

## What the application does

The application schedule the events to the cloud events to start/stop the instance for the instance id. 

##We have exactly one page with:

* two text boxes 
* two submit button
