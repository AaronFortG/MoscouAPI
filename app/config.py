import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("SUPABASE_DATABASE_URL is not set in the .env file")