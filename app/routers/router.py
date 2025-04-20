from views.dashboard_view import dashboard_view
from views.produtos_view import produtos_view
from views.configuracoes_view import configuracoes_view

def carregar_modulo(modulo, page):
    if modulo == "Dashboard":
        return dashboard_view(page)
    if modulo == "Produtos":
        return produtos_view(page)
    if modulo == "Configurações":
        return configuracoes_view(page, page.update)
    return None
