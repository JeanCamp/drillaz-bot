import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from services.config_service import ConfigService
from services.permission_service import PermissionService
from utils.embeds import EmbedBuilder
from config import Config
from typing import Optional

class ConfigCommands(commands.Cog):
    """Comandos de configuração do bot"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="config_cargo_cupula", description="Define o cargo de Alta Cúpula (apenas Alta Cúpula)")
    @app_commands.describe(
        cargo_id="ID do cargo de Alta Cúpula"
    )
    async def config_cargo_cupula(
        self,
        interaction: Interaction,
        cargo_id: str
    ):
        """Define o cargo de Alta Cúpula"""
        
        # Verifica permissão
        if not PermissionService.can_config_bot(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode configurar o bot.",
                ephemeral=True
            )
            return
        
        try:
            cargo_id_int = int(cargo_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ ID do cargo inválido. Deve ser um número.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Salva no banco de dados
                await ConfigService.set_config(
                    session=session,
                    key='cargo_cupula_id',
                    value=str(cargo_id_int),
                    description='ID do cargo de Alta Cúpula'
                )
                
                # Atualiza a configuração em memória
                Config.CARGO_CUPULA_ID = cargo_id_int
                
                embed = EmbedBuilder.create_success_embed(
                    f"Cargo de Alta Cúpula definido para ID: {cargo_id_int}"
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao configurar cargo: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="config_canal_logs", description="Define o canal de logs (apenas Alta Cúpula)")
    @app_commands.describe(
        canal_id="ID do canal de logs"
    )
    async def config_canal_logs(
        self,
        interaction: Interaction,
        canal_id: str
    ):
        """Define o canal de logs"""
        
        # Verifica permissão
        if not PermissionService.can_config_bot(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode configurar o bot.",
                ephemeral=True
            )
            return
        
        try:
            canal_id_int = int(canal_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ ID do canal inválido. Deve ser um número.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Salva no banco de dados
                await ConfigService.set_config(
                    session=session,
                    key='canal_logs_id',
                    value=str(canal_id_int),
                    description='ID do canal de logs'
                )
                
                # Atualiza a configuração em memória
                Config.CANAL_LOGS_ID = canal_id_int
                
                embed = EmbedBuilder.create_success_embed(
                    f"Canal de logs definido para ID: {canal_id_int}"
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao configurar canal: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="config_canal_cofre", description="Define o canal do cofre (apenas Alta Cúpula)")
    @app_commands.describe(
        canal_id="ID do canal do cofre"
    )
    async def config_canal_cofre(
        self,
        interaction: Interaction,
        canal_id: str
    ):
        """Define o canal do cofre"""
        
        # Verifica permissão
        if not PermissionService.can_config_bot(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode configurar o bot.",
                ephemeral=True
            )
            return
        
        try:
            canal_id_int = int(canal_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ ID do canal inválido. Deve ser um número.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Salva no banco de dados
                await ConfigService.set_config(
                    session=session,
                    key='canal_cofre_id',
                    value=str(canal_id_int),
                    description='ID do canal do cofre'
                )
                
                # Atualiza a configuração em memória
                Config.CANAL_COFRE_ID = canal_id_int
                
                embed = EmbedBuilder.create_success_embed(
                    f"Canal do cofre definido para ID: {canal_id_int}"
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao configurar canal: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="config_canal_bau", description="Define o canal do baú (apenas Alta Cúpula)")
    @app_commands.describe(
        canal_id="ID do canal do baú"
    )
    async def config_canal_bau(
        self,
        interaction: Interaction,
        canal_id: str
    ):
        """Define o canal do baú"""
        
        # Verifica permissão
        if not PermissionService.can_config_bot(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode configurar o bot.",
                ephemeral=True
            )
            return
        
        try:
            canal_id_int = int(canal_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ ID do canal inválido. Deve ser um número.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Salva no banco de dados
                await ConfigService.set_config(
                    session=session,
                    key='canal_bau_id',
                    value=str(canal_id_int),
                    description='ID do canal do baú'
                )
                
                # Atualiza a configuração em memória
                Config.CANAL_BAU_ID = canal_id_int
                
                embed = EmbedBuilder.create_success_embed(
                    f"Canal do baú definido para ID: {canal_id_int}"
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao configurar canal: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="config_canal_geral", description="Define o canal geral para frases automáticas (apenas Alta Cúpula)")
    @app_commands.describe(
        canal_id="ID do canal geral"
    )
    async def config_canal_geral(
        self,
        interaction: Interaction,
        canal_id: str
    ):
        """Define o canal geral"""
        
        # Verifica permissão
        if not PermissionService.can_config_bot(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode configurar o bot.",
                ephemeral=True
            )
            return
        
        try:
            canal_id_int = int(canal_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ ID do canal inválido. Deve ser um número.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Salva no banco de dados
                await ConfigService.set_config(
                    session=session,
                    key='canal_geral_id',
                    value=str(canal_id_int),
                    description='ID do canal geral para frases automáticas'
                )
                
                # Atualiza a configuração em memória
                Config.CANAL_GERAL_ID = canal_id_int
                
                embed = EmbedBuilder.create_success_embed(
                    f"Canal geral definido para ID: {canal_id_int}"
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao configurar canal: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="config_intervalo_frases", description="Define o intervalo das frases automáticas em minutos (apenas Alta Cúpula)")
    @app_commands.describe(
        minutos="Intervalo em minutos (mínimo: 1, máximo: 1440)"
    )
    async def config_intervalo_frases(
        self,
        interaction: Interaction,
        minutos: app_commands.Range[int, 1, 1440]
    ):
        """Define o intervalo das frases automáticas"""
        
        # Verifica permissão
        if not PermissionService.can_config_bot(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode configurar o bot.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Salva no banco de dados
                await ConfigService.set_config(
                    session=session,
                    key='intervalo_frases',
                    value=str(minutos),
                    description='Intervalo em minutos para frases automáticas'
                )
                
                # Atualiza a configuração em memória
                Config.INTERVALO_FRASES = minutos
                
                embed = EmbedBuilder.create_success_embed(
                    f"Intervalo de frases automáticas definido para {minutos} minutos"
                )
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao configurar intervalo: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="config_listar", description="Lista todas as configurações atuais (apenas Alta Cúpula)")
    async def config_listar(self, interaction: Interaction):
        """Lista todas as configurações atuais"""
        
        # Verifica permissão
        if not PermissionService.can_config_bot(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode ver as configurações.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Busca todas as configurações
                configs = await ConfigService.get_all_configs(session)
                
                # Cria embed
                embed = Embed(
                    title="⚙️ CONFIGURAÇÕES DO BOT",
                    description="Configurações atuais do sistema",
                    color=0x00bfff
                )
                
                # Adiciona configurações do arquivo .env
                embed.add_field(
                    name="📁 ARQUIVO .ENV",
                    value=f"Cargo Alta Cúpula: {Config.CARGO_CUPULA_ID}\n"
                          f"Canal Logs: {Config.CANAL_LOGS_ID}\n"
                          f"Canal Cofre: {Config.CANAL_COFRE_ID}\n"
                          f"Canal Baú: {Config.CANAL_BAU_ID}\n"
                          f"Canal Geral: {Config.CANAL_GERAL_ID}\n"
                          f"Intervalo Frases: {Config.INTERVALO_FRASES} minutos",
                    inline=False
                )
                
                # Adiciona configurações do banco de dados
                if configs:
                    bd_configs = "\n".join([
                        f"{c.key}: {c.value}"
                        for c in configs
                    ])
                    embed.add_field(
                        name="💾 BANCO DE DADOS",
                        value=bd_configs if bd_configs else "Nenhuma configuração adicional",
                        inline=False
                    )
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao listar configurações: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ConfigCommands(bot))
