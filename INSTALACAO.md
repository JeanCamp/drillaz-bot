# 🚀 Guia Rápido de Instalação

## Passo 1: Preparação do Ambiente

### 1.1 Verifique se tem Python 3.12+ instalado
```bash
python --version
```

Se não tiver, baixe em: https://www.python.org/downloads/

### 1.2 Navegue até a pasta do projeto
```bash
cd "C:\Users\Jean\Desktop\PROJETO SITE\MEU DUO"
```

### 1.3 Crie ambiente virtual (opcional mas recomendado)
```bash
python -m venv venv
```

### 1.4 Ative o ambiente virtual
```bash
venv\Scripts\activate
```

## Passo 2: Instalação das Dependências

```bash
pip install -r requirements.txt
```

## Passo 3: Configuração do .env

### 3.1 Copie o arquivo de exemplo
```bash
copy .env.example .env
```

### 3.2 Edite o arquivo .env
Abra o arquivo `.env` e preencha com suas informações:

```env
# Token do Discord (OBTENHA NO DISCORD DEVELOPER PORTAL)
DISCORD_TOKEN=seu_token_aqui

# Banco de dados (não precisa mudar se usar SQLite)
DATABASE_URL=sqlite:///data/gangue.db

# IDs do Discord (OBTENHA NO DISCORD COM MODO DESENVOLVEDOR)
CARGO_CUPULA_ID=123456789012345678
CANAL_LOGS_ID=123456789012345678
CANAL_COFRE_ID=123456789012345678
CANAL_BAU_ID=123456789012345678
CANAL_GERAL_ID=123456789012345678

# Intervalo de frases automáticas em minutos
INTERVALO_FRASES=30
```

## Passo 4: Obter as IDs do Discord

### 4.1 Ativar Modo Desenvolvedor no Discord
1. Vá em Configurações do Discord
2. Avançado → Modo Desenvolvedor (ative)

### 4.2 Obter ID do Cargo
1. Clique com botão direito no cargo "Alta Cúpula"
2. Copiar ID
3. Cole em `CARGO_CUPULA_ID`

### 4.3 Obter IDs dos Canais
1. Clique com botão direito em cada canal
2. Copiar ID
3. Cole nos campos respectivos:
   - Canal de logs → `CANAL_LOGS_ID`
   - Canal do cofre → `CANAL_COFRE_ID`
   - Canal do baú → `CANAL_BAU_ID`
   - Canal geral → `CANAL_GERAL_ID`

## Passo 5: Criar o Bot no Discord Developer Portal

### 5.1 Acesse o Discord Developer Portal
https://discord.com/developers/applications

### 5.2 Crie uma Aplicação
1. Clique em "New Application"
2. Dê um nome (ex: "Bot Gangue")
3. Clique em "Create"

### 5.3 Configure o Bot
1. Vá em "Bot" no menu lateral
2. Clique em "Add Bot"
3. Confirme clicando em "Yes, do it!"
4. Em "Privileged Gateway Intents", ative:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent

### 5.4 Copie o Token
1. Clique em "Reset Token" (ou "Copy Token" se já existir)
2. Copie o token gerado
3. Cole em `DISCORD_TOKEN` no arquivo `.env`

### 5.5 Convide o Bot para o Servidor
1. Vá em "OAuth2" → "URL Generator"
2. Scopes: Selecione `bot` e `applications.commands`
3. Bot Permissions: Selecione:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Application Commands
   - ✅ Read Messages/View Channels
4. Copie a URL gerada
5. Abra no navegador e selecione seu servidor
6. Autorize o bot

## Passo 6: Criar Canais no Discord

Crie os seguintes canais no seu servidor:

```
📋・logs-gangue          (privado - apenas Alta Cúpula)
💰・cofre                 (público - comandos do cofre)
📦・bau                   (público - comandos do baú)
💬・geral                 (público - frases automáticas)
```

### Importante:
- O canal `📋・logs-gangue` deve ser privado e acessível apenas pela Alta Cúpula
- Configure as permissões do canal para restringir acesso

## Passo 7: Executar o Bot

```bash
python bot.py
```

Se tudo estiver correto, você verá:
```
🚀 Iniciando bot...
📋 Prefixo: !
🔧 Intents: message_content=True, guilds=True, members=True
📦 Carregando extensões...
✅ commands.cofre carregado
✅ commands.bau carregado
✅ commands.config carregado
✅ commands.frase carregado
✅ commands.relatorio carregado
✅ Bot conectado como SeuBot (ID: 123456789012345678)
📊 Servidores: 1
📁 Inicializando banco de dados...
✅ Banco de dados inicializado
✅ Frases padrão verificadas
🔄 Sincronizando comandos slash...
✅ 20 comandos sincronizados
🔄 Task de frases automáticas iniciada (intervalo: 30 minutos)
```

## Passo 8: Testar o Bot

### 8.1 Teste comandos básicos
No Discord, digite `/` e veja os comandos disponíveis.

### 8.2 Teste depósito no cofre
Use `/cofre_deposito` com um valor pequeno para testar.

### 8.3 Verifique o canal de logs
Entre no canal `📋・logs-gangue` e veja se o log foi enviado.

## 🔧 Solução de Problemas Comuns

### Erro: "DISCORD_TOKEN não está definido"
- Verifique se criou o arquivo `.env`
- Verifique se o token está correto

### Erro: "Bot não tem permissão"
- Verifique se o bot foi convidado corretamente
- Verifique as permissões do bot no servidor

### Comandos não aparecem
- Espere alguns minutos após iniciar
- Verifique se as intents estão ativadas no Developer Portal
- Tente reiniciar o bot

### Erro de banco de dados
- Verifique se a pasta `data/` existe
- Verifique se o bot tem permissão de escrita

## 📝 Próximos Passos

1. Configure os canais corretamente usando `/config_canal_*`
2. Adicione frases personalizadas usando `/frase_adicionar`
3. Teste todos os comandos com valores pequenos
4. Ajuste o intervalo de frases se necessário
5. Treine os membros da gangue a usar os comandos

## 🆘 Precisa de Ajuda?

- Consulte o `README.md` para documentação completa
- Verifique os logs no console para identificar erros
- Use `/config_listar` para verificar configurações atuais
