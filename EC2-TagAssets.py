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
    tags_to_use = ['Environment']
    print("tags to copy ::", tags_to_use)

    if debugMode:
        # get filtered instance list instead
        filters = [{'Name': 'tag:Owner', 'Values': ['cc']}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        # get list of ALL instances
        instances = ec2.instances.all()
    
    
    for instance in instances:

        tags = instance.tags
        to_tag = [t for t in tags if t['Key'] in tags_to_use]

        # make sure there actually are tags to write
        if len(to_tag) == 0:
            print(instance.id,"has no tags to copy")
            continue
        else:
            
            # tag EBS volumes
            for vol in instance.volumes.all():
                if debugMode:
                    print(f"Tagging volume {vol.id} from instance {instance.id}")
                    print(f"With tags: {to_tag}")
                else:
                    vol.create_tags(Tags=to_tag)

            # tag network interfaces
            for eni in instance.network_interfaces:
                if debugMode:
                    print(f"Tagging interface {eni.id} from instance {instance.id}")
                    print(f"With tags: {to_tag}")
                else:
                    eni.create_tags(Tags=to_tag)

