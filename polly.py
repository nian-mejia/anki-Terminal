import main
import time
import boto3
import time
import yaml
from boto3.session import Session

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

choise  = choise.replace("[", "\033[1;33m[").replace(" ", " \033[0;37m")

def delete(my_bucket, name_file):
    respuesta = my_bucket.delete_objects(Bucket=lista_aws["buckets"],
                                        Delete={'Objects': [{'Key': name_file}]})
    return respuesta

def delete_audio():
    lista, my_bucket = list_audios()
    if lista:
        eliminar = str(input("\033[0;37mEliminar un archivo y/n: \033[1;32m")).lower()
        if eliminar == "y":
            file = str(input("\033[0;37mNombre del archivo: \033[1;32m"))
            respuesta = delete(my_bucket, file)            
            if respuesta["Deleted"][0]["DeleteMarker"] == True:
                print("\033[0;37mSolicitud enviada")
                verificar = str(
                    input("\033[0;37m¿Desea verificar si se eliminó correctamente? y/n: \033[1;32m")).lower()
                if verificar == "y":
                    print("\033[0;37mLista de audios:\n")
                    lista, b = list_audios()
                    if not lista:
                        print("\033[0;37mLista vacia. Intenta nuevamente")
            else:
                print("\033[1;31mError en la solicitud")
        else:
            run()
    else:
        print("\033[0;37m\nLista vacia. Intenta nuevamente")

    run()


def status():
    statu = {'scheduled': "peticion", 'inProgress': "en proceso",
                    'completed': "generado", 'failed': "fallido"}

    generado = statu["completed"]      
    estado   = statu["scheduled"]   
    while estado != generado:
        try:
            polly_client = cliente()
            task_status = polly_client.get_speech_synthesis_task(TaskId=taskId)
            s = task_status["SynthesisTask"]["TaskStatus"]
            estado =  statu[s]
            print("\033[0;37mEspera el audio está en \033[1;33m{}\033[0;37m, puede tomar unos segundos".format(estado))
            print("\033[0;37mAudio " + estado)
            time.sleep(5)

        except:
            print("\033[0;37mIntenta crear primero el audio")
            polly_tarea()
    
    if generado:
        global word
        copy(taskId + ".mp3", word)
        s3 = sessionS3()
        my_bucket = s3.Bucket(lista_aws["buckets"])
        delete(my_bucket, taskId + ".mp3")
    
    run()

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
        print("\033[1;32m", s3_files.key)
        lista.append(s3_files.key)

    return lista, my_bucket


def list_sound():
    lista, my_bucket = list_audios()
    if lista:
        download = str(input("\033[0;37mDescargar un archivo y/n: \033[1;32m")).lower()
        if download == "y":
            file = str(input("\033[0;37mNombre del archivo: \033[1;32m"))
            try:
                my_bucket.download_file(file, "{}{}".format(
                    lista_aws["root"], file.replace(" ", "_")))
                print("\033[0;33mDescarga completada")
            except:
                print("\033[1;31mEste archivo no se encontró")

        else:
            run()
    else:
        print("\033[0;32m\nLista vacia. Intenta nuevamente")

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


def polly_tarea():
    global word 

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
    
    word = word.replace(" ", "_") + ".mp3"

    print("\033[0;37mTask id is \033[1;32m{} ".format(taskId))
    status()
    run()


def descargar():
    global word
    try:
        file = word
    except:
        print("\033[0;37mPrimero crea una palabra o descarga una ya generada en listar")
        run()
    
    s3 = sessionS3()
    my_bucket = s3.Bucket(lista_aws["buckets"])

    print("\033[0;37mDescargando elemento...")

    my_bucket.download_file(file, "{}{}".format(
        lista_aws["root"], word))
    print("\033[1;32mDescarga completada")

    run()


def solicitud():
    global word
    word = str(input("\033[0;37mIngresa una palabra/oración: \033[1;32m")).lower()
    if not word:
        solicitud()
    return word


def run():
    pagina = str(input(choise))

    print("\033[0;37m")

    if pagina == "1":
        print("Crear audio nuevo")
        polly_tarea()

    elif pagina == "2":
        print("Descargar audio nuevo")
        descargar()

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
