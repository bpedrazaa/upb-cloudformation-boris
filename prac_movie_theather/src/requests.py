import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

users_table = os.environ['THEATER_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)

# REQUEST NO 1
# Function to get the information of a movie from the database
def getMovieInfo(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    movie_id = array_path[-1]
    
    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': 'info_' + movie_id
        }
    )
    
    item = response['Item']
    del item['pk']
    del item['sk']
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

# REQUEST NO 2
# Function to create a new movie with information in the database
def putMovieInfo(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    movie_id = array_path[-1]
    
    body = event["body"]
    body_object = json.loads(body)
    
    
    table.put_item(
        Item={
            'pk': movie_id,
            'sk': 'info_' + movie_id,
            'title': body_object['title'],
            'year': body_object['year'],
            'actors': body_object['actors']
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Movie and information created')
    }
    

# REQUEST NO 3
# Function to get all the cinema rooms related to a movie
def getRooms(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    movie_id = array_path[-2]
    
    date = event["queryStringParameters"]["date"]
    final_pk = movie_id + "-date_" + date
    print(json.dumps(final_pk))
    
    response = table.query(
        KeyConditionExpression=Key('pk').eq(final_pk) & Key('sk').begins_with('cinema_room')
    )
    
    items = response['Items']
    for item in items:
        del item['pk']
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
    
# REQUEST NO 4
# Function to get all the customers related to a movie and a cinema roon
def getCustomers(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    room_id = array_path[-1]
    movie_id = array_path[-3]

    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': room_id
        }
    )
    
    item = response['Item']
    del item['pk']
    del item['sk']
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    

# REQUEST NO 5
# Function to get the information of a cinemaRoom
def getRoomInfo(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    room_id = array_path[-1]
    
    response = table.get_item(
        Key={
            'pk': room_id,
            'sk': room_id
        }
    )
    
    item = response['Item']
    del item['pk']
    del item['sk']
    print(json.dumps(item["capacity"]))
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
    
# REQUEST NO 5
# Function to get the information of a Customer
def getCustomerInfo(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    customer_id = array_path[-1]
    
    response = table.get_item(
        Key={
            'pk': customer_id,
            'sk': customer_id
        }
    )
    
    item = response['Item']
    del item['pk']
    del item['sk']
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    

# REQUEST NO 7
# Function to put a list of customers into a cinema room
def putCustomersList(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    room_id = array_path[-1]
    
    # First we review if the capacity of the room is enough
    response = table.get_item(
        Key={
            'pk': room_id,
            'sk': room_id
        }
    )
    item = response['Item']
    # Get the capacity and the is3D attribute
    capacity = item["capacity"]
    is_3D = item["is_3D"]
    
    body = event["body"]
    body_object = json.loads(body)
    count_customers = len(body_object['customers'])
    
    new_capacity = int(capacity) - count_customers
    
    response = ""
    if new_capacity >= 0:
        table.put_item(
            Item={
                'pk': room_id,
                'sk': room_id,
                'customers': body_object['customers'],
                'capacity': new_capacity,
                'is_3D': is_3D
            }
        )
        response = "List of customers added to the cinema room"
        
    else:  
        response = "The capacity of the cinema room is already full"
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
    