from datetime import datetime, timezone, timedelta
from typing import Optional

# Fuso horário brasileiro (UTC-3)
FUSO_BRASILEIRO = timezone(timedelta(hours=-3))

def format_currency(value: float) -> str:
    """Formata valor para moeda brasileira"""
    return f"R$ {value:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def format_datetime(dt: Optional[datetime]) -> str:
    """Formata datetime para padrão brasileiro com fuso horário correto"""
    if dt is None:
        return "N/A"
    
    # Se o datetime não tem timezone, assume UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Converte para fuso brasileiro
    dt_brasil = dt.astimezone(FUSO_BRASILEIRO)
    
    return dt_brasil.strftime("%d/%m/%Y %H:%M")

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
