from flet import colors

def get_theme_colors(theme: str = "claro"):
    if theme == "escuro":
        # Mantendo o tema escuro original, com pequenas melhorias
        return {
            "primaria": colors.BLUE_GREY_800,      # Cor principal para botões e destaques
            "secundaria": colors.BLUE_GREY_600,    # Cor para hover ou elementos secundários
            "fundo": colors.BLUE_GREY_900,         # Fundo principal
            "menu_bg": colors.BLUE_GREY_800,       # Fundo do menu lateral
            "texto": colors.WHITE,                 # Cor do texto
            "texto_secundario": colors.GREY_300,   # Novo: para textos menos destacados
            "borda": colors.BLUE_GREY_700,         # Novo: para bordas ou divisores
            "logo": "img/logo_escuro.png"          # Logo do tema escuro
        }
    else:
        # Nova paleta para tema claro
        return {
            "primaria": colors.INDIGO_600,         # Um índigo vibrante, mas profissional, para botões e destaques
            "secundaria": colors.INDIGO_100,       # Tom claro de índigo para hover ou fundos secundários
            "fundo": colors.GREY_50,               # Fundo quase branco, sutil e limpo
            "menu_bg": colors.BLUE_100,           # Fundo do menu lateral, com tom suave de índigo
            "texto": colors.GREY_900,              # Texto escuro para alto contraste
            "texto_secundario": colors.GREY_600,   # Novo: para textos menos destacados (ex.: placeholders)
            "borda": colors.GREY_300,              # Novo: para bordas ou divisores
            "logo": "img/logo_claro.png"           # Logo do tema claro
        }