import flet as ft
from views.dashboard_view import dashboard_view
from views.produtos_view import produtos_view
from views.configuracoes_view import configuracoes_view
from views.cadastro_produto_view import cadastro_produto_view
from views.cadastro_categoria_view import cadastro_categoria_view
from views.cadastro_unidade_view import cadastro_unidade_view
from views.categorias_view import categorias_view
from views.unidades_view import unidades_view
from models.produto_model import buscar_produto_por_id
from models.categoria_model import listar_categorias
from models.unidade_model import listar_unidades

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

    if modulo == "cadastrar-categoria":
        return cadastro_categoria_view(
            page,
            ao_cancelar=lambda e: page.go("/categorias"),
            ao_salvar=lambda e: page.go("/categorias")
        )

    if modulo == "editar-categoria":
        query = page.route.split("?")
        id_categoria = None
        if len(query) > 1:
            params = query[1].split("&")
            for param in params:
                if param.startswith("id="):
                    id_categoria = param.split("=")[1]

        categoria = next((c for c in listar_categorias() if c["id"] == id_categoria), None)

        return cadastro_categoria_view(
            page,
            ao_cancelar=lambda e: page.go("/categorias"),
            ao_salvar=lambda e: page.go("/categorias"),
            categoria=categoria
        )

    if modulo == "cadastrar-unidade":
        return cadastro_unidade_view(
            page,
            ao_cancelar=lambda e: page.go("/unidades"),
            ao_salvar=lambda e: page.go("/unidades")
        )

    if modulo == "editar-unidade":
        query = page.route.split("?")
        id_unidade = None
        if len(query) > 1:
            params = query[1].split("&")
            for param in params:
                if param.startswith("id="):
                    id_unidade = param.split("=")[1]

        unidade = next((u for u in listar_unidades() if u["id"] == id_unidade), None)

        return cadastro_unidade_view(
            page,
            ao_cancelar=lambda e: page.go("/unidades"),
            ao_salvar=lambda e: page.go("/unidades"),
            unidade=unidade
        )

    if modulo == "categorias":
        return categorias_view(page)

    if modulo == "unidades":
        return unidades_view(page)

    if modulo == "configuracoes":
        return configuracoes_view(page, atualizar_interface)

    return lambda: page.add(
        ft.Text(f"Módulo '{modulo}' não implementado.", size=20, color="red")
    )
