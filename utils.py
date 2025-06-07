def _validate_ints_below_10(*args) -> None:
    # The fundamental methods are only allowed to work with single-digit integers
    for i, value in enumerate(args):
        value = int(value)
        assert isinstance(value, int), f"Value #{i} ({value}) must be an integer"
        assert 0 <= value < 10, f"Value #{i} ({value}) must be less than 10"


# These are the fundamental operations we can perform

def _add_ints(v1: str | int, v2: str | int) -> int:
    int1, int2 = int(v1), int(v2)
    _validate_ints_below_10(int1, int2)
    return int1 + int2


def _subtract_ints(v1: str | int, v2: str | int) -> int:
    int1, int2 = int(v1), int(v2)
    _validate_ints_below_10(int1, int2)
    return int1 - int2


def _multiply_ints(v1: str | int, v2: str | int) -> int:
    int1, int2 = int(v1), int(v2)
    _validate_ints_below_10(int1, int2)
    return int1 * int2

# End fundamental operations


# Utility methods

def _pad_strings(v1: str, v2: str, is_decimal: bool) -> str:
    # helper function to align two strings of numbers in terms of place value
    length = max(len(v1), len(v2))
    if is_decimal:
        v1 = v1.ljust(length, '0')
        v2 = v2.ljust(length, '0')
    else:
        v1 = v1.rjust(length, '0')
        v2 = v2.rjust(length, '0')

    return v1, v2


def _format_int_and_decimal(integer: str, decimal: str) -> str:
    if decimal:
        return f"{integer}.{decimal}"
    else:
        return integer


def _align_numbers(v1: str, v2: str) -> tuple[str, str]:
    # helper function to align two strings of numbers in terms of place value
    integer1, decimal1 = _int_and_decimal(v1)
    integer2, decimal2 = _int_and_decimal(v2)

    integer1, integer2 = _pad_strings(integer1, integer2, False)
    decimal1, decimal2 = _pad_strings(decimal1, decimal2, True)

    v1 = _format_int_and_decimal(integer1, decimal1)
    v2 = _format_int_and_decimal(integer2, decimal2)
    assert len(v1) == len(v2), "Strings must be of equal length."
    return v1, v2


def _int_and_decimal(value: str) -> tuple[str, str]:
    # Helper function to split a string into integer and decimal parts
    if '.' in value:
        integer_part, decimal_part = value.split('.')
    else:
        integer_part, decimal_part = value, ''
    return integer_part, decimal_part


def _string_set(string: str, index: int, value: str | int) -> str:
    # Helper function to set a character in a string at a specific index
    assert len(str(value)) == 1, "Value must be a single character."
    return f'{string[:index]}{str(value)}{string[index + 1:]}'


def _is_zero(value: str) -> bool:
    for replace in ('.', '0', '-'):
        value = value.replace(replace, '')
    return len(value) == 0


def _equivalent_division(number1: str, number2: str) -> tuple[str]:
    # 1 / 0.23 === 100 / 23
    # but diviing by an integer is so much easier
    if '.' in number2:
        integer2, decimal2 = number2.split('.')

        if '.' in number1:
            integer1, decimal1 = number1.split('.')
            max_decimals = max(len(decimal1), len(decimal2))
            number1 = f"{integer1}{decimal1.ljust(max_decimals, '0')}"
            number2 = f"{integer2}{decimal2.ljust(max_decimals, '0')}"
        else:
            # number1 does not have a decimal => pad with zeroes
            number1 = f'{number1}{"0" * len(decimal2)}'
            number2 = number2.replace('.', '')

    return number1, number2


def _clean_number(number: str) -> str:
    if _is_zero(number):
        return '0'

    number = number.lstrip('0')
    if '.' in number:
        # only strip trailing zeroes after the decimal point
        # otherwise, the 0 is an integral part of place-value
        number = number.rstrip('0')

    if number.startswith('.'):
        number = '0' + number
    if number.endswith('.'):
        number = number[:-1]
    return number


def _lte(number1: str, number2: str) -> bool:
    # use string comparison for number1 <= number2
    number1 = _clean_number(number1)
    number2 = _clean_number(number2)

    if number1 == number2:
        return True
    
    if number1.startswith('-') and number2.startswith('-'):
        # both numbers are negative, so we can compare them as if they were positive
        return not _lte(number1[1:], number2[1:])
    elif number1.startswith('-') and not number2.startswith('-'):
        return True
    elif not number1.startswith('-') and number2.startswith('-'):
        return False

    if len(number1) < len(number2):
        return True
    elif len(number1) > len(number2):
        return False
    else:
        # same length - compare each char
        for char1, char2 in zip(number1, number2):
            if char1 < char2:
                return True
            elif char1 > char2:
                return False
            else:
                # maybe unnecessary to have this block, but it makes the logic clear
                continue
    
    # if we get here, something has gone wrong
    raise ValueError(f"Cannot compare {number1} and {number2} for less than or equal to (<=)")
