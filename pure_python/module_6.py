from datetime import datetime, timedelta

# 1--------------------------------------------------------------------------------------------------------
NEWSPAPERS = {
    "The Moscow Times": "Wednesday, October 2, 2002",
    "The Guardian": "Friday, 11.10.13",
    "Daily News": "Thursday, 18 August 1977",
}


def task_1():
    date_patterns = {}

    for newspaper in NEWSPAPERS:
        if newspaper == "The Moscow Times":
            date_patterns["moscow_times_pattern"] = "%A, %B %d, %Y"
        elif newspaper == "The Guardian":
            date_patterns["guardian_pattern"] = "%A, %d.%m.%y"
        elif newspaper == "Daily News":
            date_patterns["daily_news_pattern"] = "%A, %d %B %Y"

    date_moscow_times = datetime.strptime(
        NEWSPAPERS["The Moscow Times"], date_patterns["moscow_times_pattern"]
    )
    date_guardian = datetime.strptime(
        NEWSPAPERS["The Guardian"], date_patterns["guardian_pattern"]
    )
    date_daily_news = datetime.strptime(
        NEWSPAPERS["Daily News"], date_patterns["daily_news_pattern"]
    )

    print(date_moscow_times, date_guardian, date_daily_news)


# task_1()

# 2--------------------------------------------------------------------------------------------------------
STREAM = ["2018-04-02", "2018-02-29", "2018-19-02"]


def task_2():
    res = []
    for date in STREAM:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            res.append(True)
        except ValueError:
            res.append(False)

    print(res)


# task_2()


# 3--------------------------------------------------------------------------------------------------------
def task_3(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return []

    if start_date > end_date:
        return []

    dates_list = []
    while start_date <= end_date:
        dates_list.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)

    return dates_list


# print(task_3("2024-02-02", "2024-03-30"))

# 4--------------------------------------------------------------------------------------------------------
DEFAULT_USER_COUNT = 3


def delete_and_return_last_user(region, default_list=["A100", "A101", "A102"]):
    """
    Удаляет из списка default_list последнего пользователя
    и возвращает ID нового последнего пользователя.

    Q: Что значит ошибка list index out of range?
    A: Это значит, что мы пытемся обратиться к элементу списка по номеру индекса, которого не существует в списке.

    Q: Почему при первом запуске функция работает корректно, а при втором — нет?
    A: Так как список это изменяемый объект, то при первом запуске он имеет 3 элемента, индексы [0, 1, 2],
       при первом запуске, когда удаляется последний элемент списка [0, 1] мы просим вернуть елемент с порядковым номером 1
       (3-2, 'A101'), при повторном запуске у нас в списке оставется только 1 элеминет [0], а мы просим вернуть элемент
       с индексом 1, а не 0. Поэтому возникает ошибка - list index out of range.
    """

    element_to_delete = default_list[-1]
    default_list.remove(element_to_delete)

    return default_list[DEFAULT_USER_COUNT - 2]


# delete_and_return_last_user(1)
