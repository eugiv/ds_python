--=============== МОДУЛЬ 4. УГЛУБЛЕНИЕ В SQL =======================================
--= ПОМНИТЕ, ЧТО НЕОБХОДИМО УСТАНОВИТЬ ВЕРНОЕ СОЕДИНЕНИЕ И ВЫБРАТЬ СХЕМУ PUBLIC===========
CREATE SCHEMA ivanov_module_4_sql_1;
SET search_path TO ivanov_module_4_sql_1;

--======== ОСНОВНАЯ ЧАСТЬ ==============

--ЗАДАНИЕ №1
--База данных: если подключение к облачной базе, то создаёте новую схему с префиксом в --виде фамилии, название должно быть на латинице в нижнем регистре и таблицы создаете --в этой новой схеме, если подключение к локальному серверу, то создаёте новую схему и --в ней создаёте таблицы.

--Спроектируйте базу данных, содержащую три справочника:
--· язык (английский, французский и т. п.);
--· народность (славяне, англосаксы и т. п.);
--· страны (Россия, Германия и т. п.).
--Две таблицы со связями: язык-народность и народность-страна, отношения многие ко многим. Пример таблицы со связями — film_actor.
--Требования к таблицам-справочникам:
--· наличие ограничений первичных ключей.
--· идентификатору сущности должен присваиваться автоинкрементом;
--· наименования сущностей не должны содержать null-значения, не должны допускаться --дубликаты в названиях сущностей.
--Требования к таблицам со связями:
--· наличие ограничений первичных и внешних ключей.

--В качестве ответа на задание пришлите запросы создания таблиц и запросы по --добавлению в каждую таблицу по 5 строк с данными.
 
--СОЗДАНИЕ ТАБЛИЦЫ ЯЗЫКИ

CREATE TABLE ivanov_module_4_sql_1.language (
    language_id SERIAL2 PRIMARY KEY,
    language_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    created_user VARCHAR(64) NOT NULL DEFAULT current_user,
    delete_mark BOOLEAN NOT NULL DEFAULT FALSE
);

--ВНЕСЕНИЕ ДАННЫХ В ТАБЛИЦУ ЯЗЫКИ

INSERT INTO ivanov_module_4_sql_1.language (language_name) VALUES
('английский'), ('русский'), ('французский'), ('немецкий'), ('японский');


--СОЗДАНИЕ ТАБЛИЦЫ НАРОДНОСТИ

CREATE TABLE ivanov_module_4_sql_1.ethnic (
    ethnic_id SERIAL2 PRIMARY KEY,
    ethnic_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    created_user VARCHAR(64) NOT NULL DEFAULT current_user,
    delete_mark BOOLEAN NOT NULL DEFAULT FALSE
);

--ВНЕСЕНИЕ ДАННЫХ В ТАБЛИЦУ НАРОДНОСТИ

INSERT INTO ivanov_module_4_sql_1.ethnic (ethnic_name) VALUES
('англичане'), ('русские'), ('французы'), ('немцы'), ('японцы');


--СОЗДАНИЕ ТАБЛИЦЫ СТРАНЫ

CREATE TABLE ivanov_module_4_sql_1.country (
    country_id SERIAL2 PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE,
    country_code INT2 NOT NULL UNIQUE CHECK ( country_code > 0 ),
    created_at TIMESTAMP DEFAULT current_timestamp,
    created_user VARCHAR(64) NOT NULL DEFAULT current_user,
    delete_mark BOOLEAN NOT NULL DEFAULT FALSE
);


--ВНЕСЕНИЕ ДАННЫХ В ТАБЛИЦУ СТРАНЫ

INSERT INTO ivanov_module_4_sql_1.country (country_name, country_code) VALUES
('Великобритания', 1), ('РФ', 2), ('Франция', 3), ('Германия', 4), ('Япония', 5);


--СОЗДАНИЕ ПЕРВОЙ ТАБЛИЦЫ СО СВЯЗЯМИ

CREATE TABLE ivanov_module_4_sql_1.language_ethnic (
    language_id INT2 NOT NULL,
    ethnic_id INT2 NOT NULL,
    PRIMARY KEY (language_id, ethnic_id),
    FOREIGN KEY (language_id) REFERENCES ivanov_module_4_sql_1.language(language_id) ON DELETE CASCADE,
    FOREIGN KEY (ethnic_id) REFERENCES ivanov_module_4_sql_1.ethnic(ethnic_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    created_user VARCHAR(64) NOT NULL DEFAULT current_user,
    delete_mark BOOLEAN NOT NULL DEFAULT FALSE
);


--ВНЕСЕНИЕ ДАННЫХ В ТАБЛИЦУ СО СВЯЗЯМИ

INSERT INTO ivanov_module_4_sql_1.language_ethnic (language_id, ethnic_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5);


--СОЗДАНИЕ ВТОРОЙ ТАБЛИЦЫ СО СВЯЗЯМИ

CREATE TABLE ivanov_module_4_sql_1.ethnic_country (
    ethnic_id INT2 NOT NULL,
    country_id INT2 NOT NULL,
    PRIMARY KEY (ethnic_id, country_id),
    FOREIGN KEY (ethnic_id) REFERENCES ivanov_module_4_sql_1.ethnic(ethnic_id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES ivanov_module_4_sql_1.country(country_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    created_user VARCHAR(64) NOT NULL DEFAULT current_user,
    delete_mark BOOLEAN NOT NULL DEFAULT FALSE
);


--ВНЕСЕНИЕ ДАННЫХ В ТАБЛИЦУ СО СВЯЗЯМИ

INSERT INTO ivanov_module_4_sql_1.ethnic_country (ethnic_id, country_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5);


--======== ДОПОЛНИТЕЛЬНАЯ ЧАСТЬ ==============


--ЗАДАНИЕ №1 
--Создайте новую таблицу film_new со следующими полями:
--·   	film_name - название фильма - тип данных varchar(255) и ограничение not null
--·   	film_year - год выпуска фильма - тип данных integer, условие, что значение должно быть больше 0
--·   	film_rental_rate - стоимость аренды фильма - тип данных numeric(4,2), значение по умолчанию 0.99
--·   	film_duration - длительность фильма в минутах - тип данных integer, ограничение not null и условие, что значение должно быть больше 0
--Если работаете в облачной базе, то перед названием таблицы задайте наименование вашей схемы.

CREATE TABLE ivanov_module_4_sql_1.film_new (
    film_id SERIAL PRIMARY KEY,
    film_name VARCHAR(255) NOT NULL,
    film_year INTEGER CHECK (film_year > 0),
    film_rental_rate NUMERIC(4,2) DEFAULT 0.99,
    film_duration INTEGER NOT NULL CHECK (film_duration > 0)
);


--ЗАДАНИЕ №2 
--Заполните таблицу film_new данными с помощью SQL-запроса, где колонкам соответствуют массивы данных:
--·       film_name - array['The Shawshank Redemption', 'The Green Mile', 'Back to the Future', 'Forrest Gump', 'Schindlers List']
--·       film_year - array[1994, 1999, 1985, 1994, 1993]
--·       film_rental_rate - array[2.99, 0.99, 1.99, 2.99, 3.99]
--·   	  film_duration - array[142, 189, 116, 142, 195]

INSERT INTO ivanov_module_4_sql_1.film_new (film_name, film_year, film_rental_rate, film_duration)
VALUES ('The Shawshank Redemption', 1994, 2.99, 142), ('The Green Mile', 1999, 0.99, 189),
       ('Back to the Future', 1985, 1.99, 116), ('Forrest Gump', 1994, 2.99, 142),
       ('Schindler’s List', 1993, 3.99, 195);


--ЗАДАНИЕ №3
--Обновите стоимость аренды фильмов в таблице film_new с учетом информации, 
--что стоимость аренды всех фильмов поднялась на 1.41

UPDATE ivanov_module_4_sql_1.film_new
SET film_rental_rate = film_rental_rate + 1.41;


--ЗАДАНИЕ №4
--Фильм с названием "Back to the Future" был снят с аренды, 
--удалите строку с этим фильмом из таблицы film_new

DELETE FROM ivanov_module_4_sql_1.film_new
WHERE film_name = 'Back to the Future';

--ЗАДАНИЕ №5
--Добавьте в таблицу film_new запись о любом другом новом фильме

INSERT INTO ivanov_module_4_sql_1.film_new (film_name, film_year, film_rental_rate, film_duration)
VALUES ('The Green Elefant', 1999, 10.50, 86);


--ЗАДАНИЕ №6
--Напишите SQL-запрос, который выведет все колонки из таблицы film_new, 
--а также новую вычисляемую колонку "длительность фильма в часах", округлённую до десятых

SELECT *, ROUND(film_duration::numeric / 60, 1) AS hrs_duration
FROM ivanov_module_4_sql_1.film_new;


--ЗАДАНИЕ №7 
--Удалите таблицу film_new

DROP TABLE ivanov_module_4_sql_1.film_new;
