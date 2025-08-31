#!/usr/bin/env python3
"""
Exemplo de uso do decorador de transações.
"""

from decimal import Decimal
from src import Bank
from src.entities import AccountNumber, Address, CPF, Client, DateOfBirth

def exemplo_decorator():
    """Demonstra o funcionamento do decorador de transações."""
    
    print("🎯 EXEMPLO DO DECORADOR DE TRANSAÇÕES")
    print("=" * 60)
    
    # Criar banco e cliente
    bank = Bank()
    client = Client(
        name="Exemplo Cliente",
        cpf=CPF("111.444.777-35"),
        date_of_birth=DateOfBirth("01/01/1990"),
        address=Address("Rua Exemplo", "123", "Centro", "Cidade", "Estado")
    )
    
    # Registrar cliente e criar conta
    bank.register_client(client)
    bank.create_account(client)
    account = bank.signin_account(client.cpf, AccountNumber(1))
    
    print("\n💡 O decorador será aplicado automaticamente nas transações abaixo:")
    print("-" * 50)
    
    # Realizar uma transação (o decorador será aplicado automaticamente)
    account.deposit(Decimal('500.00'))
    
    print("\n✅ Exemplo concluído! Observe o logging detalhado acima.")

if __name__ == "__main__":
    exemplo_decorator()
