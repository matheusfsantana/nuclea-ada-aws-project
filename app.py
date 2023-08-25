from flask import Flask, request, send_file, abort, jsonify
import boto3
import io
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
s3 = boto3.client('s3')

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, world!"

@app.route('/files', methods=['GET'])
def list_files():
    
    print("Listing objects...")
    
    response = s3.list_objects_v2(os.getenv('BUCKET_NAME'))
    files = response['Contents']
    #print(files)
    
    return files

@app.route('/download/file', methods=['GET'])
def download():
    try:
        nome = request.args.get('nome')
        response = s3.get_object(Bucket='relatorios-vault', Key=nome)
        file_content = response['Body'].read()
    except Exception as e:
        abort(404, "Arquivo não existe")
    
    return send_file(io.BytesIO(file_content), as_attachment=True, download_name=nome)


@app.route('/send', methods=['POST'])
def send_files():
    try:
        uploaded_file = request.files['file']
        if uploaded_file:
            file_name = uploaded_file.filename
            s3.upload_fileobj(uploaded_file, os.getenv('BUCKET_NAME'), file_name)
            return jsonify({"message": "Arquivo enviado com sucesso para o S3"}), 200
        else:
            return jsonify({"message": "Nenhum arquivo enviado"}), 400
    except Exception as e:
        return jsonify({'message': "Algum erro ocorreu"})

if __name__ == '__main__':
    app.run(debug=True)
