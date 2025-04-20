import flet as ft
from services.theme_service import get_theme_colors

def dashboard_view(page):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")
    return ft.Column([
        ft.Text("📊 Bem-vindo ao dashboard", size=30, color=tema["texto"])
    ])
