from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
import time
from typing import List, TYPE_CHECKING

from src import round_decimal, clear_cmd_line
from src.entities import AccountNumber, AgencyNumber

if TYPE_CHECKING:
    from src.entities import Client

LIMIT_PER_WITHDRAWLS = Decimal('500.00')
MAX_WITHDRAWLS = 3
DEFAULT_DECIMAL_PLACES = 2
PROCESSING_WAITING_TIME_IN_SECONDS = 2

class Account:
    """
    Classe que representa uma conta bancária.

    Fornece métodos para operações comuns como depósito, saque, transferência,
    geração de extrato e manipulação de saldo.
    """

    def __init__(self, account_number: AccountNumber, agency_number: AgencyNumber, client: Client):
        """
        Inicializa uma nova conta com saldo zero e extrato vazio.

        Args:
            account_number (AccountNumber): Número da conta.
            agency_number (AgencyNumber): Número da agência.
            client (Client): Cliente associado à conta.
        """
        self._account_number: AccountNumber = None
        self._agency_number: AgencyNumber = None
        self._client: Client = None
        self._balance: Decimal = None
        self._extract: List[str] = None
        self._total_withdrawl: int = None

        self.account_number = account_number
        self.agency_number = agency_number
        self.client = client
        self.balance = Decimal('0')
        self.extract = []
        self.total_withdrawl = 0

    @property
    def account_number(self) -> AccountNumber:
        """Retorna o número da conta."""
        return self._account_number

    @account_number.setter
    def account_number(self, account_number: AccountNumber):
        self._account_number = account_number

    @property
    def agency_number(self) -> AgencyNumber:
        """Retorna o número da agência."""
        return self._agency_number

    @agency_number.setter
    def agency_number(self, agency_number: AgencyNumber):
        self._agency_number = agency_number

    @property
    def client(self) -> Client:
        """Retorna o cliente associado à conta."""
        return self._client

    @client.setter
    def client(self, client: Client):
        self._client = client

    @property
    def balance(self) -> Decimal:
        """Retorna o saldo atual da conta."""
        return self._balance

    @balance.setter
    def balance(self, balance: Decimal):
        self._balance = balance

    @property
    def extract(self) -> List[str]:
        """Retorna o extrato da conta."""
        return self._extract

    @extract.setter
    def extract(self, extract: List[str]):
        self._extract = extract

    @property
    def total_withdrawl(self) -> int:
        """Retorna o total de saques realizados."""
        return self._total_withdrawl

    @total_withdrawl.setter
    def total_withdrawl(self, total_withdrawl: int):
        self._total_withdrawl = total_withdrawl

    def add_extract(self, message: str):
        """
        Adiciona uma entrada ao extrato com a data e saldo atual.

        Args:
            message (str): Mensagem descritiva da operação.
        """
        date_now_string = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        full_message = (f"{message} => Saldo após operação R$ "
                        f"{round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}"
                        f" - Realizado em {date_now_string}\n")
        self.extract.append(full_message)

    def generate_extract_information_text(self) -> str:
        """
        Gera uma string com todas as operações registradas no extrato.

        Returns:
            str: Texto formatado do extrato bancário.
        """
        if not self.extract:
            return "Extrato Bancário:\n\n-- Nenhuma movimentação --"
        return "Extrato Bancário:\n\n" + "".join(self.extract)

    def generate_account_information_text(self) -> str:
        """
        Gera uma string com as informações da conta e seu extrato.

        Returns:
            str: Informações formatadas da conta.
        """
        text = f"Número da conta: {str(self.account_number)}\n"
        text += f"Número da agência: {self.agency_number}\n"
        text += f"O saldo de sua conta é R$ {round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}\n"
        text += self.generate_extract_information_text()
        return text

    def add_balance(self, value: Decimal):
        """Adiciona um valor ao saldo da conta."""
        self.balance += value

    def sub_balance(self, value: Decimal):
        """Subtrai um valor do saldo da conta."""
        self.add_balance(-value)

    def add_total_withdrawl(self, total: int = 1):
        """Incrementa o total de saques realizados."""
        self.total_withdrawl += total

    def withdraw(self, value: Decimal) -> Decimal:
        """
        Realiza um saque usando a classe Withdraw.

        Args:
            value (Decimal): Valor a ser sacado.

        Raises:
            ValueError: Caso o valor seja inválido, saldo insuficiente, ultrapasse o limite de saque
                        ou o número máximo de saques permitido.

        Returns:
            Decimal: Valor sacado, se bem-sucedido.
        """
        from src.entities import Withdraw
        withdraw_transaction = Withdraw(self, value)
        success = withdraw_transaction.execute()
        if not success:
            raise ValueError("Falha ao realizar saque")
        return value

    def deposit(self, value: Decimal):
        """
        Realiza um depósito na conta usando a classe Deposit.

        Args:
            value (Decimal): Valor a ser depositado.

        Raises:
            ValueError: Se o valor for menor ou igual a zero.
        """
        from src.entities import Deposit
        deposit_transaction = Deposit(self, value)
        success = deposit_transaction.execute()
        if not success:
            raise ValueError("Falha ao realizar depósito")

    def transfer(self, value: Decimal, account_of_receipt: 'Account') -> bool:
        """
        Realiza uma transferência entre contas.

        Args:
            value (Decimal): Valor a ser transferido.
            account_of_receipt (Account): Conta destino.

        Returns:
            bool: True se bem-sucedido.

        Raises:
            ValueError: Em caso de valor inválido, saldo insuficiente ou contas iguais.
        """
        if value <= 0:
            raise ValueError("O valor é inválido para transferir")
        if value > self.balance:
            raise ValueError("O valor é maior que o saldo de sua conta")
        if self == account_of_receipt:
            raise ValueError("Não é possível transferir para a mesma conta")

        operation_info = 'Processando a transferência... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        self.sub_balance(value)
        account_of_receipt.add_balance(value)
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        clear_cmd_line(len(operation_info))
        self.add_extract(f"Você transferiu um valor de R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)} para o cliente {account_of_receipt.client.name} (CPF: {account_of_receipt.client.cpf} / Número da Conta: {account_of_receipt.account_number} / Agência: {account_of_receipt.agency_number})")
        account_of_receipt.add_extract(f"Você recebeu um valor de R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)} do cliente {self.client.name} (CPF: {self.client.cpf} / Número da Conta: {self.account_number} / Agência: {self.agency_number})")
        print(f"O seu saldo atual é de: R$ {round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}")
        return True

    def show_extract(self):
        """Exibe o extrato formatado no terminal."""
        print("="*50)
        print(self.generate_extract_information_text())

    def __eq__(self, value: 'Account') -> bool:
        """
        Compara duas contas pela combinação de número e agência.

        Args:
            value (Account): Conta a ser comparada.

        Returns:
            bool: True se forem a mesma conta.
        """
        return self.account_number == value.account_number and self.agency_number == value.agency_number

    def __str__(self) -> str:
        """
        Retorna a representação textual da conta com extrato.

        Returns:
            str: Informações completas da conta.
        """
        return self.generate_account_information_text()
