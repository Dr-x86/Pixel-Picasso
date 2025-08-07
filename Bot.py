import requests
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
            response.raise_for_status()
            
        except Exception as e:
            print(f"[BOT] - Ocurrio un error con el usuario: {self.usuario}\nCon la page_id: {self.page_id}\nResponse: {response.json()}\nExcepcion: {e}")
        
        return response

    def subir_foto(self, url_image, caption=""):
        url = f'https://graph.facebook.com/{self.page_id}/photos'
        data = {
            'caption': caption,
            'access_token': self.access_token,
            'url':url_image
        }
        return self._post_on_facebook(url,data)
    
    def comentar_post(self, post_id, mensaje):
        url = f'https://graph.facebook.com/{post_id}/comments'
    
        params = {
            'message': mensaje,
            'access_token': self.access_token
        }
        
        return self._post_on_facebook(url,params)
    
    """
    ######################################################### FUNCIONES PRINCIPALES #############################################################
    """
    
    def subir_libro(self):
        datos = apis.books()
        
        if datos is None:
            print("[BOOKS] - Error grave: No se econtraron nuevas imagenes")
            print("[BOOKS] - Error grave: No se econtraron nuevas imagenes")
            return
        try:
            respuesta = self.subir_foto(datos.get('url'),datos.get('title'))
            if respuesta.status_code == 200:
                post_id = respuesta.json()['id']
                print(f">> [BOOKS] - Picasso posteo: https://facebook.com/{self.page_id}/posts/{post_id}")
                
                recordar(datos.get('url'),'set_pixelpicasso')
                
        except Exception as e:
            print(f"[BOOKS] - Excepcion: {e}")
            print(f"[BOOKS] - Excepcion: {e}")
        
    def subir_waifu(self):
        datos = apis.waifus()
        
        if(datos is None):
            print("[WAIFU] Error grave: No se econtraron nuevas imagenes")
            print("[WAIFU] Error grave: No se econtraron nuevas imagenes")
            return
        try:
            respuesta = self.subir_foto(datos.get('url'))
            
            if respuesta.status_code == 200:
                post_id = respuesta.json()['id']
                print(f">> [WAIFU] - Picasso posteo: https://facebook.com/{self.page_id}/posts/{post_id}")
            
                if not('desconocido' in datos.get('author')):
                    print(f">> Picasso: Reconocimiento a: {datos.get('author')}")
                    self.comentar_post(post_id, f"Credits: @{datos.get('author')}")
            
                recordar(datos.get('url'),'set_pixelpicasso')
        except Exception as e:
            print(f"[WAIFU] - Excepcion: {e}")
            print(f"[WAIFU] - Excepcion: {e}")