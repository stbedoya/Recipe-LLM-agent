from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_NAME: str = "test_db"
    MONGODB_COLLECTION_NAME: str = "test_collection"
    OPENAI_API_KEY: str

settings = Settings()

