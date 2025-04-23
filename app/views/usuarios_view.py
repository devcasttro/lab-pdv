import flet as ft
from models.usuario_model import listar_usuarios
from services.theme_service import get_theme_colors

def usuarios_view(page: ft.Page):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    lista_ref = ft.Ref[ft.ListView]()
    busca_ref = ft.Ref[ft.TextField]()
    status_ref = ft.Ref[ft.Dropdown]()

    def atualizar_lista(e=None):
        termo = busca_ref.current.value.strip().lower()
        status = status_ref.current.value
        usuarios = [u for u in listar_usuarios() if u["login"] != "suporte"]

        filtrados = []
        for u in usuarios:
            if termo in u["nome"].lower() or termo in u["login"].lower():
                if status == "Ativo" and not u["status"]:
                    continue
                elif status == "Inativo" and u["status"]:
                    continue
                filtrados.append(u)

        lista_ref.current.controls = [linha_usuario(u) for u in filtrados]
        page.update()

    def linha_usuario(u):
        cor_status = tema["botao_verde"] if u["status"] else tema["botao_vermelho"]
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            border=ft.border.only(bottom=ft.BorderSide(1, tema["borda"])),
            content=ft.Row([
                ft.Text(u["nome"], expand=2),
                ft.Text(u["email"], expand=2),
                ft.Text(u["login"], expand=1),
                ft.Text("Ativo" if u["status"] else "Inativo", expand=1, color=cor_status),
                ft.Text(u.get("ultimo_acesso", "-"), expand=1),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        tooltip="Editar",
                        icon_color=tema["texto"],
                        on_click=lambda e: page.go(f"/editar-usuario?id={u['id']}")
                    )
                ], expand=0.5)
            ], spacing=20)
        )

    def ir_para_novo():
        page.go("/cadastrar-usuario")

    view = ft.Column([
        ft.Text("👥 Usuários do Sistema", size=28, color=tema["texto"]),
        ft.Divider(),

        ft.Row([
            ft.TextField(
                ref=busca_ref,
                label="Buscar por nome ou login",
                prefix_icon=ft.Icons.SEARCH,
                on_change=atualizar_lista,
                bgcolor=tema["menu_bg"],
                border_color=tema["borda"],
                focused_border_color=tema["primaria"],
                color=tema["texto"],
                expand=True,
                height=45
            ),
            ft.Dropdown(
                ref=status_ref,
                label="Status",
                width=160,
                options=[
                    ft.dropdown.Option("Ativo"),
                    ft.dropdown.Option("Inativo"),
                    ft.dropdown.Option("Ambos")
                ],
                value="Ativo",
                on_change=atualizar_lista
            ),
            ft.ElevatedButton(
                text="Novo",
                icon=ft.Icons.ADD,
                bgcolor=tema["botao_verde"],
                color=tema["texto_botao"],
                icon_color=tema["texto_botao"],
                height=45,
                on_click=lambda _: ir_para_novo()
            )
        ], spacing=10),

        ft.Container(
            border_radius=10,
            border=ft.border.all(1, tema["borda"]),
            bgcolor=tema["fundo"],
            content=ft.Column([
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    bgcolor=tema["botao_menu_hover"],
                    content=ft.Row([
                        ft.Text("Nome", expand=2),
                        ft.Text("E-mail", expand=2),
                        ft.Text("Login", expand=1),
                        ft.Text("Status", expand=1),
                        ft.Text("Último acesso", expand=1),
                        ft.Text("Ação", expand=0.5)
                    ], spacing=20)
                ),
                ft.Container(
                    height=500,
                    content=ft.ListView(
                        ref=lista_ref,
                        expand=True,
                        spacing=0,
                        auto_scroll=False,
                        padding=0,
                        controls=[]
                    )
                )
            ])
        )
    ])

    atualizar_lista()  # Garante que os dados sejam carregados inicialmente conforme o status
    return view