import argparse
import sys

from database import create_connection, check_login
from defaults.settings import Settings
from utility import Logger, LocalData, confirmar

settings = Settings()
db_file = settings.db_file
ConsoleLogger = Logger("Console")
data_local = LocalData()


def saque():
    print(f"Sacando da conta {data_local.id}")


def deposito():
    print("Depositando...")


def visualizar():
    print("Visualizando...")


def simular():
    print("Simulando investimento...")


def config():
    print("Configurações...")


def menu():
    action_dict = {1: saque, 2: deposito, 3: visualizar, 4: simular, 5: config, 6: exit}

    print("Menu".center(50, "-"))

    while True:
        for i, j in enumerate(("Saque", "Deposito", "Visualizar", "Simular", "Configurações", "Sair"), start=1):
            print(f"[{i}] {j}")

        action = input("Ação: ")
        try:
            print()
            action_dict[int(action)]()
        except IndexError:
            print("Ação não encontrada")


def main():
    connection = create_connection(db_file)
    if not connection:
        sys.exit(1)

    data_local.connection = connection

    id = confirmar("ID: ", int)
    senha = confirmar("Senha: ")
    if check_login(connection, id, senha):
        data_local.set_data(id, senha)
        print("Login efetuado com sucesso!")
    else:
        print("Login e Senha Incorretos.")
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
