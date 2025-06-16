TOTAL_DIGITS_ACCOUNT_NUMBER = 8
MAX_ACCOUNT_NUMBER = 100000000

class AccountNumber:
    """
    Representa o número de uma conta bancária, garantindo um formato fixo com validação.

    O número pode ser fornecido como string ou inteiro, sendo armazenado com preenchimento
    de zeros à esquerda para totalizar 8 dígitos.
    """

    def __init__(self, account_number: str | int):
        """
        Inicializa uma instância de AccountNumber com validação de tamanho.

        Args:
            account_number (str | int): Número da conta como string ou inteiro.

        Raises:
            ValueError: Se o número for inválido.
        """
        self._account_number: int = None
        self.account_number = account_number

    @property
    def account_number(self) -> str:
        """
        Retorna o número da conta formatado com zeros à esquerda.

        Returns:
            str: Número da conta formatado (8 dígitos).
        """
        return str(self._account_number).zfill(TOTAL_DIGITS_ACCOUNT_NUMBER)

    @account_number.setter
    def account_number(self, account_number: str | int):
        """
        Define e valida o número da conta.

        Args:
            account_number (str | int): Número da conta como string ou inteiro.

        Raises:
            ValueError: Se o número exceder o limite ou tiver formato inválido.
        """
        if isinstance(account_number, int):
            if account_number >= MAX_ACCOUNT_NUMBER:
                raise ValueError("O número da conta é inválido")
            self._account_number = account_number
        elif isinstance(account_number, str):
            account_number = str(account_number).zfill(TOTAL_DIGITS_ACCOUNT_NUMBER)
            if len(account_number) != TOTAL_DIGITS_ACCOUNT_NUMBER:
                raise ValueError("O número da conta é inválido")
            self._account_number = int(account_number)
        else:
            raise ValueError("É esperado que o número da conta seja inteiro ou string")

    def __str__(self) -> str:
        """
        Retorna a representação em string do número da conta.

        Returns:
            str: Número da conta formatado.
        """
        return self.account_number

    def __eq__(self, value: 'AccountNumber') -> bool:
        """
        Compara dois objetos AccountNumber.

        Args:
            value (AccountNumber): Outro objeto AccountNumber para comparar.

        Returns:
            bool: True se forem iguais, False caso contrário.
        """
        return self.account_number == value.account_number
