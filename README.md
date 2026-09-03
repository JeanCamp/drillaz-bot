# 🤖 Bot de Gestão de Gangue - GTA RP

Bot completo para Discord desenvolvido em Python usando discord.py para gerenciar os recursos de uma gangue em servidores de GTA RP. O sistema controla o cofre (dinheiro) e o baú (itens) com registro completo de todas as movimentações.

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Comandos](#comandos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Migração para PostgreSQL](#migração-para-postgresql)
- [Segurança](#segurança)
- [Solução de Problemas](#solução-de-problemas)

## ✨ Funcionalidades

### 💰 Sistema de Cofre
- **Depósitos**: Membros podem registrar depósitos no cofre
- **Retiradas**: Apenas Alta Cúpula pode fazer retiradas
- **Saldo**: Apenas Alta Cúpula pode consultar o saldo total
- **Histórico**: Registro completo de todas as movimentações
- **Ajustes**: Ajustes administrativos com confirmação
- **Filtros**: Histórico por usuário, tipo e período

### 📦 Sistema de Baú
- **Entradas**: Membros podem registrar entrada de itens
- **Retiradas**: Membros podem retirar itens (com verificação de estoque)
- **Estoque**: Consulta de estoque por item
- **Histórico**: Registro completo de movimentações
- **Itens**: Lista completa de itens e seus estoques

### 🔐 Sistema de Permissões
- **Alta Cúpula**: Acesso total ao sistema
- **Membros**: Acesso limitado (depósitos, entradas/saídas, próprio histórico)
- **Verificação por ID de cargo** (não por nome)
- **Verificação por canal específico**

### 📊 Sistema de Relatórios
- **Relatório Geral**: Visão completa do sistema
- **Relatório do Cofre**: Detalhes financeiros
- **Relatório do Baú**: Detalhes de itens
- **Relatório por Usuário**: Movimentações individuais
- **Top Usuários**: Ranking de movimentações
- **Top Itens**: Itens mais movimentados

### 💬 Sistema de Frases Automáticas
- **Frases configuráveis**: Adicione suas próprias frases
- **Intervalo ajustável**: Configure o tempo entre frases
- **Ativação/Desativação**: Controle quais frases são usadas
- **Envio automático**: Task em background envia frases periodicamente

### 📋 Sistema de Logs
- **Canal exclusivo**: Logs enviados para canal dedicado
- **Embeds detalhados**: Informações completas de cada operação
- **Registro permanente**: Todas as movimentações são registradas
- **Acesso restrito**: Apenas Alta Cúpula tem acesso

## 📦 Requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Discord Developer Portal
- Token do bot

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
cd "C:\Users\Jean\Desktop\PROJETO SITE\MEU DUO"
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o arquivo .env

Copie o arquivo `.env.example` para `.env`:

```bash
copy .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Discord Bot Token
DISCORD_TOKEN=seu_token_aqui

# Database
DATABASE_URL=sqlite:///data/gangue.db

# Discord IDs
CARGO_CUPULA_ID=123456789012345678
CANAL_LOGS_ID=123456789012345678
CANAL_COFRE_ID=123456789012345678
CANAL_BAU_ID=123456789012345678
CANAL_GERAL_ID=123456789012345678

# Frases automáticas
INTERVALO_FRASES=30
```

## ⚙️ Configuração

### 1. Obter o Token do Bot

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação ou selecione uma existente
3. Vá em "Bot" → "Reset Token" para gerar um novo token
4. Copie o token e cole no `.env` em `DISCORD_TOKEN`

### 2. Obter IDs do Discord

#### ID do Cargo de Alta Cúpula:
1. No Discord, ative o modo desenvolvedor (Configurações → Avançado → Modo Desenvolvedor)
2. Clique com o botão direito no cargo
3. Selecione "Copiar ID"
4. Cole em `CARGO_CUPULA_ID`

#### IDs dos Canais:
1. Com o modo desenvolvedor ativado
2. Clique com o botão direito no canal
3. Selecione "Copiar ID"
4. Cole nos respectivos campos:
   - `CANAL_LOGS_ID`: Canal exclusivo para logs
   - `CANAL_COFRE_ID`: Canal para comandos do cofre
   - `CANAL_BAU_ID`: Canal para comandos do baú
   - `CANAL_GERAL_ID`: Canal para frases automáticas

### 3. Convidar o Bot para o Servidor

1. No Discord Developer Portal, vá em "OAuth2" → "URL Generator"
2. Selecione os scopes:
   - `bot`
   - `applications.commands`
3. Selecione os bot permissions:
   - `Send Messages`
   - `Embed Links`
   - `Read Message History`
   - `Use Application Commands`
   - `Read Messages/View Channels`
4. Copie a URL gerada e abra no navegador
5. Selecione o servidor e autorize o bot

### 4. Estrutura de Canais Recomendada

```
📋・logs-gangue          (privado - Alta Cúpula)
💰・cofre                 (comandos do cofre)
📦・bau                   (comandos do baú)
💬・geral                 (frases automáticas)
```

## 🎮 Comandos

### Sistema de Cofre

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/cofre_deposito` | Registra um depósito no cofre | Todos |
| `/cofre_retirada` | Registra uma retirada do cofre | Alta Cúpula |
| `/cofre_saldo` | Consulta o saldo atual do cofre | Alta Cúpula |
| `/cofre_historico` | Consulta o histórico do cofre | Alta Cúpula (próprio para membros) |
| `/cofre_ajuste` | Ajuste administrativo do saldo | Alta Cúpula |

### Sistema de Baú

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/bau_entrada` | Registra entrada de item no baú | Todos |
| `/bau_retirada` | Registra retirada de item do baú | Todos |
| `/bau_itens` | Lista todos os itens do baú | Todos |
| `/bau_historico` | Consulta o histórico do baú | Alta Cúpula (próprio para membros) |
| `/bau_estoque` | Consulta estoque de um item específico | Todos |

### Sistema de Configuração

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/config_cargo_cupula` | Define o cargo de Alta Cúpula | Alta Cúpula |
| `/config_canal_logs` | Define o canal de logs | Alta Cúpula |
| `/config_canal_cofre` | Define o canal do cofre | Alta Cúpula |
| `/config_canal_bau` | Define o canal do baú | Alta Cúpula |
| `/config_canal_geral` | Define o canal geral | Alta Cúpula |
| `/config_intervalo_frases` | Define intervalo das frases automáticas | Alta Cúpula |
| `/config_listar` | Lista todas as configurações | Alta Cúpula |

### Sistema de Frases

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/frase_adicionar` | Adiciona uma nova frase | Alta Cúpula |
| `/frase_remover` | Remove uma frase | Alta Cúpula |
| `/frase_listar` | Lista todas as frases | Alta Cúpula |
| `/frase_ativar` | Ativa uma frase | Alta Cúpula |
| `/frase_desativar` | Desativa uma frase | Alta Cúpula |
| `/frase_testar` | Envia uma frase aleatória para teste | Alta Cúpula |

### Sistema de Relatórios

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/relatorio` | Gera relatório geral da gangue | Alta Cúpula |
| `/relatorio_cofre` | Gera relatório do cofre | Alta Cúpula |
| `/relatorio_bau` | Gera relatório do baú | Alta Cúpula |
| `/relatorio_usuario` | Gera relatório de um usuário | Alta Cúpula (próprio para membros) |

## 📁 Estrutura do Projeto

```
bot-gangue/
├── .env                          # Variáveis de ambiente
├── .env.example                  # Exemplo de configuração
├── .gitignore                    # Arquivos ignorados pelo git
├── requirements.txt              # Dependências Python
├── README.md                     # Documentação
├── bot.py                        # Ponto de entrada do bot
├── config.py                     # Configurações gerais
│
├── database/                     # Camada de dados
│   ├── __init__.py
│   ├── connection.py            # Conexão com banco de dados
│   └── models.py                # Modelos ORM (SQLAlchemy)
│
├── commands/                     # Comandos Slash
│   ├── __init__.py
│   ├── cofre.py                 # Comandos do cofre
│   ├── bau.py                   # Comandos do baú
│   ├── config.py                # Comandos de configuração
│   ├── frase.py                 # Comandos de frases
│   └── relatorio.py             # Comandos de relatórios
│
├── events/                       # Eventos do Discord
│   ├── __init__.py
│   └── on_ready.py              # Evento de inicialização
│
├── services/                     # Lógica de negócio
│   ├── __init__.py
│   ├── cofre_service.py         # Serviço do cofre
│   ├── bau_service.py           # Serviço do baú
│   ├── log_service.py           # Serviço de logs
│   ├── frase_service.py         # Serviço de frases
│   ├── permission_service.py    # Verificação de permissões
│   ├── config_service.py        # Serviço de configurações
│   └── relatorio_service.py     # Serviço de relatórios
│
├── utils/                        # Utilitários
│   ├── __init__.py
│   ├── embeds.py                # Embeds formatados
│   ├── validators.py            # Validações de entrada
│   └── formatters.py            # Formatação de dados
│
└── data/                         # Dados persistentes
    └── gangue.db                # Banco SQLite inicial
```

## 🗄️ Migração para PostgreSQL

O projeto está preparado para migração de SQLite para PostgreSQL. Para fazer a migração:

### 1. Instale o driver PostgreSQL

```bash
pip install asyncpg
```

### 2. Altere a DATABASE_URL no .env

```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco
```

### 3. Crie o banco de dados PostgreSQL

```sql
CREATE DATABASE gangue;
```

### 4. O SQLAlchemy criará as tabelas automaticamente

Na primeira execução, o SQLAlchemy criará todas as tabelas necessárias no PostgreSQL.

## 🔒 Segurança

### Boas Práticas

1. **Nunca compartilhe o token do bot**: O token dá controle total sobre o bot
2. **Use variáveis de ambiente**: Nunca coloque senhas/tokens no código
3. **Limitar permissões do bot**: Dê apenas as permissões necessárias
4. **Canal de logs privado**: O canal de logs deve ser acessível apenas pela Alta Cúpula
5. **Backup regular**: Faça backup do arquivo `data/gangue.db` regularmente

### Validações Implementadas

- ✅ Valores negativos bloqueados
- ✅ Valores zero bloqueados
- ✅ Verificação de saldo suficiente
- ✅ Verificação de estoque suficiente
- ✅ Validação de formato de entrada
- ✅ Verificação de permissões em todas as operações
- ✅ Confirmação para operações sensíveis
- ✅ Verificação de canal específico

## 🛠️ Solução de Problemas

### Bot não conecta

1. Verifique se o token está correto no `.env`
2. Verifique se o bot foi convidado para o servidor
3. Verifique se as intents estão ativadas no Developer Portal

### Comandos não aparecem

1. Espere alguns minutos após iniciar o bot (sincronização de comandos)
2. Verifique se o bot tem permissão de "Use Application Commands"
3. Tente reiniciar o bot

### Erro de permissão

1. Verifique se o ID do cargo está correto no `.env`
2. Verifique se o usuário tem o cargo correto
3. Verifique se o canal está configurado corretamente

### Erro de banco de dados

1. Verifique se a pasta `data/` existe
2. Verifique se o bot tem permissão de escrita na pasta
3. Se usar PostgreSQL, verifique a conexão

### Frases automáticas não funcionam

1. Verifique se `CANAL_GERAL_ID` está configurado
2. Verifique se `INTERVALO_FRASES` é maior que 0
3. Verifique se existem frases ativas no banco
4. Use `/frase_testar` para testar manualmente

## 🚀 Execução

### Iniciar o bot

```bash
python bot.py
```

### Parar o bot

Pressione `Ctrl+C` no terminal

## 📝 Notas Importantes

- O bot usa SQLite por padrão, mas está preparado para PostgreSQL
- Todas as movimentações são registradas permanentemente
- O saldo pode ser reconstruído a partir do histórico
- O sistema de logs é extremamente detalhado
- As permissões são verificadas por ID, não por nome
- Valores monetários são formatados no padrão brasileiro (R$)
- Datas são formatadas no padrão brasileiro (dd/mm/yyyy HH:MM)

## 🤝 Suporte

Para suporte ou dúvidas, consulte a documentação ou entre em contato com o desenvolvedor.

## 📄 Licença

Este projeto foi desenvolvido para uso em servidores de GTA RP e está disponível para modificação e uso conforme necessário.
