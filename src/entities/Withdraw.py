from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from src.entities import Transaction

if TYPE_CHECKING:
    from src.entities import Account

class Withdraw(Transaction):
    """
    Representa uma transação de saque em uma conta bancária.
    
    Herda de Transaction e implementa a lógica específica para saques,
    incluindo validações de saldo, limites e registro no extrato da conta.
    """
    
    def __init__(self, account: Account, value: Decimal):
        """
        Inicializa uma transação de saque.
        
        Args:
            account (Account): A conta onde o saque será realizado.
            value (Decimal): O valor a ser sacado.
        """
        super().__init__(account, value)
    
    def execute(self) -> bool:
        """
        Executa o saque na conta.
        
        Returns:
            bool: True se o saque foi realizado com sucesso, False caso contrário.
        """
        try:
            from src import round_decimal
            DEFAULT_DECIMAL_PLACES = 2
            LIMIT_PER_WITHDRAWLS = Decimal('500.00')
            MAX_WITHDRAWLS = 3
            
            # Validações específicas para saque
            if self.value <= 0:
                raise ValueError("O valor é inválido para saque")
            elif self.value > self.account.balance:
                raise ValueError(f"Saldo insuficiente... Seu saldo atual é de R$ {round_decimal(self.account.balance, DEFAULT_DECIMAL_PLACES)}")
            elif self.value > LIMIT_PER_WITHDRAWLS:
                raise ValueError(f"O valor do saque excede o limite de R$ {round_decimal(LIMIT_PER_WITHDRAWLS, DEFAULT_DECIMAL_PLACES)}")
            elif self.account.total_withdrawl >= MAX_WITHDRAWLS:
                raise ValueError(f"O total de saque excedeu o limite de {MAX_WITHDRAWLS} saques")
            
            # Interface visual
            operation_info = 'Processando o saque... Aguarde um momento!'
            print(operation_info, end='', flush=True)
            
            # Subtrai o valor do saldo da conta
            self.account.sub_balance(self.value)
            
            # Incrementa o contador de saques
            self.account.add_total_withdrawl()
            
            # Delay e limpeza de tela
            import time
            from src import clear_cmd_line
            PROCESSING_WAITING_TIME_IN_SECONDS = 2
            time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
            clear_cmd_line(len(operation_info))
            print("Saque realizado com sucesso!")
            
            # Registra a transação no extrato
            self.account.add_extract(f"Você sacou R$ {round_decimal(self.value, DEFAULT_DECIMAL_PLACES)}")
            print(f"O seu saldo atual é de: R$ {round_decimal(self.account.balance, DEFAULT_DECIMAL_PLACES)}")
            
            return True
            
        except Exception as e:
            print(f"Erro ao realizar saque: {e}")
            return False
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string do saque.
        
        Returns:
            str: Descrição do saque.
        """
        from src import round_decimal
        DEFAULT_DECIMAL_PLACES = 2
        return f"Saque de R$ {round_decimal(self.value, DEFAULT_DECIMAL_PLACES)} da conta {self.account.account_number}"
