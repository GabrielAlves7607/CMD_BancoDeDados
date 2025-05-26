# 📦 BD Interativo - Sistema de Banco de Dados via CMD

Este é um sistema de banco de dados interativo em Python, executado diretamente no terminal (CMD), que permite:

- Criar um banco de dados com colunas personalizadas
- Inserir, atualizar, buscar e remover registros
- Visualizar os dados como imagem gerada automaticamente

---

## 🚀 Como Funciona

Ao iniciar o script, você define quantas colunas deseja (além do ID automático) e escolhe os nomes das colunas. Em seguida, o sistema oferece comandos interativos para manipular os dados.

---

## 📌 Funcionalidades

- `inserir`: Adiciona um novo registro ao banco de dados.
- `atualizar`: Atualiza o valor de uma coluna de um registro específico.
- `mostrar`: Gera uma imagem da tabela com os registros atuais.
- `buscar`: Exibe registros que contenham um valor específico em uma coluna.
- `remover`: Remove registros por nome ou pelo ID.
- `ajuda`: Lista todos os comandos disponíveis.
- `sair`: Encerra o sistema.

---

## 💻 Requisitos

Antes de rodar o sistema, instale as dependências:

```bash
pip install pandas matplotlib
