import json
import boto3
import base64

s3 = boto3.client('s3')
bucket_name = 'relatorios-vault'

def lambda_handler(event, context):

    print(event)

    path = event['routeKey']
    print(f"http: {path}")

    if path == "GET /files":
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = response['Contents']
        json_data = json.dumps(files, default=str)

        return {
            'statusCode': 200,
            'body': json_data,
            'headers': {
                    'Content-Type': 'application/json'
                }
        }
    elif path == "GET /download/{filename}":
        fname = event['pathParameters']['filename']
        try:
            response = s3.get_object(Bucket=bucket_name, Key=fname)
            file_content = response['Body'].read()
            return {
                'statusCode': 200,
                'body':base64.b64encode(file_content),
                'isBase64Encoded': True
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }
    elif path == "POST /upload":
        file_content = event['body']
        query = event['queryStringParameters']
        fname = query['nome']
        decode_content = base64.b64decode(file_content)

        s3_upload = s3.put_object(Bucket=bucket_name, Key=fname, Body=decode_content)

        return {
            'statusCode': 200,
            'body': json.dumps('Objeto salvo com sucesso!')
        }

    else:
        return {
            'statusCode': 404,
            'body': json.dumps("url inválida")
        }
