from os import name
from flask import Flask, jsonify, render_template, request
import json
import boto3
import logging
import random
import string 
import conf.credentials as conf


client = boto3.client('lambda',
                        region_name= conf.region,
                        aws_access_key_id=conf.aws_access_key_id,
                        aws_secret_access_key=conf.aws_secret_access_key)

client2 = boto3.client('events',
                        region_name= conf.region,
                        aws_access_key_id=conf.aws_access_key_id,
                       aws_secret_access_key=conf.aws_secret_access_key)
app = Flask(__name__)
app.logger.setLevel(logging.ERROR)
@app.route('/')
def sample_lambda():
   return render_template('sample_lambda.html')
data = {}
@app.route('/start_stop_ec2',methods = ['POST', 'GET'])
def start_stop_ec2():
   if request.method == 'POST':
        result = request.form
        data = result
        print(result['name'], result['schedule'])
        print(data) 
        instance_name =  result['name']      
        cron = "cron("+result['schedule']+")"
        #cron = result['schedule']
        S=5
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))  
        a = "Lambda_rule_"+ran
        print(a)
        print(cron)
        
        event_rule = client2.put_rule(Name=a, ScheduleExpression=cron, State='ENABLED')

        Enable_event = client2.enable_rule( Name=a, EventBusName='default')

        scheduled_lambda = [
            {
                'Id': "start_stop_ec2",
                'Arn': "arn:aws:lambda:us-east-1:130572924197:function:start_stop_ec2",
                
            }
        ]

        scheduled_lambda2 = [
            {
                'Id': "stop_ec2",
                
                'Arn': "arn:aws:lambda:us-east-1:130572924197:function:stop_ec2",
             
            }
        ]

        if result['actiontype'] == 'start':
            response2 = client2.put_targets(Rule=a,Targets=scheduled_lambda) #starting lambda
        elif result['actiontype'] == 'stop':
            response2 = client2.put_targets(Rule=a,Targets=scheduled_lambda2) #stopping lambda
        else:
            print("error")

        print(response2)
        return result

if __name__ == '__main__':
   app.run(debug = True)
   