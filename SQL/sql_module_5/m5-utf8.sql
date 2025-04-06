--=============== МОДУЛЬ 5. РАБОТА С POSTGRESQL =======================================
--= ПОМНИТЕ, ЧТО НЕОБХОДИМО УСТАНОВИТЬ ВЕРНОЕ СОЕДИНЕНИЕ И ВЫБРАТЬ СХЕМУ PUBLIC===========
SET search_path TO public;

--======== ОСНОВНАЯ ЧАСТЬ ==============

--ЗАДАНИЕ №1
--Сделайте запрос к таблице payment и с помощью оконных функций добавьте вычисляемые колонки согласно условиям:
--Пронумеруйте все платежи от 1 до N по дате платежа
--Пронумеруйте платежи для каждого покупателя, сортировка платежей должна быть по дате платежа
--Посчитайте нарастающим итогом сумму всех платежей для каждого покупателя, сортировка должна 
--быть сперва по дате платежа, а затем по размеру платежа от наименьшей к большей
--Пронумеруйте платежи для каждого покупателя по размеру платежа от наибольшего к
--меньшему так, чтобы платежи с одинаковым значением имели одинаковое значение номера.
--Можно составить на каждый пункт отдельный SQL-запрос, а можно объединить все колонки в одном запросе.

SELECT customer_id, payment_id, payment_date,
    ROW_NUMBER() OVER (ORDER BY payment_date) AS column_1,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY payment_date) AS column_2,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY payment_date, amount) AS column_3,
    DENSE_RANK () OVER (PARTITION BY customer_id ORDER BY amount DESC) AS column_4
FROM payment;


--ЗАДАНИЕ №2
--С помощью оконной функции выведите для каждого покупателя стоимость платежа и стоимость 
--платежа из предыдущей строки со значением по умолчанию 0.0 с сортировкой по дате платежа.

SELECT customer_id, payment_id, payment_date, amount,
    LAG(amount, 1, 0.0) OVER (PARTITION BY customer_id ORDER BY payment_date) AS last_amount
FROM payment;


--ЗАДАНИЕ №3
--С помощью оконной функции определите, на сколько каждый следующий платеж покупателя больше или меньше текущего.

SELECT customer_id, payment_id, payment_date, amount,
    amount - LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY payment_date) as difference
FROM payment;


--ЗАДАНИЕ №4
--С помощью оконной функции для каждого покупателя выведите данные о его последней оплате аренды.

WITH cte_last_payment AS (
    SELECT customer_id, payment_id, payment_date, amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY payment_date DESC) AS payment_num
    FROM payment
    )

SELECT customer_id, payment_id, payment_date, amount
FROM cte_last_payment
WHERE payment_num = 1
ORDER BY customer_id;


--======== ДОПОЛНИТЕЛЬНАЯ ЧАСТЬ ==============

--ЗАДАНИЕ №1
--С помощью оконной функции выведите для каждого сотрудника сумму продаж за август 2005 года 
--с нарастающим итогом по каждому сотруднику и по каждой дате продажи (без учёта времени) 
--с сортировкой по дате.

WITH cte_sum_amount AS (
    SELECT staff_id, payment_date::date, SUM(amount) as sum_amount
    FROM payment
    WHERE payment_date >= '2005-08-01' AND payment_date < '2005-09-01'
    GROUP BY staff_id, payment_date::date
)

SELECT *,
    SUM(sum_amount) OVER (PARTITION BY staff_id ORDER BY payment_date) AS sum
FROM cte_sum_amount;


--ЗАДАНИЕ №2
--20 августа 2005 года в магазинах проходила акция: покупатель каждого сотого платежа получал
--дополнительную скидку на следующую аренду. С помощью оконной функции выведите всех покупателей,
--которые в день проведения акции получили скидку




--ЗАДАНИЕ №3
--Для каждой страны определите и выведите одним SQL-запросом покупателей, которые попадают под условия:
-- 1. покупатель, арендовавший наибольшее количество фильмов
-- 2. покупатель, арендовавший фильмов на самую большую сумму
-- 3. покупатель, который последним арендовал фильм






