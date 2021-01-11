import requests
from bs4 import BeautifulSoup
import main

choise = """
[1] Buscar ejemplos
[9] Atras

Ingresa un número: """

def words():
    word = str(input("Ingresa una palabra: ")).lower()
    return word

def ingles_example():
    word = words()
    url = f'https://www.ingles.com/traductor/{word}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    example = soup.select("._1f2Xuesa")
    for i in example:
        print(i.text)
    run()


def run():
    pagina = str(input(choise))

    if pagina == "1":
        print("Buscar ejemplos")
        ingles_example()
    elif pagina == "9":
        print("Atras")
        main.inicio()
    else:
        print("Ingresa una opción correcta")
        run()

if __name__ == "__main__":
    run()