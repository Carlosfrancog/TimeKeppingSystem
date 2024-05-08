import json
import os

def display_records():
    try:
        with open('Datas/registros.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            registros = data.get('registros', [])

            os.system('cls' or 'clear')
            if registros:
                print("REGISTROS:")
                for registro in registros:
                    print(f"Nome: {registro['Nome']}")
                    print(f"Cargo: {registro['Cargo']}")
                    print(f"Jornada de trabalho: {registro['Jornada de trabalho']}")
                    print(f"Horario de entrada: {registro['Horario de entrada']}")
                    print(f"Horario de saida: {registro['Horario de saida']}")
                    print(f"Horario de almoco: {registro['Horario de almoco']}")
                    print(f"ID: {registro['ID']}")
                    print()
            else:
                print("Não há registros para exibir.")
    except FileNotFoundError:
        print("Arquivo de registros não encontrado.")
    except json.decoder.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")

