import boto3
import os
from dotenv import load_dotenv

load_dotenv()


def enviar_relatorio():
    s3 = boto3.client('s3')

    caminho = os.getcwd() + '/relatorios'
    relatorios = os.listdir('relatorios')

    if len(relatorios) <= 0:
        print('Sem relatórios')
    else:
        for relatorio in relatorios:
            arquivo = os.path.join(caminho, relatorio)
            with open(arquivo, 'rb') as data:
                print(arquivo)

if __name__ == "__main__":
    enviar_relatorio()
