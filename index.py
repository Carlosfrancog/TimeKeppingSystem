import os
import json
from MainCode import MainClass

def registrar_usuario():
    os.system("cls" or "clear")
    nome = input("Digite seu nome: ")
    email = input("Digite seu email: ")
    telefone = input("Digite seu telefone: ")
    senha = input("Digite sua senha: ")
    verify = False

    # Verifica se a senha atende aos critérios especificados
    if (
        len(senha) < 8
        or not any(char.isupper() for char in senha)
        or not any(char in "!@#$%^&*()-_+=~`'\";:/?.,<>{}[]|\\"
                for char in senha)
    ):
        verify = True

    while verify is True:
        print("A senha deve conter pelo menos 8 caracteres, uma letra maiúscula e um caractere especial.")
        senha = input("Digite sua senha: ")
        if (
            len(senha) >= 8
            and any(char.isupper() for char in senha)
            and any(char in "!@#$%^&*()-_+=~`'\";:/?.,<>{}[]|\\"
                    for char in senha)
        ):
            verify = False

    # Salva as informações do usuário em um arquivo JSON
    novo_usuario = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "senha": senha
    }

    # Verifica se o arquivo JSON de registros existe e carrega os registros
    arquivo_registros = "keys/Registers.json"
    if os.path.exists(arquivo_registros) and os.path.getsize(arquivo_registros) > 0:
        with open(arquivo_registros, "r") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                registros = []
    else:
        registros = []

    registros.append(novo_usuario)

    # Salva os registros atualizados no arquivo JSON
    with open(arquivo_registros, "w") as f:
        json.dump(registros, f, indent=4)

    input("REGISTRADO! Pressione ENTER para voltar para o menu...")
    os.system("cls" or "clear")
    menu_principal()

def fazer_login():
    os.system("cls" or "clear")
    # Carregar o arquivo JSON de registros
    arquivo_registros = "keys/Registers.json"
    if os.path.exists(arquivo_registros) and os.path.getsize(arquivo_registros) > 0:
        with open(arquivo_registros, "r") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                registros = []
    else:
        print("Nenhum usuário registrado ainda.")
        input("Pressione ENTER para voltar para o menu...")
        os.system("cls" or "clear")
        menu_principal()
        return

    # Solicitar email e senha para login
    email_login = input("Digite seu email: ")
    senha_login = input("Digite sua senha: ")

    # Verificar se o email e a senha correspondem a algum registro
    for usuario in registros:
        if usuario["email"] == email_login and usuario["senha"] == senha_login:
            print("Login bem-sucedido!")
            input("Pressione ENTER para ir para o menu...")
            MainClass()  # Chamando a classe Main
            return

    # Se não encontrar correspondência, exibir mensagem de erro e voltar para o menu
    print("Email ou senha incorretos. Tente novamente.")
    input("Pressione ENTER para voltar para o menu...")
    os.system("cls" or "clear")
    menu_principal()

def menu_principal():
    quest = input("""
    ____________________
    |   REGISTRAR  [1] |
    |     LOGIN    [2] |          
    |     SAIR     [3] |
    --------------------
:""")
    while quest not in "123":
        os.system('cls' or 'clear')
        quest = input("""
    ____________________
    |   REGISTRAR  [1] |
    |     LOGIN    [2] |          
    |     SAIR     [3] |
    --------------------
:""")
    

    if quest == "1":
        registrar_usuario()
    elif quest == "2":
        fazer_login()
    elif quest == "3":
        exit()

menu_principal()
