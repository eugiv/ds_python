--=============== МОДУЛЬ 3. ОСНОВЫ SQL =======================================
--= ПОМНИТЕ, ЧТО НЕОБХОДИМО УСТАНОВИТЬ ВЕРНОЕ СОЕДИНЕНИЕ И ВЫБРАТЬ СХЕМУ PUBLIC===========
SET search_path TO public;

--======== ОСНОВНАЯ ЧАСТЬ ==============

--ЗАДАНИЕ №1
--Выведите для каждого покупателя его адрес проживания, 
--город и страну проживания.

SELECT CONCAT_WS(' ', c.last_name, c.first_name), a.address, ct.city, cn.country
FROM customer AS c
JOIN address AS a ON a.address_id = c.address_id
JOIN city AS ct ON ct.city_id = a.city_id
JOIN country AS cn ON cn.country_id = ct.country_id;


--ЗАДАНИЕ №2
--С помощью SQL-запроса посчитайте для каждого магазина количество его покупателей.

SELECT s.store_id AS "ID магазина", COUNT(c.store_id) AS "Количество покупателей"
FROM store AS s
JOIN customer AS c ON c.store_id = s.store_id
GROUP BY s.store_id;


--Доработайте запрос и выведите только те магазины, 
--у которых количество покупателей больше 300-от.
--Для решения используйте фильтрацию по сгруппированным строкам 
--с использованием функции агрегации.

SELECT s.store_id AS "ID магазина", COUNT(c.customer_id) AS "Количество покупателей"
FROM store AS s
JOIN customer AS c ON c.store_id = s.store_id
GROUP BY s.store_id
HAVING COUNT(c.customer_id) > 300;


-- Доработайте запрос, добавив в него информацию о городе магазина, 
--а также фамилию и имя продавца, который работает в этом магазине.

SELECT st_cnt."ID магазина", st_cnt."Количество покупателей", ct.city AS "Город",
       CONCAT_WS(' ', st.last_name, st.first_name) AS "Имя сотрудника"
FROM city AS ct
    JOIN address AS a ON ct.city_id = a.city_id
    JOIN
        (SELECT s.store_id AS "ID магазина", s.address_id, COUNT(c.customer_id) AS "Количество покупателей", s.manager_staff_id
        FROM store AS s
        JOIN customer AS c ON c.store_id = s.store_id
        GROUP BY s.store_id
        HAVING COUNT(c.customer_id) > 300) AS st_cnt ON st_cnt.address_id = a.address_id
    JOIN staff AS st ON st.staff_id = st_cnt.manager_staff_id;


--ЗАДАНИЕ №3
--Выведите ТОП-5 покупателей, 
--которые взяли в аренду за всё время наибольшее количество фильмов

SELECT CONCAT_WS(' ', c.last_name, c.first_name) AS "Фамилия и имя покупателя" ,COUNT(r.rental_id) AS "Количество фильмов"
FROM rental AS r
JOIN customer AS c ON c.customer_id = r.customer_id
GROUP BY c.customer_id
ORDER BY "Количество фильмов" DESC
LIMIT 5;


--ЗАДАНИЕ №4
--Посчитайте для каждого покупателя 4 аналитических показателя:
--  1. количество фильмов, которые он взял в аренду
--  2. общую стоимость платежей за аренду всех фильмов (значение округлите до целого числа)
--  3. минимальное значение платежа за аренду фильма
--  4. максимальное значение платежа за аренду фильма

SELECT CONCAT_WS(' ', c.last_name, c.first_name) AS "Фамилия и имя покупателя" ,COUNT(r.rental_id) AS "Количество фильмов",
       ROUND(SUM(p.amount), 0) AS "Общая стоимость платежей", MIN(p.amount) AS "Минимальная стоимость платежа",
       MAX(p.amount) AS "Максимальная стоимость платежа"
FROM payment AS p
JOIN customer AS c ON c.customer_id = p.customer_id
JOIN rental AS r ON r.rental_id =p.rental_id
GROUP BY c.customer_id;


--ЗАДАНИЕ №5
--Используя данные из таблицы городов, составьте все возможные пары городов так, чтобы 
--в результате не было пар с одинаковыми названиями городов. Решение должно быть через Декартово произведение.
 
