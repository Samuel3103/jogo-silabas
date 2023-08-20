import os


def gerar_chave_secreta():
    return os.urandom(24).hex()

print(gerar_chave_secreta())
