# Arquivo __init__.py para permitir importações simplificadas

# Importando todas as classes para permitir importação simplificada
from .Account import Account
from .AccountNumber import AccountNumber
from .Address import Address
from .AgencyNumber import AgencyNumber
from .Client import Client
from .CPF import CPF
from .DateOfBirth import DateOfBirth
from .Transaction import Transaction
from .Deposit import Deposit
from .Withdraw import Withdraw
from .Transfer import Transfer
from .AccountIterator import AccountIterator

__all__ = [
    'Account',
    'AccountNumber', 
    'Address',
    'AgencyNumber',
    'Client',
    'CPF',
    'DateOfBirth',
    'Transaction',
    'Deposit',
    'Withdraw',
    'Transfer',
    'AccountIterator'
]
