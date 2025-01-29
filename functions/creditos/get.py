import json
import boto3
from decimal import Decimal

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource("dynamodb")
tabla = dynamodb.Table("Creditos")

def lambda_handler(event, context):
    try:
        # 1️⃣ Leer cliente desde pathParameters
        path_params = event.get("pathParameters", {})
        cliente_id = path_params.get("cliente")

        if not cliente_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Se requiere el cliente en el path"})
            }

        # 2️⃣ Consultar DynamoDB buscando créditos del cliente
        response = tabla.scan()
        for item in response["Items"]:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
        response["Items"] = [item for item in response["Items"] if item["cliente"] == int(cliente_id)]


        headers = {
                'Access-Control-Allow-Origin': '*',  # Required for CORS support to work
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
            }
    

        # 3️⃣ Devolver la respuesta con los créditos encontrados
        return {
            "headers": headers,
            "statusCode": 200,
            "body": json.dumps(response["Items"])
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
