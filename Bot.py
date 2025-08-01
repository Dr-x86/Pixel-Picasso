import requests
import os
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
    ######################################################### FUNCIONES PRINCIPALES #############################################################
    """
    
    def subir_contenido_ia(self):
        imagen = apis.generar_con_ia(self.tema)
        if (imagen):
            respuesta = self.subir_foto_local(imagen,"")
            if respuesta:
                post_id = respuesta.json()['id']
                print(f">> [IA] - Picasso posteo: https://facebook.com/{self.page_id}/posts/{post_id}")
            os.remove("images/imagenIA.png")
        else:
            print(">>[IA] Error grave: No generó la imagen")
            print(">>[IA] Error grave: No generó la imagen")
    
    def subir_meme(self):
        datos = apis.memes()
        if datos is None:
            print("[MEME] - Error grave: Datos = None en ultima capa")
            print("[MEME] - Error grave: Datos = None en ultima capa")
            return
        try: 
            respuesta = self.subir_foto(datos.get('url'),f" '{datos.get('title')}' ")
            
            if respuesta.status_code == 200:
                post_id = respuesta.json()['id']
                titulo = datos.get('title').lower()
                print(f">> [MEME] - Picasso posteo: https://facebook.com/{self.page_id}/posts/{post_id}")
            
                # if "my" in titulo or "(oc)" in titulo or "by me" in titulo: # Honor a quien honor merece
                    # print(f">> Picasso: Reconocimiento a: {datos.get('author')}")
                    # self.comentar_post(post_id, f"Credits: @{datos.get('author')}")
                
                if [x for x in ['(oc)','my','by me','mine','[oc]','i made','i did','i make',"i drew"] if x in titulo]: # Honor a quien honor merece
                    print(f">> Bot: comento ")
                    self.comentar_post(post_id,f"Credits: @{datos.get('author')}")
                else:
                    print(f">> Bot: comento ")
                    self.comentar_post(post_id,f"Suggested by: {datos.get('author')}")
                
                
                recordar(datos.get('url'),'set_pixelpicasso')
                
        except Exception as e:
            print(f"[MEME] - Excepcion: {e}")
            print(f"[MEME] - Excepcion: {e}")

    def subir_libro(self):
        datos = apis.books()
        
        if datos is None:
            print("[BOOKS] - Error grave: Datos=None en ultima capa")
            print("[BOOKS] - Error grave: Datos=None en ultima capa")
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
            print("[WAIFU] Error grave: datos = None en ultima capa")
            print("[WAIFU] Error grave: datos = None en ultima capa")
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