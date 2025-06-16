

import re


class CPF():
    def __init__(self, cpf: str):
        self._cpf: str = None

        self.cpf = cpf

    def _clear_cpf(self, cpf: str) -> str:
        return re.sub(r'\D', '', cpf)

    def _is_valid(self, cpf: str) -> bool:
        # Limpar o CPF para remover tudo que não seja os números
        cpf_raw: str = self._clear_cpf(cpf)

        if len(cpf_raw) != 11: # Total de dígitos é diferente de 11
            return False
        if cpf_raw == cpf_raw[0] * 11: # Todos os números iguais
            return False
        
        # Validação do primeiro dígito
        total_sum = sum(int(num) * weight for num, weight in zip(cpf_raw[:9], range(10, 1, -1)))
        first_digit = (total_sum * 10) % 11
        first_digit = first_digit if first_digit < 10 else 0

        # Validação do segundo dígito
        total_sum = sum(int(num) * weight for num, weight in zip(cpf_raw[:9] + str(first_digit), range(11, 1, -1)))
        second_digit = (total_sum * 10) % 11
        second_digit = second_digit if second_digit < 10 else 0

        return cpf_raw[-2:] == f"{first_digit}{second_digit}"
    
    @property
    def cpf(self, ) -> str:
        return f"{self._cpf[:3]}.{self._cpf[3:6]}.{self._cpf[6:9]}-{self._cpf[9:]}"
   
    @cpf.setter
    def cpf(self, cpf: str):
        if not self._is_valid(cpf): 
            raise ValueError("O CPF informado não é válido")
        self._cpf = self._clear_cpf(cpf)

    def __str__(self, ) -> str:
        return self.cpf
    
    def __eq__(self, value: 'CPF') -> bool:
        return self.cpf == value.cpf