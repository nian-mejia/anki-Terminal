import requests
from bs4 import BeautifulSoup
import eng_to_ipa as engipa
import main
from blessings import Terminal
t = Terminal()

choise = """
[1] IPA_Lexico
[2] IPA_CMU
[9] Atras

Ingresa un número: """

choise = choise.replace("[", f"{t.bold_yellow}[").replace(" ",  f"{t.normal} ")

def ipa_requests(url, selector):
    word = str(input("Ingresa una palabra: ")).lower()
    url += word
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select(selector)
    return titles


def cleaner(ipa):
    ipa = ipa.replace("r", "ɹ")
    if not ipa:
        return ipa
    elif "/" not in ipa:
        ipa = "/"+ipa+"/"

    return f"{t.bold_green}"+ipa

def lexico():
    url = "https://www.lexico.com/en/definition/"
    selector = "span.phoneticspelling"
    titles = ipa_requests(url, selector)

    if titles:
        ipa = titles[1].text
        ipa = cleaner(ipa)
        print(ipa)

        try:
            ipa2 = titles[3].text
            ipa2 = cleaner(ipa2)
            if ipa != ipa2:
                print(ipa2)

        except:
            pass

        if not ipa:
            ipa = titles[0].text
            ipa = cleaner(ipa)
            print(ipa)

    else:
        print("Word not find")



def ipa_cmu(word = None):
    def palabra(word):
        palabra = engipa.ipa_list(word)
        for i in palabra[0]:
            i = cleaner(i)
            print(i)

    def frase(word):
        oracion = engipa.convert(word)
        oracion = cleaner(oracion)
        print(oracion)

    if not word:
        word = str(input("Ingresa una palabra: ")).lower()

    word_list = word.split()

    if len(word_list) == 1:
        palabra(word)

    elif len(word_list) >= 2:
        frase(word)
    else:
        print("Error")



def run():
    pagina = str(input(choise))

    if pagina == "1":
        print("Lexico")
        lexico()
        run()
    elif pagina == "2":
        print("CMU")
        ipa_cmu()
        run()
    elif pagina == "9":
        print("Atras")
        main.inicio()
    else:
        print("Ingresa una opción correcta")
        run()
