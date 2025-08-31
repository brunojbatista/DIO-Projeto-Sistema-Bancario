from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities import Account

class AccountIterator:
    """
    Iterador personalizado para iterar sobre todas as contas do banco.
    
    Permite iterar sobre as contas retornando informações básicas de cada uma,
    incluindo número da conta, agência e saldo atual.
    """
    
    def __init__(self, accounts: list[Account]):
        """
        Inicializa o iterador com a lista de contas.
        
        Args:
            accounts (list[Account]): Lista de contas do banco.
        """
        self._accounts = accounts
        self._index = 0
    
    def __iter__(self) -> AccountIterator:
        """Retorna o próprio iterador."""
        return self
    
    def __next__(self) -> dict:
        """
        Retorna a próxima conta com suas informações básicas.
        
        Returns:
            dict: Dicionário com informações da conta (número, agência, saldo, cliente).
            
        Raises:
            StopIteration: Quando não há mais contas para iterar.
        """
        if self._index >= len(self._accounts):
            raise StopIteration
        
        account = self._accounts[self._index]
        self._index += 1
        
        # Retorna informações básicas da conta
        return {
            'account_number': str(account.account_number),
            'agency_number': str(account.agency_number),
            'balance': account.balance,
            'client_name': account.client.name,
            'client_cpf': str(account.client.cpf),
            'total_transactions': len(account.transactions)
        }
    
    def __len__(self) -> int:
        """Retorna o número total de contas."""
        return len(self._accounts)
    
    def reset(self):
        """Reseta o índice do iterador para o início."""
        self._index = 0
    
    def get_account_info_formatted(self, account_info: dict) -> str:
        """
        Formata as informações da conta para exibição.
        
        Args:
            account_info (dict): Informações da conta retornadas pelo iterador.
            
        Returns:
            str: String formatada com as informações da conta.
        """
        from src import round_decimal
        DEFAULT_DECIMAL_PLACES = 2
        
        return (f"Conta: {account_info['account_number']} | "
                f"Agência: {account_info['agency_number']} | "
                f"Cliente: {account_info['client_name']} | "
                f"CPF: {account_info['client_cpf']} | "
                f"Saldo: R$ {round_decimal(account_info['balance'], DEFAULT_DECIMAL_PLACES)} | "
                f"Transações: {account_info['total_transactions']}")
