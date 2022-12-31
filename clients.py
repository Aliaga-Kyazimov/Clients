import psycopg2 as ps2

conn = ps2.connect(database='clients', user='postgres', password='')
cur = conn.cursor()

def create_table(connection, cursor):
    cursor.execute("""
    CREATE TABLE if not exists clients(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR (40) NOT NULL,
    last_name VARCHAR (40) NOT NULL,
    mail TEXT UNIQUE,
    mobile INTEGER UNIQUE
    );
    """)
    connection.commit()

def new_client(cursor):
    first_name = input('Введите имя клиента: ')
    last_name = input('Введите фамилию клиента: ')
    mail = input('Введите почту клиента: ')
    mobile = int(input('Введите телефон клиента (если нет, введите 0): '))

    if mobile != 0:
        cursor.execute (f"""
        INSERT INTO clients(first_name, last_name, mail, mobile) VALUES('{first_name}', '{last_name}', '{mail}', {mobile})
        RETURNING id;
        """)
    else:
        cursor.execute(f"""
               INSERT INTO clients(first_name, last_name, mail) VALUES('{first_name}', '{last_name}', '{mail}')
               RETURNING id;
               """)

    print(cursor.fetchone())

def add_mobile(connection, cursor, mobile, client_id):
    cursor.execute(f"""
    UPDATE clients
    SET mobile = {mobile}
    WHERE id = {client_id};
    """)
    connection.commit()

def change_data(connection, cursor, client_id):
    column = input('Какой столбец Вы бы хотели изменить: ')
    if column == 'mobile':
        value = int(input(f'Введите новый {column}: '))
    else:
        value = input(f'Введите новый {column}: ')
    cursor.execute(f"""
    UPDATE clients
    SET {column} = '{value}'
    WHERE id = {client_id};
    """)
    connection.commit()

def del_mobile(connection, cursor, client_id):
    cursor.execute(f"""
    UPDATE clients
    SET mobile = ''
    WHERE id = {client_id};
    """)
    connection.commit()

def del_client(connection, cursor, client_id):
    cursor.execute(f"""
    DELETE FROM clients
    WHERE id = {client_id}
    """)
    connection.commit()

def find_client(cursor):
    column = input('По какому значению (столбцу) желаете осуществить поиск: ')
    if column == 'mobile':
        value = int(input(f'Введите значение {column}: '))
    else:
        value = input(f'Введите значение {column}: ')
    cursor.execute(f"""
    SELECT first_name, last_name, mail, mobile FROM clients WHERE {column} = %s;
    """, (value,))
    print(cur.fetchone())


conn.close()
cur.close()