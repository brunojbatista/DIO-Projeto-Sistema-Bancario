import re

class CPF:
    """
    Classe que representa e valida um CPF (Cadastro de Pessoa Física) brasileiro.

    A classe armazena o CPF de forma segura, realiza validação automática 
    durante a atribuição e fornece acesso ao valor formatado.
    """

    def __init__(self, cpf: str):
        """
        Inicializa a instância com o CPF fornecido.

        Args:
            cpf (str): CPF a ser atribuído no formato livre (com ou sem pontuação).

        Raises:
            ValueError: Se o CPF for inválido.
        """
        self._cpf: str = None
        self.cpf = cpf

    def _clear_cpf(self, cpf: str) -> str:
        """
        Remove todos os caracteres não numéricos do CPF.

        Args:
            cpf (str): CPF no formato livre.

        Returns:
            str: CPF contendo apenas os números.
        """
        return re.sub(r'\D', '', cpf)

    def _is_valid(self, cpf: str) -> bool:
        """
        Verifica se um CPF é válido conforme a regra de formação dos dígitos verificadores.

        Args:
            cpf (str): CPF a ser validado.

        Returns:
            bool: True se o CPF for válido, False caso contrário.
        """
        cpf_raw: str = self._clear_cpf(cpf)

        if len(cpf_raw) != 11:
            return False
        if cpf_raw == cpf_raw[0] * 11:
            return False

        # Primeiro dígito verificador
        total_sum = sum(int(num) * weight for num, weight in zip(cpf_raw[:9], range(10, 1, -1)))
        first_digit = (total_sum * 10) % 11
        first_digit = first_digit if first_digit < 10 else 0

        # Segundo dígito verificador
        total_sum = sum(int(num) * weight for num, weight in zip(cpf_raw[:9] + str(first_digit), range(11, 1, -1)))
        second_digit = (total_sum * 10) % 11
        second_digit = second_digit if second_digit < 10 else 0

        return cpf_raw[-2:] == f"{first_digit}{second_digit}"

    @property
    def cpf(self) -> str:
        """
        Retorna o CPF formatado com pontuação.

        Returns:
            str: CPF no formato xxx.xxx.xxx-xx.
        """
        return f"{self._cpf[:3]}.{self._cpf[3:6]}.{self._cpf[6:9]}-{self._cpf[9:]}"

    @cpf.setter
    def cpf(self, cpf: str):
        """
        Define o CPF após validar e limpar os dados.

        Args:
            cpf (str): CPF a ser atribuído.

        Raises:
            ValueError: Se o CPF for inválido.
        """
        if not self._is_valid(cpf):
            raise ValueError("O CPF informado não é válido")
        self._cpf = self._clear_cpf(cpf)

    def __str__(self) -> str:
        """
        Retorna o CPF formatado ao usar a função str().

        Returns:
            str: CPF formatado.
        """
        return self.cpf

    def __eq__(self, value: 'CPF') -> bool:
        """
        Verifica igualdade entre dois objetos CPF.

        Args:
            value (CPF): Outro CPF a ser comparado.

        Returns:
            bool: True se os dois CPFs forem iguais.
        """
        return self.cpf == value.cpf
