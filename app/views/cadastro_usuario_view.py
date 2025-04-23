import flet as ft
import re
from services.theme_service import get_theme_colors
from models.usuario_model import adicionar_usuario, editar_usuario

def cadastro_usuario_view(page: ft.Page, ao_cancelar, ao_salvar, usuario: dict = None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    nome = ft.TextField(label="Nome", expand=3, value=usuario["nome"] if usuario else "")
    email = ft.TextField(label="E-mail", expand=2, value=usuario.get("email", "") if usuario else "")
    login = ft.TextField(
        label="Login",
        expand=1.5,
        value=usuario["login"] if usuario else ""
    )
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, expand=1.5)
    confirmar_senha = ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True, expand=1.5)
    status = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("Ativo"),
            ft.dropdown.Option("Inativo")
        ],
        value="Ativo" if not usuario or usuario.get("status", True) else "Inativo",
        expand=1
    )
    erro = ft.Text("", color=tema["botao_vermelho"], size=12)

    def validar():
        if not nome.value.strip():
            erro.value = "O nome é obrigatório."
            return False

        if email.value.strip():
            padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(padrao_email, email.value.strip()):
                erro.value = "Informe um e-mail válido."
                return False

        if not login.value.strip():
            erro.value = "O login é obrigatório."
            return False

        if not usuario and not senha.value.strip():
            erro.value = "A senha é obrigatória no cadastro."
            return False

        if senha.value.strip() or confirmar_senha.value.strip():
            if senha.value != confirmar_senha.value:
                erro.value = "As senhas não coincidem."
                return False

        erro.value = ""
        return True

    def salvar(e):
        if not validar():
            page.update()
            return

        dados = {
            "nome": nome.value.strip(),
            "email": email.value.strip() if email.value.strip() else None,
            "login": login.value.strip().lower(),
            "senha": senha.value.strip() if senha.value else None,
            "status": 1 if status.value == "Ativo" else 0
        }

        try:
            if usuario:
                editar_usuario(usuario["id"], dados)
            else:
                adicionar_usuario(dados)
            ao_salvar(e)
        except Exception as ex:
            erro.value = str(ex)
            page.update()

    return ft.Column([
        ft.Text("✏️ Editar Usuário" if usuario else "➕ Novo Usuário", size=30, color=tema["texto"]),
        ft.Divider(),

        ft.Text("📋 Informações do Usuário", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
        ft.Row([nome], spacing=10),
        ft.Row([email, login], spacing=10),
        ft.Row([senha, confirmar_senha], spacing=10),
        ft.Row([status], spacing=10),

        erro,
        ft.Divider(),

        ft.Row([
            ft.ElevatedButton(
                text="💾 Salvar",
                bgcolor=tema["botao_verde"],
                color=tema["texto_botao"],
                height=45,
                on_click=salvar
            ),
            ft.ElevatedButton(
                text="❌ Cancelar",
                bgcolor=tema["botao_vermelho"],
                color=tema["texto_botao"],
                height=45,
                on_click=ao_cancelar
            ),
        ], spacing=10)
    ], spacing=15)