import sqlite3
from datetime import datetime
from typing import List, Optional

from database.connection import conectar


def criar_tabela_motivos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motivos_movimentacao (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            status INTEGER DEFAULT 1,
            criado_em TEXT,
            atualizado_em TEXT
        )
    ''')
    conn.commit()
    conn.close()


def listar_motivos(ativos_apenas=True) -> List[dict]:
    criar_tabela_motivos()
    conn = conectar()
    cursor = conn.cursor()
    query = "SELECT * FROM motivos_movimentacao"
    if ativos_apenas:
        query += " WHERE status = 1"
    query += " ORDER BY nome COLLATE NOCASE"
    cursor.execute(query)
    colunas = [col[0] for col in cursor.description]
    resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return resultados


def buscar_motivo_por_id(id_motivo: str) -> Optional[dict]:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM motivos_movimentacao WHERE id = ?", (id_motivo,))
    row = cursor.fetchone()
    conn.close()
    if row:
        colunas = [col[0] for col in cursor.description]
        return dict(zip(colunas, row))
    return None


def adicionar_motivo(nome: str) -> str:
    import uuid
    motivo_id = str(uuid.uuid4())
    agora = datetime.now().isoformat()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO motivos_movimentacao (id, nome, status, criado_em, atualizado_em)
        VALUES (?, ?, ?, ?, ?)
    ''', (motivo_id, nome.strip(), 1, agora, agora))
    conn.commit()
    conn.close()
    return motivo_id


def editar_motivo(id_motivo: str, novo_nome: str):
    conn = conectar()
    cursor = conn.cursor()
    agora = datetime.now().isoformat()
    cursor.execute('''
        UPDATE motivos_movimentacao SET nome = ?, atualizado_em = ? WHERE id = ?
    ''', (novo_nome.strip(), agora, id_motivo))
    conn.commit()
    conn.close()


def alterar_status_motivo(id_motivo: str, novo_status: int):
    conn = conectar()
    cursor = conn.cursor()
    agora = datetime.now().isoformat()
    cursor.execute('''
        UPDATE motivos_movimentacao SET status = ?, atualizado_em = ? WHERE id = ?
    ''', (novo_status, agora, id_motivo))
    conn.commit()
    conn.close()
