import psycopg2


def con():
    return psycopg2.connect(
        dbname='dabs6e5qj7mi83',
        user='cfzzhyrcmvrsxr',
        password='2149282f7b998fcbbfec62fe63dd97f9165eb76e746fc3c9ab1ec761b1b1fae4',
        host='ec2-35-169-9-79.compute-1.amazonaws.com',
        port=5432
    )


def create_user_table():
    conn = con()
    cur = conn.cursor()
    cur.execute('''
        create table if not exists users(
            id serial primary key,
            first_name varchar(30),
            last_name varchar(30),
            phone varchar(13),
            address varchar(150),
            created_date timestamp default current_timestamp
        )
    ''')
    conn.commit()
    conn.close()


def insert_data(data: dict):
    conn = con()
    cur = conn.cursor()
    cur.execute('''
            insert into users(phone, first_name, last_name, address)
            values (%s, %s, %s, %s)
        ''', (data['phone'], data['first_name'], data['last_name'], data['address']))
    conn.commit()
    conn.close()
