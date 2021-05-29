import argparse
import sys

from database import create_connection, check_login, read_query, execute_query, transaction
from defaults.settings import Settings
from defaults import validation
from utility import Logger, LocalData, confirmar, affirmations
from queries import *

settings = Settings()
db_file = settings.db_file
ConsoleLogger = Logger("Console")
local_data = LocalData()


def login_required(func):
    def wrapper():
        if local_data.logged:
            func()
        else:
            ConsoleLogger.log("Login necessário!", color='red')
            login()
    return wrapper


@login_required
def saque():
    saldo = read_query(local_data.connection, user_by_id.format("balance", local_data.id))[0][0]
    print(f"Saldo: R${saldo}")
    amount = confirmar("Sacar: R$", tipo=float, confirm=settings.CONFIRM, goto=menu)
    if saldo >= amount >= 0:
        execute_query(local_data.connection, update_info.format("balance", saldo - amount, local_data.id))
        ConsoleLogger.log(f"R${amount} retirados da conta.")
    else:
        ConsoleLogger.log("Quantidade Inválida")


@login_required
def deposito():
    while True:
        saldo = read_query(local_data.connection, user_by_id.format("balance", local_data.id))[0][0]
        print(f"Saldo: R${saldo}")
        amount = confirmar("Depositar: R$", tipo=float, confirm=settings.CONFIRM, goto=menu, validation=validation.check_income)
        if amount <= 10_000:
            execute_query(local_data.connection, update_info.format("balance", saldo + amount, local_data.id))
            ConsoleLogger.log(f"R${amount} adicionado na conta, Você agora possui R${saldo+amount}")
            break
        else:
            ConsoleLogger.log("Quantidade Inválida, o valor a ser depositado deve ser no máximo R$10.000. Tente novamente.")


@login_required
def visualizar():
    conta = read_query(local_data.connection, user_by_id.format("id, name, balance", local_data.id))[0]
    conta_id = conta[0]
    nome = conta[1]
    saldo = conta[2]
    print("-" * 70)
    print(f"Nome: {nome}\tConta Corrente: {conta_id}\tSaldo: {saldo}")


@login_required
def simular():
    invest_inicial = confirmar("Valor do investimento inicial: R$", tipo=float, confirm=settings.CONFIRM, goto=menu, validation=validation.check_income)
    invest_tempom = confirmar("O tempo de investimento em meses: ", tipo=int, confirm=settings.CONFIRM, goto=menu, validation=validation.check_income)
    if invest_tempom / 12 >= 5:
        taxa = 0.5 / 100  # 0,5% taxa por mes caso estiver investindo por mais de 5 anos
    else:
        taxa = 1 / 100  # 1% taxa por mes caso estiver investindo por menos que 5 anos

    juros = 1.5 / 100  # juros mensal de 1,5%
    invest = invest_inicial

    for x in range(1, invest_tempom+1):
        invest += invest*juros
        if x % 12 == 0:
            invest -= invest*taxa

    if invest_tempom < 12:  #se o tempo for menor que 12 meses desconta 1% do valor total
        invest -= invest*taxa

    print(f'O valor total investido foi: R${invest_inicial:.2f}')
    print(f'O total acumulado no investimento foi: R${(invest - invest_inicial):.2f}')
    print(f'O valor total final do investimento é: R${invest:.2f}')


@login_required
def transferir():
    receiver = confirmar("ID Recebedor: ", int, settings.CONFIRM, goto=menu)
    amount = confirmar("Quantidade R$", float, settings.CONFIRM, goto=menu)
    desc = input("Comentario: ")
    print(receiver, amount)
    if not transaction(local_data.connection, local_data.id, receiver, amount, desc):
        ConsoleLogger.log("Transferência Inválida")


def config():
    confirm = input("Desativar confirmações? (s, n): ")
    settings.CONFIRM = True
    if confirm.lower() in affirmations:
        settings.CONFIRM = False

    dlog = input("Desativar logs? (s, n): ")
    Logger.enabled = True
    if dlog.lower() in affirmations:
        Logger.enabled = False


def login():
    print("-" * 70)
    conta_id = confirmar("Conta Corrente: ", int, goto=menu)
    senha = confirmar("Senha: ", goto=menu)
    print("-" * 70)
    if check_login(local_data.connection, conta_id, senha):
        local_data.set_data(conta_id, senha)
        local_data.logged = True
        ConsoleLogger.log("Login efetuado com sucesso!", color='green')
        visualizar()
    else:
        ConsoleLogger.log("Login e Senha Incorretos.", color='red')
        login()


def logout():
    local_data.logged = False
    local_data.id = None
    local_data.password = None
    ConsoleLogger.log("Logout efetuado.")
    menu()


def info():
    print("Informações sobre o projeto...")


def sair():
    local_data.id = None
    local_data.connection = None
    local_data.senha = None
    ConsoleLogger.log("Saída efetuada.")
    sys.exit()


def options():
    in_name = ["Saque", "Deposito", "Visualizar", "Simular", "Transferir", "Configurações", "Log out", "Informações",  "Sair"]
    in_dict = {1: saque, 2: deposito, 3: visualizar, 4: simular, 5: transferir, 6: config, 7: logout, 8: info, 9: sair}

    out_name = ["Login", "Informações", "Sair"]
    out_dict = {1: login, 2: info, 3: sair}

    if local_data.logged:
        action_name = in_name
        action_dict = in_dict
    else:
        action_name = out_name
        action_dict = out_dict

    return action_name, action_dict


def menu():
    while True:
        action_name, action_dict = options()

        print("Menu".center(70, "-"))
        for i, j in enumerate(action_name, start=1):
            print(f"[{i}] {j}")

        action = confirmar("Ação: ", confirm=False, tipo=int, goto=sair)
        try:
            action_dict[action]()
        except IndexError:
            ConsoleLogger.log("Ação não encontrada")
            continue
        except ValueError:
            ConsoleLogger.log("Ação inválida")
            continue
        except KeyError:
            ConsoleLogger.log("Ação não encontrada")
            continue


def main():
    connection = create_connection(db_file)
    local_data.connection = connection
    if not connection:
        sys.exit(1)

    ConsoleLogger.log("Durante qualquer momento você pode escrever 'sair' ou 'cancelar' para sair do input", color='yellow')

    menu()

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
