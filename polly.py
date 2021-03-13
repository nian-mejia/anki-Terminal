import main
import time
import boto3
import time
import yaml
from boto3.session import Session
from blessings import Terminal
from progress.bar import IncrementalBar


# Create object text to change the color
t = Terminal()

with open(r'aws_key.yaml') as file_aws:
    lista_aws = yaml.full_load(file_aws)
    file_aws.close()

choise = """
[1] Crear audio nuevo
[2] Descargar audio nuevo
[3] Descargar audios creados
[4] Eliminar audio creados
[9] Atras
    
Ingresa un número: """

choise = choise.replace("[", f"{t.bold_yellow}[").replace(" ", f" {t.normal}")

def delete(my_bucket, name_file):
    respuesta = my_bucket.delete_objects(Bucket=lista_aws["buckets"],
                                        Delete={'Objects': [{'Key': name_file}]})
    return respuesta

def delete_audio():
    lista, my_bucket = list_audios()
    if lista:
        eliminar = str(input(f"{t.normal}Eliminar un archivo y/n: {t.bold_yellow}")).lower()
        if eliminar == "y":
            file = str(input(f"{t.normal}Nombre del archivo: {t.bold_yellow}"))
            respuesta = delete(my_bucket, file)            
            if respuesta["Deleted"][0]["DeleteMarker"] == True:
                print(f"{t.normal}Solicitud enviada")
                verificar = str(
                    input(f"{t.normal}¿Desea verificar si se eliminó correctamente? y/n: {t.bold_yellow}")).lower()
                if verificar == "y":
                    print(f"{t.normal}Lista de audios:\n")
                    lista, b = list_audios()
                    if not lista:
                        print(f"{t.normal}Lista vacia. Intenta nuevamente")
            else:
                print(f"{t.bold_red}Error en la solicitud")
        else:
            run()
    else:
        print(f"{t.normal}\nLista vacia. Intenta nuevamente")

    run()


def status(word, taskId):
    statu = {'scheduled': "en petición", 'inProgress': "en proceso",
                    'completed': "generado", 'failed': "fallido"}

    generado = statu["completed"]      
    estado   = statu["scheduled"]   
    
    # Create incrementalBar
    bar = IncrementalBar(f"{t.normal}Creating audio{t.bold_green}", max=4)

    while estado != generado:
        try:
            polly_client = cliente()
            task_status = polly_client.get_speech_synthesis_task(TaskId=taskId)
            s = task_status["SynthesisTask"]["TaskStatus"]
            estado =  statu[s]
            #print(f"{t.normal}Espera el audio {t.bold_green}{estado}{t.normal}, puede tomar unos segundos")
            bar.next()
            time.sleep(5)

        except:
            print(f"{t.normal}Intenta crear primero el audio")
            polly_tarea()
    
    if generado:
        bar.finish()
        copy(taskId + ".mp3", word)
        s3 = sessionS3()
        my_bucket = s3.Bucket(lista_aws["buckets"])
        delete(my_bucket, taskId + ".mp3")
    

def copy(old_name, new_name):
    s3 = sessionS3()
    my_bucket = s3.Bucket(lista_aws["buckets"])
    my_bucket.copy({"Bucket" : lista_aws["buckets"], 
                    'Key' : old_name},
                     Key = new_name)

def list_audios():
    s3 = sessionS3()
    my_bucket = s3.Bucket(lista_aws["buckets"])

    lista = []

    for s3_files in my_bucket.objects.all():
        print(f"{t.bold_green}{s3_files.key}")
        lista.append(s3_files.key)

    return lista, my_bucket


def list_sound():
    lista, my_bucket = list_audios()
    if lista:
        download = str(input(f"{t.normal}Descargar un archivo y/n: {t.bold_yellow}")).lower()
        if download == "y":
            file = str(input(f"{t.normal}Nombre del archivo: {t.bold_yellow}"))
            try:
                my_bucket.download_file(file, "{}{}".format(
                    lista_aws["root"], file.replace(" ", "_")))
                print(f"{t.bold_green}Descarga completada")
            except:
                print(f"{t.bold_red}Este archivo no se encontró")
        else:
            run()
    else:
        print(f"{t.bold_yellow}\nLista vacia. Intenta nuevamente")
    run()


def cliente():
    polly_client = boto3.Session(
        aws_access_key_id=lista_aws["access_key_id"],
        aws_secret_access_key=lista_aws["secret_access_key"],
        region_name='us-east-1').client("polly")
    return polly_client


def sessionS3():
    session = Session(aws_access_key_id=lista_aws["access_key_id"],
                      aws_secret_access_key=lista_aws["secret_access_key"],
                      region_name='us-east-1')
    s3 = session.resource('s3')
    return s3


def polly_tarea(word = None):
    
    if not word:
        word = solicitud()
        
    polly_client = cliente()
    response = polly_client.start_speech_synthesis_task(
        Engine='neural',
        LanguageCode='en-US',
        OutputS3BucketName=lista_aws["buckets"],
        OutputFormat='mp3',
        SampleRate='24000',
        VoiceId='Salli',
        Text=word)

    taskId = response['SynthesisTask']['TaskId']
    
    global newWord
    newWord = word.replace(" ", "_") + ".mp3"

    print(f"{t.normal}Task id is {t.bold_yellow}{taskId} ")
    status(newWord, taskId)
    return newWord

def descargar(word = None):
    global newWord

    word = newWord
    try:
        file = word
    except:
        print(f"{t.normal}Primero crea una palabra o descarga una ya generada en listar")
        run()
    
    s3 = sessionS3()
    my_bucket = s3.Bucket(lista_aws["buckets"])

    print(f"{t.bold_green}Descargando elemento...")

    my_bucket.download_file(file, "{}{}".format(
        lista_aws["root"], word))
    print(f"{t.bold_green}Descarga completada")

    


def solicitud():
    global word
    word = str(input(f"{t.normal}Ingresa una palabra/oración: {t.bold_yellow}")).lower()
    if not word:
        solicitud()
    return word


def run():
    pagina = str(input(choise))

    print(f"{t.normal}")

    if pagina == "1":
        print("Crear audio nuevo")
        polly_tarea()
        run()

    elif pagina == "2":
        print("Descargar audio nuevo")
        descargar()
        run()

    elif pagina == "3":
        print("Descargar audios creados")
        list_sound()

    elif pagina == "4":
        print("Eliminar audio creados")
        delete_audio()

    elif pagina == "9":
        print("Atras")
        main.inicio()
    else:
        print("Ingresa una opción correcta")
        run()
