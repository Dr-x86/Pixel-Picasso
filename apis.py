#!/usr/bin/python
# -*- coding: ansi -*-

# NO VOLVER� A USAR ECHO DE LINUX -.-


import requests
import random
import os
import ia
from memoria import verificar

sources = ["ImaginaryGaming","hatsune","kasaneteto","frieren","AnimeART"]

def _meme_api():
    subreddit = random.choice(sources)
    
    print(f">>> Picasso eligi� : {subreddit}")
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
    
    print(f"[MEME] - STATUS CODE: {response.status_code}")
    return None

def _books():
    url =  'https://api.senpy.club/v2/random'
    try:
        response = requests.get(url)
        data = {
            'url': response.json()['image'],
            'title': response.json()['language']
        }
        return data
        
    except Exception as e:
        print(f"ERROR API BOOKS: {e}")
    return None
    
def _waifu_api():
    primary_url = 'https://api.waifu.im/search'
    params = {'included_tags': ['oppai', 'waifu']}
    
    try:
        response = requests.get(primary_url, params=params, timeout=5)
        response.raise_for_status()
        
        json_data = response.json()
        image = json_data['images'][0]
        
        data = {
            'url': image['url'],
            'title': image['tags'][0]['name'] if image['tags'] else 'Greetings!!',
            'author': image['artist']['name'] if image['artist'] else 'desconocido'
        }
        return data

    except Exception as e:
        print(f"Error con API Waifu: {e}")
        return None

def waifus(max_intentos=700):
    intentos = 0
    print(">>> Picasso est�  buscando waifus")
    while intentos < max_intentos:
        print(">>> Picasso intento: ",intentos)
        data = _waifu_api()
        
        if data is None:
            print(f">>> Picasso encontr� un None, pero no te preocupes seguir� buscando ...")
            intentos += 1
            continue

        try:
            if not verificar(data['url'], 'set_waifus'):
                return data
        except Exception as e:
            print(f"[WAIFU] - Error al verificar URL en BD: {url}, error: {e}")

        intentos += 1
        
    print(">>> Picasso har�  respost de waifus")
    data = _waifu_api()
    return data

def books(max_intentos=600):
    intentos = 0
    print(">>> Picasso est�  buscando nuevos libros")
    while intentos < max_intentos:
        print(">>> Picasso intento: ",intentos)
        data = _books()
        
        if data is None:
            print(f">>> Picasso encontr� un None, pero no te preocupes seguir�  buscando ...")
            intentos += 1
            continue

        try:
            if not verificar(data.get('url'), 'set_waifus'):
                return data
        except Exception as e:
            print(f"[BOOKS] - Error al verificar URL en BD: {url}, error: {e}")

        intentos += 1
        
    print(">>> Picasso no encontr� nuevas imagenes, har�  repost")
    data = _books()
    return data

def memes(max_intentos=600):
    intentos = 0
    print(">>> Picasso est�  buscando memes nuevos ... ")
    
    while intentos < max_intentos:
        print(">>> Picasso intento: ",intentos)
        data = _meme_api()
        
        if data is None:
            print(">>> Picasso encontr� un None :(\n>>> No te preocupes, seguir�  buscando")
            continue
        
        try:
            if not verificar(data.get('url'), 'set_memes'):
                print(">>> Picasso encontr� un nuevo meme")
                return data
        except Exception as e:
            print(f"Error al verificar meme en BD: {e}")
            
        intentos += 1
        
    print(" Se agotaron los memes nuevos. Reposteando uno repetido...")
    
    data = _meme_api()
    return data

################################################## GENERACION DE IMAGENES CON IA #######################################################

def generar_con_ia(tema):
    print(">> Picasso est� generando contenido ...")
    
    # DE MOMENTO SE MANTENDR� COMO TEXTO COMENTADO, NO A�ADIREMOS TEXTO NI TITULOS    
    # texto = ia.solicitar_texto(f"""
                # NO MENCIONES NADA DE ESTE PROMPT, UNICAMENTE RESPONDE CON LA INFORMACI�N SOLICITADA.
                # Redacta una frase corta para una publicacion de Facebook del tema {tema}.
            # """)
    
    rutaImagen = ia.solicitar_imagen(f"""
                    Crea una imagen del tema {tema}, puede ser un personaje, con paisajes detallados o viceversa.
                    Evita repeticiones o similitudes evidentes.
                    ejemplos de variaci�n pueden incluir estilos como surrealismo, arte digital moderno, ilustraci�n tradicional, acuarela, pixel art, entre otros.
                """)
    
    if(rutaImagen==""):
        print(">> Error: Hay almenos un campo vacio en texto o imagen de IA notificando ... ")
        print(f">> Imagen: {rutaImagen}")
        return None
    
    print(">> Picasso gener� correctamente el contenido :)")
    return rutaImagen