import requests
from bs4 import BeautifulSoup


def wiktionary():
    word = str(input("Ingresa una palabra: ")).lower()
    URL = ("https://en.wiktionary.org/wiki/" + word)
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select("span.ib-content.qualifier-content")

    if titles:
        type_ipa = []

        for title in titles:
            if title.a:
                if word in title.text:
                    continue
                else:
                    type_ipa.append(title.text)

        ipas_list = soup.select("span.IPA")

        ipas = [ipa.text for ipa in ipas_list]
        dic = dict(zip(type_ipa, ipas))
        print(dic)
    else:
        print("Word not find")



def lexico():
    word = str(input("Ingresa una palabra: ")).lower()
    URL = ("https://www.lexico.com/definition/" + word)
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select("span.phoneticsspelling")

    if titles:
        ipa = titles[1].text
        print(ipa)
    else:
        print("Word not find")


if __name__ == "__main__":
    pagina = int(input("""
   Wiktionary [1]
   Lexico [2]
   """))

    if pagina == 1:
        print("Wiktionary")
        wiktionary()
    elif pagina == 2:
        print("Lexico")
        lexico()
    else:
        print("Ingresa una opción correcta")
