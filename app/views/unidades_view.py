import flet as ft
from models.unidade_model import listar_unidades
from services.theme_service import get_theme_colors

def unidades_view(page: ft.Page):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    unidades = listar_unidades()
    lista_unidades = ft.Ref[ft.ListView]()
    campo_busca = ft.Ref[ft.TextField]()

    def atualizar_lista(e=None):
        termo = campo_busca.current.value.strip().lower()
        filtradas = [
            u for u in unidades
            if termo in u["nome"].lower() or termo in u.get("tag", "").lower()
        ]
        lista_unidades.current.controls = [linha_unidade(u) for u in filtradas]
        page.update()

    def linha_unidade(u):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            border=ft.border.only(bottom=ft.BorderSide(1, tema["borda"])),
            content=ft.Row([
                ft.Text(u["nome"], expand=3),
                ft.Text(u["tag"], expand=2),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.EDIT,
                        tooltip="Editar",
                        icon_color=tema["texto"],
                        on_click=lambda _: page.go(f"/editar-unidade?id={u['id']}")
                    )
                ], expand=1)
            ], spacing=20)
        )

    def recarregar():
        nonlocal unidades
        unidades = listar_unidades()
        atualizar_lista()

    return ft.Column([
        ft.Text("📁 Unidades", size=28, color=tema["texto"]),
        ft.Divider(),
        ft.Row([
            ft.TextField(
                ref=campo_busca,
                on_change=atualizar_lista,
                label="Buscar por nome ou tag...",
                prefix_icon=ft.icons.SEARCH,
                bgcolor=tema["menu_bg"],
                border_color=tema["borda"],
                focused_border_color=tema["primaria"],
                color=tema["texto"],
                expand=True,
                height=45
            ),
            ft.ElevatedButton(
                text="Nova",
                icon=ft.icons.ADD,
                bgcolor=tema["botao_verde"],
                color=tema["texto_botao"],
                icon_color=tema["texto_botao"],
                height=45,
                on_click=lambda _: page.go("/cadastrar-unidade")
            )
        ]),
        ft.Container(
            border_radius=10,
            border=ft.border.all(1, tema["borda"]),
            bgcolor=tema["fundo"],
            content=ft.Column([
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    bgcolor=tema["botao_menu_hover"],
                    content=ft.Row([
                        ft.Text("Nome", expand=3),
                        ft.Text("Tag", expand=2),
                        ft.Text("Ação", expand=1)
                    ], spacing=20)
                ),
                ft.Container(
                    height=550,
                    content=ft.ListView(
                        ref=lista_unidades,
                        expand=True,
                        spacing=0,
                        auto_scroll=False,
                        padding=0,
                        controls=[linha_unidade(u) for u in unidades]
                    )
                )
            ])
        )
    ])
