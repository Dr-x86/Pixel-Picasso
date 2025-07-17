import requests
import os
import notify
import apis
from time import sleep

from dotenv import load_dotenv
load_dotenv()

ACCESSTOKEN = os.getenv("ACCESSTOKEN")
page_id = '595985150275800'

class Bot():
    def __init__(self,access_token,page_id,usuario,tema):
        self.access_token = access_token
        self.page_id = page_id
        self.usuario = usuario
        self.tema = tema
        
    def _post_on_facebook(self, url, data=None, files=None):
        try:
            response = requests.post(url, data=data, files=files)
            print("\n\n[BOT] Facebook response:", response.json())
            return response
        except Exception as e:
            notify.Me(f"[BOT] - Ocurrio un error con el usuario: {self.usuario}\nCon la page_id: {self.page_id}\nResponse: {response.json()}\nExcepcion: {e}")
            return ""
        
    def subir_foto_local(self, image_path, caption=""):
        url = f'https://graph.facebook.com/{self.page_id}/photos'
        data = {
            'caption': caption,
            'access_token': self.access_token
        }
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            return self._post_on_facebook(url, data=data, files=files)
            
    def subir_foto(self, url_image, caption=""):
        url = f'https://graph.facebook.com/{self.page_id}/photos'
        data = {
            'caption': caption,
            'access_token': self.access_token,
            'url':url_image
        }
        return self._post_on_facebook(url,data)
    
    def subir_video(self, url_video,caption=""):
        url = f'https://graph.facebook.com/{self.page_id}/videos'
        data = {
            'access_token': self.access_token,
            'description': caption,
            'file_url': url_video
        }
        return self._post_on_facebook(url,data)
        
    def subir_video_local(self,path_video,caption):
        url = f'https://graph.facebook.com/{self.page_id}/videos'
        
        with open(path_video, 'rb') as video_file:
            files = {
                'source': video_file
            }
            data = {
                'description': caption,
                'access_token': self.access_token
            }
            res = self._post_on_facebook(url,data=data,files=files)
        return res

    def comentar_post(self, post_id, mensaje):
        url = f'https://graph.facebook.com/{post_id}/comments'
    
        params = {
            'message': mensaje,
            'access_token': self.access_token
        }
        
        return self._post_on_facebook(url,params)
    
    
if __name__ == "__main__":
    print(">> Inicio de picasso")
    
    bot = Bot(ACCESSTOKEN,page_id,"Daniel","Naturaleza, casas etc.") # Setear las caracteristicas del bot
    
    # Test rápido IA
    
    imagen,titulo = apis.generar_con_ia(bot.tema)
    respuesta = bot.subir_foto_local(imagen,titulo)
    if respuesta:
        post_id = respuesta.json()['id']
        print(f">> Picasso posteo: https://facebook.com/{page_id}/posts/{post_id}")
    
    os.remove("images/imagenIA.png")
    
    # Test de externos <=================== Ratatouille
    sleep(5)
    
    datos = apis.meme()
    respuesta = bot.subir_foto(datos.get('url'),datos.get('title'))
    
    if respuesta:
        post_id = respuesta.json()['id']
        titulo = datos.get('title')
        print(f">> Picasso posteo: https://facebook.com/{page_id}/posts/{post_id}")
        
        if "me" in titulo.lower() or "(oc)" in titulo.lower() or "by me" in titulo.lower(): # Honor a quien honor merece
            print(f">> Picasso: Reconocimiento a: {datos.get('author')}")
            bot.comentar_post(post_id, "Author: " + datos.get('author'))
    
    print(">> Fin de picasso")