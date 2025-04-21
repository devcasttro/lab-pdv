import flet as ft
from services.theme_service import get_theme_colors
from models.produto_model import adicionar_produto, editar_produto, Produto

def cadastro_produto_view(page: ft.Page, ao_cancelar, ao_salvar, produto: Produto = None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    nome = ft.TextField(label="Nome do Produto", expand=3, value=produto.nome if produto else "")
    codigo_barras = ft.TextField(label="Código de Barras", expand=1, keyboard_type=ft.KeyboardType.NUMBER,
                                 value=produto.codigo_barras if produto else "")
    preco = ft.TextField(label="Preço de Venda (R$)", expand=1.5, keyboard_type=ft.KeyboardType.NUMBER,
                         value=str(produto.preco) if produto else "")
    custo = ft.TextField(label="Custo de Aquisição (R$)", expand=1.5, keyboard_type=ft.KeyboardType.NUMBER,
                         value=str(produto.custo) if produto else "")
    categoria = ft.Dropdown(
        label="Categoria",
        options=[
            ft.dropdown.Option("Alimento"),
            ft.dropdown.Option("Bebida"),
            ft.dropdown.Option("Limpeza"),
            ft.dropdown.Option("Higiene")
        ],
        expand=2.2,
        value=produto.categoria if produto else None
    )
    unidade = ft.Dropdown(
        label="Unidade",
        options=[ft.dropdown.Option(u) for u in ["un", "kg", "lt", "m", "cx"]],
        expand=1.5,
        value=produto.unidade if produto else None
    )
    estoque = ft.TextField(label="Estoque Atual", expand=1.5, keyboard_type=ft.KeyboardType.NUMBER,
                           value=str(produto.estoque) if produto else "")
    estoque_minimo = ft.TextField(label="Estoque Mínimo", expand=1.5, keyboard_type=ft.KeyboardType.NUMBER,
                                  value=str(produto.estoque_minimo) if produto else "")

    erro = ft.Text("", color=tema["botao_vermelho"], size=12)

    def validar_campos() -> bool:
        try:
            if not nome.value.strip():
                erro.value = "O nome do produto é obrigatório."
                return False
            if not preco.value.strip():
                erro.value = "O preço de venda é obrigatório."
                return False
            if codigo_barras.value:
                int(codigo_barras.value)
            if float(preco.value) < 0:
                erro.value = "O preço de venda não pode ser negativo."
                return False
            if custo.value and float(custo.value) < 0:
                erro.value = "O custo não pode ser negativo."
                return False
            if estoque.value and int(estoque.value) < 0:
                erro.value = "Estoque não pode ser negativo."
                return False
            if estoque_minimo.value and int(estoque_minimo.value) < 0:
                erro.value = "Estoque mínimo não pode ser negativo."
                return False
            erro.value = ""
            return True
        except ValueError:
            erro.value = "Preencha os campos numéricos corretamente."
            return False

    def salvar_produto(e):
        if not validar_campos():
            page.update()
            return

        dados = {
            "nome": nome.value,
            "codigo_barras": codigo_barras.value,
            "preco": preco.value or "0",
            "custo": custo.value or "0",
            "estoque": estoque.value or "0",
            "estoque_minimo": estoque_minimo.value or "0",
            "unidade": unidade.value or "",
            "categoria": categoria.value or ""
        }

        if produto:
            editar_produto(produto.id, dados)
        else:
            adicionar_produto(dados)

        ao_salvar(e)

    return ft.Column(
        controls=[
            ft.Text("✏️ Edição de Produto" if produto else "🆕 Cadastro de Produto", size=30, color=tema["texto"]),
            ft.Divider(),

            ft.Text("📋 Dados Básicos", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([codigo_barras, nome], spacing=10),
            ft.Row([unidade, categoria], spacing=10),

            ft.Divider(),
            ft.Text("💰 Dados Financeiros", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([preco, custo], spacing=10),

            ft.Divider(),
            ft.Text("📦 Dados de Estoque", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([estoque, estoque_minimo], spacing=10),

            erro,
            ft.Divider(),

            ft.Row([
                ft.ElevatedButton("💾 Salvar", bgcolor=tema["botao_verde"], color=tema["texto_botao"],
                                  height=45,
                                  on_click=salvar_produto,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                ft.ElevatedButton("❌ Cancelar", bgcolor=tema["botao_vermelho"], color=tema["texto_botao"],
                                  height=45,
                                  on_click=ao_cancelar,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ], spacing=10)
        ],
        spacing=15
    )
