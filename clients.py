import psycopg2 as ps2


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
    client_id INTEGER NOT NULL REFERENCES clients(id),
    mobile_phone INTEGER UNIQUE
    );
    """)
    connection.commit()


def new_client(connection, cursor, first_name, last_name, mail):
    cursor.execute("""
    INSERT INTO clients(first_name, last_name, mail) VALUES(%s, %s, %s) 
    RETURNING id;
    """, (first_name, last_name, mail))
    connection.commit()


def add_mobile(connection, cursor, client_id, mobile: int):
    cursor.execute("""
    INSERT INTO mobile(client_id, mobile_phone) VALUES(%s, %s);
    """, (client_id, mobile))
    connection.commit()


def change_data(cursor, client_id, first_name=None, last_name=None, mail=None):
    if first_name is not None:
        cursor.execute("""
        UPDATE clients
        SET first_name = %(first_name)s
        WHERE id = %(client_id)s;
        """, {'first_name': first_name, 'client_id': client_id})
    if last_name is not None:
        cursor.execute("""
           UPDATE clients
           SET last_name = %(last_name)s
           WHERE id = %(client_id)s;
           """, {'last_name': last_name, 'client_id': client_id})
    if mail is not None:
        cursor.execute("""
           UPDATE clients
           SET mail = %(mail)s
           WHERE id = %(client_id)s;
           """, {'mail': mail, 'client_id': client_id})


def del_mobile(cursor, client_id):
    cursor.execute("""
    DELETE FROM mobile
    WHERE client_id = %s;
    """, (client_id,))


def del_client(cursor, client_id):
    cursor.execute("""
    DELETE FROM clients
    WHERE id = %s
    """, (client_id,))


def find_client(cursor, first_name=None, last_name=None, mail=None):
    if first_name is not None:
        cursor.execute("""
        SELECT * FROM clients WHERE first_name = %(first_name)s;
        """, ({'first_name': first_name}))
    if last_name is not None:
        cursor.execute("""
        SELECT * FROM clients WHERE last_name = %(last_name)s;
        """, ({'last_name': last_name}))
    if mail is not None:
        cursor.execute("""
        SELECT * FROM clients WHERE mail = %(mail)s;
        """, ({'mail': mail}))
    print(cursor.fetchall())


with ps2.connect(database='clients', user='postgres', password='02111950') as con:
    with con.cursor() as cur:
        create_table(con, cur)
        # new_client(con, cur, 'Ivan', 'Ivanov', 'bla-bla@mail.ru')
        # new_client(con, cur, 'Darya', 'Ivanova', 'zumba@mail.ru')
        # new_client(con, cur, 'Leo', 'Messi', 'barcelona@mail.ru')
        # new_client(con, cur, 'Ivan', 'Petrov', 'tango@mail.ru')
        # new_client(con, cur, 'Vasiliy', 'Petrov', 'cha_cha@mail.ru')
        # add_mobile(con, cur, 1, 8903545)
        # add_mobile(con, cur, 1, 8989082)

        # change_data(cur, 1, first_name='Vasya', mail='sirtaki@mail.ru')
        # del_mobile(cur, 1)

        # del_client(cur, 1)

        # find_client(cur, first_name='Ivan')

        # cur.execute("""
        # SELECT * from clients;
        # """)
        # print(cur.fetchall())
        # cur.execute("""
        #         SELECT * from mobile;
        #         """)
        # print(cur.fetchall())
