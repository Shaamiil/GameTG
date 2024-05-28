import requests

str_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

russian_letter = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
                  'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

russian_letter_upper = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                        'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

english_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']

english_letter_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

special_symbols = [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=",
    "[", "]", "{", "}", "|", r"\\", ":", ";", "'", r'\"', ",", ".", "<", ">",
    "?", "/",
]

months = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август",
          "сентябрь", "октябрь", "ноябрь", "декабрь", "Январь", "Февраль", "Март",
          "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
          "Декабрь"]

roman_numerals = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII",
    "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV",
    "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX", "XXXI", "XXXII", "XXXIII", "XXXIV",
    "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL", "XLI", "XLII", "XLIII", "XLIV",
    "XLV", "XLVI", "XLVII", "XLVIII", "XLIX", "L", "LI", "LII", "LIII", "LIV", "LV", "LVI",
    "LVII", "LVIII", "LIX", "LX", "LXI", "LXII", "LXIII", "LXIV", "LXV", "LXVI", "LXVII",
    "LXVIII", "LXIX", "LXX", "LXXI", "LXXII", "LXXIII", "LXXIV", "LXXV", "LXXVI", "LXXVII",
    "LXXVIII", "LXXIX", "LXXX", "LXXXI", "LXXXII", "LXXXIII", "LXXXIV", "LXXXV", "LXXXVI",
    "LXXXVII", "LXXXVIII", "LXXXIX", "XC", "XCI", "XCII", "XCIII", "XCIV", "XCV", "XCVI",
    "XCVII", "XCVIII", "XCIX", "C", ]

elements = [
    'Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au',
    'Ba', 'Be', 'Bi', 'Bk', 'Br', 'C', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Co', 'Cr', 'Cs', 'Cu',
    'Dy',
    'Er', 'Es', 'Eu',
    'Fe', 'Fm', 'Fr',
    'Ga', 'Gd', 'Ge', 'He', 'Hf', 'Hg', 'Ho', 'Hs', 'In', 'Ir',
    'Kr',
    'La', 'Li', 'Lr', 'Lu',
    'Md', 'Mg', 'Mn', 'Mo', 'Mt',
    'Na', 'Nb', 'Nd', 'Ne', 'Ni', 'No', 'Np',
    'Os',
    'P', 'Pa', 'Pb', 'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu',
    'Ra', 'Rb', 'Re', 'Rf', 'Rg', 'Rh', 'Rn', 'Ru',
    'Sb', 'Sc', 'Se', 'Sg', 'Si', 'Sm', 'Sn', 'Sr',
    'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Tl', 'Tm',
    'Xe', 'Yb', 'Zn', 'Zr'
]


def reverse(message: str):
    new_word = ""
    index = len(message) - 1
    while index >= 0:
        new_word += message[index]
        index -= 1
    return new_word


def wordle_day():
    response = requests.get(url='https://www.nytimes.com/svc/wordle/v2/2024-05-28.json')
    wordle = (response.json()["solution"])
    return str(wordle)
