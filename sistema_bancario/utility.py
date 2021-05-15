class Logger:
    enabled = True

    def __init__(self, name):
        self.name = name

    def log(self, message, color=None):
        start = ''
        end = ''
        if color == 'green':
            start = "\033[92m"
            end = "\033[0m"
        elif color == "red":
            start = "\033[91m"
            end = "\033[0m"
        if self.enabled:
            print(f"[{self.name}] {start}{message}{end}")


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
        except ValueError:
            print("Entrada Inválida. Tente Novamente.")
        else:
            if confirm:
                if input("Confirmar (s/n): ").lower() in affirmations:
                    break
            else:
                break
    return valor
