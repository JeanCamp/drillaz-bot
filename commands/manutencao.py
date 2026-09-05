import discord
from discord import app_commands, Interaction
from discord.ext import commands
from config import Config

class ManutencaoCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="manutencao", description="Envia aviso de manutenção do bot")
    @app_commands.describe(motivo="Motivo da manutenção")
    async def manutencao(self, interaction: Interaction, motivo: str = "Manutenção programada"):
        """Envia aviso de manutenção no canal geral"""
        
        # Verifica permissão (apenas Alta Cúpula)
        if not Config.CARGO_CUPULA_ID or Config.CARGO_CUPULA_ID == 0:
            await interaction.response.send_message("❌ Cargo de Alta Cúpula não configurado.", ephemeral=True)
            return
        
        has_permission = False
        for role in interaction.user.roles:
            if role.id == Config.CARGO_CUPULA_ID:
                has_permission = True
                break
        
        if not has_permission:
            await interaction.response.send_message("❌ Apenas a Alta Cúpula pode usar este comando.", ephemeral=True)
            return
        
        await interaction.response.defer()
        
        # Envia aviso no canal geral
        if Config.CANAL_GERAL_ID and Config.CANAL_GERAL_ID != 0:
            canal_geral = self.bot.get_channel(Config.CANAL_GERAL_ID)
            if canal_geral:
                embed = discord.Embed(
                    title="🔧 AVISO DE MANUTENÇÃO",
                    description="O bot entrará em manutenção em breve.",
                    color=discord.Color.orange()
                )
                embed.add_field(name="📋 Motivo", value=motivo, inline=False)
                embed.add_field(name="⏰ Início", value=f"<t:{int(discord.utils.utcnow().timestamp())}:R>", inline=False)
                embed.set_footer(text="Sistema de gestão da gangue")
                embed.timestamp = discord.utils.utcnow()
                
                await canal_geral.send(embed=embed)
                await interaction.followup.send("✅ Aviso de manutenção enviado ao canal geral.", ephemeral=True)
            else:
                await interaction.followup.send("❌ Canal geral não encontrado.", ephemeral=True)
        else:
            await interaction.followup.send("❌ Canal geral não configurado.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ManutencaoCommands(bot))
