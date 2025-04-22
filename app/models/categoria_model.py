import uuid
from datetime import datetime
from database.connection import conectar
from typing import List, Optional

def listar_categorias(ativas: bool = True) -> List[dict]:
    conn = conectar()
    cursor = conn.cursor()
    if ativas:
        cursor.execute("SELECT * FROM categorias WHERE ativo = 1 ORDER BY LOWER(nome) ASC")
    else:
        cursor.execute("SELECT * FROM categorias ORDER BY nome ASC")
    colunas = [col[0] for col in cursor.description]
    categorias = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return categorias

def adicionar_categoria(nome, tag):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM categorias WHERE LOWER(nome) = LOWER(?)", (nome,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise Exception("Categoria já existente")
    id_categoria = str(uuid.uuid4())
    agora = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO categorias (id, nome, tag, ativo, criado_em, atualizado_em)
        VALUES (?, ?, ?, 1, ?, ?)
    """, (id_categoria, nome.strip(), tag.strip(), agora, agora))
    conn.commit()
    conn.close()
    return id_categoria

def editar_categoria(id_categoria, novo_nome, novo_tag):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE categorias SET nome = ?, tag = ?, atualizado_em = ?
        WHERE id = ?
    """, (novo_nome.strip(), novo_tag.strip(), datetime.now().isoformat(), id_categoria))
    conn.commit()
    conn.close()

def desativar_categoria(id_categoria):
    from models.produto_model import listar_produtos
    produtos = listar_produtos()
    for p in produtos:
        if p["categoria"] == id_categoria or p["categoria"] == p["categoria"]:  # fallback textual
            raise Exception("Não é possível desativar: categoria em uso")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE categorias SET ativo = 0, atualizado_em = ? WHERE id = ?
    """, (datetime.now().isoformat(), id_categoria))
    conn.commit()
    conn.close()

def reativar_categoria(id_categoria):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE categorias SET ativo = 1, atualizado_em = ? WHERE id = ?
    """, (datetime.now().isoformat(), id_categoria))
    conn.commit()
    conn.close()
