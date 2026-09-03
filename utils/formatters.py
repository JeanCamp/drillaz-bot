from datetime import datetime
from typing import Optional

def format_currency(value: float) -> str:
    """Formata valor para moeda brasileira"""
    return f"R$ {value:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def format_datetime(dt: Optional[datetime]) -> str:
    """Formata datetime para padrão brasileiro"""
    if dt is None:
        return "N/A"
    return dt.strftime("%d/%m/%Y %H:%M")

def format_number(value: int) -> str:
    """Formata número com separadores de milhar"""
    return f"{value:,}".replace(',', '.')

def get_emoji_tipo_cofre(tipo: str) -> str:
    """Retorna emoji baseado no tipo de movimentação do cofre"""
    emojis = {
        'deposito': '🟢',
        'retirada': '🔴',
        'ajuste': '⚠️'
    }
    return emojis.get(tipo.lower(), '❓')

def get_emoji_tipo_bau(tipo: str) -> str:
    """Retorna emoji baseado no tipo de movimentação do baú"""
    emojis = {
        'entrada': '🟢',
        'retirada': '🔴'
    }
    return emojis.get(tipo.lower(), '❓')

def format_tipo_cofre(tipo: str) -> str:
    """Formata tipo de movimentação do cofre"""
    tipos = {
        'deposito': 'DEPÓSITO',
        'retirada': 'RETIRADA',
        'ajuste': 'AJUSTE ADMINISTRATIVO'
    }
    return tipos.get(tipo.lower(), tipo.upper())

def format_tipo_bau(tipo: str) -> str:
    """Formata tipo de movimentação do baú"""
    tipos = {
        'entrada': 'ENTRADA',
        'retirada': 'RETIRADA'
    }
    return tipos.get(tipo.lower(), tipo.upper())
