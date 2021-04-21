import argparse
# import hashlib  # Para fazer o hash da senha
import sys


from database import create_connection, read_query, insert_user, execute_query, DBLogger
from utility import confimar, affirmations, Logger

from defaults.settings import Settings

settings = Settings()
db_file = settings.db_file
ConsoleLogger = Logger("Console")


def gen_id(connection):
    """Gerar ID, a partir do ultimo id + 1"""
    id = read_query(connection, "SELECT seq FROM sqlite_sequence WHERE NAME='users';")
    return id[0][0] + 1


def cadastrar_conta(connection):
    id = gen_id(connection)

    print(f"{'':-^30s}")
    print(f"{f'> Cadastrar Conta ID: {id} <':^30s}")
    print(f"{'':-^30s}")

    name = confimar("Nome Completo: ", confirm=settings.CONFIRM)
    job = confimar("Profissão: ", confirm=settings.CONFIRM)
    renda = confimar("Renda Mensal: ", float, confirm=settings.CONFIRM)
    address = confimar("Endereço: ", confirm=settings.CONFIRM)
    telefone = confimar("Telefone: ", confirm=settings.CONFIRM)
    senha = confimar("Senha: ", confirm=settings.CONFIRM)
    cadastrar = input("Cadastrar Conta (s/n)? ")

    if cadastrar.lower() in affirmations:
        dados = (name, job, renda, address, telefone, senha)
        ConsoleLogger.log("Cadastrando...")
        insert_user(connection, dados)
        ConsoleLogger.log("Cadastrado!")

    else:
        ConsoleLogger.log("Cancelando!")


def buscar_conta(connection, id=None, nome=None, info="*"):
    users = None
    if id:
        ConsoleLogger.log("Buscando por ID...")
        users = read_query(connection, f"SELECT {info} FROM USERS WHERE ID = {id};")
    elif nome:
        ConsoleLogger.log("Buscando pelo nome...")
        users = read_query(connection, f"SELECT {info} FROM USERS WHERE name LIKE '%{nome}%';")
    if users:
        print()
        print(", ".join(settings.info))
        print(f"{'':-^130s}")
        for user in users:
            print(user)
        print(f"{'':-^130s}")
        ConsoleLogger.log("Busca feita com êxito!")
    else:
        ConsoleLogger.log("Usuário não encontrado!")


def mudar_senha(connection):
    id = input('ID: ')
    user = read_query(connection,f"SELECT name FROM USERS WHERE ID = {id};")[0][0]
    ConsoleLogger.log(f"Mudando senha do usuario: {user}")
    nova_senha = input("Nova senha: ")
    if nova_senha:
        query = f"UPDATE users SET password = '{nova_senha}' WHERE id = {id};"
        execute_query(connection, query)
        ConsoleLogger.log("Senha mudada.")


def main():
    connection = create_connection(db_file)
    if not connection:
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Interface de gerente. Utilizada para cadastrar novas contas, "
                                                 "buscar uma conta existente ou definir uma nova senha de uma conta existente.")
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-disable_confirm', dest='disable_confirm', action='store_true')
    parser.add_argument('-disable_log', dest='disable_log', action='store_true')

    group.add_argument('--cadastrar', dest='cadastrar', action='store_true')
    group.add_argument('--buscar', dest='buscar', action='store_true')
    group.add_argument('--mudar_senha', dest='mudar_senha', action='store_true')

    args = parser.parse_args()

    if args.disable_confirm:
        settings.CONFIRM = False

    if args.disable_log:
        Logger.enabled = False
        DBLogger.enabled = False

    if args.cadastrar:
        cadastrar_conta(connection)

    if args.buscar:
        escolha = input("Buscar por ID ou Nome? ")
        if escolha.lower() == 'id':
            id = confimar("ID: ", int, confirm=settings.CONFIRM)
            buscar_conta(connection, id=id)
        elif escolha.lower() == 'nome':
            nome = confimar("Nome: ", confirm=settings.CONFIRM)
            buscar_conta(connection, nome=nome)

    if args.mudar_senha:
        mudar_senha(connection)


if __name__ == '__main__':
    main()
