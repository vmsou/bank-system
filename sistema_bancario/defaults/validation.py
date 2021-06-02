"""Validador de inputs

Esse seção permite verificar as entradas do úsuario ou do gerente.
Seguinda uma base de críterios retorna ao sistema se as informações
inseridas são validas
"""
import re


def check_name(name):
    """TODO: Verificar se nome possui nome e sobrenome"""
    nomeSimples = re.search(r" ", name) is None
    sobrenome = not(nomeSimples)
    return sobrenome


def check_job(title):
    """TODO: Verificar se profissão é valida [Talvez não seja necessário]"""
    return True


def check_income(income):
    income = float(income) 
    if income >= 0:
        return True
    return False


def check_address(address):
    """TODO: Verificar se endereço é valido [Pode ser OPCIONAL]"""
    return True


def check_phone(phone_number):
    """TODO: Usar regex para identificar validade do telefone"""
    phoneOK = False

    if 14 > len(phone_number) >= 8:
        phoneOK = True
    else:
        phoneOK = False
    return phoneOK


def check_password(password):
    """
    -> Para facilitar usar módulo string
        8 caracteres ou mais
        1 numero
        1 letra maiuscula
        1 letra minuscula
        Nao permitido caracteres especiais
    """

    # calculating the length
    tamanhoErro = len(password) < 8

    # searching for digits
    numeroErro = re.search(r"\d", password) is None

    # searching for uppercase
    maiusculaErro = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    minusculaErro = re.search(r"[a-z]", password) is None

    # searching for symbols
    simboloErro = re.search(r"[!#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~"+r'"]', password) is not None

    # overall result
    password_ok = not any([tamanhoErro, numeroErro, maiusculaErro, minusculaErro, simboloErro])

    # ERROS:
    if tamanhoErro:
        print('\033[0;31mA senha deve ter pelo menos 8 caracteres.\033[m')
    if numeroErro:
        print('\033[0;31mA senha deve ter no minino 1 numero.\033[m')
    if maiusculaErro:
        print('\033[0;31mA senha deve ter ao menos 1 letra maisucula.\033[m')
    if minusculaErro:
        print('\033[0;31mA senha deve ter ao menos 1 letra minuscula.\033[m')
    if simboloErro:
        print('\033[0;31mCaractere não permitido.\033[m')

    return password_ok
