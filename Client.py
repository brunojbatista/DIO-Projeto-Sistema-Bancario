import re
from Utils import is_valid_cpf

class Client:
    """
    Representa um cliente bancário com CPF e nome associados.

    Esta classe fornece métodos para definir e obter os dados de um cliente,
    validando o CPF durante a inicialização. Também permite a comparação entre
    objetos com base no CPF e exibe uma representação textual do cliente.

    Atributos:
        cpf (str): CPF do cliente (validado no formato 000.000.000-00).
        name (str): Nome do cliente.
    """

    def __init__(self, cpf: str, name: str):
        """
        Inicializa um cliente com CPF e nome, validando o CPF.

        Args:
            cpf (str): CPF do cliente.
            name (str): Nome do cliente.

        Raises:
            ValueError: Se o CPF fornecido estiver em formato inválido.
        """
        self.cpf: str = None
        self.name: str = None

        self.set_cpf(cpf)
        self.set_name(name)

    def set_cpf(self, cpf: str):
        """
        Define o CPF do cliente após validar seu formato.

        Args:
            cpf (str): CPF no formato 000.000.000-00.

        Raises:
            ValueError: Se o CPF estiver em formato inválido.
        """
        if not is_valid_cpf(cpf):
            raise ValueError("O CPF informado é inválido")
        self.cpf = cpf

    def set_name(self, name: str):
        """
        Define o nome do cliente.

        Args:
            name (str): Nome completo do cliente.
        """
        self.name = name

    def get_cpf(self) -> str:
        """
        Retorna o CPF do cliente.

        Returns:
            str: CPF do cliente.
        """
        return self.cpf

    def get_name(self) -> str:
        """
        Retorna o nome do cliente.

        Returns:
            str: Nome do cliente.
        """
        return self.name

    def __str__(self) -> str:
        """
        Retorna a representação textual do cliente.

        Returns:
            str: Nome e CPF formatados do cliente.
        """
        return f"Cliente: {self.get_name()} e CPF: {self.get_cpf()}"

    def __eq__(self, value):
        """
        Compara dois clientes com base no CPF.

        Args:
            value (Client): Outro objeto a ser comparado.

        Returns:
            bool: True se os CPFs forem iguais, False caso contrário.
        """
        return value.get_cpf() == self.get_cpf()
