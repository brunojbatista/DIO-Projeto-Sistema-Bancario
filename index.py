MENU_BANK = """
Bem vindo! Por favor escolha uma das opções:

[r] Cadastrar novo cliente
[c] Criar uma conta corrente
[a] Acessar conta
[l] Listar todas as contas
[g] Analisar logs do sistema

=> """

MENU_ACCOUNT = """
Escolha uma das opções abaixo:

[d] Depositar
[s] Sacar
[e] Extrato
[t] Transferir
[l] Limite diário
[q] Sair

=> """

from decimal import Decimal
from src import Bank
from src.entities import AccountNumber, Address, CPF, Client, DateOfBirth
import json
from collections import defaultdict

def carregar_logs(arquivo='log.txt'):
    """
    Carrega os logs do arquivo especificado.
    
    Args:
        arquivo (str): Nome do arquivo de log
        
    Returns:
        list: Lista de dicionários com os logs
    """
    logs = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                line = line.strip()
                if line:
                    try:
                        log_entry = json.loads(line)
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        print(f"⚠️  Erro ao decodificar linha: {line[:50]}...")
    except FileNotFoundError:
        print(f"❌ Arquivo {arquivo} não encontrado")
        return []
    
    return logs

def analisar_logs(logs):
    """
    Analisa os logs e gera estatísticas.
    
    Args:
        logs (list): Lista de logs carregados
        
    Returns:
        dict: Estatísticas dos logs
    """
    if not logs:
        return {}
    
    stats = {
        'total_transacoes': len(logs),
        'por_tipo': defaultdict(int),
        'por_status': defaultdict(int),
        'por_conta': defaultdict(int),
        'por_cliente': defaultdict(int),
        'duracao_media': 0,
        'transacoes_sucesso': 0,
        'transacoes_erro': 0
    }
    
    total_duracao = 0
    
    for log in logs:
        # Contagem por tipo
        stats['por_tipo'][log.get('transaction_type', 'Desconhecido')] += 1
        
        # Contagem por status
        status = log.get('status', 'Desconhecido')
        stats['por_status'][status] += 1
        
        if status == 'Sucesso':
            stats['transacoes_sucesso'] += 1
        else:
            stats['transacoes_erro'] += 1
        
        # Contagem por conta
        if 'account_number' in log:
            stats['por_conta'][log['account_number']] += 1
        
        # Contagem por cliente
        if 'client_name' in log:
            stats['por_cliente'][log['client_name']] += 1
        
        # Duração
        duracao = log.get('duration_seconds', 0)
        total_duracao += duracao
    
    if logs:
        stats['duracao_media'] = total_duracao / len(logs)
    
    return stats

def exibir_estatisticas(stats):
    """
    Exibe as estatísticas dos logs de forma organizada.
    
    Args:
        stats (dict): Estatísticas dos logs
    """
    if not stats:
        print("❌ Nenhuma estatística disponível")
        return
    
    print("\n📊 ESTATÍSTICAS DOS LOGS")
    print("=" * 50)
    
    print(f"📈 Total de transações: {stats['total_transacoes']}")
    print(f"✅ Transações com sucesso: {stats['transacoes_sucesso']}")
    print(f"❌ Transações com erro: {stats['transacoes_erro']}")
    print(f"⏱️  Duração média: {stats['duracao_media']:.3f} segundos")
    
    print("\n🏦 Transações por tipo:")
    for tipo, quantidade in stats['por_tipo'].items():
        print(f"   {tipo}: {quantidade}")
    
    print("\n👤 Transações por cliente:")
    for cliente, quantidade in stats['por_cliente'].items():
        print(f"   {cliente}: {quantidade}")
    
    print("\n🏛️  Transações por conta:")
    for conta, quantidade in stats['por_conta'].items():
        print(f"   {conta}: {quantidade}")

def exibir_logs_recentes(logs, quantidade=5):
    """
    Exibe os logs mais recentes.
    
    Args:
        logs (list): Lista de logs
        quantidade (int): Número de logs a exibir
    """
    if not logs:
        print("❌ Nenhum log disponível")
        return
    
    print(f"\n📋 ÚLTIMAS {quantidade} TRANSAÇÕES")
    print("=" * 50)
    
    logs_recentes = logs[-quantidade:]
    
    for i, log in enumerate(logs_recentes, 1):
        timestamp = log.get('timestamp', 'N/A')
        tipo = log.get('transaction_type', 'N/A')
        status = log.get('status', 'N/A')
        cliente = log.get('client_name', 'N/A')
        valor = log.get('transaction_value', 'N/A')
        
        print(f"{i}. {timestamp} | {tipo} | {status} | {cliente} | R$ {valor}")

def filtrar_logs_por_tipo(logs, tipo):
    """
    Filtra logs por tipo de transação.
    
    Args:
        logs (list): Lista de logs
        tipo (str): Tipo de transação para filtrar
        
    Returns:
        list: Logs filtrados
    """
    return [log for log in logs if log.get('transaction_type') == tipo]

def filtrar_logs_por_cliente(logs, cliente):
    """
    Filtra logs por cliente.
    
    Args:
        logs (list): Lista de logs
        cliente (str): Nome do cliente para filtrar
        
    Returns:
        list: Logs filtrados
    """
    return [log for log in logs if log.get('client_name') == cliente]

