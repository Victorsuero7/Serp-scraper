import requests, pandas as pd
from bs4 import BeautifulSoup
from mozscape import Mozscape
client = Mozscape('userapi', 'apikey')
user = {
    "referer":"referer: https://www.google.com/",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}
gslug = 'https://www.google.com/search?q='
kw = input('¿Que palabra clave quieres bucar?: ').replace(' ','+')
url = gslug+kw+'&'+'num=10'
pag = requests.get(url, headers=user)
rpag = pag.text
soup = BeautifulSoup(rpag, 'lxml')
resultado = soup.find_all('div', attrs={'class':['tF2Cxc','dFd2Tb']})
# tt = resultado.find_all('div', attrs={'class':'tF2Cxc'})
titulos = list()
for i in resultado:
    titulos.append(i.h3.text)

# urls = resultado.find('div', attrs={'class':'yuRUbf'})
enlace = list()
for i in resultado:
    enlace.append(i.a.get('href'))

md = soup.find_all('div', attrs={'class':['VwiC3b','Uroaid']})
meta = list()
for i in md:
    meta.append(i.text)



# 'https://db2.keywordsur.fr/keyword_surfer_keywords?country=ES&keywords=["{urllib.parse.quote(keyw)}"]'
pa = []
da = []
bk = []
results = client.urlMetrics(enlace, Mozscape.UMCols.domainAuthority | Mozscape.UMCols.pageAuthority | Mozscape.UMCols.equityExternalLinks)
# print(results[1].get('uu'))
for i in range(0,len(enlace)):
    pa.append(results[i].get('upa'))
    da.append(results[i].get('pda'))
    bk.append(results[i].get('ueid'))


# print(pag.status_code)
# print(pag.url)
df = pd.DataFrame({'Title':titulos, 'Url':enlace, 'meta':meta, 'Pa':pa, 'Da':da, 'Bk':bk}, index=list(range(1, len(titulos)+1)))
#df = pd.DataFrame({'meta':meta}, index=list(range(1, len(meta)+1)))
with pd.ExcelWriter('scraping serp '+kw+'.xlsx') as writer:
    df.to_excel(writer)
