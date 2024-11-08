from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os


# Load environment variables from .env
load_dotenv()

class Settings(BaseSettings):
    HOST: str
    USER: str
    DATABASE: str
    PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    @property
    def DATABASE_URL(self):
        return f"mysql+mysqlconnector://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DATABASE}"
    
    class Config:
        env_file = ".env" 

settings = Settings()



