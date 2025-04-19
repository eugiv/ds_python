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
        LEFT JOIN boarding_passes AS bp ON f.flight_id = bp.flight_id
        WHERE bp.boarding_no IS NULL
),

    seats_cumulative AS (
        SELECT f.departure_airport, f.actual_departure::date, COUNT(s.seat_no) empty_seats_per_aircraft,
            SUM(COUNT(s.seat_no)) OVER (PARTITION BY f.departure_airport, f.actual_departure::date ORDER BY
                f.actual_departure) AS seats_cum_sum,
            COUNT(f.actual_departure::date) OVER (PARTITION BY f.departure_airport,
                f.actual_departure::date) AS days_count_by_airport
        FROM flights AS f
        JOIN empty_flights AS ef ON ef.flight_id = f.flight_id
        JOIN seats AS s ON s.aircraft_code = f.aircraft_code
        GROUP BY f.departure_airport, f.actual_departure
)

SELECT departure_airport, actual_departure, empty_seats_per_aircraft, seats_cum_sum FROM seats_cumulative
WHERE days_count_by_airport > 1
ORDER BY departure_airport, actual_departure;


--ЗАДАНИЕ №5
--Найдите процентное соотношение перелетов по маршрутам от общего количества перелетов.
--Выведите в результат названия аэропортов и процентное отношение.
--Решение должно быть через оконную функцию.

SELECT ad.airport_name AS dept_airport_name, aa.airport_name AS arr_airport_name,
       COUNT(f.flight_id) * 100 / SUM(COUNT(f.flight_id)) OVER () AS flights_percent_rate
       FROM flights AS f
JOIN airports AS ad ON ad.airport_code = f.departure_airport
JOIN airports AS aa ON aa.airport_code = f.arrival_airport
WHERE status='Arrived'
GROUP BY ad.airport_code, aa.airport_code;


--ЗАДАНИЕ №6
--Выведите количество пассажиров по каждому коду сотового оператора, если учесть,
--что код оператора - это три символа после +7

WITH phone_codes AS (
    SELECT
        SUBSTRING(contact_data->>'phone' FROM POSITION('+7' IN contact_data->>'phone') + 2 FOR 3)
        AS cell_code
    FROM tickets
    WHERE contact_data->>'phone' IS NOT NULL
)

SELECT cell_code, COUNT(cell_code) AS passengers_num
FROM phone_codes
GROUP BY cell_code;


--ЗАДАНИЕ №7
--Классифицируйте финансовые обороты (сумма стоимости перелетов) по маршрутам:
--До 50 млн - low
--От 50 млн включительно до 150 млн - middle
--От 150 млн включительно - high
--Выведите в результат количество маршрутов в каждом полученном классе

SELECT turnover_class, COUNT(turnover_class) AS routes_sum FROM(
    SELECT
        CASE
            WHEN SUM(amount) < 50000000 THEN 'low'
            WHEN SUM(amount) >= 50000000 AND SUM(amount) < 150000000 THEN 'middle'
            ELSE 'high'
        END AS turnover_class
    FROM ticket_flights AS ft
    JOIN flights AS f ON f.flight_id = ft.flight_id
    GROUP BY f.departure_airport, f.arrival_airport) AS cls
GROUP BY turnover_class;


--ЗАДАНИЕ №8
--Вычислите медиану стоимости перелетов, медиану размера бронирования и отношение медианы
--бронирования к медиане стоимости перелетов, округленной до сотых

WITH flights_median AS (
  SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS med_flght_amnt
  FROM ticket_flights
),
    bookings_median AS (
  SELECT
     PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) AS med_book_amnt
  FROM bookings
        )
SELECT
  ROUND((mba.med_book_amnt / mfa.med_flght_amnt)::numeric, 2) AS median_rate
FROM flights_median AS mfa, bookings_median AS mba;


--ЗАДАНИЕ №9
--Найдите значение минимальной стоимости полета 1 км для пассажиров.
--То есть нужно найти расстояние между аэропортами и с учетом стоимости перелетов
--получить искомый результат

--CREATE EXTENSION cube;
--CREATE EXTENSION earthdistance;

WITH distance_between_airports_km AS (SELECT CONCAT(a1.airport_code, a2.airport_code) AS joint_apt_id,
       earth_distance(ll_to_earth(a1.latitude, a1.longitude),
                      ll_to_earth(a2.latitude, a2.longitude)) / 1000 as airport_distance_km
FROM airports AS a1, airports AS a2
WHERE a1.airport_code != a2.airport_code),

min_amount_between_airports AS (SELECT CONCAT(f.departure_airport, f.arrival_airport) AS joint_apt_id,
                                       MIN(tf.amount) AS min_route_amount FROM flights AS f
JOIN ticket_flights AS tf ON tf.flight_id = f.flight_id
GROUP BY f.departure_airport, f.arrival_airport)

SELECT ROUND((min_route_amount / airport_distance_km)::numeric, 2) AS min_flight_rate_per_km FROM distance_between_airports_km AS dbak
JOIN min_amount_between_airports AS maba ON maba.joint_apt_id = dbak.joint_apt_id
ORDER BY min_flight_rate_per_km
LIMIT 1;
