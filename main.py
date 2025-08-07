from time import sleep
from Bot import Picasso
from config import ACCESSTOKEN

page_id = '595985150275800'

if __name__ == "__main__":
    print(">> Inicio de picasso")
    
    # Mi propio flujo
    
    bot = Picasso(ACCESSTOKEN,page_id,"Daniel","Waifus en pixel art") # Setear las caracteristicas del bot
    bot.subir_waifu()
    sleep(2)
    bot.subir_libro()
    
    print(">> Fin de picaso")