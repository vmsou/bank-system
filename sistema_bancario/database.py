import sqlite3

from utility import Logger

from queries import *

settings = Settings()

db_file = settings.db_file
db_name = settings.db_name
exchanges = settings.exchanges  # Transactions


class DatabaseLogger(Logger):
    def __init__(self, name):
        super().__init__(name)

    def log_transaction(self, connection, sender, receiver, amount):
        execute_query(connection, transaction_db.format(exchanges, sender, receiver, amount))
        if self.enabled:
            print(f"[{self.name}] {sender}: R$ {amount:,.2f} -> {receiver}")


DBLogger = DatabaseLogger("Database")


def create_connection(database_name):
    connection = None
    try:
        connection = sqlite3.connect(database_name)
        DBLogger.log("Connection to DB was successful.")
    except sqlite3.Error as e:
        DBLogger.log(f"Error: {e}")
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
    execute_query(connection, add_user.format(db_name, data))


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
    execute_query(connection, sequence_starting)


def _read_users(connection):
    users = read_query(connection, select_users)
    for user in users:
        DBLogger.log(user)


def _read_sequence(connection):
    sequences = read_query(connection, show_sequence)

    for sequence in sequences:
        DBLogger.log(sequence)


def transaction(connection, sender, receiver, amount):
    # TODO: Verificar se quantidade é compativel com o banco de dados
    # TODO: Subtrair e adicionar informações no banco de dados
    # TODO: Usar DBLogger
    ...


if __name__ == '__main__':
    connection = create_connection(db_file)
    _prepare_table(connection)
    #dados = ("Vinicius3", "Engenheiro de Software", 11000, 'Rua Teste 999', '(41) 98765-4321')
    #insert_user(connection, dados)



