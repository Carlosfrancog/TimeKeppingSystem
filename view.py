import tkinter as tk
from tkinter import messagebox
import os
import json

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro e Login")
        self.root.geometry("500x500")

        self.frame = tk.Frame(self.root, bg="#e6e6fa")  # Fundo roxo claro
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.label = tk.Label(self.frame, text="Escolha uma opção:", bg="#e6e6fa", font=("Arial", 14))
        self.label.pack(pady=20)

        self.registrar_button = tk.Button(self.frame, text="Registrar", command=self.registrar, font=("Arial", 12))
        self.registrar_button.pack(pady=10, ipadx=20, ipady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login, font=("Arial", 12))
        self.login_button.pack(pady=10, ipadx=20, ipady=5)

        self.sair_button = tk.Button(self.frame, text="Sair", command=self.sair, font=("Arial", 12))
        self.sair_button.pack(pady=10, ipadx=20, ipady=5)

    def registrar(self):
        self.frame.destroy()  # Destruir o frame atual
        self.frame = tk.Frame(self.root, bg="#e6e6fa")
        self.frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)

        self.nome_label = tk.Label(self.frame, text="Nome:", bg="#e6e6fa", font=("Arial", 12))
        self.nome_label.grid(row=0, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        self.email_label = tk.Label(self.frame, text="Email:", bg="#e6e6fa", font=("Arial", 12))
        self.email_label.grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        self.telefone_label = tk.Label(self.frame, text="Telefone:", bg="#e6e6fa", font=("Arial", 12))
        self.telefone_label.grid(row=2, column=0, padx=10, pady=5)
        self.telefone_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.telefone_entry.grid(row=2, column=1, padx=10, pady=5)

        self.senha_label = tk.Label(self.frame, text="Senha:", bg="#e6e6fa", font=("Arial", 12))
        self.senha_label.grid(row=3, column=0, padx=10, pady=5)
        self.senha_entry = tk.Entry(self.frame, show="*", font=("Arial", 12))
        self.senha_entry.grid(row=3, column=1, padx=10, pady=5)

        self.registrar_button = tk.Button(self.frame, text="Registrar", command=self.registrar_usuario, font=("Arial", 12))
        self.registrar_button.grid(row=4, columnspan=2, pady=20)

    def registrar_usuario(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        senha = self.senha_entry.get()
        verify = False

        # Verifica se a senha atende aos critérios especificados
        if (
            len(senha) < 8
            or not any(char.isupper() for char in senha)
            or not any(char in "!@#$%^&*()-_+=~`'\";:/?.,<>{}[]|\\"
                    for char in senha)
        ):
            verify = True

        if verify:
            messagebox.showerror("Erro", "A senha deve conter pelo menos 8 caracteres, uma letra maiúscula e um caractere especial.")
            return

        novo_usuario = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "senha": senha
        }

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

        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        self.frame.destroy()  # Destruir o frame de registro após o registro bem-sucedido

    def login(self):
        messagebox.showinfo("Info", "Função de login não implementada ainda!")

    def sair(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
