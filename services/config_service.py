from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Config
from typing import Optional

class ConfigService:
    """Serviço para gerenciar configurações do bot"""
    
    @staticmethod
    async def get_config(session: AsyncSession, key: str) -> Optional[str]:
        """Busca uma configuração por chave"""
        result = await session.execute(
            select(Config).where(Config.key == key)
        )
        config = result.scalar_one_or_none()
        return config.value if config else None
    
    @staticmethod
    async def set_config(session: AsyncSession, key: str, value: str, description: str = None) -> Config:
        """Define ou atualiza uma configuração"""
        result = await session.execute(
            select(Config).where(Config.key == key)
        )
        config = result.scalar_one_or_none()
        
        if config:
            config.value = value
            if description:
                config.description = description
        else:
            config = Config(key=key, value=value, description=description)
            session.add(config)
        
        await session.commit()
        await session.refresh(config)
        return config
    
    @staticmethod
    async def get_all_configs(session: AsyncSession) -> list[Config]:
        """Retorna todas as configurações"""
        result = await session.execute(
            select(Config).order_by(Config.key)
        )
        return result.scalars().all()
    
    @staticmethod
    async def delete_config(session: AsyncSession, key: str) -> bool:
        """Remove uma configuração"""
        result = await session.execute(
            select(Config).where(Config.key == key)
        )
        config = result.scalar_one_or_none()
        
        if config:
            await session.delete(config)
            await session.commit()
            return True
        return False
