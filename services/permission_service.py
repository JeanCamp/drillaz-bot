from typing import Optional
from discord import Member, Guild
from config import Config

class PermissionService:
    """Serviço para verificação de permissões"""
    
    @staticmethod
    def is_alta_cupula(member: Member) -> bool:
        """Verifica se o membro pertence à Alta Cúpula"""
        if not member or not member.guild:
            return False
        
        # Verifica se o membro tem o cargo de Alta Cúpula
        for role in member.roles:
            if role.id == Config.CARGO_CUPULA_ID:
                return True
        return False
    
    @staticmethod
    def can_view_cofre_saldo(member: Member) -> bool:
        """Verifica se pode ver o saldo do cofre (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def can_view_cofre_historico(member: Member) -> bool:
        """Verifica se pode ver o histórico completo do cofre (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def can_cofre_retirada(member: Member) -> bool:
        """Verifica se pode fazer retirada do cofre (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def can_cofre_ajuste(member: Member) -> bool:
        """Verifica se pode fazer ajuste administrativo no cofre (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def can_cofre_deposito(member: Member) -> bool:
        """Verifica se pode fazer depósito no cofre (todos os membros)"""
        return member is not None and member.guild is not None
    
    @staticmethod
    def can_view_bau_historico(member: Member) -> bool:
        """Verifica se pode ver o histórico completo do baú (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def can_bau_entrada(member: Member) -> bool:
        """Verifica se pode fazer entrada no baú (todos os membros)"""
        return member is not None and member.guild is not None
    
    @staticmethod
    def can_bau_retirada(member: Member) -> bool:
        """Verifica se pode fazer retirada do baú (todos os membros)"""
        return member is not None and member.guild is not None
    
    @staticmethod
    def can_config_bot(member: Member) -> bool:
        """Verifica se pode configurar o bot (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def can_view_relatorio(member: Member) -> bool:
        """Verifica se pode ver relatórios (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def can_manage_frases(member: Member) -> bool:
        """Verifica se pode gerenciar frases (apenas Alta Cúpula)"""
        return PermissionService.is_alta_cupula(member)
    
    @staticmethod
    def check_channel(channel_id: int, allowed_channel_id: int) -> bool:
        """Verifica se o comando está sendo usado no canal correto"""
        if allowed_channel_id == 0:
            return True  # Canal não configurado, permite qualquer canal
        return channel_id == allowed_channel_id
    
    @staticmethod
    def get_user_info(member: Member) -> dict:
        """Retorna informações do usuário para logging"""
        return {
            'user_id': str(member.id),
            'user_name': member.display_name,
            'user_mention': member.mention
        }
