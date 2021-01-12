import ipa
import translator
import polly
import example
import yaml

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

def run():
    config = config_def()
    choise_options(config)