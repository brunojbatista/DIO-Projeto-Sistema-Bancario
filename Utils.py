from decimal import ROUND_HALF_UP, Decimal
import re

def clear_cmd_line(length: int):
    """
    Limpa a linha atual no terminal imprimindo espaços em branco.

    Args:
        length (int): Número de caracteres a sobrescrever com espaço.
    """
    print('\r' + ' ' * length, end='\r')


def is_valid_cpf(cpf: str) -> bool:
    """
    Verifica se um CPF está no formato válido.

    Formato aceito: '000.000.000-00'

    Args:
        cpf (str): CPF a ser validado.

    Returns:
        bool: True se o CPF estiver no formato correto, False caso contrário.
    """
    return re.search(r"^\s*\d{3}\.\d{3}\.\d{3}\-\d{2}\s*$", cpf) is not None or \
        re.search(r"^\s*\d{11}\s*$", cpf) is not None

def clear_cpf(cpf: str):
    return re.sub(r"(\.|\-)", "", cpf)

def format_cpf(cpf: str) -> str:
    str_formatted = clear_cpf(cpf)
    remain_caracteres = 11 - len(str_formatted)
    if remain_caracteres > 0:
        str_formatted = ("0" * remain_caracteres) + str_formatted
    return f"{str_formatted[0:3]}.{str_formatted[3:6]}.{str_formatted[6:9]}\-{str_formatted[9:11]}"

def round_decimal(value: Decimal, decimal_places: int) -> Decimal:
    """
    Arredonda um valor Decimal para um número específico de casas decimais,
    utilizando o modo ROUND_HALF_UP (arredondamento comercial).

    Args:
        value (Decimal): Valor a ser arredondado.
        decimal_places (int): Número de casas decimais desejadas.

    Returns:
        Decimal: Valor arredondado.
    """
    fator = Decimal('1.' + ('0' * decimal_places))
    return value.quantize(fator, rounding=ROUND_HALF_UP)
