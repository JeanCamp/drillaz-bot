from discord import TextChannel
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import CofreMovimentacao, BauMovimentacao
from utils.embeds import EmbedBuilder

class LogService:
    """Serviço para gerenciar logs no Discord"""
    
    @staticmethod
    async def send_cofre_log(
        session: AsyncSession,
        movimentacao: CofreMovimentacao,
        user_mention: str,
        canal_logs: TextChannel
    ):
        """Envia log de movimentação do cofre para o canal de logs"""
        embed = EmbedBuilder.create_cofre_log_embed(movimentacao, user_mention)
        await canal_logs.send(embed=embed)
    
    @staticmethod
    async def send_bau_log(
        session: AsyncSession,
        movimentacao: BauMovimentacao,
        user_mention: str,
        canal_logs: TextChannel
    ):
        """Envia log de movimentação do baú para o canal de logs"""
        embed = EmbedBuilder.create_bau_log_embed(movimentacao, user_mention)
        await canal_logs.send(embed=embed)
    
    @staticmethod
    async def send_error_log(
        canal_logs: TextChannel,
        error_message: str,
        context: str = None
    ):
        """Envia log de erro para o canal de logs"""
        from utils.embeds import EmbedBuilder
        
        embed = EmbedBuilder.create_error_embed(error_message)
        if context:
            embed.add_field(name="Contexto", value=context, inline=False)
        
        await canal_logs.send(embed=embed)
