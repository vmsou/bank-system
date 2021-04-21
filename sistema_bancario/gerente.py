import sys
import argparse

from database import create_connection, read_query, insert_user, execute_query
from utility import confimar, affirmations

from defaults.settings import Settings

settings = Settings()
db_file = settings.db_file

CONFIRM = True


def gen_id(connection):
    """Gerar ID, a partir do ultimo id + 1"""
    id = read_query(connection, "SELECT seq FROM sqlite_sequence WHERE NAME='users';")
    return id[0][0] + 1


def cadastrar_conta(connection):
    id = gen_id(connection)

    print(f"{'':-^30s}")
    print(f"{f'> Cadastrar Conta ID: {id} <':^30s}")
    print(f"{'':-^30s}")

    name = confimar("Nome Completo: ", confirm=CONFIRM)
    job = confimar("Profissão: ", confirm=CONFIRM)
    renda = confimar("Renda Mensal: ", float, confirm=CONFIRM)
    address = confimar("Endereço: ", confirm=CONFIRM)
    telefone = confimar("Telefone: ", confirm=CONFIRM)
    senha = confimar("Senha: ", confirm=CONFIRM)
    cadastrar = input("Cadastrar Conta (s/n)? ")

    if cadastrar.lower() in affirmations:
        dados = (name, job, renda, address, telefone, senha)
        print(f"[Console] Cadastrando...")
        insert_user(connection, dados)
        print("[Console] Cadastrado!")

    else:
        print("[Console] Cancelando...")


def buscar_conta(connection, id=None, nome=None, info="*"):
    users = None
    if id:
        print("[Console] Buscando por ID...")
        users = read_query(connection, f"SELECT {info} FROM USERS WHERE ID = {id};")
    elif nome:
        print("[Console] Buscando pelo nome...")
        users = read_query(connection, f"SELECT {info} FROM USERS WHERE name LIKE '%{nome}%';")
    if users:
        print(", ".join(settings.info))
        for user in users:
            print(user)
    else:
        print("[Console] Usuário não encontrado!")


def mudar_senha(connection):
    id = input('ID: ')
    user = read_query(connection,f"SELECT name FROM USERS WHERE ID = {id};")[0][0]
    print(f"[Console] Mudando senha do usuario: {user}")
    nova_senha = input("Nova senha: ")
    if nova_senha:
        query = f"UPDATE users SET password = '{nova_senha}' WHERE id = {id};"
        execute_query(connection, query)
        print('[Console] Senha mudada.')


def main():
    connection = create_connection(db_file)
    if not connection:
        sys.exit(1)

    global CONFIRM

    parser = argparse.ArgumentParser(description="Interface de gerente. Utilizada para cadastrar novas contas, "
                                                 "buscar uma conta existente ou definir uma nova senha de uma conta existente.")
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('--disable_confirm', dest='disable_confirm', action='store_true')

    group.add_argument('--cadastrar', dest='cadastrar', action='store_true')
    group.add_argument('--buscar', dest='buscar', action='store_true')
    group.add_argument('--mudar_senha', dest='mudar_senha', action='store_true')

    args = parser.parse_args()

    if args.disable_confirm:
        CONFIRM = False

    if args.cadastrar:
        cadastrar_conta(connection)

    if args.buscar:
        escolha = input("Buscar por ID ou Nome? ")
        if escolha.lower() == 'id':
            id = confimar("ID: ", int, confirm=CONFIRM)
            buscar_conta(connection, id=id)
        elif escolha.lower() == 'nome':
            nome = confimar("Nome: ", confirm=CONFIRM)
            buscar_conta(connection, nome=nome)

    if args.mudar_senha:
        mudar_senha(connection)


if __name__ == '__main__':
    main()
