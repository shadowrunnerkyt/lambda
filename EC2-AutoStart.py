## Python 3.8

import boto3
import logging
from datetime import datetime

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    
    # get time now, convert to string
    now = datetime.now()
    current = now.strftime("%H%M")
    print("Current Time =", current)
    
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [
        {'Name': 'tag:AutoStart', 'Values': [current]},
        {'Name': 'instance-state-name', 'Values': ['stopped']}
    ]
    
    # get filtered instance list
    instances = ec2.instances.filter(Filters=filters)
    
    # get instance IDs from instance list
    StartInstanceIDs = [instance.id for instance in instances]
    
    # make sure there are actually instances to start 
    if len(StartInstanceIDs) > 0:
        # list instance IDs
        print(StartInstanceIDs)
        
        #perform the start
        Starting = ec2.instances.filter(InstanceIds=StartInstanceIDs).start()
        print(Starting)
    else:
        print("Nothing to do here")
