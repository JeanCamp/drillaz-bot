import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from services.cofre_service import CofreService
from services.permission_service import PermissionService
from services.log_service import LogService
from utils.embeds import EmbedBuilder
from utils.validators import ValidationError
from config import Config
from typing import Optional

class CofreCommands(commands.Cog):
    """Comandos do sistema de Cofre"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def get_canal_logs(self):
        """Retorna o canal de logs configurado"""
        if Config.CANAL_LOGS_ID == 0:
            return None
        return self.bot.get_channel(Config.CANAL_LOGS_ID)
    
    @app_commands.command(name="cofre_deposito", description="Registra um depósito no cofre")
    @app_commands.describe(
        valor="Valor do depósito",
        motivo="Motivo do depósito"
    )
    async def cofre_deposito(
        self,
        interaction: Interaction,
        valor: app_commands.Range[float, 0.01],
        motivo: Optional[str] = None
    ):
        """Registra um depósito no cofre"""
        
        # Verifica se está no canal correto
        if not PermissionService.check_channel(interaction.channel_id, Config.CANAL_COFRE_ID):
            await interaction.response.send_message(
                "❌ Este comando só pode ser utilizado no canal do cofre.",
                ephemeral=True
            )
            return
        
        # Verifica permissão
        if not PermissionService.can_cofre_deposito(interaction.user):
            await interaction.response.send_message(
                "❌ Você não tem permissão para fazer depósitos no cofre.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        user_info = PermissionService.get_user_info(interaction.user)
        
        try:
            async for session in get_db():
                # Registra o depósito
                movimentacao = await CofreService.deposito(
                    session=session,
                    user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    valor=valor,
                    motivo=motivo
                )
                
                # Envia log
                canal_logs = await self.get_canal_logs()
                if canal_logs:
                    await LogService.send_cofre_log(
                        session=session,
                        movimentacao=movimentacao,
                        user_mention=user_info['user_mention'],
                        canal_logs=canal_logs
                    )
                
                # Responde ao usuário
                embed = EmbedBuilder.create_success_embed(
                    f"Depósito de R$ {valor:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.') + 
                    f" registrado com sucesso!\n\n"
                    f"Saldo após operação: R$ {movimentacao.saldo_posterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
                await interaction.followup.send(embed=embed)
                
        except ValidationError as e:
            embed = EmbedBuilder.create_error_embed(str(e))
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao processar depósito: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="cofre_retirada", description="Registra uma retirada do cofre (apenas Alta Cúpula)")
    @app_commands.describe(
        valor="Valor da retirada",
        motivo="Motivo da retirada"
    )
    async def cofre_retirada(
        self,
        interaction: Interaction,
        valor: app_commands.Range[float, 0.01],
        motivo: Optional[str] = None
    ):
        """Registra uma retirada do cofre"""
        
        # Verifica se está no canal correto
        if not PermissionService.check_channel(interaction.channel_id, Config.CANAL_COFRE_ID):
            await interaction.response.send_message(
                "❌ Este comando só pode ser utilizado no canal do cofre.",
                ephemeral=True
            )
            return
        
        # Verifica permissão
        if not PermissionService.can_cofre_retirada(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode fazer retiradas do cofre.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        user_info = PermissionService.get_user_info(interaction.user)
        
        try:
            async for session in get_db():
                # Registra a retirada
                movimentacao = await CofreService.retirada(
                    session=session,
                    user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    valor=valor,
                    motivo=motivo
                )
                
                # Envia log
                canal_logs = await self.get_canal_logs()
                if canal_logs:
                    await LogService.send_cofre_log(
                        session=session,
                        movimentacao=movimentacao,
                        user_mention=user_info['user_mention'],
                        canal_logs=canal_logs
                    )
                
                # Responde ao usuário
                embed = EmbedBuilder.create_success_embed(
                    f"Retirada de R$ {valor:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.') + 
                    f" registrada com sucesso!\n\n"
                    f"Saldo após operação: R$ {movimentacao.saldo_posterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
                await interaction.followup.send(embed=embed)
                
        except ValidationError as e:
            embed = EmbedBuilder.create_error_embed(str(e))
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao processar retirada: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="cofre_saldo", description="Consulta o saldo atual do cofre (apenas Alta Cúpula)")
    async def cofre_saldo(self, interaction: Interaction):
        """Consulta o saldo atual do cofre"""
        
        # Verifica permissão
        if not PermissionService.can_view_cofre_saldo(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode consultar o saldo do cofre.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Busca saldo atual
                saldo = await CofreService.get_saldo_atual(session)
                
                # Busca última movimentação
                ultima_mov = await CofreService.get_ultima_movimentacao(session)
                
                # Cria embed
                embed = EmbedBuilder.create_cofre_saldo_embed(saldo, ultima_mov)
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao consultar saldo: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="cofre_historico", description="Consulta o histórico do cofre")
    @app_commands.describe(
        usuario="Filtrar por usuário (opcional)",
        tipo="Filtrar por tipo: deposito, retirada (opcional)",
        periodo="Filtrar por período em dias (opcional)"
    )
    async def cofre_historico(
        self,
        interaction: Interaction,
        usuario: Optional[Member] = None,
        tipo: Optional[str] = None,
        periodo: Optional[app_commands.Range[int, 1, 365]] = None
    ):
        """Consulta o histórico do cofre"""
        
        # Verifica permissão
        if not PermissionService.can_view_cofre_historico(interaction.user):
            # Se não for Alta Cúpula, só pode ver próprio histórico
            if usuario and usuario.id != interaction.user.id:
                await interaction.response.send_message(
                    "❌ Você só pode consultar seu próprio histórico.",
                    ephemeral=True
                )
                return
            usuario = interaction.user  # Força a ver apenas próprio histórico
        
        await interaction.response.defer()
        
        user_id = str(usuario.id) if usuario else None
        
        # Valida tipo se fornecido
        if tipo and tipo.lower() not in ['deposito', 'retirada', 'ajuste']:
            await interaction.followup.send(
                "❌ Tipo inválido. Use: deposito, retirada ou ajuste",
                ephemeral=True
            )
            return
        
        try:
            async for session in get_db():
                # Busca histórico
                historico = await CofreService.get_historico(
                    session=session,
                    limit=50,
                    user_id=user_id,
                    tipo=tipo.lower() if tipo else None,
                    periodo_dias=periodo
                )
                
                # Cria embed
                titulo = "💰 HISTÓRICO DO COFRE"
                if usuario:
                    titulo += f" - @{usuario.display_name}"
                if tipo:
                    titulo += f" - {tipo.upper()}"
                if periodo:
                    titulo += f" - Últimos {periodo} dias"
                
                embed = EmbedBuilder.create_cofre_historico_embed(historico, titulo)
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao consultar histórico: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="cofre_ajuste", description="Ajuste administrativo do saldo do cofre (apenas Alta Cúpula)")
    @app_commands.describe(
        novo_saldo="Novo saldo do cofre",
        motivo="Motivo do ajuste"
    )
    async def cofre_ajuste(
        self,
        interaction: Interaction,
        novo_saldo: app_commands.Range[float, 0],
        motivo: str
    ):
        """Faz um ajuste administrativo no saldo do cofre"""
        
        # Verifica permissão
        if not PermissionService.can_cofre_ajuste(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode fazer ajustes no cofre.",
                ephemeral=True
            )
            return
        
        # Verifica se está no canal correto
        if not PermissionService.check_channel(interaction.channel_id, Config.CANAL_COFRE_ID):
            await interaction.response.send_message(
                "❌ Este comando só pode ser utilizado no canal do cofre.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        user_info = PermissionService.get_user_info(interaction.user)
        
        try:
            async for session in get_db():
                # Busca saldo atual
                saldo_anterior = await CofreService.get_saldo_atual(session)
                
                # Executa o ajuste direto (sem confirmação por enquanto)
                movimentacao = await CofreService.ajuste(
                    session=session,
                    user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    novo_saldo=novo_saldo,
                    motivo=motivo
                )
                
                # Envia log
                canal_logs = await self.get_canal_logs()
                if canal_logs:
                    await LogService.send_cofre_log(
                        session=session,
                        movimentacao=movimentacao,
                        user_mention=user_info['user_mention'],
                        canal_logs=canal_logs
                    )
                
                # Responde
                embed = EmbedBuilder.create_success_embed(
                    f"Ajuste administrativo realizado com sucesso!\n\n"
                    f"Saldo anterior: R$ {movimentacao.saldo_anterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.') + "\n"
                    f"Novo saldo: R$ {movimentacao.saldo_posterior:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao fazer ajuste: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CofreCommands(bot))
#   A t u a l i z a � � o   d e   e x i b i � � o   d e   t i p o   d e   d i n h e i r o 
 