def menu_analisador_logs():
    """
    Menu do analisador de logs integrado ao sistema bancário.
    """
    print("\n🔍 ANALISADOR DE LOGS DO SISTEMA BANCÁRIO")
    print("=" * 60)
    
    # Carregar logs
    logs = carregar_logs()
    
    if not logs:
        print("❌ Nenhum log encontrado. Execute algumas transações primeiro.")
        return
    
    # Analisar logs
    stats = analisar_logs(logs)
    
    # Exibir estatísticas
    exibir_estatisticas(stats)
    
    # Exibir logs recentes
    exibir_logs_recentes(logs, 10)
    
    # Menu de opções
    while True:
        print("\n" + "=" * 50)
        print("🎯 OPÇÕES DE ANÁLISE:")
        print("1. Ver logs de depósitos")
        print("2. Ver logs de saques")
        print("3. Ver logs de transferências")
        print("4. Ver logs de um cliente específico")
        print("5. Ver logs de uma conta específica")
        print("6. Ver logs com erro")
        print("0. Voltar ao menu principal")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '0':
            print("👋 Voltando ao menu principal...")
            break
        elif opcao == '1':
            logs_depositos = filtrar_logs_por_tipo(logs, 'Deposit')
            print(f"\n💰 LOGS DE DEPÓSITOS ({len(logs_depositos)} transações):")
            for log in logs_depositos:
                print(f"   {log['timestamp']} | {log['client_name']} | R$ {log['transaction_value']} | {log['status']}")
        elif opcao == '2':
            logs_saques = filtrar_logs_por_tipo(logs, 'Withdraw')
            print(f"\n💸 LOGS DE SAQUES ({len(logs_saques)} transações):")
            for log in logs_saques:
                print(f"   {log['timestamp']} | {log['client_name']} | R$ {log['transaction_value']} | {log['status']}")
        elif opcao == '3':
            logs_transferencias = filtrar_logs_por_tipo(logs, 'Transfer')
            print(f"\n🔄 LOGS DE TRANSFERÊNCIAS ({len(logs_transferencias)} transações):")
            for log in logs_transferencias:
                print(f"   {log['timestamp']} | {log['client_name']} → {log.get('destination_client', 'N/A')} | R$ {log['transaction_value']} | {log['status']}")
        elif opcao == '4':
            cliente = input("Digite o nome do cliente: ").strip()
            logs_cliente = filtrar_logs_por_cliente(logs, cliente)
            if logs_cliente:
                print(f"\n👤 LOGS DO CLIENTE {cliente} ({len(logs_cliente)} transações):")
                for log in logs_cliente:
                    print(f"   {log['timestamp']} | {log['transaction_type']} | R$ {log['transaction_value']} | {log['status']}")
            else:
                print(f"❌ Nenhum log encontrado para o cliente {cliente}")
        elif opcao == '5':
            conta = input("Digite o número da conta: ").strip()
            logs_conta = [log for log in logs if log.get('account_number') == conta]
            if logs_conta:
                print(f"\n🏦 LOGS DA CONTA {conta} ({len(logs_conta)} transações):")
                for log in logs_conta:
                    print(f"   {log['timestamp']} | {log['transaction_type']} | R$ {log['transaction_value']} | {log['status']}")
            else:
                print(f"❌ Nenhum log encontrado para a conta {conta}")
        elif opcao == '6':
            logs_erro = [log for log in logs if log.get('status') != 'Sucesso']
            if logs_erro:
                print(f"\n❌ LOGS COM ERRO ({len(logs_erro)} transações):")
                for log in logs_erro:
                    print(f"   {log['timestamp']} | {log['transaction_type']} | {log['client_name']} | {log.get('error_message', 'Erro desconhecido')}")
            else:
                print("✅ Nenhum erro encontrado nos logs")
        else:
            print("❌ Opção inválida!")

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
            elif option_account == 'l':
                print("\n📊 INFORMAÇÕES DO LIMITE DIÁRIO")
                print("-" * 40)
                daily_count = account.get_daily_transactions_count()
                remaining = account.get_remaining_daily_transactions()
                print(f"Transações realizadas hoje: {daily_count}")
                print(f"Transações restantes: {remaining}")
                print(f"Limite diário: 10 transações")
                if remaining == 0:
                    print("⚠️  Você atingiu o limite diário de transações!")
                elif remaining <= 2:
                    print("⚠️  Atenção: Poucas transações restantes para hoje!")
                else:
                    print("✅ Você ainda pode realizar transações hoje.")
                print("-" * 40)
            elif option_account == 'q':
                print("Você saiu do menu da sua conta bancária!")
                break
    elif option_bank == 'l':
        print("\n📊 LISTANDO TODAS AS CONTAS DO BANCO")
        print("=" * 80)
        
        if not bank.accounts:
            print("Nenhuma conta cadastrada no banco.")
        else:
            accounts_iterator = bank.get_accounts_iterator()
            print(f"Total de contas: {len(accounts_iterator)}")
            print("-" * 80)
            
            for i, account_info in enumerate(accounts_iterator, 1):
                formatted_info = accounts_iterator.get_account_info_formatted(account_info)
                print(f"{i:2d}. {formatted_info}")
            
            print("-" * 80)
            print("✅ Listagem concluída!")
    elif option_bank == 'g':
        menu_analisador_logs()
    else:
        print("Operação inválida, tente as opções disponíveis por favor!")