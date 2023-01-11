import psycopg2 as ps2

with ps2.connect(database='clients', user='postgres', password='') as con:
    with con.cursor() as cur:

        def create_table(connection, cursor):
            cursor.execute("""
            CREATE TABLE if not exists clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR (40) NOT NULL,
            last_name VARCHAR (40) NOT NULL,
            mail TEXT UNIQUE
            );
            """)
            cursor.execute("""
            CREATE TABLE if not exists mobile(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL
            mobile_phone INTEGER UNIQUE
            );
            """)


        def new_client(cursor, first_name, last_name, mail):

            cursor.execute("""
            INSERT INTO clients(first_name, last_name, mail) VALUES(%s, %s, %s)
            RETURNING id;
            """, (first_name, last_name, mail))

            print(cursor.fetchone())


        def add_mobile(cursor, mobile: int, client_id):
            cursor.execute("""
            UPDATE mobile
            SET mobile_phone = %s
            WHERE client_id = %s;
            """, (mobile, client_id))  # Хотелось бы уточнить, можно ли так передавать %s?


        def change_data(cursor, client_id, column, value):

            cursor.execute("""
            UPDATE clients
            SET %s = %s
            WHERE id = %s;
            """, (column, value, client_id))


        def del_mobile(cursor, client_id):
            cursor.execute("""
            UPDATE mobile
            SET mobile_phone = ''
            WHERE id = %s;
            """, (client_id))


        def del_client(cursor, client_id):
            cursor.execute("""
            DELETE FROM clients
            WHERE id = %s
            """, (client_id,))


        def find_client(cursor, column, value):

            cursor.execute("""
            SELECT first_name, last_name, mail, mobile FROM clients WHERE %s = %s;
            """, (column, value))


        def user_request():
            function = int(input('Какую функцию Вы бы хотели реализовать: \n'
                                 '1) Добавить нового клиента \n'
                                 '2) Добавить телефон существующего клиента \n'
                                 '3) Изменить данные о клиенте \n'
                                 '4) Удалить телефон существующего клиента \n'
                                 '5) Удалить существующего клиента \n'
                                 '6) Найти клиента \n'))
            if function == 1:
                new_client(cur, 'Vasya', 'Petrov', 'bla-bla-mail')
            elif function == 2:
                add_mobile(cur, 8900000000, 2)
            elif function == 3:
                change_data(cur, 2, 'mail', 'sugar-mail')
            elif function == 4:
                del_mobile(cur, 2)
            elif function == 5:
                del_client(cur, 3)
            else:
                find_client(cur, 'mail', 'sugar-mail')
            print(user_request())


        user_request()