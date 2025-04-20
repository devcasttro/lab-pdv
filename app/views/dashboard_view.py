import flet as ft
from services.theme_service import get_theme_colors


def dashboard_view(page: ft.Page):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    return ft.Column(
        controls=[
            ft.Text("📊 Bem-vindo ao Dashboard", size=30, color=tema["texto"]),
            ft.Divider(),
            ft.Text("Este painel será aprimorado com indicadores, gráficos e métricas em tempo real.", color=tema["texto_secundario"])
        ],
        spacing=20
    )
