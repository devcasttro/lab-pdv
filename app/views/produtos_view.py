import flet as ft
from services.theme_service import get_theme_colors

def produtos_view(page):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    produtos_mock = [
        {"codigo": "001", "nome": "Produto A", "estoque": 10, "preco": 19.90, "unidade": "un"},
        {"codigo": "002", "nome": "Produto B", "estoque": 5, "preco": 9.50, "unidade": "kg"},
        {"codigo": "003", "nome": "Produto C", "estoque": 0, "preco": 14.00, "unidade": "lt"},
    ]

    header = ft.Row([
        ft.Text("📦 Produtos", size=30, color=tema["texto"], expand=True),
    ])

    campo_busca = ft.TextField(
        hint_text="Buscar produto...",
        prefix_icon=ft.Icons.SEARCH,
        border_color=tema["borda"],
        border_radius=20,
        content_padding=15,
        height=45,
        expand=True
    )

    tabela = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.Text("Código", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("Produto", weight=ft.FontWeight.BOLD, expand=3),
                    ft.Text("Estoque", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("Preço (R$)", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("Un.", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("Ação", weight=ft.FontWeight.BOLD, expand=1),
                ]),
                bgcolor=tema["menu_bg"],
                padding=10,
                border_radius=5
            )
        ] + [
            ft.Container(
                content=ft.Row([
                    ft.Text(prod["codigo"], expand=1),
                    ft.Text(prod["nome"], expand=3),
                    ft.Text(str(prod["estoque"]), expand=1),
                    ft.Text(f"{prod['preco']:.2f}", expand=1),
                    ft.Text(prod["unidade"], expand=1),
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color=tema.get("botao_alarme", "#FF9100"), tooltip="Editar"),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=tema.get("botao_vermelho", "#D32F2F"), tooltip="Excluir")
                    ], expand=1)
                ]),
                padding=10,
                border=ft.border.all(1, tema.get("borda", "#CCCCCC")),
                border_radius=5
            )
            for prod in produtos_mock
        ],
        spacing=5
    )

    botao_novo = ft.Row(
        [
            ft.Container(
                content=ft.ElevatedButton(
                    icon=ft.icons.ADD,
                    text="Novo",
                    bgcolor=tema.get("botao_verde", "#00C853"),
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        padding=ft.padding.symmetric(horizontal=30, vertical=15),
                    ),
                    tooltip="Adicionar novo produto"
                ),
                alignment=ft.alignment.bottom_right,
                padding=10
            )
        ],
        alignment=ft.MainAxisAlignment.END
    )

    return ft.Column(
        controls=[
            header,
            campo_busca,
            ft.Divider(),
            tabela,
            ft.Divider(height=20, color="transparent"),
            botao_novo
        ],
        spacing=20
    )
