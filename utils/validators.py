from typing import Optional, Tuple
import re

class ValidationError(Exception):
    """Exceção para erros de validação"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class Validators:
    """Validadores de entrada"""
    
    @staticmethod
    def validate_valor(valor: float) -> float:
        """Valida se o valor é positivo e válido"""
        if valor is None:
            raise ValidationError("O valor não pode ser nulo")
        
        if valor <= 0:
            raise ValidationError("O valor deve ser maior que zero")
        
        if valor > 1_000_000_000:  # Limite de 1 bilhão
            raise ValidationError("O valor excede o limite máximo permitido")
        
        return valor
    
    @staticmethod
    def validate_quantidade(quantidade: int) -> int:
        """Valida se a quantidade é positiva e válida"""
        if quantidade is None:
            raise ValidationError("A quantidade não pode ser nula")
        
        if quantidade <= 0:
            raise ValidationError("A quantidade deve ser maior que zero")
        
        if quantidade > 1_000_000:  # Limite de 1 milhão
            raise ValidationError("A quantidade excede o limite máximo permitido")
        
        return quantidade
    
    @staticmethod
    def validate_motivo(motivo: Optional[str]) -> str:
        """Valida o motivo da operação"""
        if motivo is None or motivo.strip() == "":
            return "Sem motivo informado"
        
        if len(motivo) > 500:
            raise ValidationError("O motivo deve ter no máximo 500 caracteres")
        
        return motivo.strip()
    
    @staticmethod
    def validate_item_nome(nome: str) -> str:
        """Valida o nome do item"""
        if not nome or nome.strip() == "":
            raise ValidationError("O nome do item não pode ser vazio")
        
        nome = nome.strip()
        
        if len(nome) > 200:
            raise ValidationError("O nome do item deve ter no máximo 200 caracteres")
        
        return nome
    
    @staticmethod
    def validate_intervalo(intervalo: int) -> int:
        """Valida o intervalo de frases automáticas"""
        if intervalo < 1:
            raise ValidationError("O intervalo deve ser de pelo menos 1 minuto")
        
        if intervalo > 1440:  # 24 horas
            raise ValidationError("O intervalo não pode exceder 24 horas")
        
        return intervalo
    
    @staticmethod
    def validate_frase(frase: str) -> str:
        """Valida a frase automática"""
        if not frase or frase.strip() == "":
            raise ValidationError("A frase não pode ser vazia")
        
        frase = frase.strip()
        
        if len(frase) > 1000:
            raise ValidationError("A frase deve ter no máximo 1000 caracteres")
        
        return frase
    
    @staticmethod
    def validate_saldo_suficiente(saldo_atual: float, valor_solicitado: float) -> bool:
        """Valida se há saldo suficiente para a operação"""
        return saldo_atual >= valor_solicitado
    
    @staticmethod
    def validate_estoque_suficiente(estoque_atual: int, quantidade_solicitada: int) -> bool:
        """Valida se há estoque suficiente para a operação"""
        return estoque_atual >= quantidade_solicitada
    
    @staticmethod
    def parse_valor(valor_str: str) -> float:
        """Converte string para float, tratando formatos brasileiros"""
        try:
            # Remove caracteres não numéricos exceto vírgula e ponto
            cleaned = re.sub(r'[^\d.,-]', '', valor_str)
            
            if not cleaned:
                raise ValidationError("Valor inválido")
            
            # Substitui vírgula por ponto se for formato brasileiro
            if ',' in cleaned and '.' not in cleaned:
                cleaned = cleaned.replace(',', '.')
            elif ',' in cleaned and '.' in cleaned:
                # Se tiver ambos, assume que vírgula é decimal e ponto é milhar
                cleaned = cleaned.replace('.', '').replace(',', '.')
            
            valor = float(cleaned)
            return Validators.validate_valor(valor)
            
        except ValueError:
            raise ValidationError("Valor inválido. Use o formato: 1000 ou 1.000,00")
    
    @staticmethod
    def parse_quantidade(qtd_str: str) -> int:
        """Converte string para int"""
        try:
            quantidade = int(qtd_str)
            return Validators.validate_quantidade(quantidade)
        except ValueError:
            raise ValidationError("Quantidade inválida. Deve ser um número inteiro positivo")
