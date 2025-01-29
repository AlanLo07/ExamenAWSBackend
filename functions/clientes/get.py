import boto3
import json

def scan_clientes_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Clientes')

    try:
        response = table.scan()
        data = response.get('Items', [])
        print(f"Data: {data}")
        return data
    except Exception as e:
        print(f"Error scanning Clientes table: {e}")
        return None

def lambda_handler(event, context):
        clientes = scan_clientes_table()
        if clientes:
            clientes.sort(key=lambda x: int(x['id']))
            clientes = list(map(lambda x: {k: str(v) for k, v in x.items()}, clientes))
            headers = {
                'Access-Control-Allow-Origin': '*',  # Required for CORS support to work
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,GET"
            }
            return {
                'headers': headers,
                'statusCode': 200,
                'body': json.dumps(clientes)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "No se encontraron clientes."})
            }