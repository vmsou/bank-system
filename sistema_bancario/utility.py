class Logger:
    enabled = True

    def __init__(self, name):
        self.name = name

    def log(self, message):
        if self.enabled:
            print(f"[{self.name}] " + message)


affirmations = ('sim', 's', 'si', 'y', 'yes')


def confimar(mensagem, tipo=str, confirm=True):
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