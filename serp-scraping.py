import requests, pandas as pd
from bs4 import BeautifulSoup
user = {
    "referer":"referer: https://www.google.com/",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}
gslug = 'https://www.google.com/search?q='
kw = input('¿Que palabra clave quieres bucar?: ').replace(' ','+')
url = gslug+kw+'&'+'num=100'
pag = requests.get(url, headers=user)
rpag = pag.text
soup = BeautifulSoup(rpag, 'lxml')
tt = soup.find_all('div', attrs={'class':'yuRUbf'})
titulos = list()
for i in tt:
    titulos.append(i.h3.text)
urls = soup.find_all('div', attrs={'class':'yuRUbf'})
enlace = list()
for i in urls:
    enlace.append(i.a.get('href'))
md = soup.find_all('div', attrs={'class':['VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc', 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf']})
meta = list()
for i in md:
    meta.append(i.text)
print(pag.status_code)
print(pag.url)
df = pd.DataFrame({'Title':titulos, 'Url':enlace, 'Description':meta}, index=list(range(1, len(titulos)+1)))
#df = pd.DataFrame({'meta':meta}, index=list(range(1, len(meta)+1)))
with pd.ExcelWriter('scraping serp '+kw+'.xlsx') as writer:
    df.to_excel(writer)
