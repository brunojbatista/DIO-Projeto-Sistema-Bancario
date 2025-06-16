class Address:
    """
    Representa um endereço com informações como rua, número, bairro, cidade e estado.
    """

    def __init__(self, street: str, number: str, district: str, city: str, state: str):
        """
        Inicializa uma instância de Address com os dados fornecidos.

        Args:
            street (str): Nome da rua.
            number (str): Número do endereço.
            district (str): Bairro.
            city (str): Cidade.
            state (str): Estado.
        """
        self._street: str = None
        self._number: str = None
        self._district: str = None
        self._city: str = None
        self._state: str = None

        self.street = street
        self.number = number
        self.district = district
        self.city = city
        self.state = state

    @property
    def street(self) -> str:
        """
        Retorna o nome da rua.

        Returns:
            str: Rua do endereço.
        """
        return self._street

    @street.setter
    def street(self, street: str):
        """
        Define o nome da rua.

        Args:
            street (str): Nome da rua.
        """
        self._street = street

    @property
    def number(self) -> str:
        """
        Retorna o número do endereço.

        Returns:
            str: Número.
        """
        return self._number

    @number.setter
    def number(self, number: str):
        """
        Define o número do endereço.

        Args:
            number (str): Número do endereço.
        """
        self._number = number

    @property
    def district(self) -> str:
        """
        Retorna o bairro do endereço.

        Returns:
            str: Bairro.
        """
        return self._district

    @district.setter
    def district(self, district: str):
        """
        Define o bairro do endereço.

        Args:
            district (str): Bairro.
        """
        self._district = district

    @property
    def city(self) -> str:
        """
        Retorna a cidade do endereço.

        Returns:
            str: Cidade.
        """
        return self._city

    @city.setter
    def city(self, city: str):
        """
        Define a cidade do endereço.

        Args:
            city (str): Cidade.
        """
        self._city = city

    @property
    def state(self) -> str:
        """
        Retorna o estado do endereço.

        Returns:
            str: Estado.
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """
        Define o estado do endereço.

        Args:
            state (str): Estado.
        """
        self._state = state

    def __str__(self) -> str:
        """
        Retorna uma representação textual completa do endereço.

        Returns:
            str: Endereço formatado.
        """
        return f"{self.street}, nº {self.number}, {self.district} - {self.city}/{self.state}"
