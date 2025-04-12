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


