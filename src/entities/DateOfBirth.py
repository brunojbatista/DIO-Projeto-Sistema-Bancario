import datetime

class DateOfBirth:
    """
    Classe que representa uma data de nascimento.

    Armazena a data como um objeto `datetime` e fornece métodos para
    configuração e formatação da data a partir de uma string.
    """

    def __init__(self, date_str: str):
        """
        Inicializa a instância da classe com uma data no formato string.

        Args:
            date_str (str): Data de nascimento no formato "dd/mm/yyyy".
        """
        self._date: datetime.datetime = None
        self.date = date_str

    @property
    def date(self):
        """
        Retorna a data de nascimento como objeto `datetime`.

        Returns:
            datetime.datetime: Data armazenada.
        """
        return self._date

    @date.setter
    def date(self, date: str):
        """
        Define a data de nascimento a partir de uma string.

        Args:
            date (str): Data no formato "dd/mm/yyyy".

        Raises:
            ValueError: Se o formato da data for inválido.
        """
        self._date = datetime.datetime.strptime(date, "%d/%m/%Y")

    def __str__(self):
        """
        Retorna a data formatada como string no formato "dd/mm/yyyy".

        Returns:
            str: Representação formatada da data.
        """
        return datetime.datetime.strftime(self.date, "%d/%m/%Y")
