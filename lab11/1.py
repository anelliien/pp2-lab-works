import psycopg2
import csv
import json


# Подключение к базе данных
conn = psycopg2.connect(
    dbname="suppliers",
    user="postgres",
    password="qwerty",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# SQL-based: Создание таблицы
def create_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone_number VARCHAR(20) UNIQUE
        );
    ''')
    conn.commit()

# SQL-based: Вставка из CSV
def insert_from_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            name, phone = row
            try:
                cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
            except psycopg2.IntegrityError:
                conn.rollback()
                print(f"Duplicate or invalid: {name} - {phone}")
            else:
                conn.commit()
    print("CSV upload complete.")

# Procedure: Вставка или обновление
def insert_or_update_user(name, phone):
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    print("User inserted or updated.")

# Procedure: Массовая вставка
def insert_many_users(user_list):
    cur.execute("CALL insert_many_users(%s)", (user_list,))
    conn.commit()
    print("Batch insert complete.")
def insert_many_users(user_list):
    users_json = json.dumps(user_list)  # Преобразуем в JSON-строку
    cur.execute("CALL insert_many_users(%s)", (users_json,))
    conn.commit()
    print("Batch insert complete.")

# Procedure: Поиск по шаблону
def search_pattern(pattern):
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    results = cur.fetchall()
    if results:
        print("\nSearch results:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No results found.")

# Procedure: Пагинация
def get_paginated(limit, offset):
    cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
    results = cur.fetchall()
    if results:
        print(f"\nPage (limit={limit}, offset={offset}):")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No records on this page.")

# Procedure: Удаление
def delete_user(identifier):
    cur.execute("CALL delete_user(%s)", (identifier,))
    conn.commit()
    print(f"User(s) with name or phone '{identifier}' deleted.")

# Главное меню
def menu():
    create_table()
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert or update user (procedure)")
        print("2. Insert many users (procedure)")
        print("3. Load from CSV (direct SQL)")
        print("4. Search by pattern (procedure)")
        print("5. Paginate (procedure)")
        print("6. Delete user (procedure)")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == '1':
            name = input("Name: ")
            phone = input("Phone: ")
            insert_or_update_user(name, phone)
        elif choice == '2':
            n = int(input("How many users? "))
            users = []
            for _ in range(n):
                name = input("Name: ")
                phone = input("Phone: ")
                users.append([name, phone])
            insert_many_users(users)
        elif choice == '3':
            filename = input("CSV filename: ")
            insert_from_csv(filename)
        elif choice == '4':
            pattern = input("Pattern (name/phone): ")
            search_pattern(pattern)
        elif choice == '5':
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            get_paginated(limit, offset)
        elif choice == '6':
            identifier = input("Name or phone to delete: ")
            delete_user(identifier)
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

# Запуск
if __name__ == "__main__":
    menu()