#!/usr/bin/env python3
"""
Exemplo de uso do AccountIterator.
"""

from decimal import Decimal
from src import Bank
from src.entities import AccountNumber, Address, CPF, Client, DateOfBirth

def exemplo_account_iterator():
    """Demonstra o funcionamento do AccountIterator."""
    
    print("🏦 EXEMPLO DO ACCOUNT ITERATOR")
    print("=" * 50)
    
    # Criar banco e contas
    bank = Bank()
    
    # Criar clientes com CPFs válidos
    client1 = Client(
        name="João Silva",
        cpf=CPF("646.114.700-40"),
        date_of_birth=DateOfBirth("01/01/1990"),
        address=Address("Rua das Flores", "123", "Centro", "São Paulo", "SP")
    )
    
    client2 = Client(
        name="Maria Santos",
        cpf=CPF("310.849.500-30"),
        date_of_birth=DateOfBirth("15/05/1985"),
        address=Address("Avenida Principal", "456", "Jardins", "São Paulo", "SP")
    )
    
    # Registrar clientes e criar contas
    bank.register_client(client1)
    bank.register_client(client2)
    bank.create_account(client1)
    bank.create_account(client2)
    
    # Realizar algumas transações
    account1 = bank.signin_account(client1.cpf, AccountNumber(1))
    account2 = bank.signin_account(client2.cpf, AccountNumber(2))
    
    account1.deposit(Decimal('1000.00'))
    account2.deposit(Decimal('500.00'))
    
    print(f"✅ Criadas {len(bank.accounts)} contas com transações")
    
    print("\n💡 Exemplos de uso do AccountIterator:")
    print("-" * 30)
    
    # Exemplo 1: Listar todas as contas
    print("\n1️⃣ Listando todas as contas:")
    accounts_iterator = bank.get_accounts_iterator()
    for i, account_info in enumerate(accounts_iterator, 1):
        print(f"   {i}. Conta: {account_info['account_number']} - Cliente: {account_info['client_name']} - Saldo: R$ {account_info['balance']}")
    
    # Exemplo 2: Usar formatação personalizada
    print("\n2️⃣ Usando formatação personalizada:")
    accounts_iterator.reset()
    for account_info in accounts_iterator:
        formatted_info = accounts_iterator.get_account_info_formatted(account_info)
        print(f"   {formatted_info}")
    
    # Exemplo 3: Calcular saldo total
    print("\n3️⃣ Calculando saldo total do banco:")
    accounts_iterator.reset()
    total_balance = sum(acc['balance'] for acc in accounts_iterator)
    print(f"   Saldo total: R$ {total_balance}")
    
    # Exemplo 4: Contar transações
    print("\n4️⃣ Contando total de transações:")
    accounts_iterator.reset()
    total_transactions = sum(acc['total_transactions'] for acc in accounts_iterator)
    print(f"   Total de transações: {total_transactions}")
    
    print("\n✅ Exemplo concluído!")

if __name__ == "__main__":
    exemplo_account_iterator()
