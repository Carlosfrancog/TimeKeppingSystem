import os
from random import randint
from Functions import showRegisters, timeKeeping
import json

os.system('cls' or 'clear')

class RegistersEmployee:
    def __init__(self, name, office, workHours, entryTime, exitTime, lunch):
        self.name      = name
        self.office    = office
        self.idNumber  = self.Id()
        self.workHours = workHours
        self.entryTime = entryTime
        self.exitTime  = exitTime
        self.lunch     = lunch

    def Id(self):
        while True:
            new_id = ''.join(str(randint(0, 9)) for _ in range(6))
            if not any(record['ID'] == new_id for record in self.existing_records()):
                return new_id

    def existing_records(self):
        try:
            with open('Datas/registros.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('registros', [])
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    
    def Register(self):
        print('NÃO USE ACENTOS OU CARACTERES ESPECIAIS!')
        self.name = input("Digite o nome do funcionário: ")
        self.office = input(f"Digite a ocupação do funcionário {self.name}: ")
        self.workHours = input("Digite (em horas) o expediente total do funcionário: ")
        self.entryTime = input('Digite a hora de entrada do funcionário: ')
        self.exitTime = input('Digite a hora de saída do funcionário: ')
        self.lunch = input("Digite a hora de almoço do funcionário: ")
        print(f'O número de identificação para {self.name} é {int(self.idNumber)}: ')
        
        finallyQuest = str(input('\nDESEJA FINALIZAR O CADASTRO? [S/N]: ')).strip().upper()[0]

        while finallyQuest not in 'SsNn':
            print('INVÁLIDO! DIGITE S OU N')
            finallyQuest = str(input('\nDESEJA FINALIZAR O CADASTRO? [S/N]: ')).strip().upper()[0]
        
        if finallyQuest in 'Nn':
            print("RECOMEÇANDO CADASTRO...")
            os.system('cls' or 'clear')
            self.Register()
        else:
            print('REGISTRANDO FUNCIONÁRIO...')
            with open('Datas/registros.json', 'r+', encoding='utf-8') as f:
                try:
                    # Tentar carregar os dados existentes
                    data = json.load(f)
                except (FileNotFoundError, json.decoder.JSONDecodeError):
                    # Se o arquivo estiver vazio ou não existir, começar com um dicionário vazio
                    data = {}

                # Adicionar o novo registro à lista de registros
                new_record = {
                    'Nome': self.name,
                    'Cargo': self.office,
                    'Jornada de trabalho': self.workHours,
                    'Horario de entrada': self.entryTime,
                    'Horario de saida': self.exitTime,
                    'Horario de almoco': self.lunch,
                    'ID': self.idNumber
                }

                # Verificar se já existe uma lista de registros, se não, criar uma
                if 'registros' not in data:
                    data['registros'] = []

                # Adicionar o novo registro à lista
                data['registros'].append(new_record)

                # Voltar ao início do arquivo para escrever os dados
                f.seek(0)
                # Escrever os dados de volta ao arquivo
                json.dump(data, f, indent=4)

            print('FUNCIONÁRIO REGISTRADO!')
    

class MainClass:
    def __init__(self):
        while True:
            os.system('cls' or 'clear')
            menu =  str(input('''                         
    MENU:          
        [1] CADASTRAR FUNCIONÁRIO
        [2] EXIBIR FUNCIONÁRIO
        [3] LISTA DE PONTO
        [4] SAIR
:'''))[0]
            
            
            if menu == "1":
                        os.system('cls' or 'clear')
                        employee = RegistersEmployee("", "", "", "", "", "")
                        employee.Register()
            elif menu == "2":
                    os.system('cls' or 'clear')
                    showRegisters.display_records()
                    input("Pressione Enter para voltar ao menu...")
            elif menu == "3":
                    os.system('cls' or 'clear')
                    timeKeeping.display_daily_points()
                    input("prssionne Enter para voltar para o menu.")
            elif menu == "4":
                break
            elif menu == '5': #TESTE
                timeKeeping.mark_time()

    os.system('cls' or 'clear')
    


