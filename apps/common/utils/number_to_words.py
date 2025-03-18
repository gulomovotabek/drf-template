from num2words import num2words


def number_to_russian_words(number):
    if number.is_integer():
        number = int(number)

    return f"{number} ({num2words(number, lang='ru').capitalize()})"
