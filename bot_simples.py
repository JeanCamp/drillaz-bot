import discord
from discord import app_commands
from discord.ext import commands
from config import Config

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

@bot.tree.command(name="cofre_saldo")
async def cofre_saldo(interaction: discord.Interaction):
    await interaction.response.send_message("💰 Saldo do cofre: R$ 0")

@bot.tree.command(name="bau_entrada")
async def bau_entrada(interaction: discord.Interaction, item: str, quantidade: int, motivo: str = None):
    await interaction.response.send_message(f"✅ Entrada de {quantidade}x {item} registrada!")

def main():
    try:
        Config.validate()
        print('🚀 Iniciando bot simples...')
        bot.run(Config.DISCORD_TOKEN)
    except ValueError as e:
        print(f'❌ Erro de configuração: {e}')
    except Exception as e:
        print(f'❌ Erro ao iniciar o bot: {e}')

if __name__ == '__main__':
    main()
