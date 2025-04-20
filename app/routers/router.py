import flet as ft
from views.dashboard_view import dashboard_view
from views.produtos_view import produtos_view
from views.configuracoes_view import configuracoes_view
from views.cadastro_produto_view import cadastro_produto_view
from models.produto_model import buscar_produto_por_id

def carregar_modulo(modulo, page, atualizar_interface=None):
    print(f"[router] Carregando módulo: {modulo}")

    if modulo == "dashboard":
        return dashboard_view(page)

    if modulo == "produtos":
        return produtos_view(page, page.content_area, atualizar_interface)

    if modulo == "cadastrar-produto":
        return cadastro_produto_view(
            page,
            ao_cancelar=lambda e: page.go("/produtos"),
            ao_salvar=lambda e: page.go("/produtos")
        )

    if modulo == "editar-produto":
        query = page.route.split("?")
        id_produto = None
        if len(query) > 1:
            params = query[1].split("&")
            for param in params:
                if param.startswith("id="):
                    id_produto = param.split("=")[1]

        produto = buscar_produto_por_id(id_produto) if id_produto else None

        return cadastro_produto_view(
            page,
            ao_cancelar=lambda e: page.go("/produtos"),
            ao_salvar=lambda e: page.go("/produtos"),
            produto=produto
        )

    if modulo == "configuracoes":
        return configuracoes_view(page, atualizar_interface)

    return lambda: page.add(
        ft.Text(f"Módulo '{modulo}' não implementado.", size=20, color="red")
    )
