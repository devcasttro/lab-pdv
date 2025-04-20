from flet import Colors

def get_theme_colors(theme: str = "claro"):
    if theme == "escuro":
        return {
            "fundo": "#212121",                     # Área de conteúdo
            "menu_bg": "#2C2C2C",                   # Menu lateral esquerdo
            "botao_menu": "#424242",                # Botões do menu
            "botao_menu_hover": "#616161",          # Hover dos botões do menu
            "botao_comum": "#1976D2",               # Igual ao tema claro
            "botao_comum_hover": "#2196F3",
            "botao_verde": "#00E676",               # Ações positivas
            "botao_verde_hover": "#69F0AE",
            "botao_alarme": "#FFB300",              # Alertas
            "botao_alarme_hover": "#FFC107",
            "botao_vermelho": "#F44336",            # Ações destrutivas
            "botao_vermelho_hover": "#EF5350",
            "texto": "#FFFFFF",                     # Texto padrão
            "logo": "img/logo_escuro.png"
        }
    else:
        return {
            "fundo": "#F5F5F5",                     # Área de conteúdo
            "menu_bg": "#FFFFFF",                   # Menu lateral esquerdo
            "botao_menu": "#E0E0E0",                # Botões do menu
            "botao_menu_hover": "#D0D0D0",          # Hover dos botões do menu
            "botao_comum": "#1976D2",               # Botões de ação comum
            "botao_comum_hover": "#2196F3",
            "botao_verde": "#00C853",               # Ações positivas
            "botao_verde_hover": "#00E676",
            "botao_alarme": "#FF9100",              # Alertas
            "botao_alarme_hover": "#FFB300",
            "botao_vermelho": "#D32F2F",            # Ações destrutivas
            "botao_vermelho_hover": "#F44336",
            "texto": "#212121",                     # Texto padrão
            "logo": "img/logo_claro.png"
        }
