import flet as ft
from models.motivo_model import listar_motivos
from services.theme_service import get_theme_colors

def motivos_view(page: ft.Page):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    motivos = listar_motivos(ativos_apenas=False)
    lista_motivos = ft.Ref[ft.ListView]()
    campo_busca = ft.Ref[ft.TextField]()

    def atualizar_lista(e=None):
        termo = campo_busca.current.value.strip().lower()
        filtrados = [
            m for m in motivos
            if termo in m["nome"].lower()
        ]
        lista_motivos.current.controls = [linha_motivo(m) for m in filtrados]
        page.update()

    def linha_motivo(m):
        status_text = "Ativo" if m["status"] else "Inativo"
        status_cor = tema["botao_verde"] if m["status"] else tema["botao_vermelho"]

        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            border=ft.border.only(bottom=ft.BorderSide(1, tema["borda"])),
            content=ft.Row([
                ft.Text(m["nome"], expand=4),
                ft.Text(status_text, color=status_cor, expand=2),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.EDIT,
                        tooltip="Editar",
                        icon_color=tema["texto"],
                        on_click=lambda _: page.go(f"/editar-motivo?id={m['id']}")
                    )
                ], expand=1)
            ], spacing=20)
        )

    def recarregar():
        nonlocal motivos
        motivos = listar_motivos(ativos_apenas=False)
        atualizar_lista()

    return ft.Column([
        ft.Text("⚙️ Motivos de Movimentação", size=28, color=tema["texto"]),
        ft.Divider(),
        ft.Row([
            ft.TextField(
                ref=campo_busca,
                on_change=atualizar_lista,
                label="Buscar por nome...",
                prefix_icon=ft.icons.SEARCH,
                bgcolor=tema["menu_bg"],
                border_color=tema["borda"],
                focused_border_color=tema["primaria"],
                color=tema["texto"],
                expand=True,
                height=45
            ),
            ft.ElevatedButton(
                text="Novo",
                icon=ft.icons.ADD,
                bgcolor=tema["botao_verde"],
                color=tema["texto_botao"],
                icon_color=tema["texto_botao"],
                height=45,
                on_click=lambda _: page.go("/cadastrar-motivo")
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
                        ft.Text("Nome", expand=4),
                        ft.Text("Status", expand=2),
                        ft.Text("Ação", expand=1)
                    ], spacing=20)
                ),
                ft.Container(
                    height=550,
                    content=ft.ListView(
                        ref=lista_motivos,
                        expand=True,
                        spacing=0,
                        auto_scroll=False,
                        padding=0,
                        controls=[linha_motivo(m) for m in motivos]
                    )
                )
            ])
        )
    ])
