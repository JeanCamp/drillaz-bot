from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from database.models import BauItem, BauMovimentacao
from datetime import datetime, timedelta
from typing import Optional, List
from utils.validators import Validators, ValidationError

class BauService:
    """Serviço para gerenciar operações do baú"""
    
    @staticmethod
    async def get_or_create_item(session: AsyncSession, nome: str) -> BauItem:
        """Busca um item existente ou cria um novo"""
        nome = Validators.validate_item_nome(nome)
        
        result = await session.execute(
            select(BauItem).where(BauItem.nome == nome)
        )
        item = result.scalar_one_or_none()
        
        if not item:
            item = BauItem(nome=nome, estoque=0)
            session.add(item)
            await session.commit()
            await session.refresh(item)
        
        return item
    
    @staticmethod
    async def get_item_by_nome(session: AsyncSession, nome: str) -> Optional[BauItem]:
        """Busca um item pelo nome"""
        result = await session.execute(
            select(BauItem).where(BauItem.nome == nome)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_items(session: AsyncSession) -> List[BauItem]:
        """Retorna todos os itens do baú"""
        result = await session.execute(
            select(BauItem).order_by(BauItem.nome)
        )
        return result.scalars().all()
    
    @staticmethod
    async def registrar_movimentacao(
        session: AsyncSession,
        user_id: str,
        user_name: str,
        item: BauItem,
        quantidade: int,
        tipo: str,
        motivo: str
    ) -> BauMovimentacao:
        """Registra uma movimentação no baú"""
        
        estoque_anterior = item.estoque
        
        # Calcula o estoque posterior
        if tipo == 'entrada':
            estoque_posterior = estoque_anterior + quantidade
        elif tipo == 'retirada':
            estoque_posterior = estoque_anterior - quantidade
        else:
            raise ValueError(f"Tipo de movimentação inválido: {tipo}")
        
        # Atualiza o estoque do item
        item.estoque = estoque_posterior
        item.updated_at = datetime.now()
        
        # Cria a movimentação
        movimentacao = BauMovimentacao(
            user_id=user_id,
            user_name=user_name,
            item_id=item.id,
            item_nome=item.nome,
            quantidade=quantidade,
            tipo=tipo,
            motivo=motivo,
            estoque_anterior=estoque_anterior,
            estoque_posterior=estoque_posterior
        )
        
        session.add(movimentacao)
        await session.commit()
        await session.refresh(movimentacao)
        
        return movimentacao
    
    @staticmethod
    async def entrada(
        session: AsyncSession,
        user_id: str,
        user_name: str,
        item_nome: str,
        quantidade: int,
        motivo: str
    ) -> BauMovimentacao:
        """Registra uma entrada de item no baú"""
        
        # Valida a quantidade
        quantidade = Validators.validate_quantidade(quantidade)
        motivo = Validators.validate_motivo(motivo)
        
        # Busca ou cria o item
        item = await BauService.get_or_create_item(session, item_nome)
        
        # Registra a movimentação
        return await BauService.registrar_movimentacao(
            session=session,
            user_id=user_id,
            user_name=user_name,
            item=item,
            quantidade=quantidade,
            tipo='entrada',
            motivo=motivo
        )
    
    @staticmethod
    async def retirada(
        session: AsyncSession,
        user_id: str,
        user_name: str,
        item_nome: str,
        quantidade: int,
        motivo: str
    ) -> BauMovimentacao:
        """Registra uma retirada de item do baú"""
        
        # Valida a quantidade
        quantidade = Validators.validate_quantidade(quantidade)
        motivo = Validators.validate_motivo(motivo)
        
        # Busca o item
        item = await BauService.get_item_by_nome(session, item_nome)
        
        if not item:
            raise ValidationError(f"Item '{item_nome}' não encontrado no baú")
        
        # Verifica se há estoque suficiente
        if not Validators.validate_estoque_suficiente(item.estoque, quantidade):
            raise ValidationError(
                f"Estoque insuficiente. Estoque disponível: {item.estoque} unidades"
            )
        
        # Registra a movimentação
        return await BauService.registrar_movimentacao(
            session=session,
            user_id=user_id,
            user_name=user_name,
            item=item,
            quantidade=quantidade,
            tipo='retirada',
            motivo=motivo
        )
    
    @staticmethod
    async def get_historico(
        session: AsyncSession,
        limit: int = 50,
        user_id: Optional[str] = None,
        item_nome: Optional[str] = None,
        tipo: Optional[str] = None,
        periodo_dias: Optional[int] = None
    ) -> List[BauMovimentacao]:
        """Busca o histórico de movimentações do baú"""
        
        query = select(BauMovimentacao)
        
        # Filtro por usuário
        if user_id:
            query = query.where(BauMovimentacao.user_id == user_id)
        
        # Filtro por item
        if item_nome:
            query = query.where(BauMovimentacao.item_nome == item_nome)
        
        # Filtro por tipo
        if tipo:
            query = query.where(BauMovimentacao.tipo == tipo)
        
        # Filtro por período
        if periodo_dias:
            data_limite = datetime.now() - timedelta(days=periodo_dias)
            query = query.where(BauMovimentacao.created_at >= data_limite)
        
        # Ordena por data (mais recente primeiro) e limita
        query = query.order_by(BauMovimentacao.created_at.desc()).limit(limit)
        
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_ultima_movimentacao(session: AsyncSession) -> Optional[BauMovimentacao]:
        """Retorna a última movimentação do baú"""
        result = await session.execute(
            select(BauMovimentacao)
            .order_by(BauMovimentacao.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_totais_periodo(
        session: AsyncSession,
        periodo_dias: int
    ) -> dict:
        """Retorna totais de entradas e retiradas em um período"""
        data_limite = datetime.now() - timedelta(days=periodo_dias)
        
        # Total de entradas (quantidade)
        result_entradas = await session.execute(
            select(func.sum(BauMovimentacao.quantidade))
            .where(BauMovimentacao.tipo == 'entrada')
            .where(BauMovimentacao.created_at >= data_limite)
        )
        total_entradas = result_entradas.scalar() or 0
        
        # Total de retiradas (quantidade)
        result_retiradas = await session.execute(
            select(func.sum(BauMovimentacao.quantidade))
            .where(BauMovimentacao.tipo == 'retirada')
            .where(BauMovimentacao.created_at >= data_limite)
        )
        total_retiradas = result_retiradas.scalar() or 0
        
        return {
            'total_entradas': total_entradas,
            'total_retiradas': total_retiradas
        }
    
    @staticmethod
    async def get_top_usuarios(
        session: AsyncSession,
        periodo_dias: int = 30,
        limit: int = 10
    ) -> List[dict]:
        """Retorna os usuários que mais movimentaram o baú"""
        data_limite = datetime.now() - timedelta(days=periodo_dias)
        
        result = await session.execute(
            select(
                BauMovimentacao.user_id,
                BauMovimentacao.user_name,
                func.count(BauMovimentacao.id).label('quantidade'),
                func.sum(
                    case(
                        (BauMovimentacao.tipo == 'entrada', BauMovimentacao.quantidade),
                        else_=0
                    )
                ).label('total_entradas'),
                func.sum(
                    case(
                        (BauMovimentacao.tipo == 'retirada', BauMovimentacao.quantidade),
                        else_=0
                    )
                ).label('total_retiradas')
            )
            .where(BauMovimentacao.created_at >= data_limite)
            .group_by(BauMovimentacao.user_id, BauMovimentacao.user_name)
            .order_by(func.count(BauMovimentacao.id).desc())
            .limit(limit)
        )
        
        top_usuarios = []
        for row in result:
            top_usuarios.append({
                'user_id': row.user_id,
                'user_name': row.user_name,
                'quantidade': row.quantidade,
                'total_entradas': row.total_entradas or 0,
                'total_retiradas': row.total_retiradas or 0
            })
        
        return top_usuarios
    
    @staticmethod
    async def get_itens_mais_movimentados(
        session: AsyncSession,
        periodo_dias: int = 30,
        limit: int = 10
    ) -> List[dict]:
        """Retorna os itens mais movimentados"""
        data_limite = datetime.now() - timedelta(days=periodo_dias)
        
        result = await session.execute(
            select(
                BauMovimentacao.item_nome,
                func.count(BauMovimentacao.id).label('quantidade'),
                func.sum(
                    case(
                        (BauMovimentacao.tipo == 'entrada', BauMovimentacao.quantidade),
                        else_=0
                    )
                ).label('total_entradas'),
                func.sum(
                    case(
                        (BauMovimentacao.tipo == 'retirada', BauMovimentacao.quantidade),
                        else_=0
                    )
                ).label('total_retiradas')
            )
            .where(BauMovimentacao.created_at >= data_limite)
            .group_by(BauMovimentacao.item_nome)
            .order_by(func.count(BauMovimentacao.id).desc())
            .limit(limit)
        )
        
        top_itens = []
        for row in result:
            top_itens.append({
                'item_nome': row.item_nome,
                'quantidade': row.quantidade,
                'total_entradas': row.total_entradas or 0,
                'total_retiradas': row.total_retiradas or 0
            })
        
        return top_itens
