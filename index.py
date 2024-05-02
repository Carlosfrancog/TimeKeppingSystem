import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from Functions import emailCode
from keys import secrets
import Functions

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

    # Salva as informações do usuário em um arquivo JSON
    novo_usuario = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "senha": senha
    }

    # Verifica se o arquivo JSON de registros existe
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

    with open(arquivo_registros, "w") as f:
        json.dump(registros, f, indent=4)



def menu_principal():
    quest = input("""
    ____________________
    |   REGISTRAR  [1] |
    |     LOGIN    [2] |          
    |     SAIR     [3] |
    --------------------
:""")
    while quest not in "123":
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
        pass  # Adicione a lógica para o login
    elif quest == "3":
        exit()

menu_principal()
