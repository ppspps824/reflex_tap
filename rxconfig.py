import os

import reflex as rx
from dotenv import load_dotenv

load_dotenv(verbose=True)
db_password = os.getenv("SUPABASE_PASS")

config = rx.Config(
    app_name="reflex_tap",
    db_url=f"postgresql://postgres.ungflstwnvrhxjofilrb:{db_password}@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres",
)
