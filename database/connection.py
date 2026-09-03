import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import Config

# Criar engine assíncrono
engine = create_async_engine(
    Config.DATABASE_URL,
    echo=False,  # Define True para ver SQL queries no console
    future=True
)

# Criar session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    """Retorna uma sessão do banco de dados"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    # Criar diretório do banco de dados se não existir
    db_path = Config.DATABASE_URL.replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)
    
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f'📁 Diretório do banco de dados criado: {db_dir}')
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
