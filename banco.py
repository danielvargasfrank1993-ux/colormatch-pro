import sqlite3


def conectar():
    conn = sqlite3.connect("colormatch_comercial.db")
    return conn


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de Empresas/Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            plano TEXT DEFAULT 'Gratuito'
        )
    """)

    # Tabela de Cores por Cliente
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cores_cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            id_cor TEXT,
            nome_cor TEXT,
            cb REAL DEFAULT 0,
            y25 REAL DEFAULT 0,
            v930 REAL DEFAULT 0,
            sh REAL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    conn.commit()
    conn.close()


# Inicializa o banco ao carregar
criar_tabelas()