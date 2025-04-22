import uuid
from datetime import datetime
from database.connection import conectar
from typing import List, Optional

def listar_unidades(ativas: bool = True) -> List[dict]:
    conn = conectar()
    cursor = conn.cursor()
    if ativas:
        cursor.execute("SELECT * FROM unidades WHERE ativo = 1 ORDER BY LOWER(nome) ASC")
    else:
        cursor.execute("SELECT * FROM unidades ORDER BY nome ASC")
    colunas = [col[0] for col in cursor.description]
    unidades = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return unidades

def adicionar_unidade(nome, tag):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM unidades WHERE LOWER(nome) = LOWER(?)", (nome,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise Exception("Unidade já existente")
    id_unidade = str(uuid.uuid4())
    agora = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO unidades (id, nome, tag, ativo, criado_em, atualizado_em)
        VALUES (?, ?, ?, 1, ?, ?)
    """, (id_unidade, nome.strip(), tag.strip(), agora, agora))
    conn.commit()
    conn.close()
    return id_unidade

def editar_unidade(id_unidade, novo_nome, novo_tag):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE unidades SET nome = ?, tag = ?, atualizado_em = ?
        WHERE id = ?
    """, (novo_nome.strip(), novo_tag.strip(), datetime.now().isoformat(), id_unidade))
    conn.commit()
    conn.close()

def desativar_unidade(id_unidade):
    from models.produto_model import listar_produtos
    produtos = listar_produtos()
    for p in produtos:
        if p["unidade"] == id_unidade or p["unidade"] == p["unidade"]:  # fallback textual
            raise Exception("Não é possível desativar: unidade em uso")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE unidades SET ativo = 0, atualizado_em = ? WHERE id = ?
    """, (datetime.now().isoformat(), id_unidade))
    conn.commit()
    conn.close()

def reativar_unidade(id_unidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE unidades SET ativo = 1, atualizado_em = ? WHERE id = ?
    """, (datetime.now().isoformat(), id_unidade))
    conn.commit()
    conn.close()
