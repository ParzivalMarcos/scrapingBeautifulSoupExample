from bs4 import BeautifulSoup
from lxml import etree
import requests

site = requests.get("https://www.companhiadasletras.com.br/livro/9786554850131/as-aventuras-de-dorinha")

soup = BeautifulSoup(site.text, 'html.parser')

dom = etree.HTML(str(soup))

# xpath = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span')
xpath = dom.xpath('//*[@id="ficha-tecnica"]/div/div/span[contains(text(), "Páginas")]')
# //h4/a[contains(text(),'SAP M')]

for i in xpath:
    print(i.text)

    
def recuperaHTMLSite(url: str):
    # url = "https://www.companhiadasletras.com.br/Busca?action=buscar&selo=Companhia+das+Letrinhas&ordem=cronologica&pg=1&anoMin=1985&anoMax=2023&idadeMax=18"
    site = requests.get(url)
    soap = BeautifulSoup(site.text, 'html.parser')

    return soap


def recuperaHTMLSiteArquivo():
    with open("site.txt", "r") as file:
        site = file.read()
    soap = BeautifulSoup(site, 'html.parser')

    return soap


# https://www.companhiadasletras.com.br/livro/9786554850131/as-aventuras-de-dorinha