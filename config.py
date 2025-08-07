import os
from dotenv import load_dotenv
load_dotenv()

ACCESSTOKEN = os.getenv("ACCESSTOKEN")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB = os.getenv("SUPABASE_DB")