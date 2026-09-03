import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/gangue.db')
    
    # Discord IDs
    CARGO_CUPULA_ID = int(os.getenv('CARGO_CUPULA_ID', 0))
    CANAL_LOGS_ID = int(os.getenv('CANAL_LOGS_ID', 0))
    CANAL_COFRE_ID = int(os.getenv('CANAL_COFRE_ID', 0))
    CANAL_BAU_ID = int(os.getenv('CANAL_BAU_ID', 0))
    CANAL_GERAL_ID = int(os.getenv('CANAL_GERAL_ID', 0))
    
    # Frases automáticas
    INTERVALO_FRASES = int(os.getenv('INTERVALO_FRASES', 30))  # minutos
    
    @classmethod
    def validate(cls):
        """Valida se as configurações essenciais estão definidas"""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN não está definido no .env")
        if cls.CARGO_CUPULA_ID == 0:
            raise ValueError("CARGO_CUPULA_ID não está definido no .env")
        if cls.CANAL_LOGS_ID == 0:
            raise ValueError("CANAL_LOGS_ID não está definido no .env")
