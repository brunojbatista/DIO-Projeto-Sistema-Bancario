from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
import time
from typing import List, TYPE_CHECKING

from src.Utils import round_decimal, clear_cmd_line
from src.entities.AccountNumber import AccountNumber
from src.entities.AgencyNumber import AgencyNumber

if TYPE_CHECKING:
    from src.entities.Client import Client


LIMIT_PER_WITHDRAWLS = Decimal('500.00')
MAX_WITHDRAWLS = 3
DEFAULT_DECIMAL_PLACES = 2
# TOTAL_DIGITS_ACCOUNT_NUMBER = 8
# TOTAL_DIGITS_AGENCY_NUMBER = 4
PROCESSING_WAITING_TIME_IN_SECONDS = 2

class Account(ABC):
    def __init__(self, account_number: AccountNumber, agency_number: AgencyNumber, client: Client):
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
        return self._account_number

    @account_number.setter
    def account_number(self, account_number: AccountNumber):
        self._account_number = account_number

    @property
    def agency_number(self) -> AgencyNumber:
        return self._agency_number

    @agency_number.setter
    def agency_number(self, agency_number: AgencyNumber):
        self._agency_number = agency_number

    @property
    def client(self) -> Client:
        return self._client

    @client.setter
    def client(self, client: Client):
        self._client = client

    @property
    def balance(self) -> Decimal:
        return self._balance

    @balance.setter
    def balance(self, balance: Decimal):
        self._balance = balance

    @property
    def extract(self) -> List[str]:
        return self._extract

    @extract.setter
    def extract(self, extract: List[str]):
        self._extract = extract

    @property
    def total_withdrawl(self) -> int:
        return self._total_withdrawl

    @total_withdrawl.setter
    def total_withdrawl(self, total_withdrawl: int):
        self._total_withdrawl = total_withdrawl

    def add_extract(self, message: str):
        date_now_string = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        full_message = (f"{message} => Saldo após operação R$ "
                        f"{round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}"
                        f" - Realizado em {date_now_string}\n")
        self.extract.append(full_message)

    def generate_extract_information_text(self):
        text = ""
        if not self.extract:
            text += "Extrato Bancário:\n\n-- Nenhuma movimentação --"
        else:
            text += "Extrato Bancário:\n\n" + "".join(self.extract)
        return text

    def generate_account_information_text(self):
        text = f"Número da conta: {str(self.account_number)}\n"
        text += f"Número da agência: {self.agency_number}\n"
        text += f"O saldo de sua conta é R$ {round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}\n"
        text += self.generate_extract_information_text()
        return text
    
    def add_balance(self, value: Decimal):
        self.balance = self.balance + value

    def sub_balance(self, value: Decimal):
        self.add_balance(-value)

    def add_total_withdrawl(self, total: int = 1):
        self.total_withdrawl = self.total_withdrawl + total

    @abstractmethod
    def withdraw(self, value: Decimal) -> Decimal:
        pass
    
    def deposit(self, value: Decimal):
        if value <= 0:
            raise ValueError("O valor é inválido para deposito")
        operation_info = 'Processando o depósito... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        self.add_balance(value)
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        clear_cmd_line(len(operation_info))
        print("O valor foi depositado com sucesso!")
        self.add_extract(f"Você depositou R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)}")
        print(f"O seu saldo atual é de: R$ {round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}")

    def transfer(self, value: Decimal, account_of_receipt: 'Account') -> bool:
        if value <= 0:
            raise ValueError("O valor é inválido para transferir")
        current_balance: Decimal = self.balance
        if value > current_balance:
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
    
    def show_extract(self, ):
        print("="*50)
        print(self.generate_extract_information_text())
    
    def __eq__(self, value: 'Account') -> bool:
        return self.account_number == value.account_number and self.agency_number == value.agency_number

    def __str__(self) -> str:
        return self.generate_account_information_text()