import boto3
import json

apigateway_client = boto3.client("apigateway", region_name="us-east-2")
api_name = 'APIClientes'

response = apigateway_client.get_rest_apis()

for api in response["items"]:
    if api["name"] == api_name:
        print(f"✅ API '{api_name}' encontrada con ID: {api['id']}")
        api_id = api['id']
        break
else:
    # Crear API Gateway
    api_response = apigateway_client.create_rest_api(
        name="APIClientes",
        description="API de clientes",
        endpointConfiguration={"types": ["REGIONAL"]}
    )
    api_id = api_response["id"]
    print("API creada con ID:", api_id)

# Obtener el recurso raíz
resources = apigateway_client.get_resources(restApiId=api_id)
root_id = resources["items"][0]["id"]
print("ID del recurso raíz:", root_id)
print("Resources:", resources)

for resource in resources["items"]:
    if resource["path"] == "/clientes":
        print(f"✅ Recurso '/clientes' encontrado con ID: {resource['id']}")
        resource_id_clientes = resource["id"]
        break
# Crear un nuevo recurso en API Gateway (Ejemplo: "/saludo")
else:
    resource_response = apigateway_client.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart="clientes"
    )
    resource_id_clientes = resource_response["id"]
    print("Recurso '/clientes' creado con ID:", resource_id_clientes)

for resource in resources["items"]:
    if resource["path"] == "/creditos/{cliente}":
        print(f"✅ Recurso '/creditos' encontrado con ID: {resource['id']}")
        print("Recurso '/creditos' encontrado con ID:", resource)
        resource_id_creditos = resource["id"]
        break
else:
    resource_response = apigateway_client.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart="creditos"
    )
    resource_id_creditos = resource_response["id"]

    sub_recurso = apigateway_client.create_resource(
        restApiId=api_id,
        parentId=resource_id_creditos,
        pathPart="{cliente}"  # Path Parameter
    )
    resource_id_creditos = sub_recurso["id"]
    print("Recurso '/creditos' creado con ID:", resource_id_creditos)

# Crear método HTTP GET
try: 
    if apigateway_client.get_method(restApiId=api_id, resourceId=resource_id_clientes, httpMethod="GET") == {}:
        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=resource_id_clientes,
            httpMethod="GET",
            authorizationType="NONE"
            )
except Exception as e:
    apigateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id_clientes,
        httpMethod="GET",
        authorizationType="NONE"
        )
    print("Error:", e)

# Crear método HTTP POST
try:
    if apigateway_client.get_method(restApiId=api_id, resourceId=resource_id_clientes, httpMethod="POST") == {}:

        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=resource_id_clientes,
            httpMethod="POST",
            authorizationType="NONE"
        )
except Exception as e:
    apigateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id_clientes,
        httpMethod="POST",
    )

try:
    if apigateway_client.get_method(restApiId=api_id, resourceId=resource_id_creditos, httpMethod="GET") == {}:
        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=resource_id_creditos,
            httpMethod="GET",
            authorizationType="NONE"
        )
except Exception as e:
    apigateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id_creditos,
        httpMethod="GET",
        authorizationType="NONE",
    )

lambdas_arn = [f"arn:aws:lambda:us-east-2:640168420977:function:ObtenerClientes", f"arn:aws:lambda:us-east-2:640168420977:function:CrearCliente", "arn:aws:lambda:us-east-2:640168420977:function:ObtenerCreditos"]

# Vincular Lambda a API Gateway
apigateway_client.put_integration(
    restApiId=api_id,
    resourceId=resource_id_clientes,
    httpMethod="GET",
    type="AWS_PROXY",
    integrationHttpMethod="POST",
    uri=f"arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambdas_arn[0]}/invocations"
)


apigateway_client.put_integration(
    restApiId=api_id,
    resourceId=resource_id_clientes,
    httpMethod="POST",
    type="AWS_PROXY",
    integrationHttpMethod="POST",
    uri=f"arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambdas_arn[1]}/invocations"
)

apigateway_client.put_integration(
    restApiId=api_id,
    resourceId=resource_id_creditos,
    httpMethod="GET",
    type="AWS_PROXY",
    integrationHttpMethod="POST",
    uri=f"arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambdas_arn[2]}/invocations"
)


print("Integración API Gateway ↔ Lambda creada.")

lambda_client = boto3.client("lambda", region_name="us-east-2")

function_names = ["ObtenerClientes", "CrearCliente", "ObtenerCreditos"]
metodos = ["GET", "POST", "GET"]
rutas = ["clientes", "clientes", "creditos/{cliente}"]
for i, function_name in enumerate(function_names):
    print(f"🔍 Permisos de la Lambda '{function_name}':")
    try:
        response = lambda_client.get_policy(FunctionName=function_name)
    except lambda_client.exceptions.ResourceNotFoundException:
        response = lambda_client.add_permission(
            Action="lambda:InvokeFunction",
            FunctionName=function_name,
            Principal="apigateway.amazonaws.com",
            StatementId=f"APIInvoke-{function_name}",
            SourceArn=f"arn:aws:execute-api:us-east-2:640168420977:{api_id}/*/{metodos[i]}/{rutas[i]}"
        )
    print(response)


print("Permisos de API Gateway agregados a Lambda.")

apigateway_client.create_deployment(
    restApiId=api_id,
    stageName="prod"
)

print("API desplegada en el stage 'prod'.")