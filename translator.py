import main
from googletrans import Translator
from deep_translator import LingueeTranslator
from deep_translator import GoogleTranslator

choise = """
[1] Linguee
[2] Google Trasnslator
[9] Atras
    
Ingresa un número: """


def solicitud():
    word = str(input("Ingresa una palabra: ")).lower()
    if not word:
        solicitud()

    translator = Translator()
    language = translator.detect(word)
    language = language.lang

    if type(language) == list:
        if language[0] == "en" or language[0] == "es":
            return word, language[0]
        else:
            solicitud()
    else:
        if language == "en" or language == "es":
            return word, language
        else:
            solicitud()


def do_translat(translator):
    word, language = solicitud()

    if language == "en":
        dest = "es"
    else:
        dest = "en"
    if translator == LingueeTranslator:
        translated = translator(source=language, target=dest).translate(
            word, return_all=True)
    else:
        translated = translator(source=language, target=dest).translate(word)
    return translated


def linguee():
    translated = do_translat(LingueeTranslator)
    for i in translated:
        print(i.capitalize())

    run()


def googletrans():
    translated = do_translat(GoogleTranslator)
    print(translated.capitalize())
    run()


def run():
    pagina = str(input(choise))

    if pagina == "1":
        print("Linguee")
        linguee()

    elif pagina == "2":
        print("Google Trasnslator")
        googletrans()

    elif pagina == "9":
        print("Atras")
        main.inicio()

    else:
        print("Ingresa una opción correcta")
        run()
