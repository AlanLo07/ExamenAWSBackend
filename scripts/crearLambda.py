import boto3
import zipfile

archivos = ["functions/clientes/get.py", "functions/clientes/post.py","functions/creditos/get.py"]
zip_nombre = "function.zip"
function_names = ["ObtenerClientes","CrearCliente","ObtenerCreditos"]
handlers = ["functions/clientes/get.lambda_handler","functions/clientes/post.lambda_handler","functions/creditos/get.lambda_handler"]
for i,archivo in enumerate(archivos):
    with zipfile.ZipFile(zip_nombre, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(archivo)

    print("Archivo comprimido exitosamente.")

    # Cliente de AWS Lambda
    lambda_client = boto3.client('lambda', region_name='us-east-2')

    # ARN del rol IAM con permisos para Lambda
    role_arn = "arn:aws:iam::640168420977:role/LambdaRole"

    # Nombre de la función Lambda
    lambdas = lambda_client.list_functions()

    with open("function.zip", "rb") as f:
            zip_bytes = f.read()
    # Leer el archivo ZIP con el código de la función
    for lambda_ in lambdas["Functions"]:
        if lambda_["FunctionName"] == function_names[i]:
            print("La función ya existe.")
            response = lambda_client.update_function_code(
                FunctionName=function_names[i],
                ZipFile=zip_bytes# Código comprimido en ZIP
            )
            break
    else:

        # Crear la función Lambda
        response = lambda_client.create_function(
            FunctionName=function_names[i],
            Runtime="python3.8",
            Role=role_arn,
            Handler=handlers[i],
            Code={"ZipFile": zip_bytes},
            Timeout=10,
            MemorySize=128
        )

    print("Función creada:", response)
