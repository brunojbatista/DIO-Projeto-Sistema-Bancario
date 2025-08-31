from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities import Account

class Transaction(ABC):
    """
    Classe abstrata que representa uma transação bancária.
    
    Define a interface comum para todas as transações (depósito, saque, etc.)
    que podem ser realizadas em uma conta bancária.
    """
    
    def __init__(self, account: Account, value: Decimal):
        """
        Inicializa uma transação com uma conta e um valor.
        
        Args:
            account (Account): A conta onde a transação será realizada.
            value (Decimal): O valor da transação.
        """
        self._account: Account = account
        self._value: Decimal = value
    
    @property
    def account(self) -> Account:
        """Retorna a conta associada à transação."""
        return self._account
    
    @property
    def value(self) -> Decimal:
        """Retorna o valor da transação."""
        return self._value
    
    @abstractmethod
    def execute(self) -> bool:
        """
        Executa a transação na conta.
        
        Returns:
            bool: True se a transação foi executada com sucesso, False caso contrário.
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """
        Retorna uma representação em string da transação.
        
        Returns:
            str: Descrição da transação.
        """
        pass
