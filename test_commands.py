import discord
from discord import app_commands
from discord.ext import commands

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = False
intents.guilds = True
intents.members = False

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user.name}')
    print(f'📊 Servidores: {len(bot.guilds)}')
    
    # Sincronizar comandos
    print('🔄 Sincronizando comandos...')
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} comandos sincronizados')
        for cmd in synced:
            print(f'  - /{cmd.name}')
    except Exception as e:
        print(f'❌ Erro: {e}')

@bot.tree.command(name="teste")
async def teste(interaction: discord.Interaction):
    await interaction.response.send_message("✅ Comando de teste funcionou!")

@bot.tree.command(name="cofre_deposito")
async def cofre_deposito(interaction: discord.Interaction, valor: float, motivo: str = None):
    await interaction.response.send_message(f"✅ Depósito de R$ {valor} registrado!")

# Executar
if __name__ == '__main__':
    from config import Config
    bot.run(Config.DISCORD_TOKEN)
