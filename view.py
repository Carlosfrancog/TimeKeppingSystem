import tkinter as tk
from tkinter import messagebox, ttk
import re
import mysql.connector
from mysql.connector import Error
import bcrypt


'''
faltou adicionar o dashbord caso seja feito login
 como master e também um botão na página do usuario para 
 voltar para a tela de login, com uma verificação "deseja realemnte sair?"
'''


class InterfaceGrafica:
    def __init__(self, root):
        self.root = root    
        #self.root.iconbitmap("icon.ico")
        self.root.title("TimeKeeping BETA DEV VERSION CONFIDENTIAL")
        self.root.geometry("500x550")
        self.root.configure(background="#99ccff")

        # Conectando ao banco de dados
        self.connection = self.create_db_connection("localhost", "root", "123456abc", "TimeKeepingDB")

        # Verifica se há usuários "master" no banco de dados
        if not self.check_master_user():
            self.create_master_user_registration_frame()
        else:
            self.create_login_frame()

    def create_db_connection(self, host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
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

    def create_master_user_registration_frame(self):
        self.clear_frame()

        # Criando um frame para os campos de registro
        registration_frame = tk.Frame(self.root, bg="#99ccff")
        registration_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label = tk.Label(registration_frame, text="Registrar Usuário Master", font=("Arial", 14))
        self.label.pack(pady=10)

        self.nome_label = tk.Label(registration_frame, text="Nome:", bg="#e6e6fa", font=("Arial", 12))
        self.nome_label.pack(pady=5)
        self.nome_entry = tk.Entry(registration_frame, font=("Arial", 12))
        self.nome_entry.pack(pady=5)

        self.email_label = tk.Label(registration_frame, text="Email:", bg="#e6e6fa", font=("Arial", 12))
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(registration_frame, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        self.telefone_label = tk.Label(registration_frame, text="Telefone:", bg="#e6e6fa", font=("Arial", 12))
        self.telefone_label.pack(pady=5)
        self.telefone_entry = tk.Entry(registration_frame, font=("Arial", 12))
        self.telefone_entry.pack(pady=5)

        self.senha_label = tk.Label(registration_frame, text="Senha:", bg="#e6e6fa", font=("Arial", 12))
        self.senha_label.pack(pady=5)
        self.senha_entry = tk.Entry(registration_frame, show="*", font=("Arial", 12))
        self.senha_entry.pack(pady=5)

        self.registrar_button = tk.Button(registration_frame, text="Registrar", command=self.registrar_master_user, font=("Arial", 12))
        self.registrar_button.pack(pady=10)

        # Botão de login
        self.login_button = tk.Button(registration_frame, text="Login", command=self.master_login, font=("Arial", 12))
        self.login_button.pack(pady=10)

    def create_login_frame(self):
        self.clear_frame()

        # Criando um frame para os campos de login
        login_frame = tk.Frame(self.root, bg="#99ccff")
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label = tk.Label(login_frame, text="Login", font=("Arial", 14))
        self.label.pack(pady=10)

        self.email_label = tk.Label(login_frame, text="Email:", bg="#e6e6fa", font=("Arial", 12))
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(login_frame, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        self.senha_label = tk.Label(login_frame, text="Senha:", bg="#e6e6fa", font=("Arial", 12))
        self.senha_label.pack(pady=5)
        self.senha_entry = tk.Entry(login_frame, show="*", font=("Arial", 12))
        self.senha_entry.pack(pady=5)

        self.login_button = tk.Button(login_frame, text="Login", command=self.fazer_login, font=("Arial", 12))
        self.login_button.pack(pady=20)

        # Botão de voltar
        #self.voltar_button = tk.Button(login_frame, text="Voltar", command=self.create_master_user_registration_frame, font=("Arial", 12))
        #self.voltar_button.pack(pady=10)

        self.voltar_button = tk.Button(login_frame, text="Sair", command=self.KillProgram, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def master_login(self):
        # Verifica se há um usuário mestre no banco de dados
        if self.check_master_user():
            # Se houver, vá para a tela de login
            self.create_login_frame()
        else:
            # Caso contrário, volte para a tela da master
            self.create_master_user_registration_frame()

    def registrar_master_user(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        senha = self.senha_entry.get()

        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Telefone: {telefone}")

        # Verifica se todos os campos estão preenchidos
        if not all([nome, email, telefone, senha]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        print("Campos preenchidos.")

        # Verifica se o e-mail possui um formato válido
        if not re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email):
            messagebox.showerror("Erro", "Formato de e-mail inválido.")
            return

        print("Formato de e-mail válido.")

        # Verifica se o telefone possui um formato válido
        if not re.match(r"^\d{10}$", telefone):
            messagebox.showerror("Erro", "Formato de telefone inválido. Insira apenas os 10 dígitos.")
            return

        print("Formato de telefone válido.")

        # Verifica se a senha atende aos requisitos
        if not self.validar_senha(senha):
            messagebox.showerror("Erro", "A senha deve conter pelo menos 8 caracteres, uma letra maiúscula e um caractere especial.")
            return

        print("Senha válida.")

        # Hash da senha antes de armazenar
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        print(f"Senha hasheada: {hashed_password.decode('utf-8')}")

        # Insere o usuário mestre no banco de dados
        query = "INSERT INTO usuarios_master (nome, email, telefone, senha) VALUES (%s, %s, %s, %s)"
        data = (nome, email, telefone, hashed_password.decode('utf-8'))
        self.execute_query(query, data)

        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        self.create_initial_frame()

    def check_master_user(self):
        query = "SELECT * FROM usuarios_master"
        result = self.read_query(query)
        return True if result else False

    #INITIAL MASTER USER FRAME---------------------------------------------------------------------------------------------------------------
    def create_initial_frame(self):
        self.clear_frame()

        # Criando um frame para os botões
        button_frame = tk.Frame(self.root, bg="#99ccff")  # Cor de fundo personalizada
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Posiciona o frame no centro da janela

        self.label = tk.Label(button_frame, text="Escolha uma opção:", font=("Arial", 14))
        self.label.pack()

        #ver usuarios
        self.showUser_button = tk.Button(button_frame, text="Ver usuários", command=self.showUsers, font=("Arial", 12))
        self.showUser_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        #dashboard
        self.showUser_button = tk.Button(button_frame, text="Gerenciar usuários", command=self.create_dashboard_frame, font=("Arial", 12))
        self.showUser_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        # Botão Registrar
        self.registrar_button = tk.Button(button_frame, text="Registrar", command=self.registrar, font=("Arial", 12))
        self.registrar_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        # Botão Login
        self.login_button = tk.Button(button_frame, text="Login", command=self.login, font=("Arial", 12))
        self.login_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)
        #INITIAL MASTER USER FRAME---------------------------------------------------------------------------------------------------------------

    def showUsers(self):
        # Ajustar o tamanho da janela para exibir os usuários
        self.root.geometry("500x550")

        # Limpar o frame atual
        self.clear_frame()

        # Criar um novo frame para exibir os usuários
        users_frame = tk.Frame(self.root, bg="#99ccff")
        users_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label = tk.Label(users_frame, text="Usuários Registrados", font=("Arial", 14))
        self.label.pack(pady=10)

        # Criar a tabela
        columns = ("id", "nome", "email", "telefone")
        self.tree = ttk.Treeview(users_frame, columns=columns, show='headings')

        # Definir as colunas
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor=tk.CENTER, width=100)

        self.tree.pack(pady=10)

        # Ler dados do banco de dados
        query = "SELECT id, nome, email, telefone FROM usuarios"
        rows = self.read_query(query)

        # Inserir dados na tabela
        for row in rows:
            self.tree.insert("", tk.END, values=(row["id"], row["nome"], row["email"], row["telefone"]))

        # Botão de voltar
        self.voltar_button = tk.Button(users_frame, text="Voltar", command=self.create_initial_frame, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    #DASHBOARD PAGE-----------------------------------------------------------------------------------------------------------------------------------------------------
    def create_dashboard_frame(self):

        # Limpar o frame atual
        self.clear_frame()

        dashboard_frame = tk.Frame(self.root, bg="#99ccff")
        dashboard_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.label = tk.Label(dashboard_frame, text="Gerenciar usuários", font=("Arial", 14))
        self.label.pack(pady=10)

        self.cadastrar_func_button = tk.Button(dashboard_frame, text="Cadastrar Funcionário", command=self.cadastrar_funcionario_frame, font=("Arial", 12))
        self.cadastrar_func_button.pack(pady=10)

        self.visualizar_func_button = tk.Button(dashboard_frame, text="Visualizar Funcionários", command=self.visualizar_funcionarios_frame, font=("Arial", 12))
        self.visualizar_func_button.pack(pady=10)

        # Botão para voltar
        self.sair_button = tk.Button(dashboard_frame, text="Voltar", command=self.create_initial_frame, font=("Arial", 12))
        self.sair_button.pack(pady=10)


    def cadastrar_funcionario_frame(self):
        pass
    
    def visualizar_funcionarios_frame(self):
        pass
    #DASHBOARD PAGE-----------------------------------------------------------------------------------------------------------------------------------------------------





    def registrar(self):
        self.create_master_user_registration_frame()

    def login(self):
        self.create_login_frame()

    def fazer_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        # Verifica se todos os campos estão preenchidos
        if not all([email, senha]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        # Verifica o e-mail e senha na tabela usuarios_master
        query = "SELECT * FROM usuarios_master WHERE email = %s"
        result = self.read_query(query, (email,))

        if result and bcrypt.checkpw(senha.encode('utf-8'), result[0]['senha'].encode('utf-8')):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.create_initial_frame()  # Volta para a tela inicial
        else:
            # Verifica o e-mail e senha na tabela usuarios
            query = "SELECT * FROM usuarios WHERE email = %s"
            result = self.read_query(query, (email,))

            if result and bcrypt.checkpw(senha.encode('utf-8'), result[0]['senha'].encode('utf-8')):
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.create_user_frame(result[0]['nome'])  # Redireciona para a tela do usuário
            else:
                messagebox.showerror("Erro", "Credenciais inválidas.")

    def create_user_frame(self, nome_usuario):
        self.clear_frame()

        user_frame = tk.Frame(self.root, bg="#99ccff")
        user_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label = tk.Label(user_frame, text=f"Bem-vindo, {nome_usuario}", font=("Arial", 14))
        self.label.pack(pady=10)

        self.marcar_ponto_button = tk.Button(user_frame, text="Marcar Ponto", font=("Arial", 12))
        self.marcar_ponto_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        self.perfil_button = tk.Button(user_frame, text="Perfil", font=("Arial", 12))
        self.perfil_button.pack(pady=10, ipadx=20, ipady=10, fill=tk.BOTH, expand=True)

        # Botão de voltar
        self.voltar_button = tk.Button(user_frame, text="Voltar", command=self.create_login_frame, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

        self.voltar_button = tk.Button(user_frame, text="Sair", command=self.KillProgram, font=("Arial", 12))
        self.voltar_button.pack(pady=10)



    def KillProgram(self):
        exit()



    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def validar_senha(self, senha):
        if len(senha) < 8:
            return False
        if not re.search(r"[A-Z]", senha):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
