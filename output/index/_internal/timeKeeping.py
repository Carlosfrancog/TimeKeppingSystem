import json
import os
from datetime import datetime

def mark_time():
    # Pedir ao usuário o número de registro
    registro = input("Digite o número de registro: ")

    nome_funcionario = get_employee_name(registro)
    # Verificar se o número de registro existe no arquivo "registros.json"
    registros_existentes = get_existing_registers()
    if registro not in registros_existentes:
        print("Número de registro inválido.")
        return

    # Obter data e hora atual
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_atual = datetime.now().strftime("%Y-%m-%d")

    # Obter os pontos existentes do arquivo "pontos.json"
    pontos = get_existing_points()

    # Verificar se o funcionário já registrou 3 pontos no dia atual
    if registro in pontos and data_atual in pontos[registro]:
        if len(pontos[registro][data_atual]) >= 3:
            print("Você já registrou os 3 pontos do dia.")
            return

    # Permitir ao usuário marcar o ponto ao pressionar Enter
    input("Pressione Enter para marcar o ponto")

    # Verificar o tipo de ponto (entrada, almoço ou saída)
    tipo_ponto = "entrada"
    if registro in pontos and data_atual in pontos[registro]:
        if len(pontos[registro][data_atual]) == 1:
            tipo_ponto = "almoco"
        elif len(pontos[registro][data_atual]) == 2:
            tipo_ponto = "saida"

    # Adicionar o novo ponto à lista de pontos
    novo_ponto = {
        "nome_fincionario": nome_funcionario,
        "registro": registro,
        "data_hora": data_hora,
        "tipo": tipo_ponto
    }
    if registro not in pontos:
        pontos[registro] = {}
    if data_atual not in pontos[registro]:
        pontos[registro][data_atual] = []
    pontos[registro][data_atual].append(novo_ponto)

    # Registrar os pontos no arquivo "pontos.json"
    with open('Control/pontos.json', 'w') as f:
        json.dump(pontos, f, indent=4)

    print("Ponto marcado com sucesso!")

def get_existing_registers():
    try:
        with open('Datas/registros.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [registro['ID'] for registro in data.get('registros', [])]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []
    
def get_employee_name(registro):
    try:
        with open('Datas/registros.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for registro_data in data.get('registros', []):
                if registro_data['ID'] == registro:
                    return registro_data['Nome']
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pass
    return None


def get_existing_points():
    try:
        with open('Control/pontos.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}
    

def display_daily_points():
    # Obter a data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")
    # Obter os pontos existentes do arquivo "pontos.json"
    pontos = get_existing_points()

    print(f"PONTOS DO DIA {data_atual}:")
    for registro, registro_pontos in pontos.items():
        print("Nome do funcionário:", get_employee_name(registro))
        print("Registro:", registro)
        ponto_entrada = None
        ponto_almoco = None
        ponto_saida = None
        if data_atual in registro_pontos:
            for ponto in registro_pontos[data_atual]:
                tipo_ponto = ponto["tipo"]
                if tipo_ponto == "entrada":
                    ponto_entrada = ponto["data_hora"]
                elif tipo_ponto == "almoco":
                    ponto_almoco = ponto["data_hora"]
                elif tipo_ponto == "saida":
                    ponto_saida = ponto["data_hora"]
        print("Ponto de entrada:", ponto_entrada if ponto_entrada else "NULL")
        print("Ponto de almoço:", ponto_almoco if ponto_almoco else "NULL")
        print("Ponto de saída:", ponto_saida if ponto_saida else "NULL")
        print(f'-'*60)


