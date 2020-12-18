import requests
from bs4 import BeautifulSoup
import eng_to_ipa as ipa

def run():
    pagina = str(input("""
    IPA_Wiktionary [1]
    IPA_Lexico [2]
    IPA_CMU[3]
    Salir[4]
    
    Ingresa un número: """))

    if pagina == "1":
        print("Wiktionary")
        wiktionary()
    elif pagina == "2":
        print("Lexico")
        lexico()
    elif pagina == "3":
        print("CMU")
        ipa_cmu()
    elif pagina == "4":
        print("Salir")
        exit()
    else:
        print("Ingresa una opción correcta")
        run()



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
            if ipa != ipa2:
                print(ipa2)
        except:
            pass
        if not ipa:
            ipa = titles[0].text
            ipa = ipa.replace("r", "ɹ")
            print(ipa)

    else:
        print("Word not find")
    run()

def ipa_cmu():
    word = str(input("Ingresa una palabra: ")).lower()
    ipacmu = ipa.ipa_list(word)
    for i in ipacmu[0]:
        print("/"+i+"/")
        
    run()


if __name__ == "__main__":
    run()
