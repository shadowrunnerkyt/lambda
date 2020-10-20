## Python 3.8

import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')


def lambda_handler(event, context):
    # Set this to True if you don't want the function to perform all actions
    # Set this to False if you do want the funtion to perform all actions
    debugMode = False
    if debugMode:
        print('[DEBUG]')
    
    # List of tags to copy
    # WARNING: this will overwrite any existing tags
    tags_to_use = ['Environment','Owner','Project']
    print("tags to copy ::", tags_to_use)

    #instances = ec2.instances.all()
    filters = [
        {'Name': 'tag:Owner', 'Values': ['cc']}
    ]
    # get filtered instance list
    instances = ec2.instances.filter(Filters=filters)
    
    for instance in instances:

        tags = instance.tags
        to_tag = [t for t in tags if t['Key'] in tags_to_use]
        
        # tag EBS volumes
        for vol in instance.volumes.all():
            print(f"Tagging volume {vol.id} from instance {instance.id}")
            print(f"With tags: {to_tag}")
            if not debugMode:
                vol.create_tags(Tags=to_tag)

        # tag network interfaces
        for eni in instance.network_interfaces:
            print(f"Tagging interface {eni.id} from instance {instance.id}")
            print(f"With tags: {to_tag}")
            if not debugMode:
                eni.create_tags(Tags=to_tag)

