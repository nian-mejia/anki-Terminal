import ipa
import translator
import polly
import example
import yaml


choise = """
[1] IPA
[2] Traductor
[3] Ejemplos
[4] Audio
[5] Todo
[6] Ver configuración
[9] Salir

Ingresa un número: """

def config_def():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        f.close
    return config

def choise_options(config):
    if config["ipa"]["wikitionary"] and config["ipa"]["lexico"] == 1:
        print("Elije solo una opción de ipa")
    elif config["ipa"]["CMU"] and config["ipa"]["wikitionary"] == 1:
        print("Elije solo una opción de ipa")

    elif config["ipa"]["wikitionary"] == 1:
        ipa.wiktionary()
    elif config["ipa"]["lexico"] == 1:
        ipa.lexico()
    elif config["ipa"]["CMU"] == 1:
        ipa.ipa_cmu()
    else: 
        print("Revisa la configuración en config.yaml sección IPA")

    if config["translator"]["googletranslate"] and config["translator"]["linguee"] == 1:
        print("Revisa la configuración en config.yaml, has elegido varios motores de traducción")
    elif config["translator"]["googletranslate"] == 1:
        translator.googletrans()

    elif config["translator"]["linguee"] == 1:
        translator.linguee()
    else: 
        print("Revisa la configuración en config.yaml sección translate")
    
    # example.run()
    # polly.run()

def inicio():
    pagina = str(input(choise))

    if pagina == "1":
        print("IPA")
        ipa.run()

    elif pagina == "2":
        print("Traductor")
        translator.run()

    elif pagina == "3":
        print("Ejemplos")
        example.run()

    elif pagina == "4":
        print("Audio")
        polly.run()

    elif pagina == "5":
        print("Todo")
        config = config_def()
        choise_options(config)
        inicio()

    elif pagina == "6":
        print("Ver configuración")
        config = config_def()
        print(config)
        inicio()


    elif pagina == "9":
        print("Salir")
        exit()
    else:
        print("Ingresa una opción correcta")
        inicio()


if __name__ == "__main__":
    inicio()
