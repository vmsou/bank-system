import sqlite3

from defaults.settings import Settings
from utility import Logger

settings = Settings()
DBLogger = Logger("Database")

db_file = settings.db_file
db_name = settings.db_name

create_users_table = f"""
CREATE TABLE IF NOT EXISTS {db_name} (
  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  job TEXT,
  income FLOAT,
  address TEXT,
  phone TEXT,
  password TEXT NOT NULL,
  balance FLOAT NOT NULL DEFAULT 0
);
"""

create_transactions_table = f"""
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
sender INTEGER NOT NULL,
receiver INTEGER NOT NULL,
amount FLOAT,
description TEXT,
FOREIGN KEY (sender) REFERENCES {db_name} (id),
FOREIGN KEY (receiver) REFERENCES {db_name}(id)
);
"""

create_users = f"""
INSERT INTO
    {db_name}(name, job, income, address, phone)
VALUES 
    ('Vinicius', 'Programador', 10000, 'Rua Teste 123', '(41) 99999-8888'),
    ('Vinicius2', 'Desenvolvedor', 8000, 'Rua Teste 456', '(41) 98888-9999');
"""

select_users = f"SELECT * from users"


def create_connection(database_name):
    connection = None
    try:
        connection = sqlite3.connect(database_name)
        DBLogger.log("Connection to DB was successful.")
    except sqlite3.Error as e:
        DBLogger.log(f"[Database] Error: {e}")
        return False

    return connection


def execute_query(connection, query):
    """Criar uma tabela de dado de usuarios"""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        DBLogger.log("Query executed")
    except sqlite3.Error as e:
        DBLogger.log(f"Error: {e}")
    else:
        connection.commit()


def _create_user_table(connection):
    execute_query(connection, create_users_table)


def _create_transactions_table(connection):
    execute_query(connection, create_transactions_table)


def _create_users(connection):
    execute_query(connection, create_users)


def insert_user(connection, data: tuple):
    query = f"""
    INSERT INTO
        {db_name}(name, job, income, address, phone, password)
    VALUES 
        {data};
    """
    execute_query(connection, query)


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        DBLogger.log(f"Error: {e}")
    return result


def _prepare_table(connection):
    _create_user_table(connection)
    _create_transactions_table(connection)
    dados1 = ("Teste", "Emprego", "Renda Mensal", "Endereço", "Telefone", "Teste123")
    insert_user(connection, dados1)
    execute_query(connection, f"UPDATE sqlite_sequence SET seq = 9999 WHERE NAME = '{db_name}';")


def _read_users(connection):
    users = read_query(connection, select_users)
    for user in users:
        DBLogger.log(user)


def _read_sequence(connection):
    sequences = read_query(connection, "SELECT * FROM sqlite_sequence")

    for sequence in sequences:
        DBLogger.log(sequence)


if __name__ == '__main__':
    connection = create_connection(db_file)
    _prepare_table(connection)
    #dados = ("Vinicius3", "Engenheiro de Software", 11000, 'Rua Teste 999', '(41) 98765-4321')
    #insert_user(connection, dados)



