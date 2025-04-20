import flet as ft
from models.produto_model import listar_produtos, remover_produto
from services.alert_service import exibir_alerta
from services.theme_service import get_theme_colors

def produtos_view(page: ft.Page, content_area=None, atualizar_interface=None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")
    produtos = listar_produtos()

    largura_tabela = 1220
    column_spacing = 90

    def confirmar_exclusao(produto_id, produto_nome):
        def excluir_produto(e):
            print(f"[EXCLUIR] {produto_id} - {produto_nome}")
            remover_produto(produto_id)
            page.overlay.clear()

            # 🔄 Atualiza a interface
            if content_area:
                content_area.current.content = produtos_view(page, content_area, atualizar_interface)
                page.update()
            elif atualizar_interface:
                atualizar_interface()

        def cancelar(e):
            page.overlay.clear()
            page.update()

        exibir_alerta(
            page,
            titulo="🗑️ Confirmar exclusão",
            mensagem=f"Deseja realmente excluir o produto: {produto_nome}?",
            tipo="confirmacao",
            on_confirmar=excluir_produto,
            on_cancelar=cancelar,
            texto_confirmar="Excluir",
            texto_cancelar="Cancelar"
        )

    def linha_produto(p):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            border=ft.border.only(bottom=ft.BorderSide(1, tema["borda"])),
            content=ft.Row([
                ft.Text(p.codigo_barras or "-", expand=1),
                ft.Text(p.nome, expand=2),
                ft.Text("N/D", expand=1),
                ft.Text(str(p.estoque), expand=1),
                ft.Text(f"R$ {p.preco:.2f}", expand=1),
                ft.Text(p.unidade or "-", expand=1),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        tooltip="Editar",
                        icon_color=tema["texto"],
                        on_click=lambda e: page.go(f"/editar-produto?id={p.id}")
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Excluir",
                        icon_color=tema["botao_vermelho"],
                        on_click=lambda e: confirmar_exclusao(p.id, p.nome)
                    )
                ], expand=1)
            ], spacing=20)
        )

    return ft.Column([
        ft.Container(
            content=ft.Card(
                content=ft.Container(
                    padding=20,
                    bgcolor=tema["fundo"],
                    border_radius=15,
                    content=ft.Column([
                        ft.Row([
                            ft.Text("📦 Produtos", size=28, color=tema["texto"], expand=True),
                            ft.ElevatedButton(
                                text="Novo",
                                icon=ft.Icons.ADD,
                                bgcolor=tema["botao_verde"],
                                color=tema["texto_botao"],
                                icon_color=tema["texto_botao"],
                                on_click=lambda _: page.go("/cadastrar-produto"),
                                height=45,
                                width=100
                            )
                        ]),
                        ft.Divider(),
                        ft.TextField(
                            label="Pesquisar por nome ou código...",
                            prefix_icon=ft.Icons.SEARCH,
                            bgcolor=tema["menu_bg"],
                            border_color=tema["borda"],
                            focused_border_color=tema["primaria"],
                            color=tema["texto"],
                            height=50,
                        ),
                        ft.Container(
                            expand=True,
                            border_radius=10,
                            border=ft.border.all(1, tema["borda"]),
                            bgcolor=tema["fundo"],
                            content=ft.Column([
                                # Cabeçalho
                                ft.Container(
                                    width=largura_tabela,
                                    bgcolor=tema["botao_menu_hover"],
                                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                    content=ft.Row([
                                        ft.Text("Código de Barras", expand=1),
                                        ft.Text("Nome", expand=2),
                                        ft.Text("Categoria", expand=1),
                                        ft.Text("Estoque", expand=1),
                                        ft.Text("Preço", expand=1),
                                        ft.Text("Unidade", expand=1),
                                        ft.Text("Ação", expand=1),
                                    ], spacing=20)
                                ),
                                # Lista de produtos
                                ft.Container(
                                    height=480,
                                    width=largura_tabela,
                                    content=ft.ListView(
                                        expand=True,
                                        spacing=0,
                                        padding=0,
                                        auto_scroll=False,
                                        controls=[linha_produto(p) for p in produtos]
                                    )
                                )
                            ])
                        )
                    ], spacing=10)
                )
            ),
            expand=True
        )
    ])
