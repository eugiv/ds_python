--=============== МОДУЛЬ 6. POSTGRESQL =======================================
--= ПОМНИТЕ, ЧТО НЕОБХОДИМО УСТАНОВИТЬ ВЕРНОЕ СОЕДИНЕНИЕ И ВЫБРАТЬ СХЕМУ PUBLIC===========
SET search_path TO public;

--======== ОСНОВНАЯ ЧАСТЬ ==============

--ЗАДАНИЕ №1
--Напишите SQL-запрос, который выводит всю информацию о фильмах 
--со специальным атрибутом "Behind the Scenes".

SELECT film_id, INITCAP(title) AS title, special_features FROM film
WHERE 'Behind the Scenes' = any(special_features);


--ЗАДАНИЕ №2
--Напишите еще 2 варианта поиска фильмов с атрибутом "Behind the Scenes",
--используя другие функции или операторы языка SQL для поиска значения в массиве.

SELECT film_id, INITCAP(title) AS title, special_features FROM film
WHERE 'Behind the Scenes' IN (SELECT unnest(special_features));

SELECT film_id, INITCAP(title) AS title, special_features FROM film
WHERE special_features @> ARRAY['Behind the Scenes'];


--ЗАДАНИЕ №3
--Для каждого покупателя посчитайте сколько он брал в аренду фильмов 
--со специальным атрибутом "Behind the Scenes.

--Обязательное условие для выполнения задания: используйте запрос из задания 1, 
--помещенный в CTE. CTE необходимо использовать для решения задания.

WITH cte_1 AS (
    SELECT film_id, INITCAP(title) AS title, special_features FROM film
    WHERE 'Behind the Scenes' = any(special_features)
    )

SELECT customer_id, COUNT(customer_id) AS film_count FROM cte_1 AS c1
JOIN inventory AS i ON i.film_id = c1.film_id
JOIN rental AS r ON i.inventory_id = r.inventory_id
GROUP BY customer_id
ORDER BY customer_id;


--ЗАДАНИЕ №4
--Для каждого покупателя посчитайте сколько он брал в аренду фильмов
-- со специальным атрибутом "Behind the Scenes".

--Обязательное условие для выполнения задания: используйте запрос из задания 1,
--помещенный в подзапрос, который необходимо использовать для решения задания.

SELECT customer_id, COUNT(customer_id) AS film_count FROM
    (SELECT film_id, INITCAP(title) AS title, special_features FROM film
    WHERE 'Behind the Scenes' = any(special_features)) AS sbq_1
JOIN inventory AS i ON i.film_id = sbq_1.film_id
JOIN rental AS r ON i.inventory_id = r.inventory_id
GROUP BY customer_id
ORDER BY customer_id;


--ЗАДАНИЕ №5
--Создайте материализованное представление с запросом из предыдущего задания
--и напишите запрос для обновления материализованного представления

CREATE MATERIALIZED VIEW customer_film_count AS
    SELECT customer_id, COUNT(customer_id) AS film_count FROM
        (SELECT film_id, INITCAP(title) AS title, special_features FROM film
        WHERE 'Behind the Scenes' = any(special_features)) AS sbq_1
    JOIN inventory AS i ON i.film_id = sbq_1.film_id
    JOIN rental AS r ON i.inventory_id = r.inventory_id
    GROUP BY customer_id
    ORDER BY customer_id;

REFRESH MATERIALIZED VIEW customer_film_count;


--ЗАДАНИЕ №6
--С помощью explain analyze проведите анализ стоимости выполнения запросов из предыдущих заданий и ответьте на вопросы:
--1. с каким оператором или функцией языка SQL, используемыми при выполнении домашнего задания: 
--поиск значения в массиве затрачивает меньше ресурсов системы;
--2. какой вариант вычислений затрачивает меньше ресурсов системы: 
--с использованием CTE или с использованием подзапроса.

-- 1) cost: 78.84
-- 2.1) cost: 452.5
-- 2.2) cost: 68.84
-- 3) cost: 819.16
-- 4) cost: 685.47

--      Ответы на вопросы:
--      1) Наименьшая стоимость запроса в 2.2, так как оператор "@>" лучше оптимизирован для работы в массивах
--      2) В данном случае стомость выполенения подзапроса дешевле, так как он относитально простой
--          и не требует повторных вычислений (в этом случае CTE могла бы быть эфеективнее)



--======== ДОПОЛНИТЕЛЬНАЯ ЧАСТЬ ==============

--ЗАДАНИЕ №1
--Выполняйте это задание в форме ответа на сайте Нетологии

--ЗАДАНИЕ №2
--Используя оконную функцию выведите для каждого сотрудника
--сведения о самой первой продаже этого сотрудника.

WITH cte_1 AS (
    SELECT s.staff_id, f.film_id, f.title, p.amount, p.payment_date,
       c.last_name AS customer_last_name, c.first_name AS customer_first_name,
       ROW_NUMBER() OVER (PARTITION BY p.staff_id ORDER BY payment_date) AS sales_num
    FROM staff AS s
JOIN payment AS p ON p.staff_id = s.staff_id
JOIN rental AS r ON r.rental_id = p.rental_id
JOIN customer AS c ON c.customer_id = r.customer_id
JOIN inventory AS i ON i.inventory_id = r.inventory_id
JOIN film AS f ON f.film_id = i.film_id)

SELECT staff_id, film_id, title, amount, payment_date, customer_last_name,
    customer_first_name FROM cte_1
WHERE sales_num = 1;


--ЗАДАНИЕ №3
--Для каждого магазина определите и выведите одним SQL-запросом следующие аналитические показатели:
-- 1. день, в который арендовали больше всего фильмов (день в формате год-месяц-день)
-- 2. количество фильмов взятых в аренду в этот день
-- 3. день, в который продали фильмов на наименьшую сумму (день в формате год-месяц-день)
-- 4. сумму продажи в этот день

WITH days_rent_count AS (
        SELECT i.store_id, r.rental_date::date, COUNT(r.inventory_id) AS total_rentals,
            ROW_NUMBER() OVER (PARTITION BY i.store_id ORDER BY COUNT(r.inventory_id) DESC) AS store_rank
        FROM rental AS r
        JOIN inventory AS i ON i.inventory_id = r.inventory_id
        GROUP BY i.store_id, r.rental_date::date),

    rent_amount AS (
        SELECT s.store_id, p.payment_date::date, SUM(p.amount) AS ttl_amount,
            ROW_NUMBER() OVER (PARTITION BY s.store_id ORDER BY SUM(p.amount)) AS payment_rank
        FROM payment AS p
        JOIN staff AS s ON s.staff_id = p.staff_id
        GROUP BY s.store_id, p.payment_date::date)

SELECT
drc.store_id AS "ID магазина",
drc.rental_date AS "День, в который арендовали больше всего фильмов",
drc.total_rentals AS "Количество фильмов, взятых в аренду в этот день",
ra.payment_date AS "День, в который продали фильмов на наименьшую сумму",
ra.ttl_amount AS "Сумма продажи в этот день"
FROM days_rent_count AS drc
JOIN rent_amount AS ra ON ra.store_id = drc.store_id AND ra.payment_rank = 1
WHERE drc.store_rank = 1;
