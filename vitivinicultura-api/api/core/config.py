from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.

    Attributes:
        ALGORITHM (str): JWT signing algorithm.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration duration access tokens.
        DATABASE_URL (str): Database connection string.
        DEBUG (bool): Enables FastAPI debug mode if True.
        EMBRAPA_URL (str): Base URL for the Embrapa website.
        LOCAL_CACHE_FOLDER (str): Local folder path for caching Embrapa data.
        SECRET_KEY (str): Used to sign JWT tokens.
    """

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./database/users.db"
    DEBUG: bool = True
    EMBRAPA_URL: str = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    LOCAL_CACHE_FOLDER: str = os.path.join("data")
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
