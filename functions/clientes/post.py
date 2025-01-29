import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Clientes')

def lambda_handler(event, context):
    # Parse the input data
    data = json.loads(event['body'])
    nombre = data['nombre']
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
        'id': str(new_id),
        'nombre': nombre,
        'apellidoMaterno': apellidoMaterno,
        'apellidoPaterno': apellidoPaterno,
        'fechaNacimiento': fechaNacimiento
    }
    
    # Put the new client into the table
    table.put_item(Item=new_client)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Cliente creado exitosamente', 'cliente': new_client})
    }