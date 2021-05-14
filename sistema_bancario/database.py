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

    def log_transaction(self, sender, receiver, amount):
        if self.enabled:
            print(f"[{self.name}] Sender: {sender}: R$ {amount:,.2f} -> Receiver: {receiver}")


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
        print(user)


def _read_sequence(connection):
    sequences = read_query(connection, show_sequence)

    for sequence in sequences:
        DBLogger.log(sequence)


def _read_transactions(connection):
    transactions = read_query(connection, select_transactions)
    for t in transactions:
        print(t)


def transaction(connection, sender, receiver, amount, desc="NULL"):
    sender_balance = read_query(connection, user_by_id.format("balance", sender))[0][0]
    receiver_balance = read_query(connection, user_by_id.format("balance", receiver))[0][0]
    if sender_balance >= amount:
        DBLogger.log_transaction(sender, receiver, amount)
        execute_query(connection, add_transaction.format(exchanges, (sender, receiver, amount, desc)))
        execute_query(connection, update_info.format("balance", sender_balance - amount, sender))
        execute_query(connection, update_info.format("balance", receiver_balance + amount, receiver))
    else:
        print("Saldo insuficiente")


def check_login(connection, id, senha):
    try:
        password = read_query(connection, user_by_id.format("password", id))[0][0]
    except IndexError:
        return False
    else:
        if password == senha:
            return True
        return False


if __name__ == '__main__':
    connection = create_connection(db_file)
    #_prepare_table(connection)
    #dados = ("Vinicius3", "Engenheiro de Software", 11000, 'Rua Teste 999', '(41) 98765-4321')
    #insert_user(connection, dados)



