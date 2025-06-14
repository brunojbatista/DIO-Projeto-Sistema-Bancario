from datetime import datetime
import time
from Client import Client
from Utils import clear_cmd_line, format_cpf, round_decimal
from decimal import ROUND_HALF_UP, Decimal

LIMIT_PER_WITHDRAWLS = Decimal('500.00')
MAX_WITHDRAWLS = 3
PROCESSING_WAITING_TIME_IN_SECONDS = 2
DEFAULT_DECIMAL_PLACES = 2

class Account:
    """
    Classe que representa uma conta bancária para um cliente.

    Esta classe permite realizar operações básicas de uma conta bancária como:
    - Depósitos
    - Saques (com validação de limites e número máximo diário)
    - Transferências entre contas
    - Armazenamento e exibição do extrato
    - Gerenciamento de cliente associado e saldo

    A conta utiliza valores do tipo `Decimal` para garantir precisão nas operações financeiras.
    Regras importantes:
    - O limite por saque é de R$500,00
    - O máximo de saques permitidos é 3
    - Todas as operações são registradas com data/hora no extrato
    """

    def __init__(self):
        """Inicializa a conta com saldo zero, extrato vazio e nenhum saque registrado."""
        self.client: Client = None
        self.balance: Decimal = Decimal('0')
        self.statement: str = None
        self.total_withdrawals: int = None

        self.set_balance(Decimal('0'))
        self.set_statement("")
        self.set_total_withdrawl(0)

    def set_client(self, client: Client):
        """Define o cliente associado à conta."""
        self.client = client

    def set_balance(self, balance: Decimal):
        """Define o saldo da conta."""
        self.balance = balance

    def set_statement(self, statement: str):
        """Define o extrato da conta."""
        self.statement = statement

    def set_total_withdrawl(self, total_withdrawl: int):
        """Define o número total de saques realizados."""
        self.total_withdrawals = total_withdrawl

    def get_client(self) -> Client:
        """Retorna o cliente associado à conta."""
        return self.client

    def get_balance(self) -> Decimal:
        """Retorna o saldo atual da conta."""
        return self.balance

    def get_statement(self) -> str:
        """Retorna o extrato completo da conta."""
        return self.statement

    def get_total_withdrawl(self) -> int:
        """Retorna o número de saques já realizados."""
        return self.total_withdrawals

    def add_balance(self, value: Decimal):
        """Adiciona um valor ao saldo atual."""
        self.set_balance(self.get_balance() + value)

    def add_statement(self, message: str):
        """Adiciona uma nova linha ao extrato, com timestamp e saldo atualizado."""
        date_now_string = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        current_statement = self.get_statement()
        current_statement += message + f" => Saldo após operação R$ {round_decimal(self.get_balance(), DEFAULT_DECIMAL_PLACES)}" + f" - Realizado em {date_now_string}\n"
        self.set_statement(current_statement)

    def add_total_withdrawl(self, total: int = 1):
        """Incrementa o total de saques realizados."""
        self.set_total_withdrawl(self.get_total_withdrawl() + total)

    def sub_balance(self, value: Decimal):
        """Subtrai um valor do saldo atual."""
        self.set_balance(self.get_balance() - value)

    def deposit(self, value: Decimal) -> bool:
        """
        Realiza uma operação de depósito.

        Args:
            value (Decimal): Valor a ser depositado.

        Returns:
            bool: True se o depósito for bem-sucedido, False caso contrário.
        """
        if value <= 0:
            print("O valor é inválido para deposito")
            return False
        operation_info = 'Processando o depósito... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        self.add_balance(value)
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        clear_cmd_line(len(operation_info))
        print("O valor foi depositado com sucesso!")
        self.add_statement(f"Você depositou R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)}")
        print(f"O seu saldo atual é de: R$ {round_decimal(self.get_balance(), DEFAULT_DECIMAL_PLACES)}")
        return True

    def withdraw(self, value: Decimal) -> bool:
        """
        Realiza uma operação de saque.

        Args:
            value (Decimal): Valor a ser sacado.

        Returns:
            bool: True se o saque for bem-sucedido, False caso contrário.
        """
        if value <= 0:
            print("O valor é inválido para saque")
            return
        elif value > self.balance:
            print("Saldo insuficiente...")
            print(f"Seu saldo atual é de R$ {round_decimal(self.get_balance(), DEFAULT_DECIMAL_PLACES)}")
            return
        elif value > LIMIT_PER_WITHDRAWLS:
            print(f"O valor do saque excede o limite de R$ {round_decimal(LIMIT_PER_WITHDRAWLS, DEFAULT_DECIMAL_PLACES)}")
            return
        elif self.total_withdrawals >= MAX_WITHDRAWLS:
            print(f"O total de saque excedeu o limite de {MAX_WITHDRAWLS} saques")
            return
        operation_info = 'Processando o saque... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        self.sub_balance(value)
        self.add_total_withdrawl()
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        clear_cmd_line(len(operation_info))
        print("Saque realizado com sucesso!")
        self.add_statement(f"Você sacou R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)}")
        print(f"O seu saldo atual é de: R$ {round_decimal(self.get_balance(), DEFAULT_DECIMAL_PLACES)}")
        return True

    def transfer(self, value: Decimal, account_of_receipt: 'Account') -> bool:
        """
        Realiza uma transferência entre contas.

        Args:
            value (Decimal): Valor a ser transferido.
            account_of_receipt (Account): Conta destino.

        Returns:
            bool: True se a transferência for bem-sucedida, False caso contrário.
        """
        if value <= 0:
            print("O valor é inválido para transferir")
            return False
        current_balance: Decimal = self.get_balance()
        if value > current_balance:
            print("O valor é maior que o saldo de sua conta")
            return False
        operation_info = 'Processando a transferência... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        self.sub_balance(value)
        account_of_receipt.add_balance(value)
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        clear_cmd_line(len(operation_info))
        self.add_statement(f"Você transferiu um valor de R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)} para o cliente {account_of_receipt.get_client().get_name()} (CPF: {format_cpf(account_of_receipt.get_client().get_cpf())})")
        account_of_receipt.add_statement(f"Você recebeu um valor de R$ {round_decimal(value, DEFAULT_DECIMAL_PLACES)} do cliente {self.client.get_name()} (CPF: {format_cpf(self.client.get_cpf())})")
        print(f"O seu saldo atual é de: R$ {round_decimal(self.get_balance(), DEFAULT_DECIMAL_PLACES)}")
        return True

    def __str__(self):
        """
        Retorna uma representação textual da conta.

        Returns:
            str: Informações do cliente, saldo e extrato formatado.
        """
        text = "---------------------------------------------\n"
        text += "Informações da conta:\n"
        text += str(self.get_client()) + "\n"
        text += f"O seu saldo atual é de: R$ {round_decimal(self.get_balance(), DEFAULT_DECIMAL_PLACES)}\n\n"
        text += "Extrato Bancário:\n"
        text += self.get_statement()
        text += "---------------------------------------------"
        return text