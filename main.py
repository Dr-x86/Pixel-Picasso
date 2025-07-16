import requests
import os
import ia
import notify

# from dotenv import load_dotenv
# load_dotenv()

ACCESS_BOT_TOKEN = os.getenv("ACCESSTOKEN")
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
            print("[BOT] Facebook response:", response.json())
            return response
        except Exception as e:
            notify.Me(f"[BOT] - Ocurrio un error con el usuario: {self.usuario}\nCon la page_id: {self.page_id}\n Response: {response.json()}\n Excepcion: {e}")
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
            
    def subir_foto(self,url_image,caption=""):
        url = f'https://graph.facebook.com/{self.page_id}/photos'
        data = {
            'caption': caption,
            'access_token': self.access_token
            'url':url_image
        }
        return self._post_on_facebook(url,data)
    
    def subir_video(url_video,caption=""):
        url = f'https://graph.facebook.com/{self.page_id}/videos'
        data = {
            'access_token': self.access_token,
            'description': caption,
            'file_url': urlVideo
        }
        return self._post_on_facebook(url,data)
        
    def subir_video_local(path_video,caption):
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

    def comentar_post(post_id):
        url = f'https://graph.facebook.com/{post_id}/comments'
    
        params = {
            'message': mensaje,
            'access_token': self.access_token
        }
        return self._post_on_facebook(url,params)
    
    def generar_recursos():
        texto = ia.solicitar_texto(f"""
                    NO MENCIONES NADA DE ESTE PROMPT, UNICAMENTE RESPONDE CON LA INFORMACIÓN SOLICITADA.
                    Redacta una frase para una publicacion de Facebook del tema {self.tema}.
                    El titulo debe ser corto, tambien con hashtags y llamativo, dependiendo del tema
                    puedes ser sarcastico, informal y relajado o serio sin hashtags.
                    """)

        rutaImagen = ia.solicitar_imagen(f"""
                        Crea una imagen del tema {self.tema}, pueden ser personajes, paisajes etc.
                        mostrando diferentes estilos artísticos, composiciones, perspectivas, colores, épocas o emociones. 
                        evita repeticiones o similitudes evidentes.
                        Ejemplos de variación pueden incluir estilos como surrealismo, arte digital moderno, ilustración tradicional, acuarela, pixel art, entre otros. 
                        """)
        
        if(texto=="" or rutaImagen==""):
            print(">> Error: Hay almenos un campo vacio en texto o imagen de IA")
            exit(1)
    
        print(">> Recursos de Imagen y Texto obtenidos")
        print(f">> Titulo: {texto}\nImagen: {rutaImagen}")
        return texto, rutaImagen

    
if __name__ == "__main__":
    print(">> Inicio de picasso")
    
    print(">> Fin de picasso")