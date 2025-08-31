from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from src.entities import Transaction

if TYPE_CHECKING:
    from src.entities import Account

class Deposit(Transaction):
    """
    Representa uma transação de depósito em uma conta bancária.
    
    Herda de Transaction e implementa a lógica específica para depósitos,
    incluindo validações e registro no extrato da conta.
    """
    
    def __init__(self, account: Account, value: Decimal):
        """
        Inicializa uma transação de depósito.
        
        Args:
            account (Account): A conta onde o depósito será realizado.
            value (Decimal): O valor a ser depositado.
        """
        super().__init__(account, value)
    
    def execute(self) -> bool:
        """
        Executa o depósito na conta.
        
        Returns:
            bool: True se o depósito foi realizado com sucesso, False caso contrário.
        """
        try:
            if self.value <= 0:
                raise ValueError("O valor é inválido para depósito")
            
            # Interface visual
            operation_info = 'Processando o depósito... Aguarde um momento!'
            print(operation_info, end='', flush=True)
            
            # Adiciona o valor ao saldo da conta
            self.account.add_balance(self.value)
            
            # Delay e limpeza de tela
            import time
            from src import clear_cmd_line
            PROCESSING_WAITING_TIME_IN_SECONDS = 2
            time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
            clear_cmd_line(len(operation_info))
            print("O valor foi depositado com sucesso!")
            
            # A transação será registrada pela classe Account
            from src import round_decimal
            DEFAULT_DECIMAL_PLACES = 2
            print(f"O seu saldo atual é de: R$ {round_decimal(self.account.balance, DEFAULT_DECIMAL_PLACES)}")
            
            return True
            
        except Exception as e:
            print(f"Erro ao realizar depósito: {e}")
            return False
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string do depósito.
        
        Returns:
            str: Descrição do depósito.
        """
        from src import round_decimal
        DEFAULT_DECIMAL_PLACES = 2
        return f"Depósito de R$ {round_decimal(self.value, DEFAULT_DECIMAL_PLACES)} na conta {self.account.account_number}"
