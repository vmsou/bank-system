colors = {"purple": '\033[95m', "blue": '\033[94m', "ciano": '\033[96m',
         "green": '\033[92m', "yellow": '\033[93m', "red": '\033[91m'}


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

    def set_data(self, id, senha):
        self.id = id
        self.senha = senha


affirmations = ('sim', 's', 'si', 'y', 'yes')


def confirmar(mensagem, tipo=str, confirm=True, validation=None):
    while True:
        try:
            valor = tipo(input(mensagem))
            if validation is not None:
                if not validation(valor):
                    raise ValueError
        except ValueError:
            print("Entrada Inválida. Tente Novamente.")
        else:
            if confirm:
                if input("Confirmar (s/n): ").lower() in affirmations:
                    break
            else:
                break
    return valor
