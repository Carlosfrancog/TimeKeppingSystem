import tkinter as tk
from tkinter import messagebox, scrolledtext
from random import randint
import os
import re
import mysql.connector
from mysql.connector import Error
from keys import *

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap("./ViewLayer/images/icon.ico")
        self.root.title("TimeKeeping BETA DEV VERSION CONFIDENTIAL")
        self.root.geometry("500x550")
        self.root.configure(background="#99ccff")

        self.create_initial_frame()

   
        # Obtendo as informações de configuração do banco de dados
        db_config = get_db_config()

        # Conectando ao banco de dados usando as informações do arquivo de configuração
        self.connection = self.create_db_connection(db_config)

    def create_db_connection(self, db_config):
        connection = None
        try:
            connection = mysql.connector.connect(**db_config)
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        return connection

    def execute_query(self, query, data=None):
        cursor = self.connection.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")

    def read_query(self, query, data=None):
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")
            return []

    def create_initial_frame(self):
        self.clear_frame()

        # Criando um frame para os botões
        button_frame = tk.Frame(self.root, bg="#99ccff")  # Cor de fundo personalizada
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Posiciona o frame no centro da janela

        self.label = tk.Label(button_frame, text="Escolha uma opção:", font=("Arial", 14))
        self.label.pack()

        # Botão Registrar
        self.registrar_button = tk.Button(button_frame, text="Registrar", command=self.registrar, font=("Arial", 12))
        self.registrar_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        # Botão Login
        self.login_button = tk.Button(button_frame, text="Login", command=self.login, font=("Arial", 12))
        self.login_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        # Botão Sair
        self.sair_button = tk.Button(button_frame, text="Sair", command=self.killProgram, font=("Arial", 12))
        self.sair_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

    def killProgram(self):
        self.root.quit()
        print('Saiu')

    def registrar(self):
        self.clear_frame()

        self.nome_label = tk.Label(self.root, text="Nome:", bg="#e6e6fa", font=("Arial", 12))
        self.nome_label.pack(pady=5)
        self.nome_entry = tk.Entry(self.root, font=("Arial", 12))
        self.nome_entry.pack(pady=5)
        self.nome_entry.bind("<Return>", lambda event: self.email_entry.focus())  # Muda para o próximo campo ao pressionar Enter

        self.email_label = tk.Label(self.root, text="Email:", bg="#e6e6fa", font=("Arial", 12))
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        self.email_entry.bind("<Return>", lambda event: self.telefone_entry.focus())  # Muda para o próximo campo ao pressionar Enter

        self.telefone_label = tk.Label(self.root, text="Telefone:", bg="#e6e6fa", font=("Arial", 12))
        self.telefone_label.pack(pady=5)
        self.telefone_entry = tk.Entry(self.root, font=("Arial", 12))
        self.telefone_entry.pack(pady=5)
        self.telefone_entry.bind("<Return>", lambda event: self.senha_entry.focus())  # Muda para o próximo campo ao pressionar Enter

        self.senha_label = tk.Label(self.root, text="Senha:", bg="#e6e6fa", font=("Arial", 12))
        self.senha_label.pack(pady=5)
        self.senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.senha_entry.pack(pady=5)
        self.senha_entry.bind("<Return>", lambda event: self.registrar_usuario())  # Finaliza o registro ao pressionar Enter

        self.registrar_button = tk.Button(self.root, text="Registrar", command=self.registrar_usuario, font=("Arial", 12))
        self.registrar_button.pack(pady=20)

        # Botão de voltar
        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.create_initial_frame, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def registrar_usuario(self, event=None):  # Evento pode ser None quando chamado via botão, então fazemos a verificação
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        senha = self.senha_entry.get()

        if not all([nome, email, telefone, senha]):  # Verifica se todos os campos estão preenchidos
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if not self.validar_senha(senha):
            messagebox.showerror("Erro", "A senha deve conter pelo menos 8 caracteres, uma letra maiúscula e um caractere especial.")
            return

        query = "INSERT INTO Usuarios (nome, email, telefone, senha) VALUES (%s, %s, %s, %s)"
        data = (nome, email, telefone, senha)
        self.execute_query(query, data)

        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        self.create_initial_frame()

    def validar_senha(self, senha):
        if len(senha) < 8 or not re.search("[A-Z]", senha) or not re.search("[!@#$%^&*()-_+=~`'\";:/?.,<>{}[]|\\]", senha):
            return False
        return True

    def login(self):
        self.clear_frame()

        self.email_label = tk.Label(self.root, text="Email:", bg="#e6e6fa", font=("Arial", 12))
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        self.email_entry.bind("<Return>", lambda event: self.senha_entry.focus())  # Muda para o próximo campo ao pressionar Enter

        self.senha_label = tk.Label(self.root, text="Senha:", bg="#e6e6fa", font=("Arial", 12))
        self.senha_label.pack(pady=5)
        self.senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.senha_entry.pack(pady=5)
        self.senha_entry.bind("<Return>", lambda event: self.fazer_login())  # Finaliza o login ao pressionar Enter

        self.login_button = tk.Button(self.root, text="Login", command=self.fazer_login, font=("Arial", 12))
        self.login_button.pack(pady=20)

        # Botão de voltar
        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.create_initial_frame, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def fazer_login(self, event=None):  # Evento pode ser None quando chamado via botão, então fazemos a verificação
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not all([email, senha]):  # Verifica se todos os campos estão preenchidos
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        query = "SELECT * FROM Usuarios WHERE email = %s AND senha = %s"
        data = (email, senha)
        user = self.read_query(query, data)

        if user:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user[0]['nome']}!")
            self.abrir_menu()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")

    def abrir_menu(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Menu Principal", font=("Arial", 14))
        self.label.pack(pady=10)

        self.funcionarios_button = tk.Button(self.root, text="Gerenciar Funcionários", command=self.gerenciar_funcionarios, font=("Arial", 12))
        self.funcionarios_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        self.pontos_button = tk.Button(self.root, text="Gerenciar Pontos", command=self.gerenciar_pontos, font=("Arial", 12))
        self.pontos_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        self.sair_button = tk.Button(self.root, text="Sair", command=self.killProgram, font=("Arial", 12))
        self.sair_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

    def gerenciar_funcionarios(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Gerenciar Funcionários", font=("Arial", 14))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self.root, font=("Arial", 12))
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.abrir_menu, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def gerenciar_pontos(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Gerenciar Pontos", font=("Arial", 14))
        self.label.pack(pady=10)

        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.abrir_menu, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
