from __future__ import annotations

from decimal import Decimal
import time
from typing import TYPE_CHECKING

from src import round_decimal, clear_cmd_line
from src.entities import Account, AccountNumber, AgencyNumber

if TYPE_CHECKING:
    from src.entities import Client

LIMIT_PER_WITHDRAWLS = Decimal('500.00')
MAX_WITHDRAWLS = 3
DEFAULT_DECIMAL_PLACES = 2
PROCESSING_WAITING_TIME_IN_SECONDS = 2

class CheckingAccount(Account):
    """
    Representa uma conta corrente, com restrições específicas de saque.

    Herda de Account e aplica limites como valor máximo de saque e número de saques permitidos.
    """

    def __init__(self, account_number: AccountNumber, agency_number: AgencyNumber, client: Client):
        """
        Inicializa uma conta corrente com número da conta, número da agência e cliente.

        Args:
            account_number (AccountNumber): Número da conta.
            agency_number (AgencyNumber): Número da agência.
            client (Client): Cliente associado à conta.
        """
        super().__init__(account_number, agency_number, client)

    def withdraw(self, value: Decimal) -> Decimal:
        """
        Realiza um saque com verificação de saldo, limite de valor e limite de quantidade de saques.

        Args:
            value (Decimal): Valor a ser sacado.

        Raises:
            ValueError: Caso o valor seja inválido, saldo insuficiente, ultrapasse o limite de saque
                        ou o número máximo de saques permitido.

        Returns:
            Decimal: Valor sacado, se bem-sucedido.
        """
        if value <= 0:
            raise ValueError("O valor é inválido para saque")
        elif value > self.balance:
            raise ValueError(f"Saldo insuficiente... Seu saldo atual é de R$ {round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}")
        elif value > LIMIT_PER_WITHDRAWLS:
            raise ValueError(f"O valor do saque excede o limite de R$ {round_decimal(LIMIT_PER_WITHDRAWLS, DEFAULT_DECIMAL_PLACES)}")
        elif self.total_withdrawl >= MAX_WITHDRAWLS:
            raise ValueError(f"O total de saque excedeu o limite de {MAX_WITHDRAWLS} saques")
        
        operation_info = 'Processando o saque... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        self.sub_balance(value)
        self.add_total_withdrawl()
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        clear_cmd_line(len(operation_info))
        print("Saque realizado com sucesso!")
        self.add_extract(f"Você sacou R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)}")
        print(f"O seu saldo atual é de: R$ {round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}")
        return value
