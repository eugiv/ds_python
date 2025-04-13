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

WITH empty_flights AS (
        SELECT f.flight_id FROM flights AS f
        LEFT JOIN ticket_flights AS tf ON tf.flight_id = f.flight_id
        LEFT JOIN boarding_passes AS bp ON tf.ticket_no = bp.ticket_no
        GROUP BY f.flight_id
        HAVING COUNT(bp.boarding_no) = 0
),

    seats_cumulative AS (
        SELECT f.departure_airport, f.actual_departure::date, COUNT(s.seat_no) empty_seats_per_aircraft,
            SUM(COUNT(s.seat_no)) OVER (PARTITION BY f.departure_airport, f.actual_departure::date ORDER BY
                f.actual_departure) AS seats_cum_sum,
            COUNT(f.actual_departure::date) OVER (PARTITION BY f.departure_airport,
                f.actual_departure::date) AS days_count_by_airport
        FROM flights AS f
        JOIN empty_flights AS ef ON ef.flight_id = f.flight_id
        JOIN aircrafts AS a ON a.aircraft_code = f.aircraft_code
        JOIN seats AS s ON s.aircraft_code = a.aircraft_code
        WHERE f.actual_departure IS NOT NULL
        GROUP BY f.departure_airport, f.actual_departure
)

SELECT departure_airport, actual_departure, empty_seats_per_aircraft, seats_cum_sum FROM seats_cumulative
WHERE days_count_by_airport > 1
ORDER BY departure_airport, actual_departure;


--ЗАДАНИЕ №5
--Найдите процентное соотношение перелетов по маршрутам от общего количества перелетов.
--Выведите в результат названия аэропортов и процентное отношение.
--Решение должно быть через оконную функцию.