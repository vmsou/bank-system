import argparse
import sys

from database import create_connection, check_login, read_query, execute_query, transaction
from defaults.settings import Settings
from utility import Logger, LocalData, confirmar, affirmations, loading
from queries import *

settings = Settings()
db_file = settings.db_file
ConsoleLogger = Logger("Console")
local_data = LocalData()


def saque():
    saldo = read_query(local_data.connection, user_by_id.format("balance", local_data.id))[0][0]
    print(f"Saldo: R${saldo}")
    amount = confirmar("Sacar: R$", float, settings.CONFIRM)
    confirm = input(f"Sacar R${amount}? (s/n): ")
    if confirm in affirmations:
        if saldo >= amount >= 0:
            execute_query(local_data.connection, update_info.format("balance", saldo - amount, local_data.id))
            ConsoleLogger.log(f"R${amount} retirados da conta.")
        else:
            ConsoleLogger.log("Quantidade Inválida")
    else:
        print("Cancelado.")


def deposito():
    print("Depositando...")


def visualizar():
    conta = read_query(local_data.connection, user_by_id.format("id, name, balance", local_data.id))[0]
    id = conta[0]
    nome = conta[1]
    saldo = conta[2]
    print("-" * 70)
    print(f"Nome: {nome}\tConta Corrente: {id}\tSaldo: {saldo}")


def simular():
    print("Simulando investimento...")


def transferir():
    receiver = confirmar("ID Recebedor: ", int, settings.CONFIRM)
    amount = confirmar("Quantidade R$", float, settings.CONFIRM)
    desc = input("Comentario: ")
    print(receiver, amount)
    if not transaction(local_data.connection, local_data.id, receiver, amount, desc):
        ConsoleLogger.log("Transferência Inválida")


def config():
    print("Configurações...")


def sair():
    local_data.id = None
    local_data.connection = None
    local_data.senha = None
    ConsoleLogger.log("Saída efetuada.")
    sys.exit()


def menu():
    action_dict = {1: saque, 2: deposito, 3: visualizar, 4: simular, 5: transferir, 6: config, 7: sair}

    while True:
        print("Menu".center(70, "-"))
        for i, j in enumerate(("Saque", "Deposito", "Visualizar", "Simular", "Transferir", "Configurações", "Sair"), start=1):
            print(f"[{i}] {j}")

        action = int(input("Ação: "))
        print()
        try:
            action_dict[action]()
        except IndexError:
            ConsoleLogger.log("Ação não encontrada")
        except ValueError:
            ConsoleLogger.log("Ação inválida")


def main():
    connection = create_connection(db_file)
    if not connection:
        sys.exit(1)

    local_data.connection = connection
    print("-" * 70)
    id = confirmar("Conta Corrente: ", int)
    senha = confirmar("Senha: ")
    print("-" * 70)
    loading("Verificando Login") # Basicamente enfeite, o login é verificado de forma rápida
    if check_login(connection, id, senha):
        local_data.set_data(id, senha)
        ConsoleLogger.log("Login efetuado com sucesso!", color='green')
        visualizar()
    else:
        ConsoleLogger.log("Login e Senha Incorretos.", color='red')
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
