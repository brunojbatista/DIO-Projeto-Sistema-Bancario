

class Address():
    def __init__(self, street: str, number: str, district: str, city: str, state: str):
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
    def street(self):
        return self._street
    
    @street.setter
    def street(self, street: str):
        self._street = street

    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, number: str):
        self._number = number

    @property
    def district(self):
        return self._district
    
    @district.setter
    def district(self, district: str):
        self._district = district

    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, city: str):
        self._city = city

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state: str):
        self._state = state

    def __str__(self):
        return f"{self.street}, nº {self.number}, {self.district} - {self.city}/{self.state}"