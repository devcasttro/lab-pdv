import flet as ft
from services.theme_service import get_theme_colors
from models.produto_model import adicionar_produto


def cadastro_produto_view(page: ft.Page, ao_cancelar, ao_salvar):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    # Campos do formulário
    nome = ft.TextField(label="Nome do Produto", expand=True)
    codigo_barras = ft.TextField(label="Código de Barras", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    preco = ft.TextField(label="Preço de Venda (R$)", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    custo = ft.TextField(label="Custo de Aquisição (R$)", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    estoque = ft.TextField(label="Estoque Atual", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    estoque_minimo = ft.TextField(label="Estoque Mínimo", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    unidade = ft.Dropdown(
        label="Unidade",
        options=[ft.dropdown.Option(u) for u in ["un", "kg", "lt", "m", "cx"]],
        width=200
    )

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
                int(codigo_barras.value)  # Deve ser número

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
            "unidade": unidade.value or ""
        }

        adicionar_produto(dados)
        ao_salvar(e)  # <-- agora recebe 'e'

    return ft.Column(
        controls=[
            ft.Text("🆕 Cadastro de Produto", size=30, color=tema["texto"]),
            ft.Divider(),
            ft.Row([nome]),
            ft.Row([codigo_barras]),
            ft.Row([preco, custo]),
            ft.Row([unidade, estoque, estoque_minimo]),
            erro,
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton(
                    text="💾 Salvar",
                    bgcolor=tema["botao_verde"],
                    color=tema["texto_botao"],
                    on_click=salvar_produto,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                ),
                ft.ElevatedButton(
                    text="❌ Cancelar",
                    bgcolor=tema["botao_vermelho"],
                    color=tema["texto_botao"],
                    on_click=ao_cancelar,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ], spacing=10)
        ],
        spacing=15
    )
