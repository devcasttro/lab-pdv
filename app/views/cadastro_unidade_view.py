
import flet as ft
from services.theme_service import get_theme_colors
from models.unidade_model import adicionar_unidade, editar_unidade

def cadastro_unidade_view(page: ft.Page, ao_cancelar, ao_salvar, unidade: dict = None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    nome = ft.TextField(label="Nome da Unidade", expand=3, value=unidade["nome"] if unidade else "")
    tag = ft.TextField(label="Tag (Abreviação)", expand=1.5, value=unidade["tag"] if unidade else "")
    erro = ft.Text("", color=tema["botao_vermelho"], size=12)

    def validar():
        if not nome.value.strip():
            erro.value = "O nome da unidade é obrigatório."
            return False
        if not tag.value.strip():
            erro.value = "A tag é obrigatória."
            return False
        erro.value = ""
        return True

    def salvar_unidade(e):
        if not validar():
            page.update()
            return

        try:
            if unidade:
                editar_unidade(unidade["id"], nome.value, tag.value)
            else:
                adicionar_unidade(nome.value, tag.value)
            ao_salvar(e)
        except Exception as ex:
            erro.value = str(ex)
            page.update()

    return ft.Column(
        controls=[
            ft.Text("✏️ Editar Unidade" if unidade else "➕ Nova Unidade", size=30, color=tema["texto"]),
            ft.Divider(),

            ft.Text("📋 Informações da Unidade", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([nome, tag], spacing=10),

            erro,
            ft.Divider(),

            ft.Row([
                ft.ElevatedButton("💾 Salvar", bgcolor=tema["botao_verde"], color=tema["texto_botao"],
                                  on_click=salvar_unidade,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                ft.ElevatedButton("❌ Cancelar", bgcolor=tema["botao_vermelho"], color=tema["texto_botao"],
                                  on_click=ao_cancelar,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ], spacing=10)
        ],
        spacing=15
    )
