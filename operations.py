'''Codifying the arithmetic we're taught at school
We only work with single-digit integer values but we can add / subtract / multiply / divide and 
logically work with the results e.g. we work out what 123.456 + 7.89 is by manipulating integers
in sequence.
'''

from utils import (
    _add_ints,
    _subtract_ints,
    _multiply_ints,
    _is_zero,
    _clean_number,
    _align_numbers,
    _equivalent_division,
    _lte,
    _string_set,
)


def add(
    number1: str, 
    number2: str, 
) -> str:
    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):
        # add the absolute values and negate the result
        return f'-{add(number1[1:], number2[1:])}'
    
    elif number1.startswith('-'):  # -4 + 2 => 2 - 4
        return subtract(number2, number1[1:])

    elif number2.startswith('-'):  # -4 + 2 => 2 - 4
        return subtract(number1, number2[1:])

    # neither input is negative

    v1, v2 = _align_numbers(number1, number2)

    # This just applies add_int inside a loop and carries the 1 if necessary
    carry = 0
    output = ''
    for i in range(len(v1) - 1, -1, -1):
        if v1[i] == '.':
            output = '.' + output
            continue

        int1 = int(v1[i])
        int2 = int(v2[i])
        result = _add_ints(int1, int2)
        if carry:  # can only ever be 1 or 0?
            result += carry

        if result >= 10:
            carry = 1
            result -= 10
        else:
            carry = 0
        
        # pre-pend, not append, to the output
        output = str(result) + output
        
    if carry:
        return f'1{output}'
    return output


def subtract(
    number1: str, 
    number2: str, 
) -> str:
    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):            
        result = subtract(number1[1:], number2[1:])
        if result.startswith('-'):
            # if we subtract a bigger negative from a smaller negative, we get a positive result
            return result[1:]
        return f'-{result}'

    elif number1.startswith('-'):  # -4 - 2 => -(4 + 2)
        return f'-{add(number1[1:], number2)}'
    elif number2.startswith('-'): # 4 - -2 => 4 + 2
        return add(number1, number2[1:])

    # neither input is negative

    v1, v2 = _align_numbers(number1, number2)

    # both numbers are aligned - easy to see which is bigger. String sorting even makes this possible
    negative = None
    for int1, int2 in zip(v1, v2):
        if int1 == int2:
            continue
        elif int1 > int2:
            negative = False
        else:
            negative = True
        break
    
    # numbers are identical
    if negative is None:
        return '0'
    elif negative:
        # swap the numbers so we can do the subtraction
        v1, v2 = v2, v1

    output = ''
    for i in range(len(v1)-1, -1, -1):
        if v1[i] == '.':
            output = '.' + output
            continue

        int1 = int(v1[i])
        int2 = int(v2[i])
        result = _subtract_ints(int1, int2)
        if result < 0:
            # we need to borrow from higher value places
            # we know a higher value place exists because the values aren't equal 
            # and we know v1 > v2
            for j in range(i-1, -1, -1):
                if v1[j] == '.':
                    continue
                elif v1[j] == '0':
                    v1 = _string_set(v1, j, 9)
                else:
                    v1 = _string_set(v1, j, int(v1[j]) - 1)
                    result += 10  # 3 - 6 = -3, but 13 - 6 = 7 => result += 10
                    break
        
        # pre-pend, not append, to the output
        output = str(result) + output
        
    # strip any leading / trailing zeros?
    output = _clean_number(output)
    if negative:
        output = '-' + output
    return output


def multiply(
    number1: str, 
    number2: str, 
) -> str:
    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):            
        return multiply(number1[1:], number2[1:])
    elif number1.startswith('-'):
        return f'-{multiply(number1[1:], number2)}'
    elif number2.startswith('-'):
        return f'-{multiply(number1, number2[1:])}'

    # neither input is negative

    # save ourselves some CPU cycles
    if _is_zero(number1) or _is_zero(number2):
        return '0'

    v1, v2 = _align_numbers(number1, number2)

    # count all decimal places, then perform total integer multiplication, and re-add the 
    # decimal place later
    decimal_places = 0
    if '.' in v1:
        i, d = v1.split('.')
        decimal_places += len(d)
        v1 = v1.replace('.', '')
    if '.' in v2:
        i, d = v2.split('.')
        decimal_places += len(d)
        v2 = v2.replace('.', '')

    numbers = []  # as we multiply, we end up with a bunch of numbers to be added together
    # start at right-most value of v2, multiply by each digit of v1
    padding = 0
    for i in range(len(v2)-1, -1, -1):
        int2 = int(v2[i])

        # when multiplying, need to pad the right-hand side with zeros 
        # i.e. we are multiplying by 30, not 3 -> pad the right
        output = '0' * padding
        carry = 0
        for j in range(len(v1)-1, -1, -1):
            int1 = int(v1[j])
            result = _multiply_ints(int1, int2)
            result = add(str(result), str(carry))

            if len(result) > 1:
                # can only be max 2-digits. Even if we are multiplying 9999 * 9999, then max of
                # and operation will be 81 + 8 => 89 i.e. still 2 digits
                carry = int(result[0])
                result = result[1]
            else:
                carry = 0
        
            # pre-pend, not append, to the output
            output = str(result) + output
        
        # inner loop has finished - add to numbers and perform next loop
        if carry:
            output = str(carry) + output
        
        numbers.append(output)
        padding += 1

    # All numbers have now been created -> sum them all up
    total = '0'
    for number in numbers:
        total = add(total, number)

    # re-add the decimal place
    if decimal_places > 0:
        integer = total[:-decimal_places]
        decimal = total[-decimal_places:]
        total = f'{integer}.{decimal}'

    total = _clean_number(total)
    return total
    

def divide(
    number1: str, 
    number2: str, 
    max_decimals: int = 10,
) -> str:
    if _is_zero(number2):
        raise ZeroDivisionError()

    # handle negative inputs
    if number1.startswith('-') and number2.startswith('-'):            
        return divide(number1[1:], number2[1:])
    elif number1.startswith('-'):
        return f'-{divide(number1[1:], number2)}'
    elif number2.startswith('-'):
        return f'-{divide(number1, number2[1:])}'

    # neither input is negative

    # save ourselves some CPU cycles
    if _is_zero(number1):
        return '0'
    
    v1, v2 = _equivalent_division(number1, number2)
    if '.' not in v1:
        v1 = f'{v1}.0'  # ensure we always have a decimal so no special case handling

    # I always used to do multiplication 1-9 of the divisor, and then just look up the biggest 
    # one that fits...
    lookup = {i: multiply(v2, str(i)) for i in range(0, 10)}

    output = ''
    value = ''
    decimal = False
    n_decimals = 0
    i = 0
    while True:
        # Can't think of the requisite logic for a single conditional
        # we msut run until at least len(v1), and if we have a remainder at that point, we keep 
        # going until we exceed max_decimals
        if i >= len(v1) and n_decimals >= max_decimals:
            break

        if i < len(v1):
            if v1[i] == '.':
                output += '.'
                decimal = True
                i += 1
                continue

            value = f'{value}{v1[i]}'
        else:
            value = f'{value}0'

        # lookup goes down to 0 - so something will always fit
        for j in range(9, -1, -1):
            multiple = lookup[j]
            if _lte(multiple, value):
                output += str(j)
                value = subtract(value, multiple)
                if decimal:
                    n_decimals += 1
                break

        # we have finished iterating over the number and we have no remainder -> finshed!
        if i >= len(v1) and value == '0':
            break
        
        i += 1

    output = _clean_number(output)
    return output
