import tkinter as tk
from tkinter import messagebox, scrolledtext
from random import randint
import os
import json
import re


class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap("./ViewLayer/images/icon.ico")
        self.root.title("TimeKeeping BETA DEV VERSION CONFIDENTIAL")
        self.root.geometry("500x550")
        self.root.configure(background="#99ccff")

        self.create_initial_frame()

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

        novo_usuario = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "senha": senha
        }

        arquivo_registros = "ViewLayer/Registers.json"
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

    def fazer_login(self):
        email_login = self.email_entry.get()
        senha_login = self.senha_entry.get()

        arquivo_registros = "ViewLayer/Registers.json"
        if os.path.exists(arquivo_registros) and os.path.getsize(arquivo_registros) > 0:
            with open(arquivo_registros, "r") as f:
                try:
                    registros = json.load(f)
                except json.JSONDecodeError:
                    registros = []
        else:
            messagebox.showerror("Erro", "Nenhum usuário registrado ainda.")
            return

        for usuario in registros:
            if usuario["email"] == email_login and usuario["senha"] == senha_login:
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                self.clear_frame()
                self.show_menu_principal()  # Após o login bem-sucedido, mostra o menu principal
                return

        messagebox.showerror("Erro", "Email ou senha incorretos. Tente novamente.")

    def show_menu_principal(self):
        self.clear_frame()

        # Adiciona um frame para conter os botões do menu principal
        menu_frame = tk.Frame(self.root, bg="#99ccff")
        menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Define o tamanho e o estilo dos botões do menu
        button_style = {"font": ("Arial", 12), "width": 30, "height": 2, "bg": "#6495ED", "fg": "white"}

        # Adiciona botões para cada opção do menu principal
        cadastrar_funcionario_button = tk.Button(menu_frame, text="CADASTRAR FUNCIONÁRIO", command=self.cadastrar_funcionario, **button_style)
        cadastrar_funcionario_button.pack(pady=10)

        exibir_funcionario_button = tk.Button(menu_frame, text="EXIBIR FUNCIONÁRIO", command=self.exibir_funcionario, **button_style)
        exibir_funcionario_button.pack(pady=10)

        lista_ponto_button = tk.Button(menu_frame, text="LISTA DE PONTO", command=self.lista_ponto, **button_style)
        lista_ponto_button.pack(pady=10)

        sair_button = tk.Button(menu_frame, text="SAIR", command=self.sair, **button_style)
        sair_button.pack(pady=10)

    def cadastrar_funcionario(self):
        self.clear_frame()

        self.nome_label = tk.Label(self.root, text="Nome:", bg="#e6e6fa", font=("Arial", 12))
        self.nome_label.pack(pady=5)
        self.nome_entry = tk.Entry(self.root, font=("Arial", 12))
        self.nome_entry.pack(pady=5)

        self.office_label = tk.Label(self.root, text="Cargo:", bg="#e6e6fa", font=("Arial", 12))
        self.office_label.pack(pady=5)
        self.office_entry = tk.Entry(self.root, font=("Arial", 12))
        self.office_entry.pack(pady=5)

        self.workhours_label = tk.Label(self.root, text="Jornada de Trabalho (em horas):", bg="#e6e6fa", font=("Arial", 12))
        self.workhours_label.pack(pady=5)
        self.workhours_entry = tk.Entry(self.root, font=("Arial", 12))
        self.workhours_entry.pack(pady=5)

        self.entrytime_label = tk.Label(self.root, text="Horário de Entrada:", bg="#e6e6fa", font=("Arial", 12))
        self.entrytime_label.pack(pady=5)
        self.entrytime_entry = tk.Entry(self.root, font=("Arial", 12))
        self.entrytime_entry.pack(pady=5)

        self.exittime_label = tk.Label(self.root, text="Horário de Saída:", bg="#e6e6fa", font=("Arial", 12))
        self.exittime_label.pack(pady=5)
        self.exittime_entry = tk.Entry(self.root, font=("Arial", 12))
        self.exittime_entry.pack(pady=5)

        self.lunchtime_label = tk.Label(self.root, text="Horário de Almoço:", bg="#e6e6fa", font=("Arial", 12))
        self.lunchtime_label.pack(pady=5)
        self.lunchtime_entry = tk.Entry(self.root, font=("Arial", 12))
        self.lunchtime_entry.pack(pady=5)

        self.cadastrar_funcionario_button = tk.Button(self.root, text="Cadastrar Funcionário", command=self.salvar_funcionario, font=("Arial", 12))
        self.cadastrar_funcionario_button.pack(pady=20)

        # Botão de voltar
        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.show_menu_principal, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def salvar_funcionario(self):
        nome = self.nome_entry.get()
        cargo = self.office_entry.get()
        jornada_trabalho = self.workhours_entry.get()
        horario_entrada = self.entrytime_entry.get()
        horario_saida = self.exittime_entry.get()
        horario_almoco = self.lunchtime_entry.get()

        # Verifica se todos os campos estão preenchidos
        if not all([nome, cargo, jornada_trabalho, horario_entrada, horario_saida, horario_almoco]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        # Gerar ID automaticamente e verificar se já existe
        novo_id = self.gerar_novo_id()
        while novo_id in self.existing_ids():
            novo_id = self.gerar_novo_id()

        novo_funcionario = {
            "index": 0,  # Inicializando o índice com 0
            "Nome": nome,
            "Cargo": cargo,
            "Jornada de Trabalho": jornada_trabalho,
            "Horario de Entrada": horario_entrada,
            "Horario de Saida": horario_saida,
            "Horario de Almoco": horario_almoco,
            "ID": novo_id
        }

        arquivo_registros = "ViewLayer/Funcionarios.json"
        with open(arquivo_registros, "r+") as f:
            try:
                registros = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                registros = []

            # Definindo o índice para o próximo registro
            novo_funcionario["index"] = len(registros)

            registros.append(novo_funcionario)

            f.seek(0)
            json.dump(registros, f, indent=4)

        messagebox.showinfo("Sucesso", "Funcionário registrado com sucesso!")
        self.show_menu_principal()


    def gerar_novo_id(self):
        return ''.join(str(randint(0, 9)) for _ in range(6))

    def existing_ids(self):
        try:
            with open('ViewLayer/Funcionarios.json', 'r') as f:
                data = json.load(f)
                if data:
                    return [registro.get('ID') for registro in data]
                else:
                    return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def exibir_funcionario(self):
        self.clear_frame()

        self.search_label = tk.Label(self.root, text="Pesquisar por ID:", bg="#e6e6fa", font=("Arial", 12))
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root, font=("Arial", 12))
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Pesquisar", command=self.pesquisar_funcionario, font=("Arial", 12))
        self.search_button.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self.root, width=60, height=15, font=("Arial", 12))
        self.text_area.pack(pady=10)
        self.text_area.config(state="disabled")  # Configura a área de texto como somente leitura

        # Carrega automaticamente o primeiro funcionário
        self.pesquisar_funcionario()

        self.proximo_button = tk.Button(self.root, text="Próximo", command=self.exibir_proximo_funcionario, font=("Arial", 12))
        self.proximo_button.pack(pady=10)

        # Botão de voltar
        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.show_menu_principal, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def pesquisar_funcionario(self):
        search_id = self.search_entry.get()

        arquivo_registros = "ViewLayer/Funcionarios.json"
        if os.path.exists(arquivo_registros) and os.path.getsize(arquivo_registros) > 0:
            with open(arquivo_registros, "r") as f:
                try:
                    registros = json.load(f)
                except json.JSONDecodeError:
                    registros = []
        else:
            registros = []

        # Se o campo de pesquisa está vazio, carrega o primeiro funcionário
        if not search_id:
            if registros:
                funcionario = registros[0]
                self.text_area.config(state="normal")  # Habilita a área de texto para escrita temporariamente
                self.text_area.delete("1.0", tk.END)  # Limpa a área de texto
                self.text_area.insert(tk.END, f"ID: {funcionario['ID']}\n")
                self.text_area.insert(tk.END, f"Nome: {funcionario['Nome']}\n")
                self.text_area.insert(tk.END, f"Cargo: {funcionario['Cargo']}\n")
                self.text_area.insert(tk.END, f"Jornada de Trabalho: {funcionario['Jornada de Trabalho']}\n")
                self.text_area.insert(tk.END, f"Horário de Entrada: {funcionario['Horario de Entrada']}\n")
                self.text_area.insert(tk.END, f"Horário de Saída: {funcionario['Horario de Saida']}\n")
                self.text_area.insert(tk.END, f"Horário de Almoço: {funcionario['Horario de Almoco']}\n")
                self.text_area.config(state="disabled")  # Volta a desabilitar a área de texto
            else:
                messagebox.showerror("Erro", "Nenhum funcionário cadastrado ainda.")
            return

        for funcionario in registros:
            if funcionario["ID"] == search_id:
                self.text_area.config(state="normal")  # Habilita a área de texto para escrita temporariamente
                self.text_area.delete("1.0", tk.END)  # Limpa a área de texto
                self.text_area.insert(tk.END, f"ID: {funcionario['ID']}\n")
                self.text_area.insert(tk.END, f"Nome: {funcionario['Nome']}\n")
                self.text_area.insert(tk.END, f"Cargo: {funcionario['Cargo']}\n")
                self.text_area.insert(tk.END, f"Jornada de Trabalho: {funcionario['Jornada de Trabalho']}\n")
                self.text_area.insert(tk.END, f"Horário de Entrada: {funcionario['Horario de Entrada']}\n")
                self.text_area.insert(tk.END, f"Horário de Saída: {funcionario['Horario de Saida']}\n")
                self.text_area.insert(tk.END, f"Horário de Almoço: {funcionario['Horario de Almoco']}\n")
                self.text_area.config(state="disabled")  # Volta a desabilitar a área de texto
                return

        messagebox.showerror("Erro", f"Nenhum funcionário encontrado com o ID {search_id}.")

    def exibir_proximo_funcionario(self):
        arquivo_registros = "ViewLayer/Funcionarios.json"
        if os.path.exists(arquivo_registros) and os.path.getsize(arquivo_registros) > 0:
            with open(arquivo_registros, "r") as f:
                try:
                    registros = json.load(f)
                except json.JSONDecodeError:
                    registros = []
        else:
            registros = []

        # Se não houver registros, exibe uma mensagem de erro
        if not registros:
            messagebox.showerror("Erro", "Nenhum funcionário cadastrado ainda.")
            return

        # Obtém o índice atual do funcionário exibido
        current_index = getattr(self, 'current_index', 0)

        # Obtém o próximo índice
        next_index = (current_index + 1) % len(registros)

        # Obtém o próximo funcionário
        proximo_funcionario = registros[next_index]

        # Exibe as informações do próximo funcionário na tela
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, f"ID: {proximo_funcionario['ID']}\n")
        self.text_area.insert(tk.END, f"Nome: {proximo_funcionario['Nome']}\n")
        self.text_area.insert(tk.END, f"Cargo: {proximo_funcionario['Cargo']}\n")
        self.text_area.insert(tk.END, f"Jornada de Trabalho: {proximo_funcionario['Jornada de Trabalho']}\n")
        self.text_area.insert(tk.END, f"Horário de Entrada: {proximo_funcionario['Horario de Entrada']}\n")
        self.text_area.insert(tk.END, f"Horário de Saída: {proximo_funcionario['Horario de Saida']}\n")
        self.text_area.insert(tk.END, f"Horário de Almoço: {proximo_funcionario['Horario de Almoco']}\n")
        self.text_area.config(state="disabled")

        # Atualiza o índice atual do funcionário exibido
        self.current_index = next_index

    def lista_ponto(self):
        self.clear_frame()

        self.search_label = tk.Label(self.root, text="Pesquisar por ID:", bg="#e6e6fa", font=("Arial", 12))
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root, font=("Arial", 12))
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Pesquisar", command=self.exibir_ponto, font=("Arial", 12))
        self.search_button.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self.root, width=60, height=15, font=("Arial", 12))
        self.text_area.pack(pady=10)
        self.text_area.config(state="disabled")  # Configura a área de texto como somente leitura

        self.exibir_ponto_button = tk.Button(self.root, text="Exibir Ponto", command=self.exibir_ponto, font=("Arial", 12))
        self.exibir_ponto_button.pack(pady=5)

        # Botão de voltar
        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.show_menu_principal, font=("Arial", 12))
        self.voltar_button.pack(pady=10)

    def exibir_ponto(self):
        search_id = self.search_entry.get()

        arquivo_registros = "ViewLayer/Ponto.json"
        if os.path.exists(arquivo_registros) and os.path.getsize(arquivo_registros) > 0:
            with open(arquivo_registros, "r") as f:
                try:
                    registros = json.load(f)
                except json.JSONDecodeError:
                    registros = []
        else:
            registros = []

        if not search_id:
            if registros:
                ponto = registros[0]
                self.text_area.config(state="normal")  # Habilita a área de texto para escrita temporariamente
                self.text_area.delete("1.0", tk.END)  # Limpa a área de texto
                self.text_area.insert(tk.END, f"ID: {ponto['ID']}\n")
                self.text_area.insert(tk.END, f"Data: {ponto['Data']}\n")
                self.text_area.insert(tk.END, f"Hora de Entrada: {ponto['Hora de Entrada']}\n")
                self.text_area.insert(tk.END, f"Hora de Saída: {ponto['Hora de Saída']}\n")
                self.text_area.insert(tk.END, f"Horas Trabalhadas: {ponto['Horas Trabalhadas']}\n")
                self.text_area.insert(tk.END, f"Horas Extras: {ponto['Horas Extras']}\n")
                self.text_area.insert(tk.END, f"Horas de Almoço: {ponto['Horas de Almoço']}\n")
                self.text_area.insert(tk.END, f"Observações: {ponto['Observações']}\n")
                self.text_area.config(state="disabled")  # Volta a desabilitar a área de texto
            else:
                messagebox.showerror("Erro", "Nenhum ponto registrado ainda.")
            return

        for ponto in registros:
            if ponto["ID"] == search_id:
                self.text_area.config(state="normal")  # Habilita a área de texto para escrita temporariamente
                self.text_area.delete("1.0", tk.END)  # Limpa a área de texto
                self.text_area.insert(tk.END, f"ID: {ponto['ID']}\n")
                self.text_area.insert(tk.END, f"Data: {ponto['Data']}\n")
                self.text_area.insert(tk.END, f"Hora de Entrada: {ponto['Hora de Entrada']}\n")
                self.text_area.insert(tk.END, f"Hora de Saída: {ponto['Hora de Saída']}\n")
                self.text_area.insert(tk.END, f"Horas Trabalhadas: {ponto['Horas Trabalhadas']}\n")
                self.text_area.insert(tk.END, f"Horas Extras: {ponto['Horas Extras']}\n")
                self.text_area.insert(tk.END, f"Horas de Almoço: {ponto['Horas de Almoço']}\n")
                self.text_area.insert(tk.END, f"Observações: {ponto['Observações']}\n")
                self.text_area.config(state="disabled")  # Volta a desabilitar a área de texto
                return

        messagebox.showerror("Erro", f"Nenhum ponto encontrado com o ID {search_id}.")

    def sair(self):
        self.clear_frame()
        self.create_initial_frame()

    def clear_frame(self):
        # Limpa todos os widgets do frame
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        # Inicia a execução da interface
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()