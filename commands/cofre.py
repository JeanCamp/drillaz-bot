import discord
from discord import app_commands, Interaction, Member, Embed
from discord.ext import commands
from discord import Color
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from database.connection import get_db
from services.cofre_service import CofreService
from services.permission_service import PermissionService
from services.log_service import LogService
from utils.embeds import EmbedBuilder
from utils.validators import ValidationError
from utils.formatters import format_currency, format_datetime, get_emoji_tipo_cofre
from config import Config
from typing import Optional

class CofreCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='testar_cofre')
    async def testar_cofre(self, ctx):
        await ctx.send("✅ Módulo do cofre está funcionando!")
    
    async def get_canal_logs(self):
        if Config.CANAL_LOGS_ID == 0:
            return None
        return self.bot.get_channel(Config.CANAL_LOGS_ID)
    
    @app_commands.command(name="deposito", description="Registra um depósito no cofre")
    @app_commands.describe(valor="Valor do depósito", tipo="Tipo de dinheiro: limpo ou sujo", motivo="Motivo do depósito")
    async def cofre_deposito(self, interaction: Interaction, valor: app_commands.Range[float, 0.01], tipo: str = "limpo", motivo: str = None):
        if not PermissionService.can_cofre_deposito(interaction.user):
            await interaction.response.send_message("❌ Você não tem permissão para fazer depósitos no cofre.", ephemeral=True)
            return
        
        await interaction.response.defer()
        user_info = PermissionService.get_user_info(interaction.user)
        
        if tipo.lower() not in ['limpo', 'sujo']:
            await interaction.followup.send("❌ Tipo de dinheiro inválido. Use: limpo ou sujo", ephemeral=True)
            return
        
        tipo_dinheiro = tipo.lower()
        
        try:
            async for session in get_db():
                movimentacao = await CofreService.deposito(
                    session=session,
                    user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    valor=valor,
                    tipo_dinheiro=tipo_dinheiro,
                    motivo=motivo or "Depósito"
                )
                
                canal_logs = await self.get_canal_logs()
                if canal_logs:
                    await LogService.send_cofre_log(
                        session=session,
                        movimentacao=movimentacao,
                        user_mention=user_info['user_mention'],
                        canal_logs=canal_logs
                    )
                
                embed = EmbedBuilder.create_success_embed(
                    f"Depósito de R$ {valor:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.') + 
                    f" ({tipo_dinheiro.upper()}) registrado com sucesso!\n\n"
                    f"Saldo após operação: R$ {movimentacao.saldo_posterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
                await interaction.followup.send(embed=embed)
                
        except ValidationError as e:
            embed = EmbedBuilder.create_error_embed(str(e))
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao processar depósito: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="retirada", description="Registra uma retirada do cofre (apenas Alta Cúpula)")
    @app_commands.describe(valor="Valor da retirada", tipo="Tipo de dinheiro: limpo ou sujo", motivo="Motivo da retirada")
    async def cofre_retirada(self, interaction: Interaction, valor: app_commands.Range[float, 0.01], tipo: str = "limpo", motivo: str = None):
        if not PermissionService.can_cofre_retirada(interaction.user):
            await interaction.response.send_message("❌ Apenas a Alta Cúpula pode fazer retiradas do cofre.", ephemeral=True)
            return
        
        await interaction.response.defer()
        user_info = PermissionService.get_user_info(interaction.user)
        
        if tipo.lower() not in ['limpo', 'sujo']:
            await interaction.followup.send("❌ Tipo de dinheiro inválido. Use: limpo ou sujo", ephemeral=True)
            return
        
        tipo_dinheiro = tipo.lower()
        
        try:
            async for session in get_db():
                movimentacao = await CofreService.retirada(
                    session=session,
                    user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    valor=valor,
                    tipo_dinheiro=tipo_dinheiro,
                    motivo=motivo or "Retirada"
                )
                
                canal_logs = await self.get_canal_logs()
                if canal_logs:
                    await LogService.send_cofre_log(
                        session=session,
                        movimentacao=movimentacao,
                        user_mention=user_info['user_mention'],
                        canal_logs=canal_logs
                    )
                
                embed = EmbedBuilder.create_success_embed(
                    f"Retirada de R$ {valor:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.') + 
                    f" ({tipo_dinheiro.upper()}) registrada com sucesso!\n\n"
                    f"Saldo após operação: R$ {movimentacao.saldo_posterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
                await interaction.followup.send(embed=embed)
                
        except ValidationError as e:
            embed = EmbedBuilder.create_error_embed(str(e))
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao processar retirada: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="saldo", description="Consulta o saldo atual do cofre (apenas Alta Cúpula)")
    async def cofre_saldo(self, interaction: Interaction):
        if not PermissionService.can_view_cofre_saldo(interaction.user):
            await interaction.response.send_message("❌ Apenas a Alta Cúpula pode consultar o saldo do cofre.", ephemeral=True)
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                saldos = await CofreService.get_saldos_totais(session)
                ultima_mov = await CofreService.get_ultima_movimentacao(session)
                
                embed = Embed(
                    title="💰 COFRE DA GANGUE",
                    description="Saldo atual disponível",
                    color=Color.gold()
                )
                
                embed.add_field(name="💵 Dinheiro Limpo", value=f"R$ {saldos['limpo']:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.'), inline=True)
                embed.add_field(name="💵 Dinheiro Sujo", value=f"R$ {saldos['sujo']:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.'), inline=True)
                embed.add_field(name="💵 TOTAL", value=f"R$ {saldos['total']:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.'), inline=True)
                
                if ultima_mov:
                    emoji = get_emoji_tipo_cofre(ultima_mov.tipo)
                    embed.add_field(
                        name="📋 Última Movimentação",
                        value=f"{emoji} {format_currency(ultima_mov.valor)} ({ultima_mov.tipo_dinheiro})\n"
                              f"Responsável: <@{ultima_mov.user_id}>\n"
                              f"Motivo: {ultima_mov.motivo or 'Sem motivo'}\n"
                              f"Data: {format_datetime(ultima_mov.created_at)}",
                        inline=False
                    )
                
                embed.timestamp = datetime.now()
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao consultar saldo: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="historico", description="Consulta o histórico do cofre")
    async def cofre_historico(self, interaction: Interaction):
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                historico = await CofreService.get_historico(session=session, limit=10)
                
                if not historico:
                    await interaction.followup.send("Nenhuma movimentação encontrada.")
                    return
                
                mensagem = "💰 HISTÓRICO DO COFRE:\n\n"
                for mov in historico:
                    emoji = "🟢" if mov.tipo == 'deposito' else "🔴"
                    mensagem += f"{emoji} {mov.tipo.upper()}: R$ {mov.valor:.0f}\n"
                    mensagem += f"   Responsável: {mov.user_name}\n"
                    mensagem += f"   Data: {mov.created_at.strftime('%d/%m/%Y %H:%M')}\n\n"
                
                await interaction.followup.send(mensagem)
                
        except Exception as e:
            await interaction.followup.send(f"Erro ao consultar histórico: {str(e)}")
    
    @app_commands.command(name="ajuste", description="Ajuste administrativo do saldo do cofre (apenas Alta Cúpula)")
    @app_commands.describe(novo_saldo="Novo saldo do cofre", motivo="Motivo do ajuste")
    async def cofre_ajuste(self, interaction: Interaction, novo_saldo: app_commands.Range[float, 0], motivo: str):
        if not PermissionService.can_cofre_ajuste(interaction.user):
            await interaction.response.send_message("❌ Apenas a Alta Cúpula pode fazer ajustes no cofre.", ephemeral=True)
            return
        
        await interaction.response.defer()
        user_info = PermissionService.get_user_info(interaction.user)
        
        try:
            async for session in get_db():
                saldo_anterior = await CofreService.get_saldo_atual(session)
                
                embed = EmbedBuilder.create_info_embed(
                    f"Ajuste administrativo realizado sem confirmação (temporário).\n\n"
                    f"Saldo anterior: R$ {saldo_anterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.') + "\n"
                    f"Novo saldo: R$ {novo_saldo:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao preparar ajuste: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CofreCommands(bot))
