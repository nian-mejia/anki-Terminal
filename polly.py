import main
import boto3
import time
import yaml
from boto3.session import Session

with open(r'aws_key.yaml') as file_aws:
    lista_aws = yaml.full_load(file_aws)
    file_aws.close()

choise = """
[1] Crear audio
[2] Estado
[3] Descargar audio
[4] Listar
[5] Eliminar audio
[9] Atras
    
Ingresa un número: """


def delete_audio():
    run()



def status():
    try:
        task_status = polly_client.get_speech_synthesis_task(TaskId=taskId)
        s = task_status["SynthesisTask"]["TaskStatus"]
        statu = {'scheduled': "en peticion", 'inProgress': "en proceso",
                 'completed': "generado", 'failed': "fallido"}
        print("Audio " + statu[s])

    except:
        print("Intenta crear primero el audio")
        run()


def list_sound():
    session = seccion()
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(lista_aws["buckets"])

    lista = []

    for s3_files in my_bucket.objects.all():
        print(s3_files.key)
        lista.append(s3_files.key)

    if lista:
        download = str(input("Descargar un archivo y/n: ")).lower()
        if download == "y":
            file = str(input("Nombre del archivo: "))
            try:
                my_bucket.download_file(file, "{}{}.mp3".format(
                    lista_aws["root"], file.replace(" ", "_")))
                print("Descarga completada")
            except:
                print("Este archivo no se encontró")

        else:
            run()
    else:
        print("\nLista vacia. Intenta nuevamente")

    run()


def cliente():
    polly_client = boto3.Session(
        aws_access_key_id=lista_aws["access_key_id"],
        aws_secret_access_key=lista_aws["secret_access_key"],
        region_name='us-east-1').client("polly")
    return polly_client


def seccion():
    session = Session(aws_access_key_id=lista_aws["access_key_id"],
                      aws_secret_access_key=lista_aws["secret_access_key"],
                      region_name='us-east-1')
    return session


def polly_tarea():
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

    global taskId
    taskId = response['SynthesisTask']['TaskId']

    print("Task id is {} ".format(taskId))
    status()
    run()


def descargar():
    try:
        file = taskId + ".mp3"
    except:
        print("Primero crea una palabra o descarga una ya generada en listar")
        run()

    session = seccion()

    s3 = session.resource('s3')
    my_bucket = s3.Bucket(lista_aws["buckets"])

    print("Descargando elemento...")

    
    my_bucket.download_file(file, "{}{}.mp3".format(
        lista_aws["root"], word.replace(" ", "_")))
    print("Descarga completada")
    
    run()


def solicitud():
    global word
    word = str(input("Ingresa una palabra/oración: ")).lower()
    if not word:
        solicitud()
    return word


def run():
    pagina = str(input(choise))

    if pagina == "1":
        print("Crear audio")
        polly_tarea()

    elif pagina == "2":
        print("Estado")
        status()

    elif pagina == "3":
        print("Descargar audio")
        descargar()

    elif pagina == "4":
        print("Listar audios")
        list_sound()

    elif pagina == "5":
        print("Eliminar audios")
        delete_audio()

    elif pagina == "9":
        print("Atras")
        main.inicio()
    else:
        print("Ingresa una opción correcta")
        run()
