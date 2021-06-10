import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

users_table = os.environ['USERS_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)

def getUser(event, context):
    print(json.dumps({"running": True}))
    
    response = table.get_item(
        Key={
            'pk': 'user_',
            'sk': 'age'
        }
    )
    item = response['Item']
    print(item)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def putUser(event, context):
    print(json.dumps({"running": True}))
    
    table.put_item(
        Item={
            'pk': 'user_',
            'sk': 'age'
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }