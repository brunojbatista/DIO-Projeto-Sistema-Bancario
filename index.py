MENU_UNLOGGED = """
Bem vindo! Por favor escolha uma das opções:

[e] Entrar na conta
[c] Criar uma conta corrente

=> """

MENU_LOGGED = """
Você está no menu do banco XPTO
Escolha uma das opções abaixo:

[d] Depositar
[s] Sacar
[e] Extrato
[t] Transferir
[q] Sair

=> """

from Bank import Bank
        
bank: Bank = Bank()

while True:
    print("="*80)
    option_unlogged = input(MENU_UNLOGGED).strip()
    if option_unlogged == 'e':
        client_cpf = input("Digite seu CPF: ")
        if not bank.sing_in_account(client_cpf):
            print("Usuário informado inexistente")
            continue
        while True:
            print("-----------------------------------------------------")
            option_logged = input(MENU_LOGGED).strip()
            if option_logged == 'd': bank.deposit_operation()
            elif option_logged == 's': bank.withdraw_operation()
            elif option_logged == "e": bank.show_account_information()
            elif option_logged == "t": bank.transfer_operation()
            elif option_logged == 'q': 
                if bank.close_operation(): 
                    break
            else: print("Operação inválida, tente as opções disponíveis por favor!")
    elif option_unlogged == 'c':
        client_name = input("Digite seu Nome: ").strip()
        client_cpf = input("Digite seu CPF: ").strip()
        client_date_of_birth = input("Digite sua data de nascimento: ").strip()
        client_address = input("Digite seu endereço: ").strip()
        if not bank.create_checking_account(client_name, client_cpf, client_date_of_birth, client_address):
            continue
        print("Conta criada com sucesso!")
    else:
        print("Operação inválida, tente as opções disponíveis por favor!")
