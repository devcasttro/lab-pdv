import flet as ft
from services.theme_service import get_theme_colors

def exibir_alerta(
    page: ft.Page,
    titulo: str,
    mensagem: str,
    tipo: str = "info",  # opções: 'info', 'sucesso', 'erro', 'confirmacao'
    on_confirmar=None,
    on_cancelar=None,
    texto_confirmar: str = "Confirmar",
    texto_cancelar: str = "Cancelar",
    largura: int = 360,
    altura_minima: int = 200,
):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")

    # Cores por tipo
    cor_fundo = {
        "info": tema["fundo"],
        "sucesso": "#E8F5E9",
        "erro": "#FFEBEE",
        "confirmacao": tema["fundo"]
    }.get(tipo, tema["fundo"])

    icone = {
        "info": "ℹ️",
        "sucesso": "✅",
        "erro": "❌",
        "confirmacao": "🗑️"
    }.get(tipo, "🔔")

    botoes = []
    if on_cancelar:
        botoes.append(
            ft.ElevatedButton(
                texto_cancelar,
                height=40,
                width=100,
                bgcolor=tema["botao_vermelho"],
                color=tema["texto_botao"],
                on_click=on_cancelar
            )
        )
    if on_confirmar:
        botoes.append(
            ft.ElevatedButton(
                texto_confirmar,
                height=40,
                width=100,
                bgcolor=tema["botao_verde"],
                color=tema["texto_botao"],
                on_click=on_confirmar
            )
        )

    # Modal personalizado em Stack para não esticar verticalmente
    alerta = ft.Container(
        bgcolor=ft.colors.with_opacity(0.6, ft.Colors.BLACK87),
        alignment=ft.alignment.center,
        visible=True,
        width=page.width,
        height=page.height,
        content=ft.Container(
            width=largura,
            height=altura_minima,
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
            border_radius=12,
            bgcolor=cor_fundo,
            content=ft.Column([
                ft.Text(f"{icone} {titulo}", size=20, weight=ft.FontWeight.BOLD, text_align="center", color=tema["texto"]),
                ft.Text(mensagem, size=14, text_align="center", color=tema["texto"]),
                ft.Row(botoes, alignment="center", spacing=10) if botoes else ft.Container(height=10)
            ], spacing=12, horizontal_alignment="center")
        )
    )

    # Fecha alerta ao clicar fora (se não for confirmação)
    def fechar_automaticamente(e=None):
        alerta.visible = False
        page.overlay.remove(alerta)
        page.update()

    # Adiciona à overlay e fecha com ESC ou clique externo se for alerta simples
    page.overlay.append(alerta)
    page.update()

    if not on_confirmar and not on_cancelar:
        page.run_task(lambda: page.sleep(2.5).then(lambda: fechar_automaticamente()))
