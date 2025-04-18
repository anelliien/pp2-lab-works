import psycopg2
import csv

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="suppliers",
    user="postgres",
    password="qwerty",   # Или твой пароль от postgres
    host="localhost",
    port="5432"
)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Создание таблицы phonebook, если она не существует
def create_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone_number VARCHAR(20) UNIQUE
        );
    ''')
    conn.commit()

# Вставка новой записи через консоль
def insert_from_console():
    name = input("Enter first name: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Inserted.")

# Загрузка и вставка данных из CSV файла
def insert_from_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            name, phone = row
            try:
                cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
            except psycopg2.IntegrityError:
                conn.rollback()
                print(f"Duplicate or invalid entry: {name} - {phone}")
            else:
                conn.commit()
    print("CSV upload complete.")

# Обновление данных (имени или номера телефона)
def update_data():
    target = input("Update by (name/phone): ")
    if target == "name":
        old_name = input("Old name: ")
        new_name = input("New name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    elif target == "phone":
        old_phone = input("Old phone: ")
        new_phone = input("New phone: ")
        cur.execute("UPDATE phonebook SET phone_number = %s WHERE phone_number = %s", (new_phone, old_phone))
    conn.commit()
    print("Updated.")

# Запрос данных (по имени, телефону или всех записей)
# Запрос данных (по имени, телефону или всех записей)
def query_data():
    filter_by = input("Filter by (name/phone/all): ").strip().lower()
    
    if filter_by == "name":
        name = input("Enter part of the name: ").strip()
        cur.execute("SELECT * FROM phonebook WHERE LOWER(first_name) LIKE LOWER(%s)", ('%' + name + '%',))
    elif filter_by == "phone":
        phone = input("Enter part of the phone number: ").strip()
        cur.execute("SELECT * FROM phonebook WHERE phone_number LIKE %s", ('%' + phone + '%',))
    else:
        cur.execute("SELECT * FROM phonebook")
    
    results = cur.fetchall()
    
    if results:
        print("\nFound the following records:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No records found.")


# Главное меню
def menu():
    create_table()
    while True:
        print("\n1. Insert from console\n2. Insert from CSV\n3. Update\n4. Query\n5. Delete\n6. Exit")
        choice = input("Choose: ")
        if choice == '1':
            insert_from_console()
        elif choice == '2':
            insert_from_csv("contacts.csv")  # Убедись, что файл contacts.csv лежит в той же папке
        elif choice == '3':
            update_data()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_data()
        elif choice == '6':
            break

    cur.close()
    conn.close()

# Запуск программы
menu()
