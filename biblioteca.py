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