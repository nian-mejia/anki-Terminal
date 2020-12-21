import main
import detectlanguage
from googletrans import Translator
from deep_translator import LingueeTranslator
from deep_translator import GoogleTranslator

choise = """
[1] Linguee EN - ES
[2] Linguee ES - EN
[3] Google Trasnlator EN - ES
[4] Google Translator ES - EN
[9] Atras

Ingresa un número: """

def solicitud():
    word = str(input("Ingresa una palabra: ")).lower()
    if not word:
        solicitud()

    translator = Translator()
    language   = translator.detect(word)
    language   = language.lang

    return word, language

def do_translat(translator):
    word,language = solicitud()    
    
    if language == "en":
        dest = "es"
    else:
        dest = "en"
    if translator == LingueeTranslator:
        translated = translator(source=language, target= dest).translate(word, return_all=True)
    else:
        translated = translator(source=language, target= dest).translate(word)
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
        print("Linguee EN - ES")
        linguee_en_es()
    
    elif pagina == "2":
        print("Linguee ES - EN")
        linguee_es_en()

    elif pagina == "3":
        print("Google Trasnslator EN - ES")
        googletrans_en_es()

    elif pagina == "4":
        print("Google Trasnslator ES - EN")
        googletrans_es_en()        

    elif pagina == "9":
        print("Atras")
        main.inicio()
        
    else:
        print("Ingresa una opción correcta")
        run()