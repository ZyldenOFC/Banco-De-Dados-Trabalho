import sqlite3

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS autores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS editoras (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor_id INTEGER,
                editora_id INTEGER,
                ano_publicacao INTEGER,
                edicao TEXT,
                disponivel INTEGER DEFAULT 1,
                FOREIGN KEY (autor_id) REFERENCES autores(id),
                FOREIGN KEY (editora_id) REFERENCES editoras(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                data TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos_livros (
                emprestimo_id INTEGER,
                livro_id INTEGER,
                data_devolucao TEXT,
                PRIMARY KEY (emprestimo_id, livro_id),
                FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(id),
                FOREIGN KEY (livro_id) REFERENCES livros(id)
            )
        """)
        self.conn.commit()

    def cadastrar_usuario(self, nome):
        self.cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
        self.conn.commit()

    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        return self.cursor.fetchall()

    def cadastrar_autor(self, nome):
        self.cursor.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
        self.conn.commit()

    def listar_autores(self):
        self.cursor.execute("SELECT * FROM autores")
        return self.cursor.fetchall()

    def cadastrar_editora(self, nome):
        self.cursor.execute("INSERT INTO editoras (nome) VALUES (?)", (nome,))
        self.conn.commit()

    def listar_editoras(self):
        self.cursor.execute("SELECT * FROM editoras")
        return self.cursor.fetchall()

    def cadastrar_livro(self, titulo, autor_id, editora_id, ano, edicao, disponivel):
        self.cursor.execute("""
            INSERT INTO livros (titulo, autor_id, editora_id, ano_publicacao, edicao, disponivel)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titulo, autor_id, editora_id, ano, edicao, disponivel))
        self.conn.commit()

    def listar_livros(self):
        self.cursor.execute("SELECT * FROM livros")
        return self.cursor.fetchall()

    def cadastrar_emprestimo(self, usuario_id, data):
        self.cursor.execute("INSERT INTO emprestimos (usuario_id, data) VALUES (?, ?)", (usuario_id, data))
        self.conn.commit()
        return self.cursor.lastrowid

    def listar_emprestimos(self):
        self.cursor.execute("SELECT * FROM emprestimos")
        return self.cursor.fetchall()

    def cadastrar_emprestimo_livro(self, emprestimo_id, livro_id, data_devolucao):
        self.cursor.execute("""
            INSERT INTO emprestimos_livros (emprestimo_id, livro_id, data_devolucao)
            VALUES (?, ?, ?)
        """, (emprestimo_id, livro_id, data_devolucao))
        self.conn.commit()

    def listar_emprestimos_livros(self):
        self.cursor.execute("SELECT * FROM emprestimos_livros")
        return self.cursor.fetchall()

    def fechar_conexao(self):
        self.conn.close()

def menu():
    db = BibliotecaDB()
    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Cadastrar Autor")
        print("4. Listar Autores")
        print("5. Cadastrar Editora")
        print("6. Listar Editoras")
        print("7. Cadastrar Livro")
        print("8. Listar Livros")
        print("9. Cadastrar Empréstimo")
        print("10. Listar Empréstimos")
        print("11. Cadastrar Livro em Empréstimo")
        print("12. Listar Livros Emprestados")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do usuário: ")
            db.cadastrar_usuario(nome)
            print("Usuário cadastrado!")
        elif opcao == "2":
            print("\n--- Usuários ---")
            for r in db.listar_usuarios(): print(f"ID: {r[0]} | Nome: {r[1]}")
        elif opcao == "3":
            nome = input("Nome do autor: ")
            db.cadastrar_autor(nome)
            print("Autor cadastrado!")
        elif opcao == "4":
            print("\n--- Autores ---")
            for r in db.listar_autores(): print(f"ID: {r[0]} | Nome: {r[1]}")
        elif opcao == "5":
            nome = input("Nome da editora: ")
            db.cadastrar_editora(nome)
            print("Editora cadastrada!")
        elif opcao == "6":
            print("\n--- Editoras ---")
            for r in db.listar_editoras(): print(f"ID: {r[0]} | Nome: {r[1]}")
        elif opcao == "7":
            titulo = input("Título do livro: ")
            autor_id = int(input("ID do Autor: "))
            editora_id = int(input("ID da Editora: "))
            ano = int(input("Ano de publicação: "))
            edicao = input("Edição: ")
            disponivel = int(input("Disponível (1-Sim, 0-Não): "))
            db.cadastrar_livro(titulo, autor_id, editora_id, ano, edicao, disponivel)
            print("Livro cadastrado!")
        elif opcao == "8":
            print("\n--- Livros ---")
            for r in db.listar_livros(): print(f"ID: {r[0]} | Título: {r[1]} | Autor ID: {r[2]} | Editora ID: {r[3]} | Ano: {r[4]} | Edição: {r[5]} | Disp: {r[6]}")
        elif opcao == "9":
            u_id = int(input("ID do Usuário: "))
            data = input("Data (DD/MM/AAAA): ")
            emp_id = db.cadastrar_emprestimo(u_id, data)
            print(f"Empréstimo registrado com ID: {emp_id}")
        elif opcao == "10":
            print("\n--- Empréstimos ---")
            for r in db.listar_emprestimos(): print(f"ID Empréstimo: {r[0]} | Usuário ID: {r[1]} | Data: {r[2]}")
        elif opcao == "11":
            emp_id = int(input("ID do Empréstimo: "))
            livro_id = int(input("ID do Livro: "))
            data_dev = input("Data de devolução (DD/MM/AAAA): ")
            db.cadastrar_emprestimo_livro(emp_id, livro_id, data_dev)
            print("Livro vinculado ao empréstimo!")
        elif opcao == "12":
            print("\n--- Livros Emprestados ---")
            for r in db.listar_emprestimos_livros(): print(f"ID Empréstimo: {r[0]} | Livro ID: {r[1]} | Devolução: {r[2]}")
        elif opcao == "0":
            db.fechar_conexao()
            print("Encerrando...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
