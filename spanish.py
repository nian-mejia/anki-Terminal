import main
from deep_translator import LingueeTranslator
from deep_translator import GoogleTranslator

choise = """
[1] Linguee
[2] Google Trasnslator
[3] Atras
    
Ingresa un número: """

def solicitud():
    word = str(input("Ingresa una palabra: ")).lower()
    if not word:
        solicitud()
    return word     

def linguee():
    word = solicitud()
    translated = LingueeTranslator(source='en', target='es').translate(word, return_all=True)
    print("")
    for i in translated:
        print(i.capitalize())
    run()

def googletrans():
    word = solicitud()
    translated = GoogleTranslator(source='en', target='es').translate(text=word)
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

    elif pagina == "3":
        print("Atras")
        main.inicio()
        
    else:
        print("Ingresa una opción correcta")
        run()