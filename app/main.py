import flet as ft
from services.theme_service import get_theme_colors

def main(page: ft.Page):
    page.title = "labPDV - Sistema de Vendas"
    page.window_resizable = True
    page.window_full_screen = True
    page.update()

    # Tema padrão: claro
    if page.client_storage.get("tema_escuro") is None:
        page.client_storage.set("tema_escuro", False)

    content_area = ft.Ref[ft.Container]()
    menu_ref = ft.Ref[ft.Container]()
    logo_ref = ft.Ref[ft.Image]()

    # Lista de módulos
    modulos = [
        ("PDV", "💰"),
        ("Produtos", "📦"),
        ("Clientes", "🛡️"),
        ("Fornecedores", "🚚"),
        ("Contas a Pagar", "📤"),
        ("Contas a Receber", "📥"),
        ("Relatórios", "📊"),
        ("Configurações", "⚙️")
    ]

    menu_refs = {}
    menu_botoes = []

    def obter_tema():
        tema_escuro = page.client_storage.get("tema_escuro")
        return get_theme_colors("escuro" if tema_escuro else "claro")

    tema = obter_tema()

    def navegar(modulo):
        for btn in menu_botoes:
            btn.bgcolor = tema["secundaria"] if menu_refs.get(modulo) == btn else tema["primaria"]
            btn.update()

        if modulo == "Configurações":
            content_area.current.content = configuracoes_view()
        else:
            content_area.current.content = ft.Text(
                f"✨ Você está no módulo: {modulo}", size=30, color=tema["texto"]
            )

        page.update()

    def criar_botao(modulo, icone):
        def navegar_modulo(e):
            navegar(modulo)

        btn = ft.Container(
            width=200,
            content=ft.TextButton(
                content=ft.Row([
                    ft.Text(f"{icone} {modulo}", text_align="left", expand=True)
                ]),
                on_click=navegar_modulo,
                style=ft.ButtonStyle(
                    padding=15,
                    shape=ft.RoundedRectangleBorder(radius=6),
                    bgcolor=tema["primaria"],
                    color=tema["texto"],
                    overlay_color=tema["secundaria"]
                )
            ),
            bgcolor=tema["primaria"],
            border_radius=8,
            padding=0
        )
        menu_refs[modulo] = btn
        menu_botoes.append(btn)
        return btn

    def configuracoes_view():
        return ft.Column([
            ft.Text("⚙️ Configurações do Sistema", size=30, color=tema["texto"]),
            ft.Divider(),
            ft.Row([
                ft.Text("🌙 Tema Escuro:", expand=True, color=tema["texto"]),
                ft.Switch(
                    value=page.client_storage.get("tema_escuro"),
                    on_change=lambda e: alternar_tema(e.control.value)
                )
            ]),
            ft.Divider(),
            ft.Text("🔒 Gerenciar permissões", color=tema["texto"]),
            ft.Text("📧 Configurar envio de e-mails", color=tema["texto"]),
            ft.Text("🌐 Integração com painel administrativo", color=tema["texto"]),
            ft.Text("🕓 Ajustar fuso horário", color=tema["texto"]),
            ft.Text("🖨️ Configurar impressora padrão", color=tema["texto"]),
        ], spacing=10)

    def alternar_tema(valor):
        page.client_storage.set("tema_escuro", valor)
        modulo_atual = None

        # Descobre qual botão está ativo
        for modulo, ref in menu_refs.items():
            if ref.bgcolor == tema["secundaria"]:
                modulo_atual = modulo
                break

        atualizar_interface()

        if modulo_atual:
            navegar(modulo_atual)


    def construir_menu():
        menu_refs.clear()
        menu_botoes.clear()

        logo = ft.Container(
            content=ft.Image(src=tema["logo"], width=100, ref=logo_ref),
            alignment=ft.alignment.center,
            padding=10
        )

        botoes = [criar_botao(modulo, icone) for modulo, icone in modulos if modulo != "Configurações"]

        # Botão de Configurações (fora do loop para ficar fixo no rodapé)
        btn_config = criar_botao("Configurações", "⚙️")

        coluna_menu = ft.Column(
            controls=[
                ft.Column(  # Parte de cima
                    controls=[
                        logo,
                        ft.Container(height=10),
                        ft.Column(controls=botoes, spacing=10, expand=True)
                    ],
                    expand=True
                ),
                btn_config  # Parte de baixo (rodapé)
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        menu_container = ft.Container(
            ref=menu_ref,
            content=coluna_menu,
            bgcolor=tema["menu_bg"],
            padding=10,
            width=200,
            border_radius=ft.border_radius.only(top_right=12, bottom_right=12)
        )

        return menu_container


    def atualizar_interface():
        nonlocal tema
        tema = obter_tema()

        novo_menu = construir_menu()

        page.controls.clear()
        page.add(
            ft.Row([
                novo_menu,
                ft.Container(
                    ref=content_area,
                    expand=True,
                    padding=30,
                    content=ft.Text("✨ Bem-vindo ao labPDV", size=30, color=tema["texto"]),
                    bgcolor=tema["fundo"]
                )
            ], expand=True)
        )

        page.theme_mode = ft.ThemeMode.DARK if page.client_storage.get("tema_escuro") else ft.ThemeMode.LIGHT
        page.update()

    # Primeira montagem
    atualizar_interface()

ft.app(target=main)
