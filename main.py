import ipa
import spanish
#help(ipa)

choise = """
[1] IPA
[2] Español
[3] Definición
[4] Audio
[5] Todo
[9] Salir
    
Ingresa un número: """

def inicio():
    pagina = str(input(choise))

    if pagina == "1":
        print("IPA")
        ipa.run()

    elif pagina == "2":
        print("Español")
        spanish.run()

    elif pagina == "3":
        print("Definición")
        inicio()

    elif pagina == "4":
        print("Audio")
        inicio()
    
    elif pagina == "5":
        print("Todo")
        inicio()

    elif pagina == "9":
        print("Salir")
        exit()
    else:
        print("Ingresa una opción correcta")
        inicio()



if __name__ == "__main__":
    inicio()