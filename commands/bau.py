import discord
from discord import app_commands, Interaction, Member, ui
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database.connection import get_db
from database.models import BauItem, BauMovimentacao
from services.bau_service import BauService
from services.permission_service import PermissionService
from services.log_service import LogService
from utils.embeds import EmbedBuilder
from utils.validators import ValidationError
from config import Config
from typing import Optional

class BauCommands(commands.Cog):
    """Comandos do sistema de Baú"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._itens_cache = None
        self._cache_timestamp = None
    
    async def get_canal_logs(self):
        """Retorna o canal de logs configurado"""
        if Config.CANAL_LOGS_ID == 0:
            return None
        return self.bot.get_channel(Config.CANAL_LOGS_ID)
    
    async def get_itens_cache(self):
        """Retorna itens do cache ou carrega do banco de dados"""
        import time
        
        # Se o cache tem menos de 5 minutos, usa cache
        if self._cache_timestamp and (time.time() - self._cache_timestamp) < 300:
            return self._itens_cache
        
        # Carrega do banco de dados
        try:
            async with get_db() as session:
                result = await session.execute(
                    select(BauItem).order_by(BauItem.nome)
                )
                itens = result.scalars().all()
                self._itens_cache = [item.nome for item in itens]
                self._cache_timestamp = time.time()
                return self._itens_cache
        except:
            return []
    
    @app_commands.command(name="bau_entrada", description="Registra uma entrada de item no baú")
    @app_commands.describe(
        item="Nome do item (use autocomplete para itens existentes)",
        quantidade="Quantidade a ser adicionada",
        motivo="Motivo da entrada"
    )
    async def bau_entrada(
        self,
        interaction: Interaction,
        item: str,
        quantidade: app_commands.Range[int, 1],
        motivo: Optional[str] = None
    ):
        """Registra uma entrada de item no baú"""
        
        # Verifica se está no canal correto
        if not PermissionService.check_channel(interaction.channel_id, Config.CANAL_BAU_ID):
            await interaction.response.send_message(
                "❌ Este comando só pode ser utilizado no canal do baú.",
                ephemeral=True
            )
            return
        
        # Verifica permissão
        if not PermissionService.can_bau_entrada(interaction.user):
            await interaction.response.send_message(
                "❌ Você não tem permissão para fazer entradas no baú.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        user_info = PermissionService.get_user_info(interaction.user)
        
        try:
            async with get_db() as session:
                # Registra a entrada
                movimentacao = await BauService.entrada(
                    session=session,
                    user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    item_nome=item,
                    quantidade=quantidade,
                    motivo=motivo or ""
                )
                
                # Envia log
                canal_logs = await self.get_canal_logs()
                if canal_logs:
                    await LogService.send_bau_log(
                        session=session,
                        movimentacao=movimentacao,
                        user_mention=user_info['user_mention'],
                        canal_logs=canal_logs
                    )
                
                embed = EmbedBuilder.create_success_embed(
                    f"Entrada de {quantidade}x {item} registrada com sucesso!\n\n"
                    f"Estoque atual: {movimentacao.estoque_posterior} unidades"
                )
                await interaction.followup.send(embed=embed)
                
        except ValidationError as e:
            embed = EmbedBuilder.create_error_embed(str(e))
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao processar entrada: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @bau_entrada.autocomplete('item')
    async def bau_entrada_autocomplete(
        self,
        interaction: Interaction,
        current: str
    ):
        """Autocomplete com itens do banco de dados (usando cache)"""
        itens = await self.get_itens_cache()
        
        if current:
            itens = [i for i in itens if current.lower() in i.lower()]
        
        return [
            app_commands.Choice(name=item, value=item)
            for item in itens[:25]
        ]
    
    @app_commands.command(name="bau_retirada", description="Registra uma retirada de item do baú")
    @app_commands.describe(
        item="Nome do item (use autocomplete para itens existentes)",
        quantidade="Quantidade a ser retirada",
        motivo="Motivo da retirada"
    )
    async def bau_retirada(
        self,
        interaction: Interaction,
        item: str,
        quantidade: app_commands.Range[int, 1],
        motivo: Optional[str] = None
    ):
        """Registra uma retirada de item do baú"""
        
        # Verifica se está no canal correto
        if not PermissionService.check_channel(interaction.channel_id, Config.CANAL_BAU_ID):
            await interaction.response.send_message(
                "❌ Este comando só pode ser utilizado no canal do baú.",
                ephemeral=True
            )
            return
        
        # Verifica permissão
        if not PermissionService.can_bau_retirada(interaction.user):
            await interaction.response.send_message(
                "❌ Você não tem permissão para fazer retiradas do baú.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        user_info = PermissionService.get_user_info(interaction.user)
        
        try:
            async with get_db() as session:
                # Registra a retirada
                movimentacao = await BauService.retirada(
                    session=session,
                    user_id=user_info['user_id'],
                    user_name=user_info['user_name'],
                    item_nome=item,
                    quantidade=quantidade,
                    motivo=motivo or ""
                )
                
                # Envia log
                canal_logs = await self.get_canal_logs()
                if canal_logs:
                    await LogService.send_bau_log(
                        session=session,
                        movimentacao=movimentacao,
                        user_mention=user_info['user_mention'],
                        canal_logs=canal_logs
                    )
                
                embed = EmbedBuilder.create_success_embed(
                    f"Retirada de {quantidade}x {item} registrada com sucesso!\n\n"
                    f"Estoque atual: {movimentacao.estoque_posterior} unidades"
                )
                await interaction.followup.send(embed=embed)
                
        except ValidationError as e:
            embed = EmbedBuilder.create_error_embed(str(e))
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao processar retirada: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @bau_retirada.autocomplete('item')
    async def bau_retirada_autocomplete(
        self,
        interaction: Interaction,
        current: str
    ):
        """Autocomplete com itens do banco de dados (usando cache)"""
        itens = await self.get_itens_cache()
        
        if current:
            itens = [i for i in itens if current.lower() in i.lower()]
        
        return [
            app_commands.Choice(name=item, value=item)
            for item in itens[:25]
        ]
    
    @app_commands.command(name="bau_itens", description="Lista todos os itens do baú e seus estoques")
    async def bau_itens(self, interaction: Interaction):
        """Lista todos os itens do baú"""
        
        await interaction.response.defer()
        
        try:
            async with get_db() as session:
                # Busca todos os itens
                itens = await BauService.get_all_items(session)
                
                # Cria embed
                embed = EmbedBuilder.create_bau_itens_embed(itens)
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao listar itens: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="bau_historico", description="Consulta o histórico do baú")
    @app_commands.describe(
        usuario="Filtrar por usuário (opcional)",
        item="Filtrar por item (opcional)",
        tipo="Filtrar por tipo: entrada, retirada (opcional)",
        periodo="Filtrar por período em dias (opcional)"
    )
    async def bau_historico(
        self,
        interaction: Interaction,
        usuario: Optional[Member] = None,
        item: Optional[str] = None,
        tipo: Optional[str] = None,
        periodo: Optional[app_commands.Range[int, 1, 365]] = None
    ):
        """Consulta o histórico do baú"""
        
        # Verifica permissão
        if not PermissionService.can_view_bau_historico(interaction.user):
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
        if tipo and tipo.lower() not in ['entrada', 'retirada']:
            await interaction.followup.send(
                "❌ Tipo inválido. Use: entrada ou retirada",
                ephemeral=True
            )
            return
        
        try:
            async with get_db() as session:
                # Busca histórico
                historico = await BauService.get_historico(
                    session=session,
                    limit=50,
                    user_id=user_id,
                    item_nome=item,
                    tipo=tipo.lower() if tipo else None,
                    periodo_dias=periodo
                )
                
                # Cria embed
                titulo = "📦 HISTÓRICO DO BAÚ"
                if usuario:
                    titulo += f" - @{usuario.display_name}"
                if item:
                    titulo += f" - {item}"
                if tipo:
                    titulo += f" - {tipo.upper()}"
                if periodo:
                    titulo += f" - Últimos {periodo} dias"
                
                embed = EmbedBuilder.create_bau_historico_embed(historico, titulo)
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao consultar histórico: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="bau_estoque", description="Consulta o estoque de um item específico")
    @app_commands.describe(
        item="Nome do item"
    )
    async def bau_estoque(
        self,
        interaction: Interaction,
        item: str
    ):
        """Consulta o estoque de um item específico"""
        
        await interaction.response.defer()
        
        try:
            async with get_db() as session:
                # Busca o item
                item_obj = await BauService.get_item_by_nome(session, item)
                
                if not item_obj:
                    embed = EmbedBuilder.create_error_embed(f"Item '{item}' não encontrado no baú.")
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
                
                # Cria embed
                embed = discord.Embed(
                    title=f"📦 ESTOQUE: {item_obj.nome}",
                    description=f"Quantidade disponível: {item_obj.estoque}",
                    color=0x00ff00
                )
                embed.add_field(name="📅 Última atualização", value=item_obj.updated_at.strftime("%d/%m/%Y %H:%M"), inline=False)
                embed.set_footer(text=f"ID do item: {item_obj.id}")
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao consultar estoque: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="bau_deletar_item", description="Deleta um item do baú e suas movimentações (apenas Alta Cúpula)")
    @app_commands.describe(
        item="Nome do item a ser deletado"
    )
    async def bau_deletar_item(
        self,
        interaction: Interaction,
        item: str
    ):
        """Deleta um item do baú e suas movimentações"""
        
        # Verifica permissão (apenas Alta Cúpula)
        if not PermissionService.can_view_bau_historico(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a Alta Cúpula pode deletar itens do baú.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            async with get_db() as session:
                # Busca o item
                item_obj = await BauService.get_item_by_nome(session, item)
                
                if not item_obj:
                    embed = EmbedBuilder.create_error_embed(f"Item '{item}' não encontrado no baú.")
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
                
                # Conta movimentações
                from sqlalchemy import func, select
                result = await session.execute(
                    select(func.count()).select_from(BauMovimentacao).where(BauMovimentacao.item_id == item_obj.id)
                )
                total_movimentacoes = result.scalar()
                
                # Mostra confirmação
                embed = discord.Embed(
                    title="⚠️ CONFIRMAÇÃO DE DELEÇÃO",
                    description=f"Você está prestes a deletar o item **{item_obj.nome}**",
                    color=discord.Color.orange()
                )
                embed.add_field(name="📦 Item", value=item_obj.nome, inline=True)
                embed.add_field(name="🔢 Estoque atual", value=str(item_obj.estoque), inline=True)
                embed.add_field(name="📋 Movimentações", value=str(total_movimentacoes), inline=True)
                embed.add_field(
                    name="⚠️ AVISO",
                    value="Isso deletará o item e TODAS as suas movimentações do histórico. Esta ação não pode ser desfeita!",
                    inline=False
                )
                
                # Adiciona botões de confirmação
                view = ConfirmarDelecaoView(item_obj.id, item_obj.nome)
                await interaction.followup.send(embed=embed, view=view)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao preparar deleção: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

class ConfirmarDelecaoView(ui.View):
    """View com botões para confirmar deleção de item"""
    
    def __init__(self, item_id: int, item_nome: str):
        super().__init__(timeout=60)
        self.item_id = item_id
        self.item_nome = item_nome
    
    @ui.button(label="✅ Confirmar", style=discord.ButtonStyle.green, emoji="✅")
    async def confirmar(self, interaction: Interaction, button: ui.Button):
        """Confirma a deleção do item"""
        await interaction.response.defer()
        
        try:
            async with get_db() as session:
                # Deleta movimentações
                await session.execute(
                    delete(BauMovimentacao).where(BauMovimentacao.item_id == self.item_id)
                )
                
                # Deleta o item
                await session.execute(
                    delete(BauItem).where(BauItem.id == self.item_id)
                )
                
                await session.commit()
                
                # Limpa o cache de itens
                # Precisamos reiniciar o bot ou implementar limpeza de cache
                
                embed = EmbedBuilder.create_success_embed(
                    f"Item **{self.item_nome}** e suas movimentações foram deletados com sucesso!"
                )
                await interaction.followup.send(embed=embed)
                
                # Desabilita os botões
                for child in self.children:
                    child.disabled = True
                await interaction.edit_original_response(view=self)
                
        except Exception as e:
            embed = EmbedBuilder.create_error_embed(f"Erro ao deletar item: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @ui.button(label="❌ Cancelar", style=discord.ButtonStyle.red, emoji="❌")
    async def cancelar(self, interaction: Interaction, button: ui.Button):
        """Cancela a deleção"""
        await interaction.response.edit_message(
            content="❌ Deleção cancelada.",
            embed=None,
            view=None
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(BauCommands(bot))
