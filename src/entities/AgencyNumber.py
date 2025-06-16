
TOTAL_DIGITS_AGENCY_NUMBER = 4
MAX_AGENCY_NUMBER = 10000

class AgencyNumber():
    def __init__(self, agency_number: str | int):
        self._agency_number: int = None

        self.agency_number = agency_number

    @property
    def agency_number(self):
        return str(self._agency_number).zfill(TOTAL_DIGITS_AGENCY_NUMBER)

    @agency_number.setter
    def agency_number(self, agency_number: str | int):
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
            raise ValueError("É esperado que a número da agência seja inteiro ou string")

    def __str__(self) -> str:
        return self.agency_number

    def __eq__(self, value: 'AgencyNumber') -> bool:
        return self.agency_number == value.agency_number