import argparse
import sys

from database import create_connection, check_login, read_query, execute_query, transaction
from defaults.settings import Settings
from utility import Logger, LocalData, confirmar, affirmations
from queries import *

settings = Settings()
db_file = settings.db_file
ConsoleLogger = Logger("Console")
data_local = LocalData()


def saque():
    saldo = read_query(data_local.connection, user_by_id.format("balance", data_local.id))[0][0]
    print(f"Saldo: R${saldo}")
    amount = confirmar("Sacar: R$", float, settings.CONFIRM)
    confirm = input(f"Sacar R${amount}? (s/n): ")
    if confirm in affirmations:
        if saldo >= amount >= 0:
            execute_query(data_local.connection, update_info.format("balance", saldo - amount, data_local.id))
            ConsoleLogger.log(f"R${amount} retirados da conta.")
        else:
            ConsoleLogger.log("Quantidade Inválida")
    else:
        print("Cancelado.")


def deposito():
    print("Depositando...")


def visualizar():
    conta = read_query(data_local.connection, user_by_id.format("id, name, balance", data_local.id))[0]
    id = conta[0]
    nome = conta[1]
    saldo = conta[2]
    print(f"Nome: {nome}\nConta Corrente: {id}\nSaldo: {saldo}\n")


def simular():
    print("Simulando investimento...")


def transferir():
    receiver = confirmar("ID Recebedor: ", int, settings.CONFIRM)
    amount = confirmar("Quantidade R$", float, settings.CONFIRM)
    desc = input("Comentario: ")
    print(receiver, amount)
    transaction(data_local.connection, data_local.id, receiver, amount, desc)


def config():
    print("Configurações...")


def menu():
    action_dict = {1: saque, 2: deposito, 3: visualizar, 4: simular, 5: transferir, 6: config, 7: sys.exit}

    print("Menu".center(50, "-"))

    while True:
        for i, j in enumerate(("Saque", "Deposito", "Visualizar", "Simular", "Transferir", "Configurações", "Sair"), start=1):
            print(f"[{i}] {j}")

        action = input("Ação: ")
        print()
        try:
            action_dict[int(action)]()
        except IndexError or KeyError:
            ConsoleLogger.log("Ação não encontrada")
        except ValueError:
            ConsoleLogger.log("Ação inválida")


def main():
    connection = create_connection(db_file)
    if not connection:
        sys.exit(1)

    data_local.connection = connection

    id = confirmar("ID: ", int)
    senha = confirmar("Senha: ")
    if check_login(connection, id, senha):
        data_local.set_data(id, senha)
        ConsoleLogger.log("Login efetuado com sucesso!")
    else:
        ConsoleLogger.log("Login e Senha Incorretos.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Interface de cliente. "
                                                 "Utilizada para o realizar diversas operações visando movimentação de dinheiro")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--saque', dest='saque', action='store_true')
    group.add_argument('--deposito', dest='deposito', action='store_true')
    group.add_argument('--visualizar', dest='visualizar', action='store_true')
    group.add_argument('--simular', dest='simular', action='store_true')

    args = parser.parse_args()

    if args.saque:
        saque()
    elif args.deposito:
        deposito()
    elif args.visualizar:
        visualizar()
    elif args.simular:
        simular()
    else:
        menu()


if __name__ == '__main__':
    main()
