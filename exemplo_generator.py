#!/usr/bin/env python3
"""
Exemplo de uso do gerador de transações.
"""

from decimal import Decimal
from src import Bank
from src.entities import AccountNumber, Address, CPF, Client, DateOfBirth

def exemplo_generator():
    """Demonstra o funcionamento do gerador de transações."""
    
    print("🔄 EXEMPLO DO GERADOR DE TRANSAÇÕES")
    print("=" * 50)
    
    # Criar banco e conta
    bank = Bank()
    client = Client(
        name="Exemplo Cliente",
        cpf=CPF("111.444.777-35"),
        date_of_birth=DateOfBirth("01/01/1990"),
        address=Address("Rua Exemplo", "123", "Centro", "Cidade", "Estado")
    )
    
    bank.register_client(client)
    bank.create_account(client)
    account = bank.signin_account(client.cpf, AccountNumber(1))
    
    # Realizar algumas transações
    account.deposit(Decimal('100.00'))
    account.withdraw(Decimal('30.00'))
    account.deposit(Decimal('50.00'))
    account.withdraw(Decimal('20.00'))
    
    print(f"\n📊 Conta criada com {len(account.transactions)} transações")
    
    print("\n💡 Exemplos de uso do gerador:")
    print("-" * 30)
    
    # Exemplo 1: Todas as transações
    print("\n1️⃣ Todas as transações:")
    for i, transaction in enumerate(account.iterate_transactions(), 1):
        print(f"   {i}. {type(transaction).__name__}: R$ {transaction.value}")
    
    # Exemplo 2: Apenas depósitos
    print("\n2️⃣ Apenas depósitos:")
    for i, transaction in enumerate(account.iterate_transactions('deposit'), 1):
        print(f"   {i}. Depósito: R$ {transaction.value}")
    
    # Exemplo 3: Apenas saques
    print("\n3️⃣ Apenas saques:")
    for i, transaction in enumerate(account.iterate_transactions('withdraw'), 1):
        print(f"   {i}. Saque: R$ {transaction.value}")
    
    # Exemplo 4: List comprehension
    print("\n4️⃣ Usando list comprehension:")
    deposit_values = [t.value for t in account.iterate_transactions('deposit')]
    withdraw_values = [t.value for t in account.iterate_transactions('withdraw')]
    print(f"   Valores dos depósitos: {deposit_values}")
    print(f"   Valores dos saques: {withdraw_values}")
    
    # Exemplo 5: Cálculos
    print("\n5️⃣ Cálculos com o gerador:")
    total_deposits = sum(t.value for t in account.iterate_transactions('deposit'))
    total_withdraws = sum(t.value for t in account.iterate_transactions('withdraw'))
    print(f"   Total de depósitos: R$ {total_deposits}")
    print(f"   Total de saques: R$ {total_withdraws}")
    print(f"   Saldo líquido: R$ {total_deposits - total_withdraws}")
    
    print("\n✅ Exemplo concluído!")

if __name__ == "__main__":
    exemplo_generator()
