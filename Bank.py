from datetime import datetime
from decimal import Decimal
import time
from typing import List

from Account import Account
from CheckingAccount import CheckingAccount
from Client import Client
from Utils import clear_cmd_line, is_valid_cpf

PROCESSING_WAITING_TIME_IN_SECONDS = 2

class Bank:
    """
    Classe que representa um banco com múltiplas contas e clientes.
    Permite operações como criação de contas, login, depósito, saque
    e exibição de informações da conta ativa.
    """

    def __init__(self):
        """
        Inicializa o banco com lista vazia de contas e nenhum cliente conectado.
        """
        self.accounts: List[(Client, Account)] = []
        self.client: Client = None
        self.account: Account = None

    def set_client(self, client: Client):
        """
        Define o cliente ativo no banco.

        Args:
            client (Client): Cliente a ser definido como ativo.
        """
        self.client = client

    def set_account(self, account: Account):
        """
        Define a conta ativa no banco.

        Args:
            account (Account): Conta a ser definida como ativa.
        """
        self.account = account

    def get_client(self) -> Client:
        """
        Retorna o cliente atualmente ativo.

        Returns:
            Client: Cliente logado no sistema.
        """
        return self.client

    def get_account(self) -> Account:
        """
        Retorna a conta atualmente ativa.

        Returns:
            Account: Conta associada ao cliente ativo.
        """
        return self.account

    def add_account(self, client: Client, account: Account):
        """
        Adiciona uma conta à lista de contas do banco.

        Args:
            client (Client): Cliente associado à conta.
            account (Account): Conta a ser adicionada.
        """
        self.accounts.append((client, account))

    def create_account(self, client_name: str, client_cpf: str, account: Account):
        """
        Cria uma nova conta associada a um cliente.

        Args:
            client_name (str): Nome do cliente.
            client_cpf (str): CPF do cliente.
            account (Account): Instância da conta a ser criada.
        """
        client = Client(client_cpf, client_name)
        account.set_client(client)
        self.add_account(client, account)

    def create_checking_account(self, client_name: str, client_cpf: str):
        """
        Cria uma nova conta corrente associada a um cliente.

        Args:
            client_name (str): Nome do cliente.
            client_cpf (str): CPF do cliente.
        """
        self.create_account(client_name, client_cpf, CheckingAccount())

    def sing_in_account(self, client_cpf: str) -> bool:
        """
        Faz login em uma conta a partir do CPF informado.

        Args:
            client_cpf (str): CPF do cliente.

        Returns:
            bool: True se o login foi bem-sucedido, False caso contrário.
        """
        for client, account in self.accounts:
            if client.get_cpf() == client_cpf:
                self.set_client(client)
                self.set_account(account)
                print("Você acabou de entrar em sua conta!")
                return True
        return False

    def sign_out_account(self) -> bool:
        """
        Faz logout da conta atual.

        Returns:
            bool: Sempre retorna True.
        """
        self.set_account(None)
        self.set_client(None)
        print("A operação com sua conta foi fechada com sucesso!")
        return True

    def deposit_operation(self) -> bool:
        """
        Realiza uma operação de depósito para a conta ativa.

        Returns:
            bool: True se o depósito foi realizado com sucesso, False caso contrário.
        """
        print("Você escolheu a opção de depósito!")
        value = Decimal('0')
        try:
            value = Decimal(input("Informe o valor do depósito: "))
        except ValueError:
            print("Só é aceito dígitos numéricos na operação!")
            return False
        return self.account.deposit(value)

    def withdraw_operation(self) -> bool:
        """
        Realiza uma operação de saque para a conta ativa.

        Returns:
            bool: True se o saque foi realizado com sucesso, False caso contrário.
        """
        value = Decimal('0')
        try:
            value = Decimal(input("Informe o valor do saque: "))
        except ValueError:
            print("Só é aceito dígitos numéricos na operação!")
            return False
        return self.account.withdraw(value)
    
    def transfer_operation(self) -> bool:
        """
        Realiza uma operação de transferência entre contas.

        Solicita o valor e o CPF do destinatário, valida os dados
        e executa a transferência caso a conta seja válida e diferente da atual.

        Returns:
            bool: True se a transferência foi realizada com sucesso, False caso contrário.
        """
        value = Decimal('0')
        client_cpf = None
        try:
            value = Decimal(input("Informe o valor a ser transferido: ").strip())
        except ValueError:
            print("Só é aceito dígitos numéricos na operação!")
            return False

        client_cpf = input("Informe o cpf do cliente: ").strip()
        if not is_valid_cpf(client_cpf):
            print("O CPF digitado é inválido!")
            return False

        account_of_receipt: Account = None
        for client, account in self.accounts:
            if client.get_cpf() == client_cpf:
                if client == self.client:
                    print("Não pode transferir para a mesma conta")
                    return False
                account_of_receipt = account
                break

        if account_of_receipt is None:
            print(f"Não foi encontrado cadastro no CPF: {client_cpf}")
            return False

        return self.account.transfer(value, account_of_receipt)


    def show_account_information(self):
        """
        Exibe as informações da conta atualmente logada.
        """
        print(self.account)
        input("Aperte qualquer botão para voltar para o menu.")

    def close_operation(self) -> bool:
        """
        Encerra a sessão atual com confirmação do usuário.

        Returns:
            bool: True se a operação foi encerrada, False se o usuário cancelou.
        """
        print("Você deseja realmente sair da operação? 1 = Sim; 0 = Não")
        option = input("Digite a opção: ")
        if option == '1':
            operation_info = 'Fechando a operação... Aguarde um momento!'
            print(operation_info, end='', flush=True)
            time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
            clear_cmd_line(len(operation_info))
            self.sign_out_account()
            return True
        return False
