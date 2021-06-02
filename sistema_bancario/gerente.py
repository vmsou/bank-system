import argparse
# import hashlib  # Para fazer o hash da senha
import sys

from database import create_connection, read_query, insert_user, execute_query, DBLogger
from queries import sequence_id, user_by_id, user_by_name, update_info
from utility import confirmar, affirmations, Logger, LocalData

from defaults.settings import Settings
from defaults import validation

settings = Settings()
local_data = LocalData()
db_file = settings.db_file
ConsoleLogger = Logger("Console")


def gen_id():
    """Gerar ID, a partir do ultimo id + 1"""
    return read_query(local_data.connection, sequence_id)[0][0] + 1


def cadastrar_conta():
    conta_id = gen_id()

    print(f"{'':-^30s}")
    print(f"{f'> Cadastrar Conta ID: {conta_id} <':^30s}")
    print(f"{'':-^30s}")

    name = confirmar("Nome Completo: ", confirm=settings.CONFIRM, goto=menu, validation=validation.check_name)
    job = confirmar("Profissão: ", confirm=settings.CONFIRM, goto=menu, validation=validation.check_job)
    renda = confirmar("Renda Mensal: ", float, confirm=settings.CONFIRM, validation=validation.check_income, goto=menu)
    address = confirmar("Endereço: ", confirm=settings.CONFIRM, goto=menu, validation=validation.check_address)
    telefone = confirmar("Telefone: ", confirm=settings.CONFIRM, goto=menu, validation=validation.check_phone)
    senha = confirmar("Senha: ", confirm=settings.CONFIRM, goto=menu, validation=validation.check_password)
    cadastrar = input("Cadastrar Conta (s/n)? ")

    if cadastrar.lower() in affirmations:
        dados = (name, job, renda, address, telefone, senha)
        ConsoleLogger.log("Cadastrando...")
        insert_user(local_data.connection, dados)
        ConsoleLogger.log("Cadastrado!")
    else:
        ConsoleLogger.log("Cancelado.")


def buscar_conta():
    info = "*"
    escolha = confirmar("Buscar por ID ou Nome? ", confirm=settings.CONFIRM, goto=menu)
    if not escolha:
        menu()

    users = None
    if escolha.lower() == 'id':
        corrente = confirmar("ID: ", int, confirm=settings.CONFIRM, goto=menu)
        if not corrente:
            menu()
        ConsoleLogger.log("Buscando por ID...")
        users = read_query(local_data.connection, user_by_id.format(info, corrente))
    elif escolha.lower() == 'nome':
        nome = confirmar("Nome: ", confirm=settings.CONFIRM, goto=menu)
        if not nome:
            menu()
        ConsoleLogger.log("Buscando pelo nome...")
        users = read_query(local_data.connection, user_by_name.format(info, nome))

    if users:
        print(f"Encontrado: {len(users)}")
        print()
        print(", ".join(settings.info))
        print(f"{'':-^130s}")
        for user in users:
            print(user)
        print(f"{'':-^130s}")
        ConsoleLogger.log("Busca feita com êxito!")
    else:
        ConsoleLogger.log("Usuário não encontrado!")


def mudar_senha():
    conta_id = confirmar('ID: ', confirm=settings.CONFIRM, goto=menu)
    user = read_query(local_data.connection, user_by_id.format('name', conta_id))[0][0]
    ConsoleLogger.log(f"Mudando senha do usuario: {user}")
    nova_senha = confirmar("Nova senha: ", confirm=settings.CONFIRM, goto=menu, validation=validation.check_password)
    execute_query(local_data.connection, update_info.format('password', nova_senha, conta_id))
    ConsoleLogger.log("Senha mudada.")


def config():
    confirm = input("Desativar confirmações? (s, n): ")
    settings.CONFIRM = True
    if confirm.lower() in affirmations:
        settings.CONFIRM = False

    dlog = input("Desativar logs? (s, n): ")
    Logger.enabled = True
    if dlog.lower() in affirmations:
        Logger.enabled = False


def sair():
    local_data.id = None
    local_data.connection = None
    local_data.senha = None
    ConsoleLogger.log("Saída efetuada.", bold=True)
    sys.exit()


def options():
    action_name = ["Cadastrar", "Buscar", "Mudar Senha", "Configurações", "Sair"]
    action_dict = {1: cadastrar_conta, 2: buscar_conta, 3: mudar_senha, 4: config, 5: sair}

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
    if not connection:
        sys.exit(1)
    ConsoleLogger.log("Durante qualquer momento você pode escrever 'sair' ou 'cancelar' para sair do input", color='yellow')
    local_data.connection = connection

    parser = argparse.ArgumentParser(description="Interface de gerente. Utilizada para cadastrar novas contas, "
                                                 "buscar uma conta existente ou definir uma nova senha de uma conta existente.")
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-disable_confirm', dest='disable_confirm', action='store_true')
    parser.add_argument('-disable_log', dest='disable_log', action='store_true')

    group.add_argument('--cadastrar', dest='cadastrar', action='store_true')
    group.add_argument('--buscar', dest='buscar', action='store_true')
    group.add_argument('--senha', dest='senha', action='store_true')

    args = parser.parse_args()

    if args.disable_confirm:
        settings.CONFIRM = False
    if args.disable_log:
        Logger.enabled = False
    if args.cadastrar:
        cadastrar_conta()
    elif args.buscar:
        buscar_conta()
    elif args.senha:
        mudar_senha()
    else:
        menu()


if __name__ == '__main__':
    main()
