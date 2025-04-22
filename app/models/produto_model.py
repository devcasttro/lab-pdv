import uuid
from datetime import datetime
from typing import List, Optional
from database.connection import conectar
from database.schema import criar_tabelas

# Criação automática das tabelas ao iniciar o módulo
criar_tabelas()

def adicionar_produto(dados: dict) -> str:
    conn = conectar()
    cursor = conn.cursor()
    id_produto = str(uuid.uuid4())

    cursor.execute("""
        INSERT INTO produtos (
            id, nome, codigo_barras, preco, custo, margem_lucro,
            estoque, estoque_minimo, unidade, categoria,
            imagem_path, ativo, criado_em, atualizado_em
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_produto,
        dados["nome"].strip(),
        dados.get("codigo_barras", "").strip(),
        float(str(dados.get("preco", "0")).replace(",", ".")),
        float(str(dados.get("custo", "0")).replace(",", ".")),
        float(str(dados.get("margem_lucro", "0")).replace(",", ".")),
        int(dados.get("estoque", 0)),
        int(dados.get("estoque_minimo", 0)),
        dados.get("unidade", "").strip(),
        dados.get("categoria", "").strip(),
        dados.get("imagem_path", ""),
        1,
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
    return id_produto

def listar_produtos(status: str = "ativos") -> List[dict]:
    conn = conectar()
    cursor = conn.cursor()

    if status == "ativos":
        cursor.execute("SELECT * FROM produtos WHERE ativo = 1 ORDER BY LOWER(nome) ASC")
    elif status == "inativos":
        cursor.execute("SELECT * FROM produtos WHERE ativo = 0 ORDER BY LOWER(nome) ASC")
    elif status == "ambos":
        cursor.execute("SELECT * FROM produtos ORDER BY LOWER(nome) ASC")
    else:
        conn.close()
        raise ValueError("Status inválido. Use 'ativos', 'inativos' ou 'ambos'.")

    colunas = [col[0] for col in cursor.description]
    produtos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return produtos

def buscar_produto_por_id(id_produto: str) -> Optional[dict]:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
    row = cursor.fetchone()
    colunas = [col[0] for col in cursor.description]
    conn.close()
    return dict(zip(colunas, row)) if row else None

def editar_produto(id_produto: str, novos_dados: dict) -> None:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos SET
            nome = ?, codigo_barras = ?, preco = ?, custo = ?, margem_lucro = ?,
            estoque = ?, estoque_minimo = ?, unidade = ?, categoria = ?,
            imagem_path = ?, ativo = ?, atualizado_em = ?
        WHERE id = ?
    """, (
        novos_dados["nome"].strip(),
        novos_dados.get("codigo_barras", "").strip(),
        float(str(novos_dados.get("preco", "0")).replace(",", ".")),
        float(str(novos_dados.get("custo", "0")).replace(",", ".")),
        float(str(novos_dados.get("margem_lucro", "0")).replace(",", ".")),
        int(novos_dados.get("estoque", 0)),
        int(novos_dados.get("estoque_minimo", 0)),
        novos_dados.get("unidade", "").strip(),
        novos_dados.get("categoria", "").strip(),
        novos_dados.get("imagem_path", ""),
        int(novos_dados.get("ativo", 1)),  # 🔥 Agora o campo ativo é atualizado!
        datetime.now().isoformat(),
        id_produto
    ))
    conn.commit()
    conn.close()

def remover_produto(id_produto: str) -> None:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produtos SET ativo = 0, atualizado_em = ? WHERE id = ?",
        (datetime.now().isoformat(), id_produto)
    )
    conn.commit()
    conn.close()

def reativar_produto(id_produto: str) -> None:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produtos SET ativo = 1, atualizado_em = ? WHERE id = ?",
        (datetime.now().isoformat(), id_produto)
    )
    conn.commit()
    conn.close()
