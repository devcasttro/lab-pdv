import flet as ft
from services.theme_service import get_theme_colors
from models.motivo_model import adicionar_motivo, editar_motivo, buscar_motivo_por_id

def cadastro_motivo_view(page: ft.Page, ao_cancelar, ao_salvar, motivo: dict = None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    nome = ft.TextField(label="Nome do Motivo", expand=3, value=motivo["nome"] if motivo else "")
    erro = ft.Text("", color=tema["botao_vermelho"], size=12)

    def validar():
        if not nome.value.strip():
            erro.value = "O nome do motivo é obrigatório."
            return False
        erro.value = ""
        return True

    def salvar_motivo(e):
        if not validar():
            page.update()
            return

        try:
            if motivo:
                editar_motivo(motivo["id"], nome.value)
            else:
                adicionar_motivo(nome.value)
            ao_salvar(e)
        except Exception as ex:
            erro.value = str(ex)
            page.update()

    return ft.Column(
        controls=[
            ft.Text("✏️ Editar Motivo" if motivo else "➕ Novo Motivo", size=30, color=tema["texto"]),
            ft.Divider(),

            ft.Text("📋 Informações do Motivo", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
            ft.Row([nome], spacing=10),

            erro,
            ft.Divider(),

            ft.Row([
                ft.ElevatedButton(
                    text="💾 Salvar",
                    bgcolor=tema["botao_verde"],
                    color=tema["texto_botao"],
                    height=45,
                    on_click=salvar_motivo,
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
