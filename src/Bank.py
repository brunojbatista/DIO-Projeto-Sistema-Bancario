from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING

from src.entities.Account import Account
from src.entities.AccountNumber import AccountNumber
from src.entities.AgencyNumber import AgencyNumber
from src.entities.CheckingAccount import CheckingAccount

if TYPE_CHECKING:
    from src.entities.Client import Client
    from src.entities.Client import CPF

PROCESSING_WAITING_TIME_IN_SECONDS = 2
AGENCY_NUMBER = 1
DEFAULT_AGENCY_NUMBER = AgencyNumber(AGENCY_NUMBER)

class Bank:
    current_account_number: int = 0

    def __init__(self):
        self._clients: List[Client] = []
        self._accounts: List[Account] = []

        self.clients = []
        self.accounts = []
    
    @property
    def clients(self) -> List[Client]:
        return self._clients
    
    @clients.setter
    def clients(self, clients: List[Client]):
        self._clients = clients

    @property
    def accounts(self) -> List[Account]:
        return self._accounts
    
    @accounts.setter
    def accounts(self, accounts: List[Account]):
        self._accounts = accounts

    def _get_client_by_cpf(self, cpf: CPF) -> Client:
        for client in self.clients:
            if client.cpf.cpf == cpf.cpf:
                return client
        return None

    def has_registered_CPF(self, cpf: CPF) -> bool:
        return self._get_client_by_cpf(cpf) != None
        
    def register_client(self, client: Client) -> bool:
        if client not in self.clients:
            clients = self.clients
            clients.append(client)
            self.clients = clients
            return True
        else:
            return False
        
    def search_client(self, cpf: CPF) -> Client:
        return self._get_client_by_cpf(cpf)
    
    def register_account(self, client: Client, account: Account):
        client.add_account(account=account)
        account.client = client
        accounts = self.accounts
        accounts.append(account)
        self.accounts = accounts
        Bank.current_account_number += 1
        return True
    
    def create_account(self, client: Client) -> bool:
        account = Account(
            account_number=AccountNumber(Bank.current_account_number),
            agency_number=AgencyNumber(AGENCY_NUMBER),
            client=client
        )
        return self.register_account(client=client, account=account)
    
    def create_checking_account(self, client: Client) -> bool:
        account = CheckingAccount(
            account_number=AccountNumber(Bank.current_account_number),
            agency_number=AgencyNumber(AGENCY_NUMBER),
            client=client
        )
        return self.register_account(client=client, account=account)
    
    def search_account(self, account_number: AccountNumber, agency_number: AgencyNumber = DEFAULT_AGENCY_NUMBER) -> Account:
        for account in self.accounts:
            if account.account_number == account_number and \
                account.agency_number == agency_number:
                return account
        return None

    def signin_account(self, cpf: CPF, account_number: AccountNumber, agency_number: AgencyNumber = DEFAULT_AGENCY_NUMBER) -> Account:
        for account in self.accounts:
            if account.account_number == account_number and \
                account.agency_number == agency_number and \
                account.client.cpf == cpf:
                return account
        return None