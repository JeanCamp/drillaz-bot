from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import Frase
from typing import List, Optional
from utils.validators import Validators, ValidationError
import random

class FraseService:
    """Serviço para gerenciar frases automáticas"""
    
    @staticmethod
    async def adicionar_frase(session: AsyncSession, frase: str) -> Frase:
        """Adiciona uma nova frase ao banco de dados"""
        frase = Validators.validate_frase(frase)
        
        nova_frase = Frase(frase=frase, ativa=True)
        session.add(nova_frase)
        await session.commit()
        await session.refresh(nova_frase)
        
        return nova_frase
    
    @staticmethod
    async def remover_frase(session: AsyncSession, frase_id: int) -> bool:
        """Remove uma frase do banco de dados"""
        result = await session.execute(
            select(Frase).where(Frase.id == frase_id)
        )
        frase = result.scalar_one_or_none()
        
        if frase:
            await session.delete(frase)
            await session.commit()
            return True
        return False
    
    @staticmethod
    async def listar_frases(session: AsyncSession, ativas_only: bool = True) -> List[Frase]:
        """Lista todas as frases (apenas ativas ou todas)"""
        query = select(Frase)
        
        if ativas_only:
            query = query.where(Frase.ativa == True)
        
        query = query.order_by(Frase.created_at.desc())
        
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def ativar_frase(session: AsyncSession, frase_id: int) -> Optional[Frase]:
        """Ativa uma frase"""
        result = await session.execute(
            select(Frase).where(Frase.id == frase_id)
        )
        frase = result.scalar_one_or_none()
        
        if frase:
            frase.ativa = True
            await session.commit()
            await session.refresh(frase)
            return frase
        return None
    
    @staticmethod
    async def desativar_frase(session: AsyncSession, frase_id: int) -> Optional[Frase]:
        """Desativa uma frase"""
        result = await session.execute(
            select(Frase).where(Frase.id == frase_id)
        )
        frase = result.scalar_one_or_none()
        
        if frase:
            frase.ativa = False
            await session.commit()
            await session.refresh(frase)
            return frase
        return None
    
    @staticmethod
    async def get_frase_aleatoria(session: AsyncSession) -> Optional[str]:
        """Retorna uma frase aleatória ativa"""
        result = await session.execute(
            select(Frase).where(Frase.ativa == True)
        )
        frases = result.scalars().all()
        
        if not frases:
            return None
        
        return random.choice(frases).frase
    
    @staticmethod
    async def get_total_frases(session: AsyncSession, ativas_only: bool = True) -> int:
        """Retorna o total de frases"""
        query = select(func.count(Frase.id))
        
        if ativas_only:
            query = query.where(Frase.ativa == True)
        
        result = await session.execute(query)
        return result.scalar() or 0
    
    @staticmethod
    async def inicializar_frases_padrao(session: AsyncSession):
        """Inicializa frases padrão se não houver nenhuma"""
        total = await FraseService.get_total_frases(session)
        
        if total == 0:
            frases_padrao = [
                "Respeito se conquista na rua.",
                "A firma não dorme.",
                "Cada movimento tem seu preço.",
                "Quem representa, representa.",
                "Na rua se ganha, na rua se perde.",
                "Lealdade acima de tudo.",
                "A gangue é família.",
                "Respeito é tudo."
            ]
            
            for frase in frases_padrao:
                await FraseService.adicionar_frase(session, frase)
