from sqlalchemy.ext.asyncio import AsyncSession
from services.cofre_service import CofreService
from services.bau_service import BauService
from typing import Optional

class RelatorioService:
    """Serviço para gerar relatórios da gangue"""
    
    @staticmethod
    async def gerar_relatorio_geral(
        session: AsyncSession,
        periodo_dias: Optional[int] = None
    ) -> dict:
        """Gera um relatório geral com todas as métricas"""
        
        # Se período não for especificado, usa 30 dias
        if periodo_dias is None:
            periodo_dias = 30
        
        # Dados do cofre
        cofre_saldo = await CofreService.get_saldo_atual(session)
        cofre_totais = await CofreService.get_totais_periodo(session, periodo_dias)
        cofre_top_usuarios = await CofreService.get_top_usuarios(session, periodo_dias, limit=5)
        
        # Dados do baú
        bau_totais = await BauService.get_totais_periodo(session, periodo_dias)
        bau_top_usuarios = await BauService.get_top_usuarios(session, periodo_dias, limit=5)
        bau_top_itens = await BauService.get_itens_mais_movimentados(session, periodo_dias, limit=5)
        
        return {
            'periodo_dias': periodo_dias,
            'cofre': {
                'saldo': cofre_saldo,
                'total_depositado': cofre_totais['total_depositado'],
                'total_retirado': cofre_totais['total_retirado'],
                'top_usuarios': cofre_top_usuarios
            },
            'bau': {
                'total_entradas': bau_totais['total_entradas'],
                'total_retiradas': bau_totais['total_retiradas'],
                'top_usuarios': bau_top_usuarios,
                'top_itens': bau_top_itens
            }
        }
    
    @staticmethod
    async def gerar_relatorio_cofre(
        session: AsyncSession,
        periodo_dias: Optional[int] = None
    ) -> dict:
        """Gera relatório específico do cofre"""
        
        if periodo_dias is None:
            periodo_dias = 30
        
        cofre_saldo = await CofreService.get_saldo_atual(session)
        cofre_totais = await CofreService.get_totais_periodo(session, periodo_dias)
        cofre_top_usuarios = await CofreService.get_top_usuarios(session, periodo_dias, limit=10)
        
        return {
            'periodo_dias': periodo_dias,
            'saldo': cofre_saldo,
            'total_depositado': cofre_totais['total_depositado'],
            'total_retirado': cofre_totais['total_retirado'],
            'top_usuarios': cofre_top_usuarios
        }
    
    @staticmethod
    async def gerar_relatorio_bau(
        session: AsyncSession,
        periodo_dias: Optional[int] = None
    ) -> dict:
        """Gera relatório específico do baú"""
        
        if periodo_dias is None:
            periodo_dias = 30
        
        bau_totais = await BauService.get_totais_periodo(session, periodo_dias)
        bau_top_usuarios = await BauService.get_top_usuarios(session, periodo_dias, limit=10)
        bau_top_itens = await BauService.get_itens_mais_movimentados(session, periodo_dias, limit=10)
        
        return {
            'periodo_dias': periodo_dias,
            'total_entradas': bau_totais['total_entradas'],
            'total_retiradas': bau_totais['total_retiradas'],
            'top_usuarios': bau_top_usuarios,
            'top_itens': bau_top_itens
        }
    
    @staticmethod
    async def gerar_relatorio_usuario(
        session: AsyncSession,
        user_id: str,
        periodo_dias: Optional[int] = None
    ) -> dict:
        """Gera relatório específico de um usuário"""
        
        if periodo_dias is None:
            periodo_dias = 30
        
        # Histórico do cofre do usuário
        cofre_historico = await CofreService.get_historico(
            session,
            limit=1000,
            user_id=user_id,
            periodo_dias=periodo_dias
        )
        
        # Histórico do baú do usuário
        bau_historico = await BauService.get_historico(
            session,
            limit=1000,
            user_id=user_id,
            periodo_dias=periodo_dias
        )
        
        # Calcula totais do cofre
        cofre_depositos = sum(m.valor for m in cofre_historico if m.tipo == 'deposito')
        cofre_retiradas = sum(m.valor for m in cofre_historico if m.tipo == 'retirada')
        
        # Calcula totais do baú
        bau_entradas = sum(m.quantidade for m in bau_historico if m.tipo == 'entrada')
        bau_retiradas = sum(m.quantidade for m in bau_historico if m.tipo == 'retirada')
        
        return {
            'periodo_dias': periodo_dias,
            'user_id': user_id,
            'cofre': {
                'total_depositos': cofre_depositos,
                'total_retiradas': cofre_retiradas,
                'quantidade_movimentacoes': len(cofre_historico)
            },
            'bau': {
                'total_entradas': bau_entradas,
                'total_retiradas': bau_retiradas,
                'quantidade_movimentacoes': len(bau_historico)
            }
        }
