import re
import numpy as np


# 1--------------------------------------------------------------------------------------------------------
def task_1():
    word = input("Enter a word: ")

    word_remnant = len(word) % 2
    half_word = len(word) // 2

    if word_remnant == 0 and len(word) > 2:
        print(word[half_word - 1 : -half_word + 1])
    elif word_remnant != 0 and len(word) > 1:
        print(word[half_word:-half_word])
    else:
        print(word)


# task_1()
# 2--------------------------------------------------------------------------------------------------------
def task_2():
    flag = False

    nums_sum = 0
    while not flag:
        num = int(input("Enter a number: "))
        if num != 0:
            nums_sum += num
        else:
            flag = True
    print(nums_sum)


# task_2()
# 3--------------------------------------------------------------------------------------------------------
boys = ["Peter", "Alex", "John", "Arthur", "Richard"]
girls = ["Kate", "Liza", "Kira", "Emma", "Trisha"]


def task_3(b: list, g: list):

    if len(b) == len(g):
        dating = zip(sorted(b), sorted(g))

        print("Идеальные пары:")
        for name_pair in list(dating):
            formated_pair = " и ".join(name_pair)
            print(formated_pair)
    else:
        print("Внимание, кто-то может остаться без пары!")


# task_3(boys, girls)
# 4--------------------------------------------------------------------------------------------------------
countries_temperature = [
    ["Таиланд", [75.2, 77, 78.8, 73.4, 68, 75.2, 77]],
    ["Германия", [57.2, 55.4, 59, 59, 53.6]],
    ["Россия", [35.6, 37.4, 39.2, 41, 42.8, 39.2, 35.6]],
    ["Польша", [50, 50, 53.6, 57.2, 55.4, 55.4]],
]


def task_4(c_t: list):

    print("Средняя температура в странах:")
    for country in c_t:
        print(
            country[0]
            + " - "
            + str("{:.1f}".format((np.mean(country[1]) - 32) * 5 / 9))
            + " C"
        )


# task_4(countries_temperature)
# --------------------------------------------------------------------------------------------------------
car_ids = ["А222ВС96", "АБ22ВВ193"]


def task_5(car_ids_list: list):

    pattern = r"^[АВЕКМНОРСТУХ]{1}[0-9]{3}[АВЕКМНОРСТУХ]{2}[0-9]{2,3}$"
    for car_id in car_ids_list:
        if re.match(pattern, car_id):
            reg = car_id[-2:]
            num = car_id[: -len(reg)]
            print(f"Номер {num} валиден. Регион: {reg}")
        else:
            print(f"Номер {car_id} не валиден")


# task_5(car_ids)
# --------------------------------------------------------------------------------------------------------
stream1 = [
    "user4,2021-01-01;3",
    "user3,2022-01-07;4",
    "user2,2022-03-29;1",
    "user1,2020-04-04;13",
    "user2,2022-01-05;7",
    "user1,2021-06-14;4",
    "user3,2022-07-02;10",
    "user4,2021-03-21;19",
    "user4,2022-03-22;4",
    "user4,2022-04-22;8",
    "user4,2021-05-03;9",
    "user4,2022-05-11;11",
]

stream2 = ["user100,2022-01-01;150", "user99,2022-01-07;205", "user1001,2022-03-29;81"]


def task_6(stream: list):

    users = []
    views = []
    for i in range(len(stream)):
        chunk = stream[i].split(",")
        users.append(chunk[0])
        views.append(int(chunk[1].split(";")[1]))

    mean_views = sum(views) / len(set(users))

    print(
        f"Среднее количество просмотров на уникального пользователя: {'{:.2f}'.format(mean_views)}"
    )


# task_6(stream1)
