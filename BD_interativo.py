import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import platform
import subprocess

def abrir_imagem(filename='tabela.png'):
    if platform.system() == "Windows":
        os.startfile(filename)
    elif platform.system() == "Darwin":
        subprocess.run(['open', filename])
    else:
        subprocess.run(['xdg-open', filename])

def gerar_imagem_tabela(df, filename='tabela.png'):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.savefig(filename)
    plt.close()

def criar_bd(colunas):
    conn = sqlite3.connect('dados.bd')
    cursor = conn.cursor()
    col_defs = ", ".join([f"{col} TEXT" for col in colunas])
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {col_defs}
        )
    ''')
    conn.commit()
    return conn, cursor

def main():

    if os.path.exists("dados.bd"):
        os.remove("dados.bd") #Remove o banco de dados antigo para recriar um novo para

    print("=== SISTEMA DE BANCO DE DADOS (CMD) ===")
    try:
        num_colunas = int(input("Quantas colunas (além de ID)? ").strip())
        if num_colunas < 1:
            print("É necessário pelo menos uma coluna.")
            return
    except ValueError:
        print("Número inválido.")
        return

    colunas = []
    for i in range(num_colunas):
        while True:
            nome = input(f"Nome da coluna {i+1}: ").strip()
            if nome.isidentifier():
                colunas.append(nome)
                break
            else:
                print("Nome inválido. Use apenas letras, números e underline.")

    conn, cursor = criar_bd(colunas)
    print("\nBanco de dados pronto. Digite 'ajuda' para ver os comandos.")

    while True:
        cmd = input("\nCMD> ").strip().lower()

        if cmd == 'ajuda':
            print("Comandos disponíveis:")
            print("  inserir     - Inserir novo registro")
            print("  atualizar   - Atualizar valor por nome")
            print("  mostrar     - Mostrar tabela (gera imagem)")
            print("  buscar      - Buscar registros por valor")
            print("  remover     - Remover por nome ou ID")
            print("  sair        - Sair do programa")

        elif cmd == 'inserir':
            valores = []
            for col in colunas:
                valor = input(f"{col.capitalize()}: ").strip()
                valores.append(valor)
            placeholders = ", ".join(["?"] * len(colunas))
            cursor.execute(f"INSERT INTO pessoas ({', '.join(colunas)}) VALUES ({placeholders})", valores)
            conn.commit()
            print("Registro inserido com sucesso.")

        elif cmd == 'atualizar':
            campo_busca = input(f"Buscar por ({colunas[0]}): ").strip()
            campo_alvo = input(f"Qual coluna deseja atualizar? ({', '.join(colunas)}): ").strip()
            if campo_alvo not in colunas:
                print("Coluna inválida.")
                continue
            novo_valor = input(f"Novo valor para {campo_alvo}: ").strip()
            cursor.execute(f"UPDATE pessoas SET {campo_alvo} = ? WHERE {colunas[0]} = ?", (novo_valor, campo_busca))
            conn.commit()
            if cursor.rowcount == 0:
                print("Nenhum registro encontrado.")
            else:
                print(f"{cursor.rowcount} registro(s) atualizado(s).")

        elif cmd == 'mostrar':
            df = pd.read_sql_query("SELECT * FROM pessoas", conn)
            if df.empty:
                print("Tabela vazia.")
            else:
                gerar_imagem_tabela(df)
                print("Imagem da tabela gerada: tabela.png")
                abrir_imagem()

        elif cmd == 'buscar':
            campo = input(f"Digite o nome da coluna para busca ({', '.join(colunas)}): ").strip()
            if campo not in colunas:
                print("Coluna inválida.")
                continue
            valor = input(f"Valor de {campo}: ").strip()
            df = pd.read_sql_query(f"SELECT * FROM pessoas WHERE {campo} = ?", conn, params=(valor,))
            if df.empty:
                print("Nenhum registro encontrado.")
            else:
                print(df.to_string(index=False))

        elif cmd == 'remover':
            valor = input("Digite o nome ou ID para remover: ").strip()
            if valor.isdigit():
                cursor.execute("DELETE FROM pessoas WHERE id = ?", (int(valor),))
            else:
                cursor.execute(f"DELETE FROM pessoas WHERE {colunas[0]} = ?", (valor,))
            conn.commit()
            print(f"{cursor.rowcount} registro(s) removido(s).")

        elif cmd == 'sair':
            print("Saindo do sistema...")
            break

        else:
            print("Comando desconhecido. Digite 'ajuda' para ver os comandos.")

    conn.close()

if __name__ == "__main__":
    main()
