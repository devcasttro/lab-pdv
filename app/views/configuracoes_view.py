import flet as ft
from services.theme_service import get_theme_colors

def configuracoes_view(page: ft.Page, atualizar_interface):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    def alternar_tema_sync(e):
        page.session.set("tema_escuro", e.control.value)
        atualizar_interface()

    def ir_para(modulo):
        page.go(f"/{modulo}")

    return ft.Column(
        controls=[
            ft.Text("⚙️ Configurações", size=30, color=tema["texto"]),
            ft.Divider(),

            ft.Text("🎨 Aparência", size=18, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([
                ft.Text("🌙 Tema Escuro", expand=True, color=tema["texto"]),
                ft.Switch(
                    value=page.session.get("tema_escuro"),
                    on_change=alternar_tema_sync
                )
            ]),
            ft.Divider(),

            ft.Text("🧩 Parâmetros do Sistema", size=18, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([
                ft.ElevatedButton(
                    text="Gerenciar Categorias",
                    icon=ft.icons.CATEGORY,
                    on_click=lambda _: ir_para("categorias"),
                    bgcolor=tema["botao_menu"],
                    color=tema["texto"]
                ),
                ft.ElevatedButton(
                    text="Gerenciar Unidades",
                    icon=ft.icons.SPACE_DASHBOARD,
                    on_click=lambda _: ir_para("unidades"),
                    bgcolor=tema["botao_menu"],
                    color=tema["texto"]
                )
            ])
        ],
        spacing=20
    )
