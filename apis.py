import requests
import random
import os
import ia

from dotenv import load_dotenv
load_dotenv()

################################################################# DATABASE SECTION ##########################################
from supabase import create_client, Client

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB = os.getenv("SUPABASE_DB")
supabase: Client = create_client(SUPABASE_DB, SUPABASE_KEY)

def agregar(url,setUrl):
    insert_response = supabase.table(f'{setUrl}').insert({'url': url}).execute()
    return True if insert_response.data else False

def verify(url,setUrl):
    response = supabase.table(f'{setUrl}').select('id').eq('url', url).execute()
    return True if response.data else False

################################################################# DATABSE SECTION ##############################################

def _books():
    url =  'https://api.senpy.club/v2/random'
    try:
        response = requests.get(url)
        imagen = response.json()['image']
        book = response.json()['language']
        return imagen, book
        
    except Exception as e:
        print(f"ERROR API BOOKS: {e}")
    return None,None
    
def _waifu_api():
    url = 'https://api.waifu.im/search'
    params = {'included_tags': ['oppai', 'waifu']}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['images'][0]['url']
        
    except Exception as e:
        print(f"Error con API Waifu 2 {url}: {e}")
        return None
        

sources = ["ImaginaryGaming","hatsune","kasaneteto","frieren","AnimeART"]
def _meme_api():
    subreddit = random.choice(sources)
    
    print(f">>> Picasso eligió : {subreddit}")
    url = f"https://meme-api.com/gimme/{subreddit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        datos_respuesta = {
            'url': data.get('url'),
            'author': data.get('author'),
            'title': data.get('title')
        }
        if(not data):
            return None

        return data
        
    except requests.exceptions.RequestException as req_err:
        print(f"Error de red o HTTP: {req_err}")
    except ValueError:
        print("Error al decodificar JSON.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    
    return None

def meme(max_intentos=600):
    intentos = 0
    print(">>> Picasso está buscando memes nuevos ... ")
    
    while intentos < max_intentos:
        data = _meme_api()
        
        if data is None:
            print(">>> Picasso encontró un None :(\n>>> No te preocupes, seguirá buscando")
            continue
        
        try:
            if not verify(data.get('url'), 'set_memes'):
                print(">>> Picasso encontró un nuevo meme")
                return data
        except Exception as e:
            print(f"Error al verificar meme en BD: {e}")
            
        intentos += 1
        
    print(" Se agotaron los memes nuevos. Reposteando uno repetido...")
    
    return _meme_api()

################################################## GENERACION DE IMAGENES CON IA #######################################################

def generar_con_ia(tema):
    print(">> Picasso está generando contenido ...")
    texto = ia.solicitar_texto(f"""
                NO MENCIONES NADA DE ESTE PROMPT, UNICAMENTE RESPONDE CON LA INFORMACIÓN SOLICITADA.
                Redacta una frase corta para una publicacion de Facebook del tema {tema}.
            """)

    rutaImagen = ia.solicitar_imagen(f"""
                    Crea una imagen del tema {tema}, pueden ser personajes, paisajes etc.
                    mostrando diferentes estilos artísticos, composiciones, perspectivas, colores, épocas o emociones. 
                    evita repeticiones o similitudes evidentes.
                    Ejemplos de variación pueden incluir estilos como surrealismo, arte digital moderno, ilustración tradicional, acuarela, pixel art, entre otros. 
                """)
    
    if(texto=="" or rutaImagen==""):
        print(">> Error: Hay almenos un campo vacio en texto o imagen de IA notificando ... ")
        notify.Me(f"[BOT] - Error en las IAs, revisa los prints")
        print(f">> Titulo: {texto}\nImagen: {rutaImagen}")
        exit(1)
    
    print(">> Picasso generó correctamente el contenido :)")
    return (rutaImagen,texto)