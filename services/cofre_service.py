from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import CofreMovimentacao
from datetime import datetime, timedelta
from typing import Optional, List
from utils.validators import Validators, ValidationError

class CofreService:
    """Serviço para gerenciar operações do cofre"""
    
    @staticmethod
    async def get_saldo_atual(session: AsyncSession) -> float:
        """Calcula o saldo atual do cofre baseado no histórico"""
        # Soma todos os depósitos e subtrai todas as retiradas
        result = await session.execute(
            select(
                func.sum(
                    func.case(
                        (CofreMovimentacao.tipo == 'deposito', CofreMovimentacao.valor),
                        (CofreMovimentacao.tipo == 'retirada', -CofreMovimentacao.valor),
                        (CofreMovimentacao.tipo == 'ajuste', CofreMovimentacao.valor),
                        else_=0
                    )
                )
            )
        )
        saldo = result.scalar() or 0.0
        return round(saldo, 2)
    
    @staticmethod
    async def registrar_movimentacao(
        session: AsyncSession,
        user_id: str,
        user_name: str,
        valor: float,
        tipo: str,
        motivo: str,
        saldo_anterior: float
    ) -> CofreMovimentacao:
        """Registra uma movimentação no cofre"""
        
        # Calcula o saldo posterior
        if tipo == 'deposito':
            saldo_posterior = saldo_anterior + valor
        elif tipo == 'retirada':
            saldo_posterior = saldo_anterior - valor
        elif tipo == 'ajuste':
            saldo_posterior = valor  # Para ajuste, o valor é o novo saldo
        else:
            raise ValueError(f"Tipo de movimentação inválido: {tipo}")
        
        # Cria a movimentação
        movimentacao = CofreMovimentacao(
            user_id=user_id,
            user_name=user_name,
            valor=valor if tipo != 'ajuste' else saldo_posterior - saldo_anterior,
            tipo=tipo,
            motivo=motivo,
            saldo_anterior=saldo_anterior,
            saldo_posterior=saldo_posterior
        )
        
        session.add(movimentacao)
        await session.commit()
        await session.refresh(movimentacao)
        
        return movimentacao
    
    @staticmethod
    async def deposito(
        session: AsyncSession,
        user_id: str,
        user_name: str,
        valor: float,
        motivo: str
    ) -> CofreMovimentacao:
        """Registra um depósito no cofre"""
        
        # Valida o valor
        valor = Validators.validate_valor(valor)
        motivo = Validators.validate_motivo(motivo)
        
        # Busca saldo atual
        saldo_anterior = await CofreService.get_saldo_atual(session)
        
        # Registra a movimentação
        return await CofreService.registrar_movimentacao(
            session=session,
            user_id=user_id,
            user_name=user_name,
            valor=valor,
            tipo='deposito',
            motivo=motivo,
            saldo_anterior=saldo_anterior
        )
    
    @staticmethod
    async def retirada(
        session: AsyncSession,
        user_id: str,
        user_name: str,
        valor: float,
        motivo: str
    ) -> CofreMovimentacao:
        """Registra uma retirada do cofre"""
        
        # Valida o valor
        valor = Validators.validate_valor(valor)
        motivo = Validators.validate_motivo(motivo)
        
        # Busca saldo atual
        saldo_anterior = await CofreService.get_saldo_atual(session)
        
        # Verifica se há saldo suficiente
        if not Validators.validate_saldo_suficiente(saldo_anterior, valor):
            raise ValidationError(
                f"Saldo insuficiente. Saldo disponível: R$ {saldo_anterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            )
        
        # Registra a movimentação
        return await CofreService.registrar_movimentacao(
            session=session,
            user_id=user_id,
            user_name=user_name,
            valor=valor,
            tipo='retirada',
            motivo=motivo,
            saldo_anterior=saldo_anterior
        )
    
    @staticmethod
    async def ajuste(
        session: AsyncSession,
        user_id: str,
        user_name: str,
        novo_saldo: float,
        motivo: str
    ) -> CofreMovimentacao:
        """Faz um ajuste administrativo no saldo do cofre"""
        
        # Valida o novo saldo
        if novo_saldo < 0:
            raise ValidationError("O saldo não pode ser negativo")
        
        motivo = Validators.validate_motivo(motivo)
        
        # Busca saldo atual
        saldo_anterior = await CofreService.get_saldo_atual(session)
        
        # Registra como ajuste
        return await CofreService.registrar_movimentacao(
            session=session,
            user_id=user_id,
            user_name=user_name,
            valor=novo_saldo,  # Para ajuste, valor é o novo saldo
            tipo='ajuste',
            motivo=motivo,
            saldo_anterior=saldo_anterior
        )
    
    @staticmethod
    async def get_historico(
        session: AsyncSession,
        limit: int = 50,
        user_id: Optional[str] = None,
        tipo: Optional[str] = None,
        periodo_dias: Optional[int] = None
    ) -> List[CofreMovimentacao]:
        """Busca o histórico de movimentações do cofre"""
        
        query = select(CofreMovimentacao)
        
        # Filtro por usuário
        if user_id:
            query = query.where(CofreMovimentacao.user_id == user_id)
        
        # Filtro por tipo
        if tipo:
            query = query.where(CofreMovimentacao.tipo == tipo)
        
        # Filtro por período
        if periodo_dias:
            data_limite = datetime.now() - timedelta(days=periodo_dias)
            query = query.where(CofreMovimentacao.created_at >= data_limite)
        
        # Ordena por data (mais recente primeiro) e limita
        query = query.order_by(CofreMovimentacao.created_at.desc()).limit(limit)
        
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_ultima_movimentacao(session: AsyncSession) -> Optional[CofreMovimentacao]:
        """Retorna a última movimentação do cofre"""
        result = await session.execute(
            select(CofreMovimentacao)
            .order_by(CofreMovimentacao.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_totais_periodo(
        session: AsyncSession,
        periodo_dias: int
    ) -> dict:
        """Retorna totais de depósitos e retiradas em um período"""
        data_limite = datetime.now() - timedelta(days=periodo_dias)
        
        # Total depositado
        result_depositos = await session.execute(
            select(func.sum(CofreMovimentacao.valor))
            .where(CofreMovimentacao.tipo == 'deposito')
            .where(CofreMovimentacao.created_at >= data_limite)
        )
        total_depositado = result_depositos.scalar() or 0.0
        
        # Total retirado
        result_retiradas = await session.execute(
            select(func.sum(CofreMovimentacao.valor))
            .where(CofreMovimentacao.tipo == 'retirada')
            .where(CofreMovimentacao.created_at >= data_limite)
        )
        total_retirado = result_retiradas.scalar() or 0.0
        
        return {
            'total_depositado': round(total_depositado, 2),
            'total_retirado': round(total_retirado, 2)
        }
    
    @staticmethod
    async def get_top_usuarios(
        session: AsyncSession,
        periodo_dias: int = 30,
        limit: int = 10
    ) -> List[dict]:
        """Retorna os usuários que mais movimentaram o cofre"""
        data_limite = datetime.now() - timedelta(days=periodo_dias)
        
        result = await session.execute(
            select(
                CofreMovimentacao.user_id,
                CofreMovimentacao.user_name,
                func.count(CofreMovimentacao.id).label('quantidade'),
                func.sum(
                    func.case(
                        (CofreMovimentacao.tipo == 'deposito', CofreMovimentacao.valor),
                        else_=0
                    )
                ).label('total_depositado'),
                func.sum(
                    func.case(
                        (CofreMovimentacao.tipo == 'retirada', CofreMovimentacao.valor),
                        else_=0
                    )
                ).label('total_retirado')
            )
            .where(CofreMovimentacao.created_at >= data_limite)
            .group_by(CofreMovimentacao.user_id, CofreMovimentacao.user_name)
            .order_by(func.count(CofreMovimentacao.id).desc())
            .limit(limit)
        )
        
        top_usuarios = []
        for row in result:
            top_usuarios.append({
                'user_id': row.user_id,
                'user_name': row.user_name,
                'quantidade': row.quantidade,
                'total_depositado': row.total_depositado or 0,
                'total_retirado': row.total_retirado or 0
            })
        
        return top_usuarios
