import flet as ft
from services.theme_service import get_theme_colors
from routers.router import carregar_modulo

def main(page: ft.Page):
    page.title = "labPDV - Sistema de Vendas"
    page.window_resizable = True
    page.window_full_screen = True

    page.session.set("tema_escuro", False)
    page.session.set("modulo_atual", "dashboard")

    content_area = ft.Ref[ft.Container]()
    page.content_area = content_area

    menu_ref = ft.Ref[ft.Container]()
    logo_ref = ft.Ref[ft.Image]()

    modulos = [
        ("dashboard", "📊"),
        ("pdv", "🖥️"),
        ("produtos", "📦"),
        ("estoque", "🏷️"),
        ("clientes", "👤"),
        ("fornecedores", "🚚"),
        ("contas-pagar", "📤"),
        ("contas-receber", "📥"),
        ("relatorios", "📊"),
        ("configuracoes", "⚙️")
    ]

    rota_para_modulo = {f"/{mod}": mod for mod, _ in modulos}
    rota_para_modulo["/cadastrar-produto"] = "cadastrar-produto"
    rota_para_modulo["/editar-produto"] = "editar-produto"
    rota_para_modulo["/categorias"] = "categorias"
    rota_para_modulo["/unidades"] = "unidades"
    rota_para_modulo["/cadastrar-categoria"] = "cadastrar-categoria"
    rota_para_modulo["/editar-categoria"] = "editar-categoria"
    rota_para_modulo["/cadastrar-unidade"] = "cadastrar-unidade"      
    rota_para_modulo["/editar-unidade"] = "editar-unidade"         
    rota_para_modulo["/motivos"] = "motivos"
    rota_para_modulo["/cadastrar-motivo"] = "cadastrar-motivo"
    rota_para_modulo["/editar-motivo"] = "editar-motivo"

    menu_refs = {}
    menu_botoes = []

    def obter_tema():
        return get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    def navegar(modulo):
        print(f"[main] Navegando para módulo: {modulo}")
        tema = obter_tema()
        modulo_atual = page.session.get("modulo_atual")

        if modulo == modulo_atual and content_area.current.content:
            content_area.current.content = None
            page.update()

        page.session.set("modulo_atual", modulo)

        for btn in menu_botoes:
            btn.bgcolor = tema["botao_menu_hover"] if menu_refs.get(modulo) == btn else tema["botao_menu"]
            btn.update()

        content_area.current.content = carregar_modulo(modulo, page, atualizar_interface)
        page.update()

    def criar_botao(modulo, icone):
        tema = obter_tema()
        nome_formatado = (
            "PDV" if modulo == "pdv"
            else "Configurações" if modulo == "configuracoes"
            else modulo.replace("-", " ").title()
        )

        botao = ft.Container(
            content=ft.TextButton(
                content=ft.Row([ft.Text(f"{icone} {nome_formatado}", expand=True)]),
                style=ft.ButtonStyle(
                    padding=15,
                    bgcolor=tema["botao_menu"],
                    color=tema["texto"],
                    overlay_color=tema["botao_menu_hover"],
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                on_click=lambda e: page.go(f"/{modulo}"),
            ),
            bgcolor=tema["botao_menu"],
            border_radius=8
        )
        menu_refs[modulo] = botao
        menu_botoes.append(botao)
        return botao

    def atualizar_interface():
        tema = obter_tema()
        menu_refs.clear()
        menu_botoes.clear()

        botoes_menu = [
            criar_botao(mod, ico)
            for mod, ico in modulos[:-1]
        ]
        botao_configuracoes = criar_botao(modulos[-1][0], modulos[-1][1])

        menu = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(src=tema["logo"], ref=logo_ref, width=100),
                    alignment=ft.alignment.center,
                    padding=10
                ),
                ft.Column(botoes_menu, spacing=10),
                ft.Container(
                    content=botao_configuracoes,
                    alignment=ft.alignment.bottom_center
                )
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
        modulo_atual = page.session.get("modulo_atual") or "dashboard"
        navegar(modulo_atual)

    def route_change(route):
        rota_completa = route.route.lower()
        rota_base = rota_completa.split("?")[0]
        print(f"[main] route_change: {rota_completa} → base: {rota_base}")
        modulo = rota_para_modulo.get(rota_base, "dashboard")
        navegar(modulo)

    page.on_route_change = route_change
    atualizar_interface()
    page.go("/dashboard")

ft.app(target=main)
