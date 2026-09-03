import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from services.relatorio_service import RelatorioService
from services.permission_service import PermissionService
from utils.embeds import EmbedBuilder
from utils.formatters import format_currency, format_number
from config import Config
from typing import Optional

class RelatorioCommands(commands.Cog):
    """Comandos de relatórios da gangue"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="relatorio", description="Gera um relatório geral da gangue (apenas Alta Cúpula)")
    @app_commands.describe(
        periodo="Período em dias (padrão: 30)"
    )
    async def relatorio(
        self,
        interaction: Interaction,
        periodo: Optional[app_commands.Range[int, 1, 365]] = 30
    ):
        """Gera um relatório geral da gangue"""
        
        # Verifica permissão
        if not PermissionService.can_view_relatorio(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode ver relatórios.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Gera o relatório
                dados = await RelatorioService.gerar_relatorio_geral(session, periodo)
                
                # Cria embed
                embed = Embed(
                    title=f"📊 RELATÓRIO DA GANGUE - ÚLTIMOS {periodo} DIAS",
                    description="Resumo das movimentações",
                    color=0x9b59b6
                )
                
                # Cofre
                cofre_text = (
                    f"💰 Saldo atual: {format_currency(dados['cofre']['saldo'])}\n"
                    f"📥 Total depositado: {format_currency(dados['cofre']['total_depositado'])}\n"
                    f"📤 Total retirado: {format_currency(dados['cofre']['total_retirada'])}"
                )
                embed.add_field(name="💵 COFRE", value=cofre_text, inline=False)
                
                # Baú
                bau_text = (
                    f"📥 Total de entradas: {format_number(dados['bau']['total_entradas'])}\n"
                    f"📤 Total de retiradas: {format_number(dados['bau']['total_retiradas'])}"
                )
                embed.add_field(name="📦 BAÚ", value=bau_text, inline=False)
                
                # Top usuários do cofre
                if dados['cofre']['top_usuarios']:
                    top_cofre = "\n".join([
                        f"{i+1}. <@{u['user_id']}> - {u['quantidade']} movimentos"
                        for i, u in enumerate(dados['cofre']['top_usuarios'][:5])
                    ])
                    embed.add_field(name="👥 Top Usuários - Cofre", value=top_cofre, inline=False)
                
                # Top usuários do baú
                if dados['bau']['top_usuarios']:
                    top_bau = "\n".join([
                        f"{i+1}. <@{u['user_id']}> - {u['quantidade']} movimentos"
                        for i, u in enumerate(dados['bau']['top_usuarios'][:5])
                    ])
                    embed.add_field(name="👥 Top Usuários - Baú", value=top_bau, inline=False)
                
                # Top itens do baú
                if dados['bau']['top_itens']:
                    top_itens = "\n".join([
                        f"{i+1}. {item['item_nome']} - {item['quantidade']} movimentos"
                        for i, item in enumerate(dados['bau']['top_itens'][:5])
                    ])
                    embed.add_field(name="📦 Top Itens", value=top_itens, inline=False)
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao gerar relatório: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="relatorio_cofre", description="Gera um relatório específico do cofre (apenas Alta Cúpula)")
    @app_commands.describe(
        periodo="Período em dias (padrão: 30)"
    )
    async def relatorio_cofre(
        self,
        interaction: Interaction,
        periodo: Optional[app_commands.Range[int, 1, 365]] = 30
    ):
        """Gera um relatório específico do cofre"""
        
        # Verifica permissão
        if not PermissionService.can_view_relatorio(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode ver relatórios.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Gera o relatório
                dados = await RelatorioService.gerar_relatorio_cofre(session, periodo)
                
                # Cria embed
                embed = Embed(
                    title=f"💰 RELATÓRIO DO COFRE - ÚLTIMOS {periodo} DIAS",
                    description="Resumo das movimentações financeiras",
                    color=0xf1c40f
                )
                
                # Dados financeiros
                financeiro_text = (
                    f"💰 Saldo atual: {format_currency(dados['saldo'])}\n"
                    f"📥 Total depositado: {format_currency(dados['total_depositado'])}\n"
                    f"📤 Total retirado: {format_currency(dados['total_retirado'])}"
                )
                embed.add_field(name="💵 FINANCEIRO", value=financeiro_text, inline=False)
                
                # Top usuários
                if dados['top_usuarios']:
                    top_usuarios = "\n".join([
                        f"{i+1}. <@{u['user_id']}> - {u['quantidade']} movimentos\n"
                        f"   Depositos: {format_currency(u['total_depositado'])} | Retiradas: {format_currency(u['total_retirado'])}"
                        for i, u in enumerate(dados['top_usuarios'][:10])
                    ])
                    embed.add_field(name="👥 Top Usuários", value=top_usuarios, inline=False)
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao gerar relatório: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="relatorio_bau", description="Gera um relatório específico do baú (apenas Alta Cúpula)")
    @app_commands.describe(
        periodo="Período em dias (padrão: 30)"
    )
    async def relatorio_bau(
        self,
        interaction: Interaction,
        periodo: Optional[app_commands.Range[int, 1, 365]] = 30
    ):
        """Gera um relatório específico do baú"""
        
        # Verifica permissão
        if not PermissionService.can_view_relatorio(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode ver relatórios.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Gera o relatório
                dados = await RelatorioService.gerar_relatorio_bau(session, periodo)
                
                # Cria embed
                embed = Embed(
                    title=f"📦 RELATÓRIO DO BAÚ - ÚLTIMOS {periodo} DIAS",
                    description="Resumo das movimentações de itens",
                    color=0x2ecc71
                )
                
                # Dados do baú
                bau_text = (
                    f"📥 Total de entradas: {format_number(dados['total_entradas'])}\n"
                    f"📤 Total de retiradas: {format_number(dados['total_retiradas'])}"
                )
                embed.add_field(name="📦 MOVIMENTAÇÕES", value=bau_text, inline=False)
                
                # Top usuários
                if dados['top_usuarios']:
                    top_usuarios = "\n".join([
                        f"{i+1}. <@{u['user_id']}> - {u['quantidade']} movimentos\n"
                        f"   Entradas: {format_number(u['total_entradas'])} | Retiradas: {format_number(u['total_retiradas'])}"
                        for i, u in enumerate(dados['top_usuarios'][:10])
                    ])
                    embed.add_field(name="👥 Top Usuários", value=top_usuarios, inline=False)
                
                # Top itens
                if dados['top_itens']:
                    top_itens = "\n".join([
                        f"{i+1}. {item['item_nome']} - {item['quantidade']} movimentos\n"
                        f"   Entradas: {format_number(item['total_entradas'])} | Retiradas: {format_number(item['total_retiradas'])}"
                        for i, item in enumerate(dados['top_itens'][:10])
                    ])
                    embed.add_field(name="📦 Top Itens", value=top_itens, inline=False)
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao gerar relatório: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="relatorio_usuario", description="Gera um relatório de um usuário específico")
    @app_commands.describe(
        usuario="Usuário para gerar o relatório",
        periodo="Período em dias (padrão: 30)"
    )
    async def relatorio_usuario(
        self,
        interaction: Interaction,
        usuario: Member,
        periodo: Optional[app_commands.Range[int, 1, 365]] = 30
    ):
        """Gera um relatório de um usuário específico"""
        
        # Verifica permissão
        # Alta Cúpula pode ver qualquer usuário
        # Membros comuns só podem ver próprio relatório
        if not PermissionService.can_view_relatorio(interaction.user):
            if interaction.user.id != usuario.id:
                await interaction.response.send_message(
                    "❌ Você só pode ver seu próprio relatório.",
                    ephemeral=True
                )
                return
        
        await interaction.response.defer()
        
        try:
            async for session in get_db():
                # Gera o relatório
                dados = await RelatorioService.gerar_relatorio_usuario(session, str(usuario.id), periodo)
                
                # Cria embed
                embed = Embed(
                    title=f"👤 RELATÓRIO DO USUÁRIO - @{usuario.display_name}",
                    description=f"Últimos {periodo} dias",
                    color=0x3498db
                )
                
                # Cofre
                cofre_text = (
                    f"📥 Total depositado: {format_currency(dados['cofre']['total_depositos'])}\n"
                    f"📤 Total retirado: {format_currency(dados['cofre']['total_retiradas'])}\n"
                    f"📊 Movimentações: {dados['cofre']['quantidade_movimentacoes']}"
                )
                embed.add_field(name="💵 COFRE", value=cofre_text, inline=False)
                
                # Baú
                bau_text = (
                    f"📥 Total de entradas: {format_number(dados['bau']['total_entradas'])}\n"
                    f"📤 Total de retiradas: {format_number(dados['bau']['total_retiradas'])}\n"
                    f"📊 Movimentações: {dados['bau']['quantidade_movimentacoes']}"
                )
                embed.add_field(name="📦 BAÚ", value=bau_text, inline=False)
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao gerar relatório: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RelatorioCommands(bot))
