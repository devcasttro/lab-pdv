import flet as ft
from services.theme_service import get_theme_colors

def configuracoes_view(page, atualizar_interface):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    def alternar_tema_sync(e):
        page.session.set("tema_escuro", e.control.value)
        atualizar_interface()

    return ft.Column([
        ft.Text("⚙️ Configurações", size=30, color=tema["texto"]),
        ft.Divider(),
        ft.Row([
            ft.Text("🌙 Tema Escuro:", expand=True, color=tema["texto"]),
            ft.Switch(
                value=page.session.get("tema_escuro"),
                on_change=alternar_tema_sync
            )
        ])
    ], spacing=10)
