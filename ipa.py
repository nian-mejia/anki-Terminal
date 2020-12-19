import requests
from bs4 import BeautifulSoup
import eng_to_ipa as engipa

choise = """
IPA_Wiktionary [1]
IPA_Lexico [2]
IPA_CMU[3]
Salir[4]
    
Ingresa un número: """


def run():
    pagina = str(input(choise))

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


def ipa_requests(url, selector):
    global word
    word = str(input("Ingresa una palabra: ")).lower()
    url += word
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select(selector)

    return titles


def wiktionary():
    url = "https://en.wiktionary.org/wiki/"
    selector = "span.ib-content.qualifier-content"

    titles = ipa_requests(url, selector)

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

        ipas_list = ipa_requests(url, "span.IPA")

        ipas = [ipa.text for ipa in ipas_list]
        dic = dict(zip(type_ipa, ipas))
        print(dic)

    else:
        print("Word not find")
    run()


def lexico():
    url = "https://www.lexico.com/en/definition/"
    selector = "span.phoneticspelling"
    titles = ipa_requests(url, selector)

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
    def palabra(word):
        palabra = engipa.ipa_list(word)
        for i in palabra[0]:
            i = i.replace("r", "ɹ")
            print("/"+i+"/")

    def frase(word):
        oracion = engipa.convert(word)
        oracion = oracion.replace("r", "ɹ")
        print("/"+oracion+"/")

    word = str(input("Ingresa una palabra: ")).lower()
    word_list = word.split()

    if len(word_list) == 1:
        palabra(word)
    elif len(word_list) >= 2:
        frase(word)
    else:
        print("Error")

    run()


if __name__ == "__main__":
    run()