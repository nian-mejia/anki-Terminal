import main
import numpy as np
from deep_translator import LingueeTranslator
from deep_translator import GoogleTranslator
from tabulate import tabulate
from blessings import Terminal
t = Terminal()

choise = """
[1] Linguee
[2] Google translator
[9] Atras

Ingresa un número: """

choise = choise.replace("[", f"{t.bold_yellow}[").replace(" ", f" {t.normal}")

def do_translat(translator, word = None):

    if not word:
        word = str(input("Ingresa una palabra: ")).lower()

    if translator == LingueeTranslator:
        try:
            translated = translator(source="en", target="es").translate(
                word, return_all=True)
            return translated
        except:
            print("Error")

    else:
        try:
            translated = translator(source="en", target="es").translate(word)
            return translated
        except:
            print("Error")

def linguee():

    translate = do_translat(LingueeTranslator)
    if translate:
        l = len(translate) / 2
        if l == int(l):
            a = np.array(translate).reshape(int(l), 2)
        else:
            translate.append(" ")
            l = len(translate) / 2
            a = np.array(translate).reshape(int(l), 2)

        print(f"{t.bold_green}{tabulate(a)}")



def googletrans(word = None):
    translated = do_translat(GoogleTranslator, word)
    if translated:
        print(f"{t.bold_green}{translated.capitalize()}")

def run():
    pagina = str(input(choise))

    if pagina == "1":
        print("Linguee")
        linguee()
        run()

    elif pagina == "2":
        print("Google Trasnslator")
        googletrans()
        run()

    elif pagina == "9":
        print("Atras")
        main.inicio()

    else:
        print("Ingresa una opción correcta")
        run()
