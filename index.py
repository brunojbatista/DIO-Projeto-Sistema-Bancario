from datetime import datetime
import time
import random
import os

LIMIT_PER_WITHDRAWLS = 500
MAX_WITHDRAWLS = 3
PROCESSING_WAITING_TIME_IN_SECONDS = 2
MENU = """
-----------------------------------------------------
Você está no menu do banco XPTO
Escolha uma das opções abaixo:

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

def clear_cmd_line(length: int):
    print('\r' + ' ' * length, end='\r')

class Bank():
    """
    Classe que representa um sistema bancário simples.
    Permite operações de depósito, saque, exibição de extrato e encerramento da conta.
    """

    def __init__(self, ):
        """
        Inicializa a conta bancária com saldo zerado, extrato vazio
        e contador de saques igual a zero.
        """
        self.balance = 0
        self.statement = ""
        self.total_withdrawals = 0

    def add_statement(self, message: str):
        """
        Adiciona uma nova entrada ao extrato bancário com data e hora da operação.

        Parâmetros:
        - message (str): Texto a ser registrado no extrato.
        """
        date_now_string = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        self.statement += message + f" - Horário da Operação em {date_now_string}\n"

    def get_statement(self, ) -> str:
        """
        Retorna o extrato completo da conta.

        Retorna:
        - str: Todas as movimentações registradas até o momento.
        """
        return self.statement

    def deposit(self, ):
        """
        Realiza uma operação de depósito.
        Valida se o valor é numérico e positivo antes de atualizar o saldo.
        Também registra a operação no extrato.
        """
        print("Você escolher a opção de depósito!")
        value = 0
        try:
            value = float(input("Informe o valor do depósito: "))
        except ValueError:
            print("Só é aceito dígitos numéricos na operação!")
            return
        if value <= 0: 
            print("O valor é inválido para deposito")
            return
        operation_info = f'Processando o depósito... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        # Operação de depósito
        self.balance += value
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        # Limpar toda a linha anterior
        clear_cmd_line(len(operation_info))
        print(f"O valor depositado com sucesso!")
        self.add_statement(f"Você depositou R$ {value:.2f}")
        print(f"O seu saldo atual é de: R$ {self.balance:.2f}")
        return True
    
    def withdraw(self, ):
        """
        Realiza uma operação de saque.
        Verifica se:
        - O valor é numérico e positivo.
        - Há saldo suficiente.
        - O valor não excede o limite por saque.
        - O limite de saques diários não foi atingido.
        Atualiza o saldo e registra no extrato, caso aprovado.
        """
        value = 0
        try:
            value = float(input("Informe o valor do saque: "))
        except ValueError:
            print("Só é aceito dígitos numéricos na operação!")
            return
        if value <= 0: 
            print("O valor é inválido para saque")
            return
        elif value > self.balance: 
            print(f"Saldo insucifiente...")
            print(f"Seu saldo atual é de R$ {self.balance:.2f}")
            return
        elif value > LIMIT_PER_WITHDRAWLS: 
            print(f"O valor do saque excede o limite de R$ {LIMIT_PER_WITHDRAWLS}.00")
            return
        elif self.total_withdrawals >= MAX_WITHDRAWLS: 
            print(f"O total de saque excedeu o limite de {MAX_WITHDRAWLS} saques")
            return
        operation_info = f'Processando o saque... Aguarde um momento!'
        print(operation_info, end='', flush=True)
        # Operação de saque
        self.balance -= value
        # Adicionar o total de saques realizados
        self.total_withdrawals += 1
        time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
        # Limpar toda a linha anterior
        clear_cmd_line(len(operation_info))
        print(f"Saque realizado com sucesso!")
        self.add_statement(f"Você sacou R$ {value:.2f}")
        print(f"O seu saldo atual é de: R$ {self.balance:.2f}")
        return True

    def print_account_statement(self, ):
        """
        Exibe todas as movimentações registradas na conta,
        bem como o saldo atual.
        """
        print("\n==================================================")
        print(">> EXTRATO BANCÁRIO:")
        if not self.get_statement(): print("Não há movimentação na conta")
        else: print(self.get_statement())
        print(f"O seu saldo atual é de: R$ {self.balance:.2f}")
        print("==========================================")
        input("Aperte qualquer botão para voltar para o menu.")

    def close_operation(self, ) -> bool:
        """
        Solicita confirmação para encerrar a aplicação bancária.
        
        Retorna:
        - bool: True se o usuário confirmou a saída, False caso contrário.
        """
        print("Você deseja realmente sair da operação? 1 = Sim; 0 = Não")
        option = input("Digite a opção: ")
        if option == '1':
            operation_info = f'Fechando a operação... Aguarde um momento!'
            print(operation_info, end='', flush=True)
            # Operação de fechamento
            time.sleep(PROCESSING_WAITING_TIME_IN_SECONDS)
            # Limpar toda a linha anterior
            clear_cmd_line(len(operation_info))
            print("A operaçao com sua conta fechada com sucesso!")
            return True
        return False
        
bankSystem = Bank()

while True:
    option = input(MENU)
    if option == 'd': bankSystem.deposit()
    elif option == 's': bankSystem.withdraw()
    elif option == "e": bankSystem.print_account_statement()
    elif option == 'q': 
        if bankSystem.close_operation(): break
    else: print("Operação inválida, tente as opções disponíveis por favor!")
