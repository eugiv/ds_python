# 1--------------------------------------------------------------------------------------------------------
ids = {
    "user1": [213, 213, 213, 15, 213],
    "user2": [54, 54, 119, 119, 119],
    "user3": [213, 98, 98, 35],
}


def task_1(ids: dict):
    unique_values = []
    for i in ids.values():
        unique_values.extend(i)

    return print(set(unique_values))


# task_1(ids)
# 2--------------------------------------------------------------------------------------------------------
queries = [
    "смотреть сериалы онлайн",
    "новости спорта",
    "афиша кино",
    "курс доллара",
    "сериалы этим летом",
    "курс по питону",
    "сериалы про спорт",
]


def task_2(queries: list):
    num_words = [len(i.split()) for i in queries]
    unique_values = list(set(num_words))
    for j in unique_values:
        print(
            f"Поисковых запросов, содержащих {j} слов(а): {round((num_words.count(j) / len(num_words)) * 100, 2)}%"
        )


# task_2(queries)
# 3--------------------------------------------------------------------------------------------------------
results = {
    "vk": {"revenue": 103, "cost": 98},
    "yandex": {"revenue": 179, "cost": 153},
    "facebook": {"revenue": 103, "cost": 110},
    "adwords": {"revenue": 35, "cost": 34},
    "twitter": {"revenue": 11, "cost": 24},
}


def task_3(res: dict):
    for k, v in res.items():
        revenue, cost = [x for x in v.values()]
        res[k]["ROI"] = round(((revenue / cost) - 1) * 100, 2)

    return print(res)


# task_3(results)
# 4--------------------------------------------------------------------------------------------------------
stats = {"facebook": 55, "yandex": 115, "vk": 120, "google": 99, "email": 42, "ok": 98}


def task_4(stat: dict):
    return print(
        f"Максимальный объем продаж на рекламном канале: {max(stat, key=stat.get)}"
    )


# task_4(stats)
# 5--------------------------------------------------------------------------------------------------------
my_list_1 = ["2018-01-01", "yandex", "cpc", 100]
my_list_2 = ["a", "b", "c", "d", "e", "f"]


def task_5(lst):
    if len(lst) == 1:
        return lst[0]
    elif len(lst) > 1:
        return {lst[0]: task_5(lst[1:])}


# print(task_5(my_list_2))
# 5--------------------------------------------------------------------------------------------------------
