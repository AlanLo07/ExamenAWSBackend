import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Clientes')

def lambda_handler(event, context):
    # Parse the input data
    data = json.loads(event['body'])
    nombre = data['nombres']
    apellidoMaterno = data['apellidoMaterno']
    apellidoPaterno = data['apellidoPaterno']
    fechaNacimiento = data['fechaNacimiento']
    
    # Get the current highest id
    response = table.scan()
    items = response['Items']
    if items:
        max_id = max(int(item['id']) for item in items)
    else:
        max_id = 0
    
    # Create a new id
    new_id = max_id + 1
    
    # Create a new client entry
    new_client = {
        'id': new_id,
        'nombres': nombre,
        'apellidoMaterno': apellidoMaterno,
        'apellidoPaterno': apellidoPaterno,
        'fechaNacimiento': fechaNacimiento
    }
    
    # Put the new client into the table
    table.put_item(Item=new_client)

    headers = {
                'Access-Control-Allow-Origin': '*',  # Required for CORS support to work
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
            }
    
    return {
        'headers': headers,
        'statusCode': 200,
        'body': json.dumps({'message': 'Cliente creado exitosamente', 'cliente': new_client})
    }