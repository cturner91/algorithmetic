import unittest

from operations import (
    add,
    divide,
    multiply,
    subtract,
)
from utils import (
    _align_numbers,
    _clean_number,
    _equivalent_division,
    _format_int_and_decimal,
    _int_and_decimal,
    _is_zero,
    _lte,
    _pad_strings,
)


class UtilsTests(unittest.TestCase):

    def test__pad_strings(self):
        self.assertEqual(_pad_strings("0", "2", False), ("0", "2"))
        self.assertEqual(_pad_strings("0", "2", True), ("0", "2"))

        self.assertEqual(_pad_strings("20", "2", False), ("20", "02"))
        self.assertEqual(_pad_strings("20", "2", True), ("20", "20"))

    def test__format_int_and_decimal(self):
        self.assertEqual(_format_int_and_decimal("1", ""), "1")
        self.assertEqual(_format_int_and_decimal("123", ""), "123")
        self.assertEqual(_format_int_and_decimal("0", "2"), "0.2")
        self.assertEqual(_format_int_and_decimal("123", "2"), "123.2")

    def test__align_numbers(self):
        self.assertEqual(_align_numbers("0", "2"), ("0", "2"))
        self.assertEqual(_align_numbers("0.1", "2"), ("0.1", "2.0"))
        self.assertEqual(_align_numbers("0", "2.0"), ("0.0", "2.0"))

        self.assertEqual(_align_numbers("123.1", "2"), ("123.1", "002.0"))
        self.assertEqual(_align_numbers("123.1", "0.002"), ("123.100", "000.002"))

    def test__int_and_decimal(self):
        self.assertEqual(_int_and_decimal("123"), ("123", ""))
        self.assertEqual(_int_and_decimal("123.456"), ("123", "456"))
        self.assertEqual(_int_and_decimal("0.002"), ("0", "002"))
        self.assertEqual(_int_and_decimal("0.0020"), ("0", "0020"))

    def test__is_zero(self):
        self.assertTrue(_is_zero("0"))
        self.assertTrue(_is_zero("0.0"))
        self.assertTrue(_is_zero("00.0000"))
        self.assertTrue(_is_zero("-00.0000"))

        self.assertFalse(_is_zero("1"))
        self.assertFalse(_is_zero("1.0"))
        self.assertFalse(_is_zero("0.1"))
        self.assertFalse(_is_zero("-0.1"))
        self.assertFalse(_is_zero("-0.00001"))
        self.assertFalse(_is_zero("100"))
    
    def test__equivalent_division(self):
        self.assertTrue(_equivalent_division("2", "1"), ("2", "1"))
        self.assertTrue(_equivalent_division("2.23", "1"), ("2.23", "1"))
        self.assertTrue(_equivalent_division("2", "1.23"), ("200", "123"))
        self.assertTrue(_equivalent_division("2.23", "1.2345"), ("22300", "12345"))
        self.assertTrue(_equivalent_division("2.2345", "1.23"), ("223.45", "123"))

    def test__clean_number(self):
        self.assertEqual(_clean_number("0"), "0")
        self.assertEqual(_clean_number("0.0"), "0")
        self.assertEqual(_clean_number("000.0"), "0")
        self.assertEqual(_clean_number("0.0100"), "0.01")
        self.assertEqual(_clean_number("000123.0045600"), "123.00456")
        self.assertEqual(_clean_number("10"), "10")
        self.assertEqual(_clean_number("10."), "10")
        self.assertEqual(_clean_number("0.10"), "0.1")

    def test__lte(self):
        self.assertTrue(_lte("2", "3"))
        self.assertTrue(_lte("3", "3"))
        self.assertFalse(_lte("4", "3"))

        self.assertTrue(_lte("22", "23"))
        self.assertTrue(_lte("23", "23"))
        self.assertFalse(_lte("24", "23"))

        self.assertTrue(_lte("-1", "2"))
        self.assertFalse(_lte("1", "-2"))
        self.assertFalse(_lte("-1", "-2"))

        self.assertFalse(_lte("10", "2"))
        self.assertTrue(_lte("2", "10"))
        self.assertTrue(_lte("-10", "-2"))

        self.assertTrue(_lte("1234", "1235"))
        self.assertTrue(_lte("1235", "1235"))
        self.assertFalse(_lte("1236", "1235"))


class TestOperation(unittest.TestCase):

    def test__add(self):
        self.assertEqual(add("0", "2"), "2")
        self.assertEqual(add("1", "2"), "3")
        self.assertEqual(add("6", "7"), "13")
        self.assertEqual(add("96", "7"), "103")
        self.assertEqual(add("6", "97"), "103")

        # negative numbers
        self.assertEqual(add("-6", "97"), "91")
        self.assertEqual(add("6", "-97"), "-91")
        self.assertEqual(add("-6", "-97"), "-103")

    def test__add__decimals(self):
        self.assertEqual(add("0", "10.2"), "10.2")
        self.assertEqual(add("0.1", "0.2"), "0.3")
        self.assertEqual(add("0.8", "0.2"), "1.0")
        self.assertEqual(add("0.8", "0.3"), "1.1")
        self.assertEqual(add("6.1", "0"), "6.1")
        self.assertEqual(add("0.7", "7.7777"), "8.4777")

        # negative numbers
        self.assertEqual(add("-0.7", "7.7777"), "7.0777")
        self.assertEqual(add("0.7", "-7.7777"), "-7.0777")
        self.assertEqual(add("-0.7", "-7.7777"), "-8.4777")

    def test__subtract(self):
        self.assertEqual(subtract("9", "7"), "2")
        self.assertEqual(subtract("12", "7"), "5")
        self.assertEqual(subtract("6", "7"), "-1")
        self.assertEqual(subtract("96", "7"), "89")
        self.assertEqual(subtract("6", "97"), "-91")
        self.assertEqual(subtract("1000", "999"), "1")

        # negative numbers
        self.assertEqual(subtract("-6", "97"), "-103")
        self.assertEqual(subtract("6", "-97"), "103")
        self.assertEqual(subtract("-6", "-97"), "91")

    def test__subtract__decimals(self):
        self.assertEqual(subtract("9.1", "7"), "2.1")
        self.assertEqual(subtract("9", "7.1"), "1.9")
        self.assertEqual(subtract("109", "7.1"), "101.9")
        self.assertEqual(subtract("100", "99.9"), "0.1")
        self.assertEqual(subtract("99.9", "100"), "-0.1")

        # negative numbers
        self.assertEqual(subtract("-99", "7.1"), "-106.1")
        self.assertEqual(subtract("99", "-7.1"), "106.1")
        self.assertEqual(subtract("-99", "-7.1"), "-91.9")
        
    def test__multiply__integers(self):
        # zero-cases
        self.assertEqual(multiply('0', '0'), "0")
        self.assertEqual(multiply('6', '0'), "0")
        self.assertEqual(multiply('0', '7'), "0")

        # integer cases
        self.assertEqual(multiply('6', '7'), "42")
        self.assertEqual(multiply('21', '37'), "777")
        self.assertEqual(multiply('563', '123'), "69249")

        # negative cases
        self.assertEqual(multiply('-563', '123'), "-69249")
        self.assertEqual(multiply('563', '-123'), "-69249")
        self.assertEqual(multiply('-563', '-123'), "69249")

    def test__multiply__decimals(self):
        self.assertEqual(multiply('6.3', '7'), "44.1")
        self.assertEqual(multiply('6.3', '76.7'), "483.21")
        self.assertEqual(multiply('123.456', '987.654'), "121931.812224")  # funny - the Python calc gives it as 121931.81222400001 - this is a floating point error

        # negative cases
        self.assertEqual(multiply('-6.3', '76.7'), "-483.21")
        self.assertEqual(multiply('6.3', '-76.7'), "-483.21")
        self.assertEqual(multiply('-6.3', '-76.7'), "483.21")

    def test__divide__integers(self):
        # zero cases
        with self.assertRaises(ZeroDivisionError):
            divide('1', '0')
        with self.assertRaises(ZeroDivisionError):
            divide('1', '0.0')
        with self.assertRaises(ZeroDivisionError):
            divide('1', '00.00')
        with self.assertRaises(ZeroDivisionError):
            divide('1', '000.00000')
        with self.assertRaises(ZeroDivisionError):
            divide('0', '0')
        self.assertEqual(divide('0', '1'), "0")

        # integer cases
        self.assertEqual(divide('6', '1'), "6")
        self.assertEqual(divide('42', '7'), "6")
        self.assertEqual(divide('777', '37'), "21")
        self.assertEqual(divide('69249', '123'), "563")

        # decimal cases
        self.assertEqual(divide('13', '6.5'), "2")
        self.assertEqual(divide('10', '4'), "2.5")
        self.assertEqual(divide('19.752', '1.2345'), "16")
        self.assertEqual(divide('19.752', '16'), "1.2345")

        # negative cases
        self.assertEqual(divide('-69249', '123'), "-563")
        self.assertEqual(divide('69249', '-123'), "-563")
        self.assertEqual(divide('-69249', '-123'), "563")

        # recurring cases
        self.assertEqual(divide('10', '3', max_decimals=1), "3.3")
        self.assertEqual(divide('10', '3', max_decimals=2), "3.33")
        self.assertEqual(divide('10', '3', max_decimals=3), "3.333")
        self.assertEqual(divide('10', '3', max_decimals=4), "3.3333")

        # irrational cases
        # 22 / 7 = 3.142857142857143
        self.assertEqual(divide('22', '7',  1), "3.1")
        self.assertEqual(divide('22', '7',  2), "3.14")
        self.assertEqual(divide('22', '7',  3), "3.142")
        self.assertEqual(divide('22', '7',  4), "3.1428")
        self.assertEqual(divide('22', '7',  5), "3.14285")
        self.assertEqual(divide('22', '7',  6), "3.142857")
        self.assertEqual(divide('22', '7',  7), "3.1428571")
        self.assertEqual(divide('22', '7',  8), "3.14285714")
        self.assertEqual(divide('22', '7',  9), "3.142857142")
        self.assertEqual(divide('22', '7', 10), "3.1428571428")
        self.assertEqual(divide('22', '7', 11), "3.14285714285")
        self.assertEqual(divide('22', '7', 12), "3.142857142857")
        self.assertEqual(divide('22', '7', 13), "3.1428571428571")
        self.assertEqual(divide('22', '7', 14), "3.14285714285714")
        self.assertEqual(divide('22', '7', 15), "3.142857142857142")  # final 3 in float must be rounded up
        # this is as far as floating point operations take me

        # given that final 2 is rounded up to 3 in floating point, let's prove the 16th value is >= 5
        result = divide('22', '7', 16)
        self.assertGreaterEqual(int(result[-1]), 5)

        # prove that we can go further
        self.assertEqual(divide('22', '7', 20), "3.14285714285714285714")
        self.assertEqual(divide('22', '7', 25), "3.1428571428571428571428571")
        self.assertEqual(divide('22', '7', 30), "3.142857142857142857142857142857")
        self.assertEqual(divide('22', '7', 50), "3.14285714285714285714285714285714285714285714285714")

    def test__divide__decimal(self):
        from decimal import Decimal, getcontext
        getcontext().prec = 50
        self.assertEqual(str(Decimal('22') / Decimal('7')), "3.1428571428571428571428571428571428571428571428571")
        self.assertEqual(divide('22', '7', 50), "3.14285714285714285714285714285714285714285714285714")


if __name__ == "__main__":
    unittest.main()
