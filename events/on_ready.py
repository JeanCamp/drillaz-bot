from discord.ext import commands
from database.connection import init_db
from services.frase_service import FraseService
from config import Config

async def on_ready(bot: commands.Bot):
    """Evento quando o bot está pronto"""
    print(f'✅ Bot conectado como {bot.user.name} (ID: {bot.user.id})')
    print(f'📊 Servidores: {len(bot.guilds)}')
    
    # Inicializa o banco de dados
    print('📁 Inicializando banco de dados...')
    await init_db()
    print('✅ Banco de dados inicializado')
    
    # Frases padrão removidas - usuário vai adicionar suas próprias frases
    # from database.connection import get_db
    # async for session in get_db():
    #     await FraseService.inicializar_frases_padrao(session)
    #     print('✅ Frases padrão verificadas')
    
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
    if Config.CANAL_GERAL_ID != 0 and Config.INTERVALO_FRASES > 0:
        bot.loop.create_task(enviar_frases_automaticas(bot))
        print(f'🔄 Task de frases automáticas iniciada (intervalo: {Config.INTERVALO_FRASES} minutos)')
    else:
        print('⚠️ Task de frases automáticas não iniciada (canal ou intervalo não configurados)')

async def enviar_frases_automaticas(bot: commands.Bot):
    """Task em background para enviar frases automáticas"""
    import asyncio
    from database.connection import get_db
    
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        try:
            # Aguarda o intervalo configurado
            await asyncio.sleep(Config.INTERVALO_FRASES * 60)
            
            # Busca o canal geral
            canal = bot.get_channel(Config.CANAL_GERAL_ID)
            if not canal:
                print(f'⚠️ Canal geral (ID: {Config.CANAL_GERAL_ID}) não encontrado')
                continue
            
            # Busca uma frase aleatória
            async for session in get_db():
                frase = await FraseService.get_frase_aleatoria(session)
                
                if frase:
                    await canal.send(f"💬 {frase}")
                    print(f'💬 Frase enviada: {frase[:50]}...')
                else:
                    print('⚠️ Nenhuma frase ativa encontrada')
                    
        except Exception as e:
            print(f'❌ Erro na task de frases automáticas: {e}')
            await asyncio.sleep(60)  # Aguarda 1 minuto antes de tentar novamente
