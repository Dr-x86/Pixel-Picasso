import requests
from memoria import verificar

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
    print(">>> Picasso esta buscando waifus")
    while intentos < max_intentos:
        print(">>> Picasso intento: ",intentos)
        data = _waifu_api()
        
        if data is None:
            print(f">>> Picasso encontro None, pero no te preocupes seguira buscando ...")
            intentos += 1
            continue

        try:
            if not verificar(data['url'], 'set_pixelpicasso'):
                return data
        except Exception as e:
            print(f"[WAIFU] - Error al verificar URL en BD: {url}, error: {e}")

        intentos += 1
        
    print(">>> Picasso hara respost de waifus")
    data = _waifu_api()
    return data

def books(max_intentos=600):
    intentos = 0
    print(">>> Picasso esta buscando nuevos libros")
    while intentos < max_intentos:
        print(">>> Picasso intento: ",intentos)
        data = _books()
        
        if data is None:
            print(f">>> Picasso encontro None, pero no te preocupes seguira buscando ...")
            intentos += 1
            continue

        try:
            if not verificar(data.get('url'), 'set_pixelpicasso'):
                return data
        except Exception as e:
            print(f"[BOOKS] - Error al verificar URL en BD: {url}, error: {e}")

        intentos += 1
        
    print(">>> Picasso no encontro nevas imagenes, hara repost")
    data = _books()
    return data