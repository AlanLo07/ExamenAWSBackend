import boto3
import zipfile

archivo = "functions/clientes/get.py"
zip_nombre = "function.zip"

with zipfile.ZipFile(zip_nombre, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(archivo)

print("Archivo comprimido exitosamente.")

# Cliente de AWS Lambda
lambda_client = boto3.client('lambda', region_name='us-east-2')

# ARN del rol IAM con permisos para Lambda
role_arn = "arn:aws:iam::640168420977:role/LambdaRole"

# Nombre de la función Lambda
function_name = "ObtenerClientes"
lambdas = lambda_client.list_functions()
for lambda_ in lambdas["Functions"]:
    if lambda_["FunctionName"] == function_name:
        print("La función ya existe.")
        lambda_client.delete_function(FunctionName=function_name)
# Leer el archivo ZIP con el código de la función
with open("function.zip", "rb") as f:
    zip_bytes = f.read()

# Crear la función Lambda
response = lambda_client.create_function(
    FunctionName=function_name,
    Runtime="python3.8",
    Role=role_arn,
    Handler="functions/clientes/get.lambda_handler",
    Code={"ZipFile": zip_bytes},
    Timeout=10,
    MemorySize=128
)

print("Función creada:", response)
