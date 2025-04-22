import flet as ft
from services.theme_service import get_theme_colors
from models.categoria_model import adicionar_categoria, editar_categoria

def cadastro_categoria_view(page: ft.Page, ao_cancelar, ao_salvar, categoria: dict = None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    nome = ft.TextField(label="Nome da Categoria", expand=3, value=categoria["nome"] if categoria else "")
    tag = ft.TextField(label="Tag (Abreviação)", expand=1.5, value=categoria["tag"] if categoria else "")
    erro = ft.Text("", color=tema["botao_vermelho"], size=12)

    def validar():
        if not nome.value.strip():
            erro.value = "O nome da categoria é obrigatório."
            return False
        if not tag.value.strip():
            erro.value = "A tag é obrigatória."
            return False
        erro.value = ""
        return True

    def salvar_categoria(e):
        if not validar():
            page.update()
            return

        try:
            if categoria:
                editar_categoria(categoria["id"], nome.value, tag.value)
            else:
                adicionar_categoria(nome.value, tag.value)
            ao_salvar(e)
        except Exception as ex:
            erro.value = str(ex)
            page.update()

    return ft.Column(
        controls=[
            ft.Text("✏️ Editar Categoria" if categoria else "➕ Nova Categoria", size=30, color=tema["texto"]),
            ft.Divider(),

            ft.Text("📋 Informações da Categoria", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([nome, tag], spacing=10),

            erro,
            ft.Divider(),

            ft.Row([
                ft.ElevatedButton(
                    text="💾 Salvar",
                    bgcolor=tema["botao_verde"],
                    color=tema["texto_botao"],
                    height=45,
                    on_click=salvar_categoria,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                ),
                ft.ElevatedButton(
                    text="❌ Cancelar",
                    bgcolor=tema["botao_vermelho"],
                    color=tema["texto_botao"],
                    height=45,
                    on_click=ao_cancelar,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ], spacing=10)
        ],
        spacing=15
    )
