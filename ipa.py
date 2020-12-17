import requests
from bs4 import BeautifulSoup


word = str(input("Ingresa una palabra: ")).lower()
URL = ("https://en.wiktionary.org/wiki/" + word)
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")
titles = soup.select("span.ib-content.qualifier-content ")

if titles:
  type_ipa = []

  for title in titles:
    if title.a:
      if word in title.text:
        continue
      else: 
        type_ipa.append(title.text)

  ipas_list = soup.select("span.IPA")

  ipas =[ipa.text for ipa in ipas_list]
  dic = dict(zip(type_ipa, ipas))

  print(dic)

else:
  print("Word not find")


