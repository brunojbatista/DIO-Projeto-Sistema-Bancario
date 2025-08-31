from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING

from src.entities import Account, AccountNumber, AgencyNumber

if TYPE_CHECKING:
    from src.entities import Client, CPF

PROCESSING_WAITING_TIME_IN_SECONDS = 2
AGENCY_NUMBER = 1
DEFAULT_AGENCY_NUMBER = AgencyNumber(AGENCY_NUMBER)

class Bank:
    """
    Classe que representa um banco com operações básicas de cadastro de clientes e contas,
    bem como busca e autenticação de contas.

    Atributos:
        current_account_number (int): Número sequencial para geração de contas.
    """
    current_account_number: int = 1

    def __init__(self):
        """
        Inicializa o banco com listas vazias de clientes e contas.
        """
        self._clients: List[Client] = []
        self._accounts: List[Account] = []

        self.clients = []
        self.accounts = []

    @property
    def clients(self) -> List[Client]:
        """
        Getter da lista de clientes.
        """
        return self._clients

    @clients.setter
    def clients(self, clients: List[Client]):
        """
        Setter da lista de clientes.

        Args:
            clients (List[Client]): Nova lista de clientes.
        """
        self._clients = clients

    @property
    def accounts(self) -> List[Account]:
        """
        Getter da lista de contas.
        """
        return self._accounts

    @accounts.setter
    def accounts(self, accounts: List[Account]):
        """
        Setter da lista de contas.

        Args:
            accounts (List[Account]): Nova lista de contas.
        """
        self._accounts = accounts

    def _get_client_by_cpf(self, cpf: CPF) -> Client:
        """
        Retorna o cliente associado ao CPF informado, se existir.

        Args:
            cpf (CPF): CPF do cliente.

        Returns:
            Client: Cliente correspondente, ou None.
        """
        for client in self.clients:
            if client.cpf.cpf == cpf.cpf:
                return client
        return None

    def has_registered_CPF(self, cpf: CPF) -> bool:
        """
        Verifica se o CPF já está cadastrado no banco.

        Args:
            cpf (CPF): CPF a ser verificado.

        Returns:
            bool: True se estiver cadastrado, False caso contrário.
        """
        return self._get_client_by_cpf(cpf) is not None

    def register_client(self, client: Client) -> bool:
        """
        Registra um novo cliente, caso ainda não esteja na lista.

        Args:
            client (Client): Cliente a ser registrado.

        Returns:
            bool: True se o cliente foi adicionado, False se já existia.
        """
        if client not in self.clients:
            clients = self.clients
            clients.append(client)
            self.clients = clients
            return True
        else:
            return False

    def search_client(self, cpf: CPF) -> Client:
        """
        Busca um cliente pelo CPF.

        Args:
            cpf (CPF): CPF do cliente.

        Returns:
            Client: Cliente encontrado, ou None.
        """
        return self._get_client_by_cpf(cpf)

    def register_account(self, client: Client, account: Account):
        """
        Registra uma nova conta bancária para um cliente.

        Args:
            client (Client): Cliente dono da conta.
            account (Account): Conta a ser registrada.

        Returns:
            bool: True após registro.
        """
        client.add_account(account=account)
        account.client = client
        accounts = self.accounts
        accounts.append(account)
        self.accounts = accounts
        Bank.current_account_number += 1
        return True

    def create_account(self, client: Client) -> bool:
        """
        Cria uma conta e a registra no banco.

        Args:
            client (Client): Cliente dono da nova conta.

        Returns:
            bool: True se registrada com sucesso.
        """
        account = Account(
            account_number=AccountNumber(Bank.current_account_number),
            agency_number=AgencyNumber(AGENCY_NUMBER),
            client=client
        )
        return self.register_account(client=client, account=account)

    def create_checking_account(self, client: Client) -> bool:
        """
        Cria uma conta corrente e a registra no banco.

        Args:
            client (Client): Cliente dono da nova conta.

        Returns:
            bool: True se registrada com sucesso.
        """
        account = Account(
            account_number=AccountNumber(Bank.current_account_number),
            agency_number=AgencyNumber(AGENCY_NUMBER),
            client=client
        )
        return self.register_account(client=client, account=account)

    def search_account(self, account_number: AccountNumber, agency_number: AgencyNumber = DEFAULT_AGENCY_NUMBER) -> Account:
        """
        Busca uma conta por número e agência.

        Args:
            account_number (AccountNumber): Número da conta.
            agency_number (AgencyNumber): Número da agência (padrão: 1).

        Returns:
            Account: Conta encontrada, ou None.
        """
        for account in self.accounts:
            if account.account_number == account_number and \
                account.agency_number == agency_number:
                return account
        return None

    def signin_account(self, cpf: CPF, account_number: AccountNumber, agency_number: AgencyNumber = DEFAULT_AGENCY_NUMBER) -> Account:
        """
        Autentica o acesso de um cliente a uma conta específica.

        Args:
            cpf (CPF): CPF do cliente.
            account_number (AccountNumber): Número da conta.
            agency_number (AgencyNumber): Número da agência (padrão: 1).

        Returns:
            Account: Conta autenticada, ou None.
        """
        for account in self.accounts:
            if account.account_number == account_number and \
                account.agency_number == agency_number and \
                account.client.cpf == cpf:
                return account
        return None

    def get_accounts_iterator(self):
        """
        Cria um iterador personalizado para todas as contas do banco.
        
        Returns:
            AccountIterator: Iterador que permite iterar sobre todas as contas.
        """
        from src.entities import AccountIterator
        return AccountIterator(self.accounts)
