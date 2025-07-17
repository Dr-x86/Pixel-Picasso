from time import sleep
from Bot import Picasso

import os
from dotenv import load_dotenv
load_dotenv()

ACCESSTOKEN = os.getenv("ACCESSTOKEN")
page_id = '595985150275800'


if __name__ == "__main__":
    print(">> Inicio de picasso")
    
    # Mi propio flujo
    
    bot = Picasso(ACCESSTOKEN,page_id,"Daniel","anime, casas, lugares.") # Setear las caracteristicas del bot
    
    bot.subir_meme()
    sleep(2)
    bot.subir_waifu()
    sleep(2)
    bot.subir_libro()
    
    """ De momento nada de IA """
    
    print(">> Fin de picaso")