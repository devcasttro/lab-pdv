from flet import Colors


def get_theme_colors(theme: str = "claro") -> dict:
    """
    Retorna o dicionário de cores conforme o tema selecionado ('claro' ou 'escuro').
    """

    if theme == "escuro":
        return {
            "primaria": "#E0E0E0",
            "secundaria": "#FFFFFF",
            "fundo": "#212121",
            "menu_bg": "#2C2C2C",
            "botao_menu": "#424242",
            "botao_menu_hover": "#616161",
            "botao_comum": "#E0E0E0",
            "botao_verde": "#00E676",
            "botao_alarme": "#FFB300",
            "botao_vermelho": "#F44336",
            "botao_verde_hover": "#69F0AE",
            "botao_alarme_hover": "#FFC107",
            "botao_vermelho_hover": "#EF5350",
            "texto": "#FFFFFF",
            "texto_secundario": Colors.GREY_300,
            "texto_botao": Colors.WHITE,
            "borda": Colors.GREY_700,
            "logo": "img/logo_escuro.png",
             "botao_azul": Colors.BLUE_500,
        }

    # Tema claro (default)
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
        "botao_verde_hover": "#00E676",
        "botao_alarme_hover": "#FFB300",
        "botao_vermelho_hover": "#F44336",
        "texto": "#212121",
        "texto_secundario": Colors.GREY_600,
        "texto_botao": Colors.WHITE,
        "borda": Colors.GREY_300,
        "logo": "img/logo_claro.png",
        "botao_azul": Colors.BLUE_500,
    }
