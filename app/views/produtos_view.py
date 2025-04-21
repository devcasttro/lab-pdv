import flet as ft
from models.produto_model import listar_produtos, remover_produto
from services.alert_service import exibir_alerta
from services.theme_service import get_theme_colors
from services.search_service import filtrar_lista

def produtos_view(page: ft.Page, content_area=None, atualizar_interface=None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")
    produtos_todos = listar_produtos()

    largura_tabela = 1220

    campo_busca = ft.Ref[ft.TextField]()
    filtro_categoria = ft.Ref[ft.Dropdown]()
    filtro_unidade = ft.Ref[ft.Dropdown]()
    filtro_preco_min = ft.Ref[ft.TextField]()
    filtro_preco_max = ft.Ref[ft.TextField]()
    lista_produtos = ft.Ref[ft.ListView]()

    def atualizar_lista(e=None):
        termo = campo_busca.current.value.strip()
        categoria = filtro_categoria.current.value
        unidade = filtro_unidade.current.value
        preco_min = filtro_preco_min.current.value.strip()
        preco_max = filtro_preco_max.current.value.strip()

        print(f"🔍 Termo: {termo}, Categoria: {categoria}, Unidade: {unidade}, Preço Min: {preco_min}, Max: {preco_max}")

        filtrados = filtrar_lista(produtos_todos, termo, campos=["nome", "codigo_barras"])

        if categoria:
            filtrados = [p for p in filtrados if getattr(p, "categoria", None) == categoria]
        if unidade:
            filtrados = [p for p in filtrados if p.unidade == unidade]
        if preco_min:
            try:
                min_val = float(preco_min)
                filtrados = [p for p in filtrados if p.preco >= min_val]
            except ValueError:
                pass
        if preco_max:
            try:
                max_val = float(preco_max)
                filtrados = [p for p in filtrados if p.preco <= max_val]
            except ValueError:
                pass

        lista_produtos.current.controls = [linha_produto(p) for p in filtrados]
        page.update()

    import uuid

    def limpar_filtros(e=None):
        campo_busca.current.value = ""
        filtro_categoria.current.value = None
        filtro_categoria.current.key = str(uuid.uuid4())  # força reconstrução
        filtro_categoria.current.update()

        filtro_unidade.current.value = None
        filtro_unidade.current.key = str(uuid.uuid4())  # força reconstrução
        filtro_unidade.current.update()

        filtro_preco_min.current.value = ""
        filtro_preco_max.current.value = ""
        atualizar_lista()


    def confirmar_exclusao(produto_id, produto_nome):
        def excluir_produto(e):
            remover_produto(produto_id)
            page.overlay.clear()
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
                ft.Text(getattr(p, "categoria", "N/D"), expand=1),
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
                            ref=campo_busca,
                            on_change=atualizar_lista,
                            label="Pesquisar por nome ou código...",
                            prefix_icon=ft.Icons.SEARCH,
                            bgcolor=tema["menu_bg"],
                            border_color=tema["borda"],
                            focused_border_color=tema["primaria"],
                            color=tema["texto"],
                            height=50,
                        ),
                        ft.Row([
                            ft.Dropdown(
                                ref=filtro_categoria,
                                label="Categoria",
                                options=[
                                    ft.dropdown.Option("Alimento"),
                                    ft.dropdown.Option("Bebida"),
                                    ft.dropdown.Option("Limpeza"),
                                    ft.dropdown.Option("Higiene")
                                ],
                                on_change=atualizar_lista,
                                width=200
                            ),
                            ft.Dropdown(
                                ref=filtro_unidade,
                                label="Unidade",
                                options=[ft.dropdown.Option(u) for u in ["un", "kg", "lt", "m", "cx"]],
                                on_change=atualizar_lista,
                                width=150
                            ),
                            ft.TextField(
                                ref=filtro_preco_min,
                                label="Preço Mínimo",
                                width=140,
                                height=45,
                                on_change=atualizar_lista
                            ),
                            ft.TextField(
                                ref=filtro_preco_max,
                                label="Preço Máximo",
                                width=140,
                                height=45,
                                on_change=atualizar_lista
                            ),
                            ft.Container(
                                expand=True,
                                alignment=ft.alignment.center_right,
                                content=ft.ElevatedButton(
                                    text="Limpar Filtros",
                                    icon=ft.Icons.CLEAR_ALL,
                                    icon_color=tema["texto_botao"],
                                    on_click=limpar_filtros,
                                    bgcolor=tema["botao_vermelho"],
                                    color=tema["texto_botao"],
                                    height=45
                                )
                            )
                        ], spacing=10),
                        ft.Container(
                            expand=True,
                            border_radius=10,
                            border=ft.border.all(1, tema["borda"]),
                            bgcolor=tema["fundo"],
                            content=ft.Column([
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
                                ft.Container(
                                    height=480,
                                    width=largura_tabela,
                                    content=ft.ListView(
                                        ref=lista_produtos,
                                        expand=True,
                                        spacing=0,
                                        padding=0,
                                        auto_scroll=False,
                                        controls=[linha_produto(p) for p in produtos_todos]
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
