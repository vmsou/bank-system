from time import sleep

colors = {"purple": '\033[95m', "blue": '\033[94m', "ciano": '\033[96m',
         "green": '\033[92m', "yellow": '\033[93m', "red": '\033[91m'}


affirmations = ('sim', 's', 'si', 'y', 'yes')
exits = ('exit', 'sair', 'cancelar', 'back', 'voltar')


class Logger:
    enabled = True

    def __init__(self, name):
        self.name = name

    def log(self, message, color=None, bold=False):
        strong = ''
        start = ''
        end = ''
        if bold:
            strong = '\033[1m'
            end = '\033[0m'
        if color in colors.keys():
            end = "\033[0m"
            start = colors[color]
        if self.enabled:
            print(f"[{self.name}]{strong}{start} {message}{end}")


class LocalData:
    def __init__(self):
        self.id = None
        self.password = None
        self.connection = None
        self.logged = False

    def set_data(self, id, senha):
        self.id = id
        self.password = senha


ConsoleLogger = Logger("Console")


def confirmar(mensagem, tipo=str, confirm=True, validation=None, goto=None):
    while True:
        try:
            valor = input(mensagem)
            if valor.lower() in exits:
                if not goto:
                    return False
                goto()

            valor = tipo(valor)
            if validation is not None:
                if not validation(valor):
                    raise ValueError
        except ValueError:
            ConsoleLogger.log("Entrada Inválida. Tente Novamente.")
        else:
            if confirm:
                if input("Confirmar (s/n): ").lower() in affirmations:
                    break
            else:
                break
    return valor


def loading(message="Carregando", min=0, max=100, step=1, delay=0.01):
    for i in range(min, max+1, step):
        print(f"\r{message}... {i}%", end='', flush=True)
        sleep(delay)
    print()

