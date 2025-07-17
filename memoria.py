import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB = os.getenv("SUPABASE_DB")
supabase: Client = create_client(SUPABASE_DB, SUPABASE_KEY)

def recordar(url,setUrl):
    insert_response = supabase.table(f'{setUrl}').insert({'url': url}).execute()
    return True if insert_response.data else False

def verificar(url,setUrl):
    response = supabase.table(f'{setUrl}').select('id').eq('url', url).execute()
    return True if response.data else False
