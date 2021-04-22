from defaults.settings import Settings

settings = Settings()
db_file = settings.db_file
db_name = settings.db_name


'''Creating Table Queries'''
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

'''Users Queries'''
select_users = f"SELECT * from users"
add_user = "INSERT INTO {}(name, job, income, address, phone, password) VALUES {};"

'''Sequence Queries'''
sequence_starting = f"UPDATE sqlite_sequence SET seq = 9999 WHERE NAME = '{db_name}';"
show_sequence = "SELECT * FROM sqlite_sequence"

'''Transaction Queries'''
transaction_db = "INSERT INTO {exchanges}(sender, receiver, amount) VALUES {sender, receiver, amount};"