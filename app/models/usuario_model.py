import uuid
import hashlib
import re
from datetime import datetime
from typing import List, Optional
from database.connection import conectar
from database.schema import criar_tabelas

criar_tabelas()

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def email_valido(email: str) -> bool:
    if not email:
        return True  # permitido vazio
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def listar_usuarios(status: Optional[str] = None) -> List[dict]:
    conn = conectar()
    cursor = conn.cursor()

    base_sql = "SELECT * FROM usuarios WHERE login != 'suporte'"
    if status == "ativo":
        base_sql += " AND status = 1"
    elif status == "inativo":
        base_sql += " AND status = 0"
    base_sql += " ORDER BY nome"

    cursor.execute(base_sql)
    colunas = [col[0] for col in cursor.description]
    usuarios = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return usuarios

def buscar_usuario_por_id(id_usuario: str) -> Optional[dict]:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    row = cursor.fetchone()
    conn.close()
    if row:
        colunas = [col[0] for col in cursor.description]
        return dict(zip(colunas, row))
    return None

def adicionar_usuario(dados: dict) -> str:
    conn = conectar()
    cursor = conn.cursor()

    email = dados["email"].strip() if dados.get("email") else ""
    login = dados["login"].strip().lower()

    if not email_valido(email):
        raise Exception("E-mail inválido.")

    # Verifica duplicidade
    cursor.execute("SELECT 1 FROM usuarios WHERE (email = ? AND email != '') OR login = ?", (email, login))
    if cursor.fetchone():
        conn.close()
        raise Exception("E-mail ou login já cadastrados.")

    id_usuario = str(uuid.uuid4())
    senha_hash = hash_senha(dados["senha"])

    cursor.execute("""
        INSERT INTO usuarios (
            id, nome, email, login, senha_hash, status,
            criado_em, atualizado_em, ultimo_acesso
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_usuario,
        dados["nome"].strip(),
        email,
        login,
        senha_hash,
        1 if dados.get("status", True) else 0,
        datetime.now().isoformat(),
        datetime.now().isoformat(),
        None
    ))

    conn.commit()
    conn.close()
    return id_usuario

def editar_usuario(id_usuario: str, dados: dict) -> None:
    conn = conectar()
    cursor = conn.cursor()

    email = dados["email"].strip() if dados.get("email") else ""
    login = dados["login"].strip().lower()

    if not email_valido(email):
        raise Exception("E-mail inválido.")

    # Verifica duplicidade (exceto o próprio)
    cursor.execute("""
        SELECT 1 FROM usuarios WHERE ((email = ? AND email != '') OR login = ?) AND id != ?
    """, (email, login, id_usuario))
    if cursor.fetchone():
        conn.close()
        raise Exception("E-mail ou login já estão em uso por outro usuário.")

    senha_hash = hash_senha(dados["senha"]) if dados.get("senha") else None

    if senha_hash:
        cursor.execute("""
            UPDATE usuarios SET nome = ?, email = ?, login = ?, senha_hash = ?, status = ?, atualizado_em = ?
            WHERE id = ?
        """, (
            dados["nome"].strip(),
            email,
            login,
            senha_hash,
            1 if dados.get("status", True) else 0,
            datetime.now().isoformat(),
            id_usuario
        ))
    else:
        cursor.execute("""
            UPDATE usuarios SET nome = ?, email = ?, login = ?, status = ?, atualizado_em = ?
            WHERE id = ?
        """, (
            dados["nome"].strip(),
            email,
            login,
            1 if dados.get("status", True) else 0,
            datetime.now().isoformat(),
            id_usuario
        ))

    conn.commit()
    conn.close()