
TOTAL_DIGITS_ACCOUNT_NUMBER = 8
MAX_ACCOUNT_NUMBER = 100000000

class AccountNumber():
    def __init__(self, account_number: str | int):
        self._account_number: int = None

        self.account_number = account_number

    @property
    def account_number(self):
        return str(self._account_number).zfill(TOTAL_DIGITS_ACCOUNT_NUMBER)

    @account_number.setter
    def account_number(self, account_number: str | int):
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
            raise ValueError("É esperado que a número da conta seja inteiro ou string")

    def __str__(self) -> str:
        return self.account_number

    def __eq__(self, value: 'AccountNumber') -> bool:
        return self.account_number == value.account_number