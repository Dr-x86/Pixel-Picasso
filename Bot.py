import requests
import os
import notify
import apis
from memoria import recordar

class Picasso():
    def __init__(self,access_token,page_id,usuario,tema):
        self.access_token = access_token
        self.page_id = page_id
        self.usuario = usuario
        self.tema = tema
        
    def _post_on_facebook(self, url, data=None, files=None):
        try:
            response = requests.post(url, data=data, files=files)
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
    
    """
    ##################### FUNCIONES PRINCIPALES
    """
    
    def subir_contenido_ia(self):
        imagen,titulo = apis.generar_con_ia(self.tema)
        if (imagen and titulo):
            respuesta = self.subir_foto_local(imagen,titulo)
            if respuesta:
                post_id = respuesta.json()['id']
                print(f">> [IA] - Picasso posteo: https://facebook.com/{page_id}/posts/{post_id}")
            os.remove("images/imagenIA.png")
        else:
            notify.Me(">>[IA] Error grave: no hay titulo ni texto")
            print("[SCRAPPER] - Error grave: Datos=None en ultima capa")
    
    def subir_meme(self):
        datos = apis.memes()
        respuesta = self.subir_foto(datos.get('url'),f" '{datos.get('title')}' ")
        
        if datos is None:
            notify.Me("[SCRAPPER] - Error grave: Datos=None en ultima capa")
            print("[SCRAPPER] - Error grave: Datos=None en ultima capa")
            return
        
        if respuesta:
            post_id = respuesta.json()['id']
            titulo = datos.get('title').lower()
            print(f">> [MEME] - Picasso posteo: https://facebook.com/{self.page_id}/posts/{post_id}")
        
            if "my" in titulo or "(oc)" in titulo or "by me" in titulo: # Honor a quien honor merece
                print(f">> Picasso: Reconocimiento a: {datos.get('author')}")
                self.comentar_post(post_id, f"Credits: @{datos.get('author')}")
            
            recordar(datos.get('url'),'set_memes')


    def subir_libro(self):
        datos = apis.books()
        
        if datos is None:
            notify.Me("[BOOKS] - Error grave: Datos=None en ultima capa")
            print("[BOOKS] - Error grave: Datos=None en ultima capa")
            return
        
        respuesta = self.subir_foto(datos.get('url'),datos.get('title'))
        if respuesta:
            post_id = respuesta.json()['id']
            print(f">> [BOOKS] - Picasso posteo: https://facebook.com/{self.page_id}/posts/{post_id}")
            
            recordar(datos.get('url'),'set_waifus')

    def subir_waifu(self):
        datos = apis.waifus()
        
        if(datos is None):
            notify.Me("[WAIFU] Error grave: datos = None en ultima capa")
            print("[WAIFU] Error grave: datos = None en ultima capa")
            return
        
        respuesta = self.subir_foto(datos.get('url'), datos.get('title'))
        if respuesta:
            post_id = respuesta.json()['id']
            print(f">> [WAIFU] - Picasso posteo: https://facebook.com/{self.page_id}/posts/{post_id}")
            
            if datos.get('author') != "desconocido" or datos.get('author') != None:
                print(f">> Picasso: Reconocimiento a: {datos.get('author')}")
                self.comentar_post(post_id, f"Credits: @{datos.get('author')}")
            
            recordar(datos.get('url'),'set_waifus')
        