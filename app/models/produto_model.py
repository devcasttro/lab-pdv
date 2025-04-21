from dataclasses import dataclass
from typing import List, Optional
import uuid

# Base de dados em memória (temporária)
produtos_memoria: List["Produto"] = []

@dataclass
class Produto:
    id: str
    nome: str
    codigo_barras: str
    preco: float
    custo: float
    estoque: int
    estoque_minimo: int
    unidade: str
    categoria: str  # NOVO

def adicionar_produto(dados: dict) -> Produto:
    novo_produto = Produto(
        id=str(uuid.uuid4()),
        nome=dados["nome"].strip(),
        codigo_barras=dados.get("codigo_barras", "").strip(),
        preco=float(dados.get("preco", 0)),
        custo=float(dados.get("custo", 0)),
        estoque=int(dados.get("estoque", 0)),
        estoque_minimo=int(dados.get("estoque_minimo", 0)),
        unidade=dados.get("unidade", "").strip(),
        categoria=dados.get("categoria", "").strip()
    )
    produtos_memoria.append(novo_produto)
    return novo_produto

def listar_produtos() -> List[Produto]:
    return produtos_memoria.copy()

def remover_produto(id_produto: str) -> None:
    global produtos_memoria
    produtos_memoria = [p for p in produtos_memoria if p.id != id_produto]

def editar_produto(id_produto: str, novos_dados: dict) -> None:
    for produto in produtos_memoria:
        if produto.id == id_produto:
            produto.nome = novos_dados.get("nome", produto.nome).strip()
            produto.codigo_barras = novos_dados.get("codigo_barras", produto.codigo_barras).strip()
            produto.preco = float(novos_dados.get("preco", produto.preco))
            produto.custo = float(novos_dados.get("custo", produto.custo))
            produto.estoque = int(novos_dados.get("estoque", produto.estoque))
            produto.estoque_minimo = int(novos_dados.get("estoque_minimo", produto.estoque_minimo))
            produto.unidade = novos_dados.get("unidade", produto.unidade).strip()
            produto.categoria = novos_dados.get("categoria", produto.categoria).strip()
            break

def buscar_produto_por_id(id_produto: str) -> Optional[Produto]:
    for p in produtos_memoria:
        if p.id == id_produto:
            return p
    return None
