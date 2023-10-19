import json
import boto3
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_client = boto3.client('ec2', region_name = os.environ.get('AWS_REGION'))

def list_elastic_ips():
    try:
        response = ec2_client.describe_addresses()
        addresses = response["Addresses"]
        logger.info(f"addresses_dict : {json.dumps(addresses)}")

        return addresses
    except Exception as e:
        logger.error(f"list_elastic_ips :: Error listing elastic IPs: {str(e)}")

def release_eip(allocation_id):
    
    try:
        response = ec2_client.release_address(AllocationId=allocation_id)
        
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(f"EIP with allocation id = {allocation_id} released successfully !")

        return response["ResponseMetadata"]["HTTPStatusCode"]
    except Exception as e:
        logger.error(f"release_eip :: Error releasing elastic IP: {str(e)}")


def lambda_handler(event, context):

    try:

        ## List the available Elastic IPs
        eip_list = list_elastic_ips()
        
        for eip in eip_list:
            if eip.get("InstanceId"):
                logger.info(f"{eip['PublicIp']} is associated with instance id : {eip['InstanceId']}")
            else:
                logger.info(f"Releasing eip = {eip['PublicIp']}")
                release_eip(eip['AllocationId'])

        return "success"
    except Exception as e:
        logger.error(f"lambda_handler :: Error in Lambda handler: {str(e)}")
        return e

