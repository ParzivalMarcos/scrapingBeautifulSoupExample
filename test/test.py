import main, json, requests
from bs4 import BeautifulSoup


def escreveArquivo(dado, nome):
    with open(nome, "w") as arquivo:
        arquivo.write(str(dado))

def recuperaDados():
    response = main.curlDadosLivros()
    jsonReturn = json.loads(response.content)
    jsonObject = json.dumps(jsonReturn, indent=4)

    return jsonObject


def lerArquivo():
    with open("vitrineLivros.json", 'r') as arquivo:
        json = arquivo.read()
        return json


def recuperaSiteTecnico():
    url = "https://www.companhiadasletras.com.br/livro/9786581776435/piscina"
    site = requests.get(url)
    soap = BeautifulSoup(site.text, 'html.parser')
    escreveArquivo(soap, "site.html")



recuperaSiteTecnico()

# escreveArquivo(recuperaDados(), "vitrineLivros.json")
