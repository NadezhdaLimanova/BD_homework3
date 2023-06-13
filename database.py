import psycopg2


class Database:

    def __init__(self, conn):
        self.conn = conn

    def createdb(self):
        with conn.cursor() as cur:
            # cur.execute("""
            #             DROP TABLE client_phone;
            #             DROP TABLE clients;
            #             """)
            cur.execute("""CREATE TABLE IF NOT EXISTS clients(id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL, surname VARCHAR(70) NOT NULL,
            email VARCHAR(70) NOT NULL UNIQUE, phone_numbers_count INTEGER NULL);""")
            cur.execute("""CREATE TABLE IF NOT EXISTS client_phone(id SERIAL PRIMARY KEY,
            name_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE, phone INTEGER NULL);""")
            conn.commit()

    def new_client(self, name, surname, email, phone_numbers_count=0):
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO clients(name, surname, email, phone_numbers_count) 
            VALUES(%s, %s, %s, %s);""",(name, surname, email, phone_numbers_count))
            conn.commit()

    def new_phone(self, name_id, phone):
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO client_phone(name_id, phone)
                        VALUES(%s, %s);""", (name_id, phone))
            cur.execute("""UPDATE clients SET phone_numbers_count = phone_numbers_count + 1
            WHERE id=%s;""", (name_id,))
            conn.commit()

    def change_data(self, name_id, new_name, new_surname, new_email, new_phone=None, phone_numbers_count=0):
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients
            SET name=%s, surname=%s, email=%s, 
            phone_numbers_count=%s WHERE id=%s RETURNING *;""",(new_name, new_surname, new_email, phone_numbers_count, name_id))
        if new_phone != None:
            with conn.cursor() as cur:
                cur.execute("""UPDATE clients SET phone_numbers_count = phone_numbers_count + 1
                WHERE id=%s;""", (name_id,))
                cur.execute("""UPDATE client_phone
                SET phone=%s WHERE id=%s;""", (new_phone, name_id))
                conn.commit()

    def delete_phone(self, name_id):
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients SET phone_numbers_count = phone_numbers_count - 1
                        WHERE id=%s;""", (name_id,))
            cur.execute("""DELETE FROM client_phone
            WHERE id=%s;""", (name_id,))
            conn.commit()

    def delete_client(self, name_id):
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM clients
            WHERE id=%s;""", (name_id,))
            conn.commit()

    def select_client(self, name=None, surname=None, email=None, phone=None):
        if name != None:
            with conn.cursor() as cur:
                cur.execute("""SELECT id from clients WHERE name=%s;""", (name,))
                print(cur.fetchall())
        if surname != None:
            with conn.cursor() as cur:
                cur.execute("""SELECT id from clients WHERE surname=%s;""", (surname,))
                print(cur.fetchall())
        if email != None:
            with conn.cursor() as cur:
                cur.execute("""SELECT id from clients WHERE email=%s;""", (email,))
                print(cur.fetchall())
        if phone != None:
            with conn.cursor() as cur:
                cur.execute("""SELECT name_id from client_phone WHERE phone=%s;""", (phone,))
                print(cur.fetchall())
        conn.commit()

    def select_all(self):
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM clients ORDER BY id""")
            print(cur.fetchall())
            cur.execute("""SELECT * FROM client_phone ORDER BY id""")
            print(cur.fetchall())


if __name__ == '__main__':
    name_1 = 'Kate'
    surname_1 = 'Ivanova'
    email_1 = 'kate@gmail.com'
    phone_1 = 89675868
    phone_2 = 88896967
    phone_3 = 88879696
    name_2 = 'Maria'
    surname_2 = 'Fedorova'
    email_2 = 'maria@gmail.com'
    name_id_1 = 1
    name_id_2 = 2

    new_name = 'Michael'
    new_surname = 'Smirnov'
    new_email = 'Michael@gmail.com'
    new_phone = 898764369


    with psycopg2.connect(database='clients', user='postgres', password='putyourpasswordhere') as conn:
        # Database(conn).createdb()
        # Database(conn).new_client(name_1, surname_1, email_1)
        # Database(conn).new_client(name_2, surname_2, email_2)
        # Database(conn).new_phone(name_id_1, phone_1)
        # Database(conn).new_phone(name_id_1, phone_2)
        # Database(conn).new_phone(name_id_2, phone_3)
        # Database(conn).change_data(name_id_2, new_name, new_surname, new_email, new_phone)
        # Database(conn).delete_phone(name_id_2)
        # Database(conn).delete_client(name_id_2)
        # Database(conn).select_client(email=email_2)
        # Database(conn).select_all()
    conn.close()
