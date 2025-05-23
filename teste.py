import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import platform
import subprocess

def criar_bd():
    conn = sqlite3.connect('dados.bd')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        idade INTEGER
    )
    ''')
    conn.commit()
    return conn, cursor

def gerar_imagem_tabela(df):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis('tight')
    ax.axis('off')
    tbl = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    plt.savefig('tabela.png')
    plt.close()

def abrir_imagem():
    if platform.system() == "Windows":
        os.startfile('tabela.png')
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(['open', 'tabela.png'])
    else:  # Linux
        subprocess.run(['xdg-open', 'tabela.png'])

def main():
    conn, cursor = criar_bd()
    print("Bem-vindo ao sistema BD! Digite 'ajuda' para ver os comandos.")
    
    while True:
        cmd = input("CMD> ").strip().lower()

        if cmd == 'ajuda':
            print("Comandos disponíveis:")
            print("  inserir - Inserir novo registro")
            print("  atualizar - Atualizar idade por nome")
            print("  mostrar - Mostrar tabela (gera imagem)")
            print("  sair - Sair do programa")
        
        elif cmd == 'inserir':
            nome = input("Nome: ").strip()
            idade = input("Idade: ").strip()
            if not idade.isdigit():
                print("Idade inválida, tente novamente.")
                continue
            cursor.execute("INSERT INTO pessoas (nome, idade) VALUES (?, ?)", (nome, int(idade)))
            conn.commit()
            print(f"Registro de {nome} inserido com sucesso.")

        elif cmd == 'atualizar':
            nome = input("Nome para atualizar: ").strip()
            idade = input("Nova idade: ").strip()
            if not idade.isdigit():
                print("Idade inválida, tente novamente.")
                continue
            cursor.execute("UPDATE pessoas SET idade = ? WHERE nome = ?", (int(idade), nome))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"Nenhum registro encontrado para {nome}.")
            else:
                print(f"Idade de {nome} atualizada para {idade}.")

        elif cmd == 'mostrar':
            df = pd.read_sql_query("SELECT * FROM pessoas", conn)
            if df.empty:
                print("Tabela vazia.")
            else:
                gerar_imagem_tabela(df)
                print("Imagem da tabela gerada: tabela.png")
                abrir_imagem()

        elif cmd == 'sair':
            print("Saindo...")
            break

        else:
            print("Comando desconhecido. Digite 'ajuda' para ver os comandos.")

    conn.close()

if __name__ == "__main__":
    main()
