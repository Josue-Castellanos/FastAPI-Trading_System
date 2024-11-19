from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+mysqlconnector://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    model_config = SettingsConfigDict(env_file=None)


class TestSettings(BaseSettings):
    TEST_DATABASE_HOSTNAME: str
    TEST_DATABASE_USERNAME: str
    TEST_DATABASE_NAME: str
    TEST_DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    
    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"mysql+mysqlconnector://{self.TEST_DATABASE_USERNAME}:{self.TEST_DATABASE_PASSWORD}@{self.TEST_DATABASE_HOSTNAME}/{self.TEST_DATABASE_NAME}"
    
    load_dotenv()
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
test_settings = TestSettings()



