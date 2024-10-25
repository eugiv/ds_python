import math

def task_1():
    phrase_1 = str(input("Enter a phrase_1: "))
    phrase_2 = str(input("Enter a phrase_2: "))

    if len(phrase_1) == len(phrase_2):
        print("Фразы равной длины")
    elif len(phrase_1) > len(phrase_2):
        print("Фраза 1 длиннее фразы 2")
    elif len(phrase_1) < len(phrase_2):
        print("Фраза 2 длиннее фразы 1")


# task_1()

def task_2():
    year = int(input("Enter a year: "))
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        print("Високосный год")
    else:
        print("Обычный год")


# task_2()

def task_3():
    day = int(input("Enter you birthday day: "))
    month_input = str(input("Enter you birthday month: "))

    month_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
                  "Ноябрь", "Декабрь"]

    month = month_list.index(month_input) + 1

    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        print("Ваш знак зодиака: Овен")
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        print("Ваш знак зодиака: Телец")
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        print("Ваш знак зодиака: Близнецы")
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        print("Ваш знак зодиака: Рак")
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        print("Ваш знак зодиака: Лев")
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        print("Ваш знак зодиака: Дева")
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        print("Ваш знак зодиака: Весы")
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        print("Ваш знак зодиака: Скорпион")
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        print("Ваш знак зодиака: Стрелец")
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        print("Ваш знак зодиака: Козерог")
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        print("Ваш знак зодиака: Водолей")
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        print("Ваш знак зодиака: Рыбы")
    else:
        print("Некорректная дата")


# task_3()

def task_4():
    w = float(input("Enter a weight: "))
    h = float(input("Enter a height: "))
    l = float(input("Enter a length: "))

    if w <= 15 and h <= 15 and l <= 15:
        print("Коробка №1")
    elif w > 200 or h > 200 or l > 200:
        print("Упаковка для лыж")
    elif 15 < w < 50 or 15 < h < 50 or 15 < l < 50:
        print("Коробка №2")
    else:
        print("Коробка №3")


# task_4()

def task_5():
    lucky_ticket = str(input("Try your luck (only even numbers): "))

    if isinstance(lucky_ticket, str) and len(lucky_ticket) % 2 == 0:
        first_half = lucky_ticket[:len(lucky_ticket) // 2]
        second_half = lucky_ticket[len(lucky_ticket) // 2:]

        sum_first_half = sum(int(num) for num in first_half)
        sum_second_half = sum(int(num) for num in second_half)

        if sum_first_half == sum_second_half:
            print("Счастливый билет")
        else:
            print("Несчастливый билет")
    else:
        print("Введен неверный формат или нечетное кол-во цифр в билете")


# task_5()

def task_6():
    figures_available = ["Круг", "Треугольник", "Прямоугольник"]
    figure = str(input("Введите тип фигуры: (Круг, Треугольник, Прямоугольник): "))

    if figure == "Круг":
        p = 3.14
        r = float(input("Введите радиус круга: "))
        a = p * (r ** 2)
        print("Площадь круга: ", a)
    elif figure == "Треугольник":
        a_side = float(input("Введите длину стороны A: "))
        b_side = float(input("Введите длину стороны B: "))
        c_side = float(input("Введите длину стороны C: "))
        perim_half = (a_side+b_side+c_side)/2
        a_heron = math.sqrt(perim_half * (perim_half - a_side) * (perim_half - b_side) * (perim_half - c_side))
        print("Площадь треугольника: ", a_heron)
    elif figure == "Прямоугольник":
        a_side = float(input("Введите длину стороны A: "))
        b_side = float(input("Введите длину стороны B: "))
        a = a_side * b_side
        print("Площадь треугольника: ", a)
    else:
        print("Введите точное название одной из 3х фигур")


# task_6()
