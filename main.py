
import json
import boto3
import os
from uuid import uuid4
from customexception import ENVException,DynamoOperationFailed


try:
    TABLE_NAME = os.environ['TABLE_NAME']
except Exception as e:
    raise ENVException(f"Environment variable is not set: {str(e)}")
    


def insert_metadata(item):
    """
    insert metadata to table 
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=item)
    except Exception as e:
        raise DynamoOperationFailed(f"Error inserting metadata:{str(e)}")
    
    
def handler(event,context):
    data = event['Records']
    for i in data:
        bucketinfo=i['s3']['bucket']
        objectinfo=i['s3']['object']
        item = {
            "eventnumber":str(uuid4()),
        "eventTime":str(i['eventTime']),
        "eventType":i['eventName'],
        "bucketName":bucketinfo['name'],
        "objectName":objectinfo['key'],       
        }
        insert_metadata(item)
        
        
        
if __name__ == '__main__':
    print("--"*100)
    handler("","")
    
    
    