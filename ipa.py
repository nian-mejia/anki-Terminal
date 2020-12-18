import requests
from bs4 import BeautifulSoup

def run():
    pagina = int(input("""
Wiktionary [1]
Lexico [2]
Salir[3]
   """))

    if pagina == 1:
        print("Wiktionary")
        wiktionary()
    elif pagina == 2:
        print("Lexico")
        lexico()
    elif pagina == 3:
        print("Salir")
        exit()
    else:
        print("Ingresa una opción correcta")



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
        
        if not type_ipa:
            type_ipa.append("IPA")

        ipas_list = soup.select("span.IPA")

        ipas = [ipa.text for ipa in ipas_list]
        dic = dict(zip(type_ipa, ipas))
        print(dic)
    else:
        print("Word not find")
    run()



def lexico():
    word = str(input("Ingresa una palabra: ")).lower()
    URL = ("https://www.lexico.com/en/definition/" + word)
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select("span.phoneticspelling")

    if titles:
        ipa = titles[1].text
        ipa = ipa.replace("r", "ɹ")
        print(ipa)
        try:
            ipa2 = titles[3].text
            ipa2 = ipa2.replace("r", "ɹ")
            print(ipa2)
        except:
            pass
    else:
        print("Word not find")
    run()


if __name__ == "__main__":
    run()