SELECT c1.city AS "Город 1", c2.city AS "Город 2" FROM city AS c1
CROSS JOIN city c2
WHERE c1.city != c2.city;


--ЗАДАНИЕ №6
--Используя данные из таблицы rental о дате выдачи фильма в аренду (поле rental_date) и 
--дате возврата (поле return_date), вычислите для каждого покупателя среднее количество 
--дней, за которые он возвращает фильмы. В результате должны быть дробные значения, а не интервал.
 
SELECT customer_id AS "ID покупателя", ROUND(AVG(DATE(return_date) - DATE(rental_date)), 2)
    AS "Среднее количество дней на возврат"
FROM rental
GROUP BY customer_id
ORDER BY customer_id;


--======== ДОПОЛНИТЕЛЬНАЯ ЧАСТЬ ==============

--ЗАДАНИЕ №1
--Посчитайте для каждого фильма сколько раз его брали в аренду и значение общей стоимости аренды фильма за всё время.

WITH rental_data AS (
        SELECT i.film_id, COUNT(r.rental_id) AS r_c, SUM(p.amount) AS a_s FROM inventory AS i
        JOIN rental AS r ON r.inventory_id = i.inventory_id
        JOIN payment AS p ON p.rental_id = r.rental_id
        GROUP BY i.film_id
    ),

    movie_genre_rental AS (
    SELECT fc.film_id, STRING_AGG(c.name, ', ') AS genres, rd.r_c, rd.a_s FROM category AS c
    JOIN film_category AS fc ON fc.category_id = c.category_id
    LEFT JOIN rental_data AS rd ON rd.film_id = fc.film_id
    GROUP BY fc.film_id, rd.r_c, rd.a_s
    )

SELECT f.title AS "Название фильма", f.rating AS "Рейтинг", mgr.genres AS "Жанр", release_year AS "Год выпуска",
       l.name AS "Язык", COALESCE(mgr.r_c, 0) AS "Количество аренд", COALESCE(mgr.a_s, 0) AS "Общая стоимость аренды" FROM film AS f
LEFT JOIN movie_genre_rental AS mgr ON mgr.film_id = f.film_id
JOIN "language" AS l ON l.language_id = f.language_id
ORDER BY f.title;


--ЗАДАНИЕ №2
--Доработайте запрос из предыдущего задания и выведите с помощью него фильмы, которые отсутствуют на dvd дисках.

WITH rental_data AS (
        SELECT i.film_id, COUNT(r.rental_id) AS r_c, SUM(p.amount) AS a_s FROM inventory AS i
        JOIN rental AS r ON r.inventory_id = i.inventory_id
        JOIN payment AS p ON p.rental_id = r.rental_id
        GROUP BY i.film_id
    ),

    movie_genre_rental AS (
    SELECT fc.film_id, rd.film_id AS inv_film_id, STRING_AGG(c.name, ', ') AS genre, rd.r_c, rd.a_s FROM category AS c
    JOIN film_category AS fc ON fc.category_id = c.category_id
    LEFT JOIN rental_data AS rd ON rd.film_id = fc.film_id
    GROUP BY fc.film_id, rd.r_c, rd.film_id, rd.a_s
    )

SELECT title AS "Название фильма", rating AS "Рейтинг", mgr.genre AS "Жанр", release_year AS "Год выпуска",
       l.name AS "Язык", COALESCE(mgr.r_c, 0) AS "Количество аренд", mgr.a_s AS "Общая стоимость аренды" FROM film AS f
LEFT JOIN movie_genre_rental AS mgr ON mgr.film_id = f.film_id
JOIN "language" AS l ON l.language_id = f.language_id
WHERE mgr.inv_film_id is NULL
ORDER BY title;


--ЗАДАНИЕ №3
--Посчитайте количество продаж, выполненных каждым продавцом. Добавьте вычисляемую колонку "Премия".
--Если количество продаж превышает 7300, то значение в колонке будет "Да", иначе должно быть значение "Нет".

SELECT s.staff_id, COUNT(p.payment_id) AS "Количество продаж",
CASE
    WHEN COUNT(payment_id) > 7300
    THEN 'Да'
    ELSE 'Нет'
END AS "Премия"
FROM payment AS p
RIGHT JOIN staff AS s ON s.staff_id=p.staff_id
GROUP BY s.staff_id;
