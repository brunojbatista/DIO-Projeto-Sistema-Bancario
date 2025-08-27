from __future__ import annotations

import re
from typing import List, TYPE_CHECKING

from src.entities import Address, CPF, DateOfBirth

if TYPE_CHECKING:
    from src.entities import Account

class Client:
    """
    Representa um cliente do sistema bancário.

    Cada cliente possui nome, CPF, data de nascimento, endereço e uma lista de contas bancárias associadas.
    """

    def __init__(self, name: str, cpf: CPF, date_of_birth: DateOfBirth, address: Address):
        """
        Inicializa uma instância de cliente.

        Args:
            name (str): Nome completo do cliente.
            cpf (CPF): Objeto CPF validado do cliente.
            date_of_birth (DateOfBirth): Data de nascimento do cliente.
            address (Address): Endereço associado ao cliente.
        """
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
    def name(self) -> str:
        """Retorna o nome do cliente."""
        return self._name

    @name.setter
    def name(self, name: str):
        """Define o nome do cliente.

        Args:
            name (str): Nome a ser atribuído.

        Raises:
            ValueError: Se o nome estiver vazio ou apenas espaços.
        """
        if re.search(r"^\s*$", name):
            raise ValueError("O nome precisa ser definido")
        self._name = name

    @property
    def cpf(self) -> CPF:
        """Retorna o CPF do cliente (objeto CPF)."""
        return self._cpf

    @cpf.setter
    def cpf(self, cpf: CPF):
        """Define o CPF do cliente."""
        self._cpf = cpf

    @property
    def date_of_birth(self) -> DateOfBirth:
        """Retorna a data de nascimento do cliente."""
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: DateOfBirth):
        """Define a data de nascimento do cliente."""
        self._date_of_birth = date_of_birth

    @property
    def address(self) -> Address:
        """Retorna o endereço do cliente."""
        return self._address

    @address.setter
    def address(self, address: Address):
        """Define o endereço do cliente."""
        self._address = address

    @property
    def accounts(self) -> List[Account]:
        """Retorna a lista de contas associadas ao cliente."""
        return self._accounts

    @accounts.setter
    def accounts(self, accounts: List[Account]):
        """Define a lista de contas do cliente."""
        self._accounts = accounts

    def add_account(self, account: Account):
        """
        Adiciona uma conta bancária à lista de contas do cliente.

        Args:
            account (Account): Objeto de conta a ser adicionado.
        """
        accounts = self.accounts
        accounts.append(account)
        self.accounts = accounts

    def generate_client_text(self) -> str:
        """
        Gera um resumo textual das informações do cliente (sem as contas).

        Returns:
            str: Texto formatado com nome, CPF, nascimento e endereço.
        """
        return (f"Cliente: {self.name} (CPF: {self.cpf})\n"
                f"Data de nascimento: {self.date_of_birth}\n"
                f"Endereço: {self.address}\n")

    def __str__(self) -> str:
        """
        Retorna uma representação completa do cliente, incluindo suas contas.

        Returns:
            str: Texto formatado com dados do cliente e suas contas.
        """
        text = self.generate_client_text()
        for account in self.accounts:
            text += "\n" + str(account)
        return text

    def __eq__(self, value: 'Client') -> bool:
        """
        Compara dois clientes com base no CPF.

        Args:
            value (Client): Outro cliente a ser comparado.

        Returns:
            bool: True se os CPFs forem iguais.
        """
        return self.cpf.cpf == value.cpf.cpf
