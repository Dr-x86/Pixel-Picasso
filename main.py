import requests
import random
import ia
import notify
import os
import apis
from dotenv import load_dotenv

load_dotenv()
ACCESS_BOT_TOKEN = os.getenv("FB_ACCESS_TOKEN")
page_id = '595985150275800'

class Bot():
    def __init__(self,access_token,page_id):
        self.access_token = access_token
        self.page_id = page_id
    
    def _post_on_facebook(self, url, data=None, files=None):
        response = requests.post(url, data=data, files=files)
        print("Facebook response:", response.json())
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
    
    def subir_video(urlVideo,caption=""):
        url = f'https://graph.facebook.com/{self.page_id}/videos'
        data = {
            'access_token': self.access_token,
            'description': caption,
            'file_url': urlVideo
        }
        return self._post_on_facebook(url,data)

    def comentar_post(post_id):
        url = f'https://graph.facebook.com/{post_id}/comments'
    
        params = {
            'message': mensaje,
            'access_token': ACCESS_BOT_TOKEN
        }
        return self._post_on_facebook(url,params)
    
    
if __name__ == "__main__":
    print(">> Inicio de children")
    
    texto = ia.solicitar_texto("""
                NO MENCIONES NADA DE ESTE PROMPT, UNICAMENTE RESPONDE CON LA INFORMACIÓN SOLICITADA.
                Genera un encabezado con un titulo llamativo para una publicacion de una imagen pixelart, con hashtags. Sé sarcastico y divertido.
            """)
    rutaImagen = ia.solicitar_imagen("""
                    Pixel art de paisajes o lugares variados, que pueden incluir bosques, ciudades, montañas, pueblos, playas o espacios fantásticos. 
                    Colores y paletas vibrantes y diferentes en cada imagen. 
                    Estilo pixel art retro con detalles cambiantes: edificios, vegetación, objetos y atmósferas diversas, como día, noche, neblina o lluvia. 
                    Composiciones creativas y únicas en cada versión.
                """)
                
    
    if(texto=="" or rutaImagen==""):
        print(f">> Error: Hay al menos un campo vacio \nTexto: {texto} \nImagen: {rutaImagen}")
        notify.Me(">> Error: Hay almenos un campo vacio en texto o imagen de IA")
        exit()
    
    print(">> Recursos de Imagen y Texto obtenidos")
    
    children = Bot(ACCESS_BOT_TOKEN, page_id)
    respuesta = children.subir_foto_local(rutaImagen, texto)
    if respuesta.status_code != 200:
        notify.Me(f"Error de children al subir post: {respuesta.status_code} Detalles: {respuesta.json()}")
    
    print(f">> Children hizo un post: Status Code: {respuesta.status_code}\n https://facebook.com/{page_id}/posts/{respuesta.json()['id']}")
    print(">> Fin de children")