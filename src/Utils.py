from decimal import ROUND_HALF_UP, Decimal
import re

TOTAL_DIGITS_ACCOUNT_NUMBER = 8
TOTAL_DIGITS_AGENCY_NUMBER = 4

def clear_cmd_line(length: int):
    """
    Limpa a linha atual no terminal imprimindo espaços em branco.

    Args:
        length (int): Número de caracteres a sobrescrever com espaço.
    """
    print('\r' + ' ' * length, end='\r')

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
