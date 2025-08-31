from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from src.entities import Transaction
from src.decorators import transaction_logger

if TYPE_CHECKING:
    from src.entities import Account

class Transfer(Transaction):
    """
    Representa uma transação de transferência entre contas bancárias.
    
    Herda de Transaction e implementa a lógica específica para transferências,
    incluindo validações e registro no extrato de ambas as contas.
    """
    
    def __init__(self, source_account: Account, destination_account: Account, value: Decimal):
        """
        Inicializa uma transação de transferência.
        
        Args:
            source_account (Account): A conta de origem (que envia o dinheiro).
            destination_account (Account): A conta de destino (que recebe o dinheiro).
            value (Decimal): O valor a ser transferido.
        """
        super().__init__(source_account, value)
        self._destination_account: Account = destination_account
    
    @property
    def destination_account(self) -> Account:
        """Retorna a conta de destino da transferência."""
        return self._destination_account
    
    @transaction_logger
    def execute(self) -> bool:
        """
        Executa a transferência entre as contas.
        
        Returns:
            bool: True se a transferência foi realizada com sucesso, False caso contrário.
        """
        try:
            from src import round_decimal, clear_cmd_line
            DEFAULT_DECIMAL_PLACES = 2
            PROCESSING_WAITING_TIME_IN_SECONDS = 2
            
            # Validações específicas para transferência
            if self.value <= 0:
                raise ValueError("O valor é inválido para transferir")
            elif self.value > self.account.balance:
                raise ValueError(f"Saldo insuficiente... Seu saldo atual é de R$ {round_decimal(self.account.balance, DEFAULT_DECIMAL_PLACES)}")
            elif self.account == self.destination_account:
                raise ValueError("Não é possível transferir para a mesma conta")
            
            # Interface visual
            operation_info = 'Processando a transferência... Aguarde um momento!'
            print(operation_info, end='', flush=True)
            
            # Executa a transferência
            self.account.sub_balance(self.value)
            self.destination_account.add_balance(self.value)
            
            # Delay e limpeza de tela
            import time
            time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
            clear_cmd_line(len(operation_info))
            print("Transferência realizada com sucesso!")
            
            # As transações serão registradas pelas classes Account
            # A transação de origem será registrada quando o método transfer() da Account for chamado
            # A transação de destino será registrada aqui
            self.destination_account.add_transaction(self)
            
            print(f"O seu saldo atual é de: R$ {round_decimal(self.account.balance, DEFAULT_DECIMAL_PLACES)}")
            
            return True
            
        except Exception as e:
            print(f"Erro ao realizar transferência: {e}")
            return False
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string da transferência.
        
        Returns:
            str: Descrição da transferência.
        """
        from src import round_decimal
        DEFAULT_DECIMAL_PLACES = 2
        return f"Transferência de R$ {round_decimal(self.value, DEFAULT_DECIMAL_PLACES)} da conta {self.account.account_number} para {self.destination_account.account_number}"
    
    def get_description_for_account(self, account: Account) -> str:
        """
        Retorna a descrição da transferência específica para uma conta.
        
        Args:
            account (Account): A conta para a qual gerar a descrição.
            
        Returns:
            str: Descrição da transferência do ponto de vista da conta especificada.
        """
        from src import round_decimal
        DEFAULT_DECIMAL_PLACES = 2
        
        if account == self.account:
            # Conta de origem
            return f"Você transferiu R$ {round_decimal(self.value, DEFAULT_DECIMAL_PLACES)} para {self.destination_account.client.name} (CPF: {self.destination_account.client.cpf} / Conta: {self.destination_account.account_number} / Agência: {self.destination_account.agency_number})"
        elif account == self.destination_account:
            # Conta de destino
            return f"Você recebeu R$ {round_decimal(self.value, DEFAULT_DECIMAL_PLACES)} de {self.account.client.name} (CPF: {self.account.client.cpf} / Conta: {self.account.account_number} / Agência: {self.account.agency_number})"
        else:
            return str(self)
