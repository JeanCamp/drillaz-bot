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
    # PostgreSQL não precisa criar diretórios, é remoto
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print('✅ Banco de dados PostgreSQL inicializado com sucesso')
    except Exception as e:
        print(f'❌ Erro ao inicializar banco de dados: {e}')
        raise
