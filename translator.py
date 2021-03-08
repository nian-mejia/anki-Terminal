import main
import numpy as np
from deep_translator import LingueeTranslator
from deep_translator import GoogleTranslator
from tabulate import tabulate

choise = """
[1] Linguee
[2] Google Trasnslator
[9] Atras
    
Ingresa un número: """

choise  = choise.replace("[", "\033[1;33m[").replace(" ", " \033[0;37m")

def do_translat(translator):
    word = str(input("Ingresa una palabra: ")).lower()
    if not word:
        do_translat()

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
        
        print("\033[1;32m", tabulate(a))

            

def googletrans():
    translated = do_translat(GoogleTranslator)
    if translated:
        print("\033[1;32m", translated.capitalize())

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
