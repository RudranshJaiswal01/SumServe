import os

class Settings:
    GROQ_API_KEY: str
    GROQ_MODEL: str
    GROQ_TIMEOUT: int

    def __init__(self):
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.GROQ_TIMEOUT = int(os.getenv("GROQ_TIMEOUT", "30"))

        if not self.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not set")

settings = Settings()
