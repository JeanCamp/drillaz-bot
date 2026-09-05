from services.log_service import LogService
from database.connection import init_db
from config import Config

async def on_ready(bot):
    """Evento quando o bot está pronto"""
    
    print(f'✅ Bot conectado como {bot.user.name}')
    print(f'📊 Servidores: {len(bot.guilds)}')
    
    # Inicializa o banco de dados
    print('📁 Inicializando banco de dados...')
    try:
        await init_db()
        print('✅ Banco de dados inicializado')
    except Exception as e:
        print(f'❌ Erro ao inicializar banco de dados: {e}')
    
    # Sincroniza os comandos slash
    print('🔄 Sincronizando comandos slash...')
    
    # Primeiro, vamos verificar quantos comandos estão na tree
    print(f'📊 Comandos na tree global: {len(bot.tree.get_commands())}')
    
    # Listar comandos na tree
    for command in bot.tree.get_commands():
        print(f'  - {command.name}')
    
    try:
        # Sincroniza globalmente
        print('🌐 Sincronizando globalmente...')
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} comandos sincronizados globalmente')
        
        # Depois sincroniza em todos os servidores
        print('🌐 Sincronizando em todos os servidores...')
        for guild in bot.guilds:
            try:
                guild_synced = await bot.tree.sync(guild=guild)
                print(f'✅ {len(guild_synced)} comandos sincronizados no servidor {guild.name} (ID: {guild.id})')
                for command in guild_synced:
                    print(f'  - /{command.name}')
            except Exception as e:
                print(f'⚠️ Erro ao sincronizar no servidor {guild.name}: {e}')
                
    except Exception as e:
        print(f'❌ Erro ao sincronizar comandos: {e}')
    
    # Inicia a task de frases automáticas
    from services.frase_service import FraseService
    print(f'🔄 Task de frases automáticas iniciada (intervalo: {Config.INTERVALO_FRASES} minutos)')
    
    # Log de inicialização
    try:
        async for session in bot.get_db():
            await LogService.log_sistema(
                session=session,
                mensagem=f"Bot inicializado em {len(bot.guilds)} servidores",
                contexto="startup"
            )
    except:
        pass
