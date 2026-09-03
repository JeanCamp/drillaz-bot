import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from services.frase_service import FraseService
from services.permission_service import PermissionService
from utils.embeds import EmbedBuilder
from utils.validators import ValidationError
from config import Config

class FraseCommands(commands.Cog):
    """Comandos de gerenciamento de frases automáticas"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="frase_adicionar", description="Adiciona uma nova frase automática (apenas Alta Cúpula)")
    @app_commands.describe(
        frase="A frase a ser adicionada"
    )
    async def frase_adicionar(
        self,
        interaction: Interaction,
        frase: str
    ):
        """Adiciona uma nova frase automática"""
        
        # Verifica permissão
        if not PermissionService.can_manage_frases(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode gerenciar frases.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Adiciona a frase
                nova_frase = await FraseService.adicionar_frase(session, frase)
                
                embed = EmbedBuilder.create_success_embed(
                    f"Frase adicionada com sucesso!\n\n"
                    f"ID: {nova_frase.id}\n"
                    f"Frase: {nova_frase.frase}"
                )
                await interaction.followup.send(embed=embed)
                
        except ValidationError as e:
            embed = EmbedBuilder.create_error_embed(str(e))
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao adicionar frase: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="frase_remover", description="Remove uma frase automática (apenas Alta Cúpula)")
    @app_commands.describe(
        frase_id="ID da frase a ser removida"
    )
    async def frase_remover(
        self,
        interaction: Interaction,
        frase_id: int
    ):
        """Remove uma frase automática"""
        
        # Verifica permissão
        if not PermissionService.can_manage_frases(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode gerenciar frases.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Remove a frase
                removida = await FraseService.remover_frase(session, frase_id)
                
                if removida:
                    embed = EmbedBuilder.create_success_embed(
                        f"Frase ID {frase_id} removida com sucesso!"
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    embed = EmbedBuilder.create_error_embed(
                        f"Frase ID {frase_id} não encontrada."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao remover frase: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="frase_listar", description="Lista todas as frases automáticas (apenas Alta Cúpula)")
    @app_commands.describe(
        inativas="Incluir frases inativas no listamento"
    )
    async def frase_listar(
        self,
        interaction: Interaction,
        inativas: bool = False
    ):
        """Lista todas as frases automáticas"""
        
        # Verifica permissão
        if not PermissionService.can_manage_frases(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode listar frases.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Lista as frases
                frases = await FraseService.listar_frases(session, ativas_only=not inativas)
                
                if not frases:
                    embed = EmbedBuilder.create_info_embed("Nenhuma frase cadastrada.")
                    await interaction.followup.send(embed=embed)
                    return
                
                # Cria embed
                embed = Embed(
                    title="💬 FRASES AUTOMÁTICAS",
                    description=f"Total: {len(frases)} frases",
                    color=0x00bfff
                )
                
                for frase in frases[:25]:  # Limita a 25 frases
                    status = "✅" if frase.ativa else "❌"
                    embed.add_field(
                        name=f"{status} ID {frase.id}",
                        value=frase.frase,
                        inline=False
                    )
                
                if len(frases) > 25:
                    embed.set_footer(text=f"Mostrando 25 de {len(frases)} frases")
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao listar frases: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="frase_ativar", description="Ativa uma frase automática (apenas Alta Cúpula)")
    @app_commands.describe(
        frase_id="ID da frase a ser ativada"
    )
    async def frase_ativar(
        self,
        interaction: Interaction,
        frase_id: int
    ):
        """Ativa uma frase automática"""
        
        # Verifica permissão
        if not PermissionService.can_manage_frases(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode gerenciar frases.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Ativa a frase
                frase = await FraseService.ativar_frase(session, frase_id)
                
                if frase:
                    embed = EmbedBuilder.create_success_embed(
                        f"Frase ID {frase_id} ativada com sucesso!"
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    embed = EmbedBuilder.create_error_embed(
                        f"Frase ID {frase_id} não encontrada."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao ativar frase: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="frase_desativar", description="Desativa uma frase automática (apenas Alta Cúpula)")
    @app_commands.describe(
        frase_id="ID da frase a ser desativada"
    )
    async def frase_desativar(
        self,
        interaction: Interaction,
        frase_id: int
    ):
        """Desativa uma frase automática"""
        
        # Verifica permissão
        if not PermissionService.can_manage_frases(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode gerenciar frases.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Desativa a frase
                frase = await FraseService.desativar_frase(session, frase_id)
                
                if frase:
                    embed = EmbedBuilder.create_success_embed(
                        f"Frase ID {frase_id} desativada com sucesso!"
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    embed = EmbedBuilder.create_error_embed(
                        f"Frase ID {frase_id} não encontrada."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao desativar frase: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="frase_testar", description="Envia uma frase aleatória para testar (apenas Alta Cúpula)")
    async def frase_testar(self, interaction: Interaction):
        """Envia uma frase aleatória para testar"""
        
        # Verifica permissão
        if not PermissionService.can_manage_frases(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode testar frases.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Busca uma frase aleatória
                frase = await FraseService.get_frase_aleatoria(session)
                
                if frase:
                    embed = Embed(
                        title="💬 FRASE ALEATÓRIA",
                        description=frase,
                        color=0x00bfff
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    embed = EmbedBuilder.create_warning_embed(
                        "Nenhuma frase ativa encontrada. Adicione frases primeiro."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao testar frase: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(FraseCommands(bot))
