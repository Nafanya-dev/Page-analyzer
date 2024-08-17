from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

SECRET_KEY: Optional[str] = os.getenv('SECRET_KEY')
DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
