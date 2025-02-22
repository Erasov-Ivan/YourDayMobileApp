import datetime


def sum_of_number(number: int) -> int:
    result = 0
    while number > 0:
        result += number % 10
        number //= 10
    return result


def sum_if_more(number: int, more_than: int = 22) -> int:
    if number > more_than:
        return sum_of_number(number=number)
    else:
        return number


def calculate_numbers_from_date(date: datetime.date) -> tuple[int, int, int, int]:
    a = sum_if_more(number=date.day)
    x = sum_if_more(number=a + date.month + sum_of_number(number=date.year))
    b = sum_if_more(number=a + date.month + sum_of_number(number=date.year) + x)
    c = sum_if_more(number=date.year)
    return a, x, b, c


async def calculate_prediction(date: datetime.date, birthdate: datetime.date) -> tuple[int, int, int]:
    a1, x1, b1, c1 = calculate_numbers_from_date(date=birthdate)
    a2, x2, b2, c2 = calculate_numbers_from_date(date=date)

    a = sum_if_more(number=a1 + a2)
    x = sum_if_more(number=x1 + x2)
    b = sum_if_more(number=b1 + b2)
    c = sum_if_more(number=c1 + c2)

    k1 = sum_if_more(number=x + b)
    k2 = sum_if_more(number=c + b)
    k3 = sum_if_more(number=k1 + k2)
    k = sum_if_more(number=k1 + k3)
    return a, b, k
