import requests
from bs4 import BeautifulSoup
import main
from blessings import Terminal
t = Terminal()

choise = """
[1] Buscar ejemplos
[9] Atras

Ingresa un número: """

choise = choise.replace("[", f"{t.bold_yellow}[").replace(" ", f" {t.normal}")


def words():
    word = str(input("Ingresa una palabra: ")).lower()
    return word


def ingles_example(word = None):
    if not word: 
        word = words()
    url = f'https://www.ingles.com/traductor/{word}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    english = soup.select("._1f2Xuesa")
    spanish = soup.select("._3WrcYAGx")
    for en, es in zip(english, spanish):
        print(en.text, "\n", es.text)


def run():
    pagina = str(input(choise))
    if pagina == "1":
        print("Buscar ejemplos")
        ingles_example()
        run()
        
    elif pagina == "9":
        print("Atras")
        main.inicio()
    else:
        print("Ingresa una opción correcta")
        run()
