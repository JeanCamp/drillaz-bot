import discord
from discord.ext import commands
from config import Config
import asyncio

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = False  # Desabilitado para não precisar de intent privilegiada
intents.guilds = True
intents.members = False  # Desabilitado para não precisar de intent privilegiada

# Cria o bot
bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)

@bot.event
async def setup_hook():
    """Carrega as extensões (cogs) do bot"""
    print('📦 Carregando extensões...')
    
    extensions = [
        'commands.cofre',
        'commands.bau',
        'commands.config',
        'commands.frase',
        'commands.relatorio',
        'commands.manutencao'
    ]
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f'✅ {extension} carregado')
        except Exception as e:
            print(f'❌ Erro ao carregar {extension}: {e}')

@bot.event
async def on_ready():
    """Evento quando o bot está pronto"""
    from events.on_ready import on_ready
    await on_ready(bot)

@bot.event
async def on_command_error(ctx, error):
    """Tratamento global de erros de comando"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignora comandos não encontrados
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argumento obrigatório faltando: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Argumento inválido: {error}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ O bot não tem permissão para executar este comando.")
    else:
        print(f"Erro não tratado: {error}")
        await ctx.send("❌ Ocorreu um erro ao executar o comando.")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    """Tratamento de interações (slash commands)"""
    # O tratamento de erros de interação é feito individualmente em cada comando
    pass

@bot.command(name='testar')
async def testar(ctx):
    """Comando de teste temporário"""
    await ctx.send("✅ Bot está funcionando! Comandos de prefixo funcionam.")

@bot.command(name='comandos')
async def listar_comandos(ctx):
    """Lista comandos disponíveis temporariamente"""
    comandos = [
        "💰 Cofre: !cofre_deposito, !cofre_saldo, !cofre_historico",
        "📦 Baú: !bau_entrada, !bau_itens, !bau_historico",
        "⚙️ Config: !config_listar",
        "💬 Frases: !frase_listar, !frase_testar",
        "📊 Relatórios: !relatorio"
    ]
    await ctx.send("📋 **Comandos disponíveis (temporarily):**\n\n" + "\n".join(comandos))

def main():
    """Função principal para iniciar o bot"""
    try:
        # Valida as configurações
        Config.validate()
        
        print('🚀 Iniciando bot...')
        print(f'📋 Prefixo: !')
        print(f'🔧 Intents: message_content=False, guilds=True, members=False')
        
        # Inicia o bot
        bot.run(Config.DISCORD_TOKEN)
        
    except ValueError as e:
        print(f'❌ Erro de configuração: {e}')
        print('Por favor, verifique o arquivo .env')
    except Exception as e:
        print(f'❌ Erro ao iniciar o bot: {e}')

if __name__ == '__main__':
    main()
