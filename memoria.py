from supabase import create_client, Client
from config import SUPABASE_DB, SUPABASE_KEY


supabase: Client = create_client(SUPABASE_DB, SUPABASE_KEY) # Inicializa el cliente para la base de datos

def recordar(url,setUrl):
    insert_response = supabase.table(f'{setUrl}').insert({'url': url}).execute()
    return True if insert_response.data else False

def verificar(url,setUrl):
    response = supabase.table(f'{setUrl}').select('id').eq('url', url).execute()
    return True if response.data else False
