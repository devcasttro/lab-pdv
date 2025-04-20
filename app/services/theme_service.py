from flet import Colors

def get_theme_colors(theme: str = "claro"):
    if theme == "escuro":
        return {
            "primaria": Colors.BLUE_700,
            "secundaria": Colors.BLUE_300,
            "fundo": "#212121",
            "menu_bg": "#2C2C2C",
            "botao_menu": "#424242",
            "botao_menu_hover": "#616161",
            "botao_comum": "#1976D2",  # igual ao tema claro, como combinamos
            "botao_verde": "#00E676",
            "botao_alarme": "#FFB300",
            "botao_vermelho": "#F44336",
            "texto": "#FFFFFF",
            "texto_secundario": Colors.GREY_300,
            "borda": "#888888",  # <- Adiciona essa linha!
            "logo": "img/logo_escuro.png"
        }
    else:
        return {
            "primaria": "#1976D2",
            "secundaria": "#2196F3",
            "fundo": "#F5F5F5",
            "menu_bg": "#FFFFFF",
            "botao_menu": "#E0E0E0",
            "botao_menu_hover": "#D0D0D0",
            "botao_comum": "#1976D2",
            "botao_verde": "#00C853",
            "botao_alarme": "#FF9100",
            "botao_vermelho": "#D32F2F",
            "texto": "#212121",
            "texto_secundario": Colors.GREY_600,
            "borda": "#CCCCCC",  # <- Adiciona essa linha!
            "logo": "img/logo_claro.png"
        }
