from __future__ import annotations

import re
from typing import List, TYPE_CHECKING

from src.entities.Address import Address
from src.entities.CPF import CPF
from src.entities.DateOfBirth import DateOfBirth

if TYPE_CHECKING:
    from src.entities.Account import Account

class Client:
    def __init__(self, name: str, cpf: CPF, date_of_birth: DateOfBirth, address: Address):
        self._name: str = None
        self._cpf: CPF = None
        self._date_of_birth: DateOfBirth = None
        self._address: Address = None
        self._accounts: List[Account] = []

        self.name = name
        self.cpf = cpf
        self.date_of_birth = date_of_birth
        self.address = address
        self.accounts = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if re.search(r"^\s*$", name):
            raise ValueError("O nome precisa ser definido")
        self._name = name

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf: CPF):
        self._cpf = cpf

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: DateOfBirth):
        self._date_of_birth = date_of_birth

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address: Address):
        self._address = address

    @property
    def accounts(self):
        return self._accounts

    @accounts.setter
    def accounts(self, accounts: List[Account]):
        self._accounts = accounts

    def add_account(self, account: Account):
        accounts = self.accounts
        accounts.append(account)
        self.accounts = accounts

    def generate_client_text(self) -> str:
        return (f"Cliente: {self.name} (CPF: {self.cpf})\n"
                f"Data de nascimento: {self.date_of_birth}\n"
                f"Endereço: {self.address}\n")

    def __str__(self) -> str:
        text = self.generate_client_text()
        for account in self.accounts:
            text += "\n" + str(account)
        return text

    def __eq__(self, value: 'Client') -> bool:
        return self.cpf.cpf == value.cpf.cpf
