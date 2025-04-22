from .connection import conectar
from datetime import datetime
import uuid

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # -----------------------
    # Tabela: produtos
    # -----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        codigo_barras TEXT,
        preco REAL NOT NULL,
        custo REAL NOT NULL,
        margem_lucro REAL NOT NULL,
        estoque INTEGER NOT NULL,
        estoque_minimo INTEGER NOT NULL,
        unidade TEXT,
        categoria TEXT,
        imagem_path TEXT,
        ativo INTEGER DEFAULT 1,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------
    # Tabela: categorias
    # -----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE,
        tag TEXT,
        ativo INTEGER DEFAULT 1,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Inserção inicial (apenas se vazio)
    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        categorias_iniciais = [
            ("Alimento", "ALIM"),
            ("Bebida", "BEB"),
            ("Limpeza", "LIMP"),
            ("Higiene", "HIG")
        ]
        for nome, tag in categorias_iniciais:
            cursor.execute("""
                INSERT INTO categorias (id, nome, tag, ativo, criado_em, atualizado_em)
                VALUES (?, ?, ?, 1, ?, ?)
            """, (str(uuid.uuid4()), nome, tag, datetime.now().isoformat(), datetime.now().isoformat()))

    # -----------------------
    # Tabela: unidades
    # -----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS unidades (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE,
        tag TEXT NOT NULL,
        ativo INTEGER DEFAULT 1,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Inserção inicial (apenas se vazio)
    cursor.execute("SELECT COUNT(*) FROM unidades")
    if cursor.fetchone()[0] == 0:
        unidades_iniciais = [
            ("Unidade", "UN"),
            ("Quilograma", "KG"),
            ("Litro", "L"),
            ("Metro", "M"),
            ("Caixa", "CX")
        ]
        for nome, tag in unidades_iniciais:
            cursor.execute("""
                INSERT INTO unidades (id, nome, tag, ativo, criado_em, atualizado_em)
                VALUES (?, ?, ?, 1, ?, ?)
            """, (str(uuid.uuid4()), nome, tag, datetime.now().isoformat(), datetime.now().isoformat()))

    conn.commit()
    conn.close()
