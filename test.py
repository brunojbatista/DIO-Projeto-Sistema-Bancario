from src.entities import Client, DateOfBirth, CPF, Address, Account

if __name__ == '__main__':
    # Criando a data de nascimento
    date_of_birth = DateOfBirth("15/06/2000")
    print(f"Data de nascimento: {date_of_birth}")

    # Criando o CPF
    cpf = CPF("075.593.650-78")
    print(f"CPF: {cpf}")

    # Criando o endereço
    address = Address(
        street="Rua Dona Maria Lacerda",
        number="140",
        district="Várzea",
        city="Recife",
        state="PE"
    )
    print(f"Endereço: {address}")

    # Criando o cliente
    client = Client(
        name="Bruno Silva",
        cpf=cpf,
        date_of_birth=date_of_birth,
        address=address
    )
    print(f"\n{client}")

    # Criando uma conta corrente (Account é abstrata, usamos CheckingAccount)
    from src.entities import CheckingAccount, AccountNumber, AgencyNumber
    
    account = CheckingAccount(
        account_number=AccountNumber(1234),
        agency_number=AgencyNumber(1),
        client=client
    )

    client.add_account(account)

    print("\nContas do cliente:")
    for acc in client.accounts:
        print(acc)