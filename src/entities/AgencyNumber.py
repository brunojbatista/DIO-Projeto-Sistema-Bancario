TOTAL_DIGITS_AGENCY_NUMBER = 4
MAX_AGENCY_NUMBER = 10000

class AgencyNumber:
    """
    Representa o número de uma agência bancária.

    Garante que o número da agência tenha 4 dígitos, seja válido dentro de um limite definido
    e possa ser informado como `str` ou `int`.
    """

    def __init__(self, agency_number: str | int):
        """
        Inicializa um número de agência com validação.

        Args:
            agency_number (str | int): Número da agência como string ou inteiro.

        Raises:
            ValueError: Se o número não for válido ou exceder os limites definidos.
        """
        self._agency_number: int = None
        self.agency_number = agency_number

    @property
    def agency_number(self) -> str:
        """
        Retorna o número da agência como uma string com zero à esquerda.

        Returns:
            str: Número da agência formatado com 4 dígitos.
        """
        return str(self._agency_number).zfill(TOTAL_DIGITS_AGENCY_NUMBER)

    @agency_number.setter
    def agency_number(self, agency_number: str | int):
        """
        Define o número da agência após realizar validações.

        Args:
            agency_number (str | int): Número a ser configurado.

        Raises:
            ValueError: Se o valor for inválido ou exceder o número máximo permitido.
        """
        if isinstance(agency_number, int):
            if agency_number >= MAX_AGENCY_NUMBER:
                raise ValueError("O número da agência é inválido")
            self._agency_number = agency_number
        elif isinstance(agency_number, str):
            agency_number = str(agency_number).zfill(TOTAL_DIGITS_AGENCY_NUMBER)
            if len(agency_number) != TOTAL_DIGITS_AGENCY_NUMBER:
                raise ValueError("O número da agência é inválido")
            self._agency_number = int(agency_number)
        else:
            raise ValueError("É esperado que o número da agência seja inteiro ou string")

    def __str__(self) -> str:
        """
        Retorna a representação textual do número da agência.

        Returns:
            str: Número da agência com 4 dígitos.
        """
        return self.agency_number

    def __eq__(self, value: 'AgencyNumber') -> bool:
        """
        Compara dois objetos AgencyNumber para verificar igualdade.

        Args:
            value (AgencyNumber): Outro número de agência.

        Returns:
            bool: True se forem iguais, False caso contrário.
        """
        return self.agency_number == value.agency_number
