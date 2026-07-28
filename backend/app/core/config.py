from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MindVault"
    OLLAMA_BASE_URL: str = "https://localhost:11434"
    LLM_MODEL: str = "llama3.2"
    EMBED_MODEL: str = "nomic-embed-text"
    CHROMA_PATH: str = "./data/chroma_db"
    UPLOAD_DIR: str = "./data/uploads"
    
    class config:
        env_file = ".env"
        
settings = Settings()    