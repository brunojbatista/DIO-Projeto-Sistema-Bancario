from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
import time
from typing import List, TYPE_CHECKING

from src import round_decimal, clear_cmd_line
from src.entities import AccountNumber, AgencyNumber

if TYPE_CHECKING:
    from src.entities import Client, Transaction, Deposit, Withdraw, Transfer

LIMIT_PER_WITHDRAWLS = Decimal('500.00')
MAX_WITHDRAWLS = 3
MAX_DAILY_TRANSACTIONS = 10
DEFAULT_DECIMAL_PLACES = 2
PROCESSING_WAITING_TIME_IN_SECONDS = 2

class Account:
    """
    Classe que representa uma conta bancária.

    Fornece métodos para operações comuns como depósito, saque, transferência,
    geração de extrato e manipulação de saldo.
    """

    def __init__(self, account_number: AccountNumber, agency_number: AgencyNumber, client: Client):
        """
        Inicializa uma nova conta com saldo zero e extrato vazio.

        Args:
            account_number (AccountNumber): Número da conta.
            agency_number (AgencyNumber): Número da agência.
            client (Client): Cliente associado à conta.
        """
        self._account_number: AccountNumber = None
        self._agency_number: AgencyNumber = None
        self._client: Client = None
        self._balance: Decimal = None
        self._transactions: List[Transaction] = None
        self._total_withdrawl: int = None

        self.account_number = account_number
        self.agency_number = agency_number
        self.client = client
        self.balance = Decimal('0')
        self.transactions = []
        self.total_withdrawl = 0

    @property
    def account_number(self) -> AccountNumber:
        """Retorna o número da conta."""
        return self._account_number

    @account_number.setter
    def account_number(self, account_number: AccountNumber):
        self._account_number = account_number

    @property
    def agency_number(self) -> AgencyNumber:
        """Retorna o número da agência."""
        return self._agency_number

    @agency_number.setter
    def agency_number(self, agency_number: AgencyNumber):
        self._agency_number = agency_number

    @property
    def client(self) -> Client:
        """Retorna o cliente associado à conta."""
        return self._client

    @client.setter
    def client(self, client: Client):
        self._client = client

    @property
    def balance(self) -> Decimal:
        """Retorna o saldo atual da conta."""
        return self._balance

    @balance.setter
    def balance(self, balance: Decimal):
        self._balance = balance

    @property
    def transactions(self) -> List[Transaction]:
        """Retorna a lista de transações da conta."""
        return self._transactions

    @transactions.setter
    def transactions(self, transactions: List[Transaction]):
        self._transactions = transactions

    @property
    def total_withdrawl(self) -> int:
        """Retorna o total de saques realizados."""
        return self._total_withdrawl

    @total_withdrawl.setter
    def total_withdrawl(self, total_withdrawl: int):
        self._total_withdrawl = total_withdrawl

    def add_transaction(self, transaction: Transaction):
        """
        Adiciona uma transação à lista de transações da conta.

        Args:
            transaction (Transaction): A transação a ser adicionada.
        """
        self.transactions.append(transaction)

    def get_daily_transactions_count(self, date: datetime = None) -> int:
        """
        Conta o número de transações realizadas em uma data específica.
        
        Args:
            date (datetime, optional): Data para verificar. Se None, usa a data atual.
            
        Returns:
            int: Número de transações na data especificada.
        """
        if date is None:
            date = datetime.now()
        
        # Normaliza a data para comparar apenas dia/mês/ano
        target_date = date.date()
        
        count = 0
        for transaction in self.transactions:
            if hasattr(transaction, '_timestamp') and transaction._timestamp:
                transaction_date = transaction._timestamp.date()
                if transaction_date == target_date:
                    count += 1
        
        return count

    def can_perform_transaction_today(self) -> bool:
        """
        Verifica se a conta pode realizar uma nova transação hoje.
        
        Returns:
            bool: True se pode realizar transação, False se atingiu o limite diário.
        """
        daily_count = self.get_daily_transactions_count()
        return daily_count < MAX_DAILY_TRANSACTIONS

    def get_remaining_daily_transactions(self) -> int:
        """
        Retorna o número de transações restantes para hoje.
        
        Returns:
            int: Número de transações que ainda podem ser realizadas hoje.
        """
        daily_count = self.get_daily_transactions_count()
        return max(0, MAX_DAILY_TRANSACTIONS - daily_count)

    def iterate_transactions(self, transaction_type: str = None):
        """
        Gerador que itera sobre as transações da conta com filtro opcional por tipo.
        
        Args:
            transaction_type (str, optional): Tipo de transação para filtrar.
                Valores aceitos: 'deposit', 'withdraw', 'transfer', None (todos)
                
        Yields:
            Transaction: Transação da conta que atende ao filtro.
        """
        from src.entities import Deposit, Withdraw, Transfer
        
        # Mapeamento de tipos para classes
        type_mapping = {
            'deposit': Deposit,
            'withdraw': Withdraw,
            'transfer': Transfer
        }
        
        # Se não foi especificado tipo, retorna todas as transações
        if transaction_type is None:
            for transaction in self.transactions:
                yield transaction
            return
        
        # Converte para lowercase para facilitar comparação
        transaction_type = transaction_type.lower()
        
        # Verifica se o tipo é válido
        if transaction_type not in type_mapping:
            valid_types = list(type_mapping.keys()) + ['None']
            raise ValueError(f"Tipo de transação inválido. Tipos válidos: {valid_types}")
        
        # Filtra transações pelo tipo especificado
        target_class = type_mapping[transaction_type]
        for transaction in self.transactions:
            if isinstance(transaction, target_class):
                yield transaction

    def add_extract(self, message: str):
        """
        Adiciona uma entrada ao extrato com a data e saldo atual.
        Método mantido para compatibilidade, mas agora usa transações.

        Args:
            message (str): Mensagem descritiva da operação.
        """
        # Este método agora é usado apenas para compatibilidade
        # As transações são adicionadas diretamente via add_transaction
        pass

    def generate_extract_information_text(self) -> str:
        """
        Gera uma string com todas as operações registradas no extrato.

        Returns:
            str: Texto formatado do extrato bancário.
        """
        if not self.transactions:
            return "Extrato Bancário:\n\n-- Nenhuma movimentação --"
        
        extract_text = "Extrato Bancário:\n\n"
        current_balance = Decimal('0')  # Começa com saldo zero
        
        for transaction in self.transactions:
            # Usa o timestamp da transação se disponível, senão usa o momento atual
            if hasattr(transaction, '_timestamp') and transaction._timestamp:
                date_string = transaction._timestamp.strftime("%d/%m/%Y às %H:%M:%S")
            else:
                date_string = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            
            # Calcula o saldo após esta transação
            from src.entities import Deposit, Withdraw, Transfer
            if isinstance(transaction, Deposit):
                current_balance += transaction.value
            elif isinstance(transaction, Withdraw):
                current_balance -= transaction.value
            elif isinstance(transaction, Transfer):
                if transaction.account == self:  # Conta de origem
                    current_balance -= transaction.value
                else:  # Conta de destino
                    current_balance += transaction.value
            
            # Gera descrição específica para cada tipo de transação
            if hasattr(transaction, 'get_description_for_account'):
                # Para transferências
                description = transaction.get_description_for_account(self)
            else:
                # Para depósitos e saques
                description = str(transaction)
            
            full_message = (f"{description} => Saldo após operação R$ "
                            f"{round_decimal(current_balance, DEFAULT_DECIMAL_PLACES)}"
                            f" - Realizado em {date_string}\n")
            extract_text += full_message
        
        return extract_text

    def generate_account_information_text(self) -> str:
        """
        Gera uma string com as informações da conta e seu extrato.

        Returns:
            str: Informações formatadas da conta.
        """
        text = f"Número da conta: {str(self.account_number)}\n"
        text += f"Número da agência: {self.agency_number}\n"
        text += f"O saldo de sua conta é R$ {round_decimal(self.balance, DEFAULT_DECIMAL_PLACES)}\n"
        text += self.generate_extract_information_text()
        return text

    def add_balance(self, value: Decimal):
        """Adiciona um valor ao saldo da conta."""
        self.balance += value

    def sub_balance(self, value: Decimal):
        """Subtrai um valor do saldo da conta."""
        self.add_balance(-value)

    def add_total_withdrawl(self, total: int = 1):
        """Incrementa o total de saques realizados."""
        self.total_withdrawl += total

    def withdraw(self, value: Decimal) -> Decimal:
        """
        Realiza um saque usando a classe Withdraw.

        Args:
            value (Decimal): Valor a ser sacado.

        Raises:
            ValueError: Caso o valor seja inválido, saldo insuficiente, ultrapasse o limite de saque,
                        o número máximo de saques permitido ou o limite diário de transações.

        Returns:
            Decimal: Valor sacado, se bem-sucedido.
        """
        # Verifica limite diário de transações
        if not self.can_perform_transaction_today():
            daily_count = self.get_daily_transactions_count()
            raise ValueError(f"Limite diário de transações excedido! "
                           f"Você já realizou {daily_count} transações hoje. "
                           f"Limite máximo: {MAX_DAILY_TRANSACTIONS} transações por dia.")
        
        from src.entities import Withdraw
        withdraw_transaction = Withdraw(self, value)
        success = withdraw_transaction.execute()
        if not success:
            raise ValueError("Falha ao realizar saque")
        
        # Adiciona a transação à lista
        self.add_transaction(withdraw_transaction)
        return value

    def deposit(self, value: Decimal):
        """
        Realiza um depósito na conta usando a classe Deposit.

        Args:
            value (Decimal): Valor a ser depositado.

        Raises:
            ValueError: Se o valor for menor ou igual a zero ou se o limite diário de transações for excedido.
        """
        # Verifica limite diário de transações
        if not self.can_perform_transaction_today():
            daily_count = self.get_daily_transactions_count()
            raise ValueError(f"Limite diário de transações excedido! "
                           f"Você já realizou {daily_count} transações hoje. "
                           f"Limite máximo: {MAX_DAILY_TRANSACTIONS} transações por dia.")
        
        from src.entities import Deposit
        deposit_transaction = Deposit(self, value)
        success = deposit_transaction.execute()
        if not success:
            raise ValueError("Falha ao realizar depósito")
        
        # Adiciona a transação à lista
        self.add_transaction(deposit_transaction)

    def transfer(self, value: Decimal, account_of_receipt: 'Account') -> bool:
        """
        Realiza uma transferência entre contas usando a classe Transfer.

        Args:
            value (Decimal): Valor a ser transferido.
            account_of_receipt (Account): Conta destino.

        Returns:
            bool: True se bem-sucedido.

        Raises:
            ValueError: Em caso de valor inválido, saldo insuficiente, contas iguais ou limite diário excedido.
        """
        # Verifica limite diário de transações
        if not self.can_perform_transaction_today():
            daily_count = self.get_daily_transactions_count()
            raise ValueError(f"Limite diário de transações excedido! "
                           f"Você já realizou {daily_count} transações hoje. "
                           f"Limite máximo: {MAX_DAILY_TRANSACTIONS} transações por dia.")
        
        from src.entities import Transfer
        transfer_transaction = Transfer(self, account_of_receipt, value)
        success = transfer_transaction.execute()
        if not success:
            raise ValueError("Falha ao realizar transferência")
        
        # Adiciona a transação à lista da conta de origem
        self.add_transaction(transfer_transaction)
        return True

    def show_extract(self):
        """Exibe o extrato formatado no terminal."""
        print("="*50)
        print(self.generate_extract_information_text())

    def __eq__(self, value: 'Account') -> bool:
        """
        Compara duas contas pela combinação de número e agência.

        Args:
            value (Account): Conta a ser comparada.

        Returns:
            bool: True se forem a mesma conta.
        """
        return self.account_number == value.account_number and self.agency_number == value.agency_number

    def __str__(self) -> str:
        """
        Retorna a representação textual da conta com extrato.

        Returns:
            str: Informações completas da conta.
        """
        return self.generate_account_information_text()
