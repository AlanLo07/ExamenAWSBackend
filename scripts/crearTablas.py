import boto3

# Crear cliente de DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-2")

# Crear la tabla
tabla = dynamodb.create_table(
    TableName="Clientes",
    KeySchema=[
        {"AttributeName": "id", "KeyType": "HASH"},   # Clave primaria (Partition Key)
    ],
    AttributeDefinitions=[
        {"AttributeName": "id", "AttributeType": "N"}
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}  # Capacidad de lectura/escritura
)

print("Creando tabla, espera un momento...")
tabla.wait_until_exists()  # Espera hasta que la tabla esté creada
print("¡Tabla creada exitosamente!")
