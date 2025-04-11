from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL") 


settings = Settings()
