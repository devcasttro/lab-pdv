from views.dashboard_view import dashboard_view
from views.produtos_view import produtos_view
from views.configuracoes_view import configuracoes_view
from views.cadastro_produto_view import cadastro_produto_view

def carregar_modulo(modulo, page, atualizar_interface=None):
    print(f"[router] Carregando módulo: {modulo}")
    if modulo == "dashboard":
        return dashboard_view(page)
    if modulo == "produtos":
        return produtos_view(page)
    if modulo == "cadastrar-produto":
        return cadastro_produto_view(
            page,
            ao_cancelar=lambda e: page.go("/produtos"),
            ao_salvar=lambda e: page.go("/produtos")
        )
    if modulo == "configuracoes":
        return configuracoes_view(page, atualizar_interface)

    return lambda: page.add(
        ft.Text(f"Módulo '{modulo}' não implementado.", size=20, color="red")
    )
