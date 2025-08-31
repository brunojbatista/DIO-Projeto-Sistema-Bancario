MENU_BANK = """
Bem vindo! Por favor escolha uma das opções:

[r] Cadastrar novo cliente
[c] Criar uma conta corrente
[a] Acessar conta

=> """

MENU_ACCOUNT = """
Escolha uma das opções abaixo:

[d] Depositar
[s] Sacar
[e] Extrato
[t] Transferir
[q] Sair

=> """

from decimal import Decimal
from src import Bank
from src.entities import AccountNumber, Address, CPF, Client, DateOfBirth
        
bank: Bank = Bank()

while True:
    print("="*80)
    option_bank = input(MENU_BANK).strip()

    if option_bank == 'r':
        client_name = input("Digite o nome: ").strip()
        
        # Criando o CPF
        client_cpf = input("Digite o CPF: ").strip()
        cpf = CPF(client_cpf)
        if bank.has_registered_CPF(cpf):
            print("Cliente já existente!")
            continue

        # Criando a data de nascimento
        client_date_of_birth = input("Digite a data de nascimento: ").strip()
        date_of_birth = DateOfBirth(client_date_of_birth)

        # Criando o endereço
        client_street = input("Digite o logradouro: ").strip()
        client_number = input("Digite o número: ").strip()
        client_district = input("Digite o bairro: ").strip()
        client_city = input("Digite o cidade: ").strip()
        client_state = input("Digite o state: ").strip()
        address = Address(
            street=client_street,
            number=client_number,
            district=client_district,
            city=client_city,
            state=client_state
        )

        print(f"Data de nascimento: {date_of_birth}")

        print(f"CPF: {cpf}")

        print(f"Endereço: {address}")

        # Criando o cliente
        client = Client(
            name=client_name,
            cpf=cpf,
            date_of_birth=date_of_birth,
            address=address
        )
        print(f"Cliente: {client}")
        if bank.register_client(client=client):
            print("Cliente cadastrado com sucesso!")
        else:
            print("Cliente já existente!")
            continue
    elif option_bank == 'c':
        try:
            client_cpf = input("Digite o CPF: ").strip()
            cpf = CPF(client_cpf)
            client = bank.search_client(cpf)
            if not client:
                print("Não há cliente com o registro do CPF!")
                continue
            if bank.create_account(client):
                print("Conta criada com sucesso!")
            else:
                print("Ocorreu um erro na criação da conta!")
                continue
        except ValueError as e:
            print(str(e))
            continue
    elif option_bank == 'a':
        cpf: CPF = None
        account_number: AccountNumber = None
        
        try:
            client_cpf = input("Digite o CPF: ").strip()
            cpf = CPF(client_cpf)
        except ValueError as e:
            print(str(e))
            continue
        
        try:
            client_account_number = input("Digite o número da conta: ").strip()
            account_number = AccountNumber(client_account_number)
        except ValueError as e:
            print(str(e))
            continue
        
        account = bank.signin_account(cpf, account_number)
        if not account:
            print("O CPF e/ou número da conta informada não existe")
            continue
        
        print("Você está agora em sua conta!")
        while True:
            print("-----------------------------------------------------")
            option_account = input(MENU_ACCOUNT).strip()
            if option_account == 'd':
                # print("Depositar na conta")
                value = input("Digite o valor: ").strip()
                try:
                    account.deposit(Decimal(value))
                except ValueError as e:
                    print(str(e))
                    continue
            elif option_account == 's':
                print("Sacar da conta")
                value = input("Digite o valor: ").strip()
                try:
                    account.withdraw(Decimal(value))
                except ValueError as e:
                    print(str(e))
                    continue
            elif option_account == 't':
                account_number: AccountNumber = None
                
                try:
                    client_account_number = input("Digite o número da conta: ").strip()
                    account_number = AccountNumber(client_account_number)
                except ValueError as e:
                    print(str(e))
                    continue

                account_of_receipt = bank.search_account(account_number)
                if not account_of_receipt:
                    print("Não existe a conta informada")
                    continue

                value = input("Digite o valor: ").strip()
                try:
                    account.transfer(Decimal(value), account_of_receipt)
                except ValueError as e:
                    print(str(e))
                    continue
            elif option_account == 'e':
                account.show_extract()
            elif option_account == 't':
                print("Transferir para outra conta")
            elif option_account == 'q':
                print("Você saiu do menu da sua conta bancária!")
                break;
    else:
        print("Operação inválida, tente as opções disponíveis por favor!")