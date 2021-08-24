import ipa
import translator
import polly
import example
from blessings import Terminal

t = Terminal()

choise = """
[1] IPA
[2] Traductor
[3] Ejemplos
[4] Audio
[5] Todo
[9] Salir

Ingresa un número: """

choise = choise.replace("[", f"{t.bold_yellow}[").replace(" ", f" {t.normal}")


def all():
    word = str(input("Ingresa una palabra: ")).lower()
    ipa.ipa_cmu(word)
    translator.googletrans(word)
    example.ingles_example(word)
    word = polly.polly_tarea(word)
    polly.descargar(word)


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
        all()

    elif pagina == "9":
        print("Salir")
        exit()
    else:
        print("Ingresa una opción correcta")
        inicio()


if __name__ == "__main__":
    inicio()
