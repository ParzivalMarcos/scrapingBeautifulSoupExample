import requests, json, csv
from lxml import etree
from bs4 import BeautifulSoup

# import requests, lxml.html

# curl --location --request POST 'https://www.companhiadasletras.com.br/Busca' \
# --header 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
# --header 'Cookie: PHPSESSID=vbrhohjgct4pkkkmr6qbajkf31' \
# --data-raw 'action=buscar&selo=Companhia+das+Letrinhas&ordem=cronologica&pg=1&anoMin=1985&anoMax=2023&idadeMax=18'

# pesquisar: https://www.geeksforgeeks.org/how-to-use-xpath-with-beautifulsoup/


# recupera dados diretamente fazendo chamada rest
def curlDadosLivros(payload=None) -> requests.Response:
    url = "https://www.companhiadasletras.com.br/Busca"
    if payload == None:
        payload = "action=buscar&selo=Companhia+das+Letrinhas&ordem=cronologica&pg=1&anoMin=1985&anoMax=2023&idadeMax=18"
        
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "PHPSESSID=vbrhohjgct4pkkkmr6qbajkf31"
    }
    r = requests.post(url, data=payload, headers=headers)
    return r


def recuperaDadosTecnicos(link) -> dict:
    url = "https://www.companhiadasletras.com.br" + link

    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')

    dom = etree.HTML(str(soup))


    paginas = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span[contains(text(), "Páginas")]')
    formato = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span[contains(text(), "Formato")]')
    peso = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span[contains(text(), "Peso")]')
    acabamento = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span[contains(text(), "Acabamento")]')
    lancamento = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span[contains(text(), "Lançamento")]')
    isbn = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span[contains(text(), "ISBN")]')

    dadosTecnicos = {
        "paginas": paginas[0].text,
        "formato": formato[0].text,
        "peso": peso[0].text,
        "acabamento": acabamento[0].text,
        "lancamento": lancamento[0].text,
        "isbn": isbn[0].text
    }

    # r = BeautifulSoup.find_all(soap, attrs={"class": "section__wrapper"})
    return dadosTecnicos


def insereDadosArquivo(dados) -> None:
    fieldNames = ['titulo', 'preco', 'paginas', 'formato', 'peso', 'acabamento', 'lancamento', 'isbn']

    with open('relatorio.csv', 'a', encoding='utf-8', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        # writer.writeheader()
        writer.writerow(dados)


response = curlDadosLivros()
jsonReturn = json.loads(response.content)

for page in range(1,(jsonReturn['totalPages']+1) ):
    # action=buscar&selo=Companhia+das+Letrinhas&ordem=cronologica&pg=1&anoMin=1985&anoMax=2023&idadeMax=18
    payload = "action=buscar&selo=Companhia+das+Letrinhas&ordem=cronologica&pg=" + str(page) + "&anoMin=1985&anoMax=2023&idadeMax=18"

    response = curlDadosLivros(payload)
    jsonReturn = json.loads(response.content)
    
    for livro in jsonReturn["livros"]:
        titulo = livro["titulo"]
        preco = livro["preco"]
        link = livro["link"]

        dadosTecnicos = recuperaDadosTecnicos(link)

        dadosTecnicos['titulo'] = titulo
        dadosTecnicos['preco'] = preco

        insereDadosArquivo(dadosTecnicos)

        print(f"Página {page} processada")
