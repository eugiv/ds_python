--======== Итоговый проект ==============

--ЗАДАНИЕ №1
--Выведите название самолетов, которые имеют менее 50 посадочных мест

SELECT a.model FROM aircrafts AS a
JOIN seats AS s ON s.aircraft_code = a.aircraft_code
GROUP BY a.model
HAVING COUNT(s.seat_no) < 50;


--ЗАДАНИЕ №2
--Выведите процентное изменение ежемесячной суммы бронирования билетов, округленной до сотых.

WITH amount_sum_months AS
    (SELECT DATE_TRUNC('month', book_date) AS month_date, SUM(total_amount) AS total_monthly_amount
    FROM bookings
    GROUP BY month_date)

SELECT month_date::date,
    ROUND(total_monthly_amount / LAG(total_monthly_amount) OVER (ORDER BY month_date) * 100, 2) - 100
    AS percent_diff
FROM amount_sum_months;


--ЗАДАНИЕ №3
--Выведите названия самолетов не имеющих бизнес - класс. Решение должно быть через функцию array_agg.

SELECT a.model FROM aircrafts AS a
JOIN seats AS s ON s.aircraft_code = a.aircraft_code
GROUP BY a.model
HAVING NOT ARRAY_AGG(s.fare_conditions) @> ARRAY['Business']::varchar[];


--ЗАДАНИЕ №4
--Вывести накопительный итог количества мест в самолетах по каждому аэропорту на каждый день, учитывая только те самолеты, которые летали пустыми и только те дни, где из одного аэропорта таких самолетов вылетало более одного.
--В результате должны быть код аэропорта, дата, количество пустых мест в самолете и накопительный итог.
-- 1. код аэропорта вылета, 2. дата вылета, 3. кол-во пустых мест в самолете, 4. накопительный итог
-- 2 СТЕ если решаем через окно
-- найти корректный критерий, что на самолет не сел ни один из пассажиров (полностью пустые самолеты)
-- посчитать кол-во мест в каждом самолете
-- понять из какого аэропорта и в какой день вылетало более 1го пустого самолета
-- в ответе 4330 строк +-

SELECT f.flight_id, COUNT(bp.boarding_no) count_bp FROM flights AS f
LEFT JOIN ticket_flights AS tf ON tf.flight_id = f.flight_id
LEFT JOIN boarding_passes AS bp ON tf.ticket_no = bp.ticket_no
GROUP BY f.flight_id
HAVING COUNT(bp.boarding_no) = 0 -- логика нахождения полностью пустых самолетов
