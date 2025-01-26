import datetime
import time


def date_string_to_unix(date_str, date_format='%d.%m', convert_to_date_object=False):
    """
    Конвертирует дату из строки в Unix-дату.

    Args:
        date_str (str): Строка с датой в формате 'день.месяц'.
        date_format (str): Формат строки с датой (по умолчанию '%d.%m').
        convert_to_date_object (bool): Если True, сначала конвертирует в объект даты, иначе - напрямую в unix.

    Returns:
        int: Unix-дата (количество секунд с начала эпохи Unix) или None, если произошла ошибка.
    """
    try:
        if convert_to_date_object:

            date_obj = datetime.datetime.strptime(date_str, date_format).date()
            # Заменяем год на текущий
            date_obj = date_obj.replace(year=datetime.date.today().year)
            return int(time.mktime(date_obj.timetuple()))
        else:

            date_obj = datetime.datetime.strptime(date_str, date_format)
            # Заменяем год на текущий
            date_obj = date_obj.replace(year=datetime.date.today().year)
            return int(time.mktime(date_obj.timetuple()))

    except ValueError:
        print("Ошибка: Неправильный формат даты или не удалось преобразовать.")
        return None


# Примеры использования:
date_str_1 = '25.12'
unix_date_1 = date_string_to_unix(date_str_1)
print(f"Unix дата для {date_str_1} (без промежуточного объекта): {unix_date_1}")

unix_date_1_with_obj = date_string_to_unix(date_str_1, convert_to_date_object=True)
print(f"Unix дата для {date_str_1} (с промежуточным объектом): {unix_date_1_with_obj}")

date_str_2 = '01.01'
unix_date_2 = date_string_to_unix(date_str_2)
print(f"Unix дата для {date_str_2} (без промежуточного объекта): {unix_date_2}")

date_str_3 = 'invalid_date'
unix_date_3 = date_string_to_unix(date_str_3)
print(f"Unix дата для {date_str_3} (без промежуточного объекта): {unix_date_3}")