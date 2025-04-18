-- Создание таблицы (если еще нет)
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    phone_number VARCHAR(20) UNIQUE
);

-- 1. Функция поиска по шаблону (имя или номер)
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, phone_number VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.phone_number
    FROM phonebook pb
    WHERE LOWER(pb.first_name) LIKE LOWER('%' || pattern || '%')
       OR pb.phone_number LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Процедура вставки или обновления по имени
CREATE OR REPLACE PROCEDURE insert_or_update_user(name TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE LOWER(first_name) = LOWER(name)) THEN
        UPDATE phonebook SET phone_number = phone WHERE LOWER(first_name) = LOWER(name);
    ELSE
        INSERT INTO phonebook(first_name, phone_number) VALUES(name, phone);
    END IF;
END;
$$;

-- 3. Процедура массовой вставки с проверкой номеров
CREATE OR REPLACE PROCEDURE insert_many_users(users TEXT[][])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    name TEXT;
    phone TEXT;
    invalid_data TEXT := '';
BEGIN
    FOR i IN 1 .. array_length(users, 1) LOOP
        name := users[i][1];
        phone := users[i][2];

        -- Простейшая проверка номера (можно улучшить)
        IF phone ~ '^\+?\d{10,15}$' THEN
            BEGIN
                INSERT INTO phonebook(first_name, phone_number)
                VALUES (name, phone);
            EXCEPTION WHEN unique_violation THEN
                UPDATE phonebook SET first_name = name WHERE phone_number = phone;
            END;
        ELSE
            invalid_data := invalid_data || FORMAT('Invalid: %s - %s\n', name, phone);
        END IF;
    END LOOP;

    RAISE NOTICE '%', invalid_data;
END;
$$;

-- 4. Функция пагинации по limit и offset
CREATE OR REPLACE FUNCTION get_phonebook_page(limit_num INT, offset_num INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT limit_num OFFSET offset_num;
END;
$$ LANGUAGE plpgsql;

-- 5. Процедура удаления по имени или номеру
CREATE OR REPLACE PROCEDURE delete_user(identifier TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE LOWER(first_name) = LOWER(identifier) 
       OR phone_number = identifier;
END;
$$;