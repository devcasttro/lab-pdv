import flet as ft
from services.theme_service import get_theme_colors


def main(page: ft.Page):
    page.title = "labPDV - Sistema de Vendas"
    page.window_resizable = True
    page.window_full_screen = True

    page.session.set("tema_escuro", False)
    page.session.set("modulo_atual", "PDV")

    content_area = ft.Ref[ft.Container]()
    menu_ref = ft.Ref[ft.Container]()
    logo_ref = ft.Ref[ft.Image]()

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
        return get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    def navegar(modulo):
        tema = obter_tema()
        page.session.set("modulo_atual", modulo)

        for btn in menu_botoes:
            btn.bgcolor = tema["botao_menu_hover"] if menu_refs.get(modulo) == btn else tema["botao_menu"]
            btn.update()

        if modulo == "Configurações":
            content_area.current.content = configuracoes_view()
        else:
            content_area.current.content = ft.Text(
                f"✨ Você está no módulo: {modulo}",
                size=30,
                color=tema["texto"]
            )
        page.update()

    def criar_botao(modulo, icone):
        tema = obter_tema()
        botao = ft.Container(
            content=ft.TextButton(
                content=ft.Row([ft.Text(f"{icone} {modulo}", expand=True)]),
                style=ft.ButtonStyle(
                    padding=15,
                    bgcolor=tema["botao_menu"],
                    color=tema["texto"],
                    overlay_color=tema["botao_menu_hover"],
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                on_click=lambda e: navegar(modulo),
            ),
            bgcolor=tema["botao_menu"],
            border_radius=8
        )
        menu_refs[modulo] = botao
        menu_botoes.append(botao)
        return botao

    def configuracoes_view():
        tema = obter_tema()

        def alternar_tema(e):
            page.session.set("tema_escuro", e.control.value)
            atualizar_interface()

        def voltar_inicio(e=None):
            navegar("PDV")

        return ft.Column([
            ft.Row([
                ft.Text("⚙️ Configurações", size=30, color=tema["texto"], expand=True),
                ft.ElevatedButton(
                    "🏠 Voltar ao Início",
                    on_click=voltar_inicio,
                    bgcolor=tema["botao_comum"],
                    color=tema["texto"]
                )
            ]),
            ft.Divider(),
            ft.Row([
                ft.Text("🌙 Tema Escuro:", expand=True, color=tema["texto"]),
                ft.Switch(
                    value=page.session.get("tema_escuro"),
                    on_change=alternar_tema
                )
            ])
        ], spacing=10)

    def atualizar_interface():
        tema = obter_tema()
        menu_refs.clear()
        menu_botoes.clear()

        menu = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(src=tema["logo"], ref=logo_ref, width=100),
                    alignment=ft.alignment.center,
                    padding=10
                ),
                ft.Container(height=10),
                ft.Column([criar_botao(mod, ico) for mod, ico in modulos[:-1]], spacing=10),
                criar_botao(modulos[-1][0], modulos[-1][1])
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )

        page.controls.clear()
        page.add(
            ft.Row([
                ft.Container(
                    ref=menu_ref,
                    content=ft.Container(
                        content=menu,
                        bgcolor=tema["menu_bg"],
                        padding=10,
                        border_radius=ft.border_radius.only(top_right=12, bottom_right=12)
                    ),
                    width=200,
                    shadow=ft.BoxShadow(blur_radius=10, spread_radius=1,
                                        color=ft.Colors.BLACK26, offset=ft.Offset(4, 0))
                ),
                ft.Container(
                    ref=content_area,
                    expand=True,
                    bgcolor=tema["fundo"],
                    padding=30
                )
            ], expand=True)
        )

        page.theme_mode = ft.ThemeMode.DARK if page.session.get("tema_escuro") else ft.ThemeMode.LIGHT
        modulo_atual = page.session.get("modulo_atual") or "PDV"
        navegar(modulo_atual)

    atualizar_interface()


ft.app(target=main)
