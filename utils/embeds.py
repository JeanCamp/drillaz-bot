from discord import Embed, Color
from datetime import datetime
from utils.formatters import format_currency, format_datetime, format_number, get_emoji_tipo_cofre, get_emoji_tipo_bau, format_tipo_cofre, format_tipo_bau

class EmbedBuilder:
    """Construtor de embeds para o bot"""
    
    @staticmethod
    def create_cofre_log_embed(movimentacao, user_mention: str) -> Embed:
        """Cria embed para log de movimentação do cofre"""
        emoji = get_emoji_tipo_cofre(movimentacao.tipo)
        tipo_formatado = format_tipo_cofre(movimentacao.tipo)
        
        embed = Embed(
            title=f"{emoji} MOVIMENTAÇÃO NO COFRE",
            description=f"Tipo: {emoji} {tipo_formatado}",
            color=Color.gold() if movimentacao.tipo == 'deposito' else Color.red() if movimentacao.tipo == 'retirada' else Color.orange()
        )
        
        embed.add_field(name="💰 Valor", value=format_currency(movimentacao.valor), inline=True)
        embed.add_field(name="👤 Usuário", value=user_mention, inline=True)
        embed.add_field(name="🆔 ID", value=movimentacao.user_id, inline=True)
        embed.add_field(name="📝 Motivo", value=movimentacao.motivo or "Sem motivo", inline=False)
        embed.add_field(name="💵 Saldo Anterior", value=format_currency(movimentacao.saldo_anterior), inline=True)
        embed.add_field(name="💵 Saldo Posterior", value=format_currency(movimentacao.saldo_posterior), inline=True)
        embed.add_field(name="📅 Data", value=format_datetime(movimentacao.created_at), inline=False)
        
        embed.set_footer(text=f"ID da movimentação: {movimentacao.id}")
        embed.set_timestamp(datetime.now())
        
        return embed
    
    @staticmethod
    def create_bau_log_embed(movimentacao, user_mention: str) -> Embed:
        """Cria embed para log de movimentação do baú"""
        emoji = get_emoji_tipo_bau(movimentacao.tipo)
        tipo_formatado = format_tipo_bau(movimentacao.tipo)
        
        embed = Embed(
            title=f"{emoji} MOVIMENTAÇÃO NO BAÚ",
            description=f"Tipo: {emoji} {tipo_formatado}",
            color=Color.green() if movimentacao.tipo == 'entrada' else Color.red()
        )
        
        embed.add_field(name="📦 Item", value=movimentacao.item_nome, inline=True)
        embed.add_field(name="🔢 Quantidade", value=format_number(movimentacao.quantidade), inline=True)
        embed.add_field(name="👤 Usuário", value=user_mention, inline=True)
        embed.add_field(name="🆔 ID", value=movimentacao.user_id, inline=True)
        embed.add_field(name="📝 Motivo", value=movimentacao.motivo or "Sem motivo", inline=False)
        embed.add_field(name="📦 Estoque Anterior", value=format_number(movimentacao.estoque_anterior), inline=True)
        embed.add_field(name="📦 Estoque Posterior", value=format_number(movimentacao.estoque_posterior), inline=True)
        embed.add_field(name="📅 Data", value=format_datetime(movimentacao.created_at), inline=False)
        
        embed.set_footer(text=f"ID da movimentação: {movimentacao.id}")
        embed.set_timestamp(datetime.now())
        
        return embed
    
    @staticmethod
    def create_cofre_saldo_embed(saldo: float, ultima_movimentacao=None) -> Embed:
        """Cria embed para exibir saldo do cofre"""
        embed = Embed(
            title="💰 COFRE DA GANGUE",
            description="Saldo atual disponível",
            color=Color.gold()
        )
        
        embed.add_field(name="💵 Saldo Atual", value=format_currency(saldo), inline=False)
        
        if ultima_movimentacao:
            emoji = get_emoji_tipo_cofre(ultima_movimentacao.tipo)
            embed.add_field(
                name="📋 Última Movimentação",
                value=f"{emoji} {format_currency(ultima_movimentacao.valor)}\n"
                      f"Responsável: <@{ultima_movimentacao.user_id}>\n"
                      f"Motivo: {ultima_movimentacao.motivo or 'Sem motivo'}\n"
                      f"Data: {format_datetime(ultima_movimentacao.created_at)}",
                inline=False
            )
        
        embed.set_timestamp(datetime.now())
        
        return embed
    
    @staticmethod
    def create_cofre_historico_embed(movimentacoes, titulo: str = "💰 HISTÓRICO DO COFRE") -> Embed:
        """Cria embed para exibir histórico do cofre"""
        embed = Embed(
            title=titulo,
            description="Movimentações em ordem cronológica",
            color=Color.blue()
        )
        
        if not movimentacoes:
            embed.add_field(name="ℹ️", value="Nenhuma movimentação encontrada", inline=False)
            return embed
        
        for mov in movimentacoes[:10]:  # Limita a 10 movimentações
            emoji = get_emoji_tipo_cofre(mov.tipo)
            tipo_formatado = format_tipo_cofre(mov.tipo)
            
            field_value = (
                f"{emoji} {tipo_formatado}\n"
                f"Valor: {format_currency(mov.valor)}\n"
                f"Responsável: <@{mov.user_id}>\n"
                f"Motivo: {mov.motivo or 'Sem motivo'}\n"
                f"Data: {format_datetime(mov.created_at)}\n"
                f"Saldo após: {format_currency(mov.saldo_posterior)}"
            )
            
            embed.add_field(
                name=f"Movimentação #{mov.id}",
                value=field_value,
                inline=False
            )
        
        if len(movimentacoes) > 10:
            embed.set_footer(text=f"Mostrando 10 de {len(movimentacoes)} movimentações")
        
        embed.set_timestamp(datetime.now())
        
        return embed
    
    @staticmethod
    def create_bau_historico_embed(movimentacoes, titulo: str = "📦 HISTÓRICO DO BAÚ") -> Embed:
        """Cria embed para exibir histórico do baú"""
        embed = Embed(
            title=titulo,
            description="Movimentações em ordem cronológica",
            color=Color.blue()
        )
        
        if not movimentacoes:
            embed.add_field(name="ℹ️", value="Nenhuma movimentação encontrada", inline=False)
            return embed
        
        for mov in movimentacoes[:10]:  # Limita a 10 movimentações
            emoji = get_emoji_tipo_bau(mov.tipo)
            tipo_formatado = format_tipo_bau(mov.tipo)
            
            field_value = (
                f"{emoji} {tipo_formatado}\n"
                f"Item: {mov.item_nome}\n"
                f"Quantidade: {format_number(mov.quantidade)}\n"
                f"Responsável: <@{mov.user_id}>\n"
                f"Motivo: {mov.motivo or 'Sem motivo'}\n"
                f"Data: {format_datetime(mov.created_at)}\n"
                f"Estoque após: {format_number(mov.estoque_posterior)}"
            )
            
            embed.add_field(
                name=f"Movimentação #{mov.id}",
                value=field_value,
                inline=False
            )
        
        if len(movimentacoes) > 10:
            embed.set_footer(text=f"Mostrando 10 de {len(movimentacoes)} movimentações")
        
        embed.set_timestamp(datetime.now())
        
        return embed
    
    @staticmethod
    def create_bau_itens_embed(itens) -> Embed:
        """Cria embed para exibir itens do baú"""
        embed = Embed(
            title="📦 ITENS DO BAÚ",
            description="Estoque atual de todos os itens",
            color=Color.green()
        )
        
        if not itens:
            embed.add_field(name="ℹ️", value="Nenhum item cadastrado no baú", inline=False)
            return embed
        
        for item in itens[:25]:  # Limita a 25 itens
            embed.add_field(
                name=item.nome,
                value=f"Estoque: {format_number(item.estoque)}",
                inline=True
            )
        
        if len(itens) > 25:
            embed.set_footer(text=f"Mostrando 25 de {len(itens)} itens")
        
        embed.set_timestamp(datetime.now())
        
        return embed
    
    @staticmethod
    def create_success_embed(message: str) -> Embed:
        """Cria embed de sucesso"""
        return Embed(
            title="✅ Sucesso",
            description=message,
            color=Color.green()
        )
    
    @staticmethod
    def create_error_embed(message: str) -> Embed:
        """Cria embed de erro"""
        return Embed(
            title="❌ Erro",
            description=message,
            color=Color.red()
        )
    
    @staticmethod
    def create_warning_embed(message: str) -> Embed:
        """Cria embed de aviso"""
        return Embed(
            title="⚠️ Aviso",
            description=message,
            color=Color.orange()
        )
    
    @staticmethod
    def create_info_embed(message: str) -> Embed:
        """Cria embed de informação"""
        return Embed(
            title="ℹ️ Informação",
            description=message,
            color=Color.blue()
        )
    
    @staticmethod
    def create_confirmacao_embed(titulo: str, detalhes: dict) -> Embed:
        """Cria embed para confirmação de operação"""
        embed = Embed(
            title=f"⚠️ {titulo}",
            description="Confirme os dados abaixo:",
            color=Color.orange()
        )
        
        for key, value in detalhes.items():
            embed.add_field(name=key, value=str(value), inline=False)
        
        embed.set_footer(text="Clique em um botão para confirmar ou cancelar")
        embed.set_timestamp(datetime.now())
        
        return embed
    
    @staticmethod
    def create_relatorio_embed(dados: dict) -> Embed:
        """Cria embed para relatório geral"""
        embed = Embed(
            title="📊 RELATÓRIO DA GANGUE",
            description="Resumo das movimentações",
            color=Color.purple()
        )
        
        # Cofre
        embed.add_field(
            name="💰 COFRE",
            value=f"Total depositado: {format_currency(dados.get('cofre_depositado', 0))}\n"
                  f"Total retirado: {format_currency(dados.get('cofre_retirado', 0))}\n"
                  f"Saldo atual: {format_currency(dados.get('cofre_saldo', 0))}",
            inline=False
        )
        
        # Baú
        embed.add_field(
            name="📦 BAÚ",
            value=f"Total de entradas: {format_number(dados.get('bau_entradas', 0))}\n"
                  f"Total de retiradas: {format_number(dados.get('bau_retiradas', 0))}",
            inline=False
        )
        
        # Top usuários
        top_usuarios = dados.get('top_usuarios', [])
        if top_usuarios:
            top_text = "\n".join([
                f"{i+1}. {u['user_name']} - {u['quantidade']} movimentos"
                for i, u in enumerate(top_usuarios[:5])
            ])
            embed.add_field(name="👥 Top Usuários", value=top_text, inline=False)
        
        embed.set_timestamp(datetime.now())
        
        return embed
