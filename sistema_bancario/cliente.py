import argparse
import sys

from database import create_connection


def saque(conta, senha):
    print(f"Sacando: {conta}")


def deposito(conta, senha):
    print("Depositando...")


def visualizar(conta):
    print("Visualizando...")


def simular():
    print("Simulando investimento...")


def main():
    if not create_connection("users.sqlite"):
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
        conta = input("Conta: ")
        senha = input("Senha: ")
        saque(conta, senha)

    if args.deposito:
        conta = input("Conta: ")
        senha = input("Senha: ")
        deposito(conta, senha)

    if args.visualizar:
        conta = input("Conta: ")
        visualizar(conta)

    if args.simular:
        simular()


if __name__ == '__main__':
    main()