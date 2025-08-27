# Arquivo __init__.py para permitir importações simplificadas

# Importando todas as classes para permitir importação simplificada
from .Account import Account
from .AccountNumber import AccountNumber
from .Address import Address
from .AgencyNumber import AgencyNumber
from .CheckingAccount import CheckingAccount
from .Client import Client
from .CPF import CPF
from .DateOfBirth import DateOfBirth

__all__ = [
    'Account',
    'AccountNumber', 
    'Address',
    'AgencyNumber',
    'CheckingAccount',
    'Client',
    'CPF',
    'DateOfBirth'
]
