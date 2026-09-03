from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

class Config(Base):
    """Configurações do bot"""
    __tablename__ = 'config'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Config(key='{self.key}', value='{self.value}')>"

class CofreMovimentacao(Base):
    """Movimentações do cofre (dinheiro)"""
    __tablename__ = 'cofre_movimentacoes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), nullable=False, index=True)
    user_name = Column(String(100), nullable=False)
    valor = Column(Float, nullable=False)
    tipo = Column(String(20), nullable=False)  # 'deposito', 'retirada', 'ajuste'
    tipo_dinheiro = Column(String(20), nullable=False, default='limpo')  # 'limpo' ou 'sujo'
    motivo = Column(Text, nullable=True)
    saldo_anterior = Column(Float, nullable=False)
    saldo_posterior = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<CofreMovimentacao(id={self.id}, tipo='{self.tipo}', tipo_dinheiro='{self.tipo_dinheiro}', valor={self.valor}, user='{self.user_name}')>"

class BauItem(Base):
    """Itens controlados pelo baú"""
    __tablename__ = 'bau_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), unique=True, nullable=False, index=True)
    estoque = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com movimentações
    movimentacoes = relationship("BauMovimentacao", back_populates="item")
    
    def __repr__(self):
        return f"<BauItem(id={self.id}, nome='{self.nome}', estoque={self.estoque})>"

class BauMovimentacao(Base):
    """Movimentações do baú (itens)"""
    __tablename__ = 'bau_movimentacoes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), nullable=False, index=True)
    user_name = Column(String(100), nullable=False)
    item_id = Column(Integer, ForeignKey('bau_items.id'), nullable=False)
    item_nome = Column(String(200), nullable=False)
    quantidade = Column(Integer, nullable=False)
    tipo = Column(String(20), nullable=False)  # 'entrada', 'retirada'
    motivo = Column(Text, nullable=True)
    estoque_anterior = Column(Integer, nullable=False)
    estoque_posterior = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # Relacionamento com item
    item = relationship("BauItem", back_populates="movimentacoes")
    
    def __repr__(self):
        return f"<BauMovimentacao(id={self.id}, tipo='{self.tipo}', item='{self.item_nome}', qtd={self.quantidade})>"

class Frase(Base):
    """Frases automáticas para o canal geral"""
    __tablename__ = 'frases'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    frase = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    ativa = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Frase(id={self.id}, frase='{self.frase[:50]}...', ativa={self.ativa})>"
