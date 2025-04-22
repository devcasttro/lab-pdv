import os
import shutil
import flet as ft
from services.theme_service import get_theme_colors
from models.produto_model import adicionar_produto, editar_produto
from models.categoria_model import listar_categorias
from models.unidade_model import listar_unidades

def cadastro_produto_view(page: ft.Page, ao_cancelar, ao_salvar, produto: dict = None):
    tema = get_theme_colors("escuro" if page.session.get("tema_escuro") else "claro")
    categorias = listar_categorias()
    unidades = listar_unidades()
    atualizando = {"interno": False}

    def parse_valor(valor):
        try:
            return float(str(valor).replace(",", "."))
        except:
            return 0

    nome = ft.TextField(label="Nome do Produto *", expand=3, value=produto["nome"] if produto else "")
    codigo_barras = ft.TextField(label="Código de Barras", expand=1, keyboard_type=ft.KeyboardType.NUMBER,
                                 value=produto["codigo_barras"] if produto else "")
    unidade = ft.Dropdown(
        label="Unidade",
        options=[ft.dropdown.Option(u["tag"], data=u["id"]) for u in unidades],
        expand=1.5,
        value=produto["unidade"] if produto else None
    )
    categoria = ft.Dropdown(
        label="Categoria",
        options=[ft.dropdown.Option(c["tag"], data=c["id"]) for c in categorias],
        expand=2.2,
        value=produto["categoria"] if produto else None
    )
    custo = ft.TextField(label="Custo de Aquisição (R$)", expand=1.5,
                         keyboard_type=ft.KeyboardType.NUMBER,
                         value=str(produto["custo"]).replace(".", ",") if produto else "")
    preco = ft.TextField(label="Preço de Venda (R$) *", expand=1.5,
                         keyboard_type=ft.KeyboardType.NUMBER,
                         value=str(produto["preco"]).replace(".", ",") if produto else "")
    margem_lucro = ft.TextField(label="Margem de Lucro (%)", expand=1.5,
                                keyboard_type=ft.KeyboardType.NUMBER,
                                value=str(produto["margem_lucro"]).replace(".", ",") if produto else "")
    estoque = ft.TextField(label="Estoque Inicial", expand=1.5,
                           keyboard_type=ft.KeyboardType.NUMBER,
                           value=str(produto["estoque"]) if produto else "",
                           disabled=bool(produto))
    estoque_minimo = ft.TextField(label="Estoque Mínimo", expand=1.5,
                                  keyboard_type=ft.KeyboardType.NUMBER,
                                  value=str(produto["estoque_minimo"]) if produto else "")
    ativo = ft.Dropdown(
        label="Status",
        options=[ft.dropdown.Option("Ativo"), ft.dropdown.Option("Inativo")],
        value="Ativo" if not produto or produto["ativo"] else "Inativo"
    )

    imagem_default = "assets/imagens_produtos/sem_foto.png"
    imagem_path = ft.TextField(visible=False, value=produto["imagem_path"] if produto else "")
    imagem_exibida = ft.Image(
        src=produto["imagem_path"] if produto and produto.get("imagem_path") else imagem_default,
        width=120, height=120,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10
    )

    botao_remover_imagem = ft.ElevatedButton(
        text="🗑️ Remover Imagem",
        bgcolor=tema["botao_vermelho"],
        color=tema["texto_botao"],
        visible=bool(produto and produto.get("imagem_path")),
        on_click=lambda e: remover_imagem()
    )

    picker = ft.FilePicker()
    page.overlay.append(picker)

    def selecionar_imagem_result(e: ft.FilePickerResultEvent):
        if e.files:
            arquivo = e.files[0]
            origem = arquivo.path
            nome_destino = os.path.basename(origem)
            destino = os.path.join("assets", "imagens_produtos", nome_destino)

            try:
                os.makedirs("assets/imagens_produtos", exist_ok=True)
                shutil.copy(origem, destino)
                imagem_path.value = destino.replace("\\", "/")
                imagem_exibida.src = imagem_path.value
                imagem_exibida.visible = True
                botao_remover_imagem.visible = True
                page.update()
            except Exception as err:
                print(f"Erro ao copiar imagem: {err}")

    picker.on_result = selecionar_imagem_result

    def remover_imagem():
        caminho = imagem_path.value.strip()
        if caminho and os.path.exists(caminho) and "sem_foto.png" not in caminho:
            try:
                os.remove(caminho)
            except Exception as err:
                print(f"Erro ao remover imagem: {err}")
        imagem_path.value = ""
        imagem_exibida.src = imagem_default
        botao_remover_imagem.visible = False
        page.update()

    erro = ft.Text("", color=tema["botao_vermelho"], size=12)

    def calcular_automatico(e=None):
        if atualizando["interno"]:
            return
        atualizando["interno"] = True
        try:
            c = parse_valor(custo.value)
            p = parse_valor(preco.value)
            m = parse_valor(margem_lucro.value)
            if e.control == preco:
                margem_lucro.value = str(round(((p - c) / c * 100), 2)) if c > 0 else "0"
            elif e.control == margem_lucro:
                preco.value = str(round(c + (c * m / 100), 2))
        except:
            pass
        atualizando["interno"] = False
        page.update()

    preco.on_change = calcular_automatico
    margem_lucro.on_change = calcular_automatico

    def validar_campos():
        try:
            if not nome.value.strip():
                erro.value = "O nome do produto é obrigatório."
                return False
            if not preco.value.strip():
                erro.value = "O preço de venda é obrigatório."
                return False
            float(preco.value.replace(",", "."))
            float(custo.value.replace(",", ".") or 0)
            float(margem_lucro.value.replace(",", ".") or 0)
            if estoque.value and int(estoque.value) < 0:
                erro.value = "Estoque não pode ser negativo."
                return False
            if estoque_minimo.value and int(estoque_minimo.value) < 0:
                erro.value = "Estoque mínimo não pode ser negativo."
                return False
            erro.value = ""
            return True
        except:
            erro.value = "Preencha os campos corretamente."
            return False

    def salvar(e):
        if not validar_campos():
            page.update()
            return

        dados = {
            "nome": nome.value,
            "codigo_barras": codigo_barras.value,
            "preco": preco.value or "0",
            "custo": custo.value or "0",
            "margem_lucro": margem_lucro.value or "0",
            "estoque": estoque.value or "0",
            "estoque_minimo": estoque_minimo.value or "0",
            "unidade": unidade.value or "",
            "categoria": categoria.value or "",
            "imagem_path": imagem_path.value or "",
            "ativo": 1 if ativo.value == "Ativo" else 0
        }

        if produto:
            editar_produto(produto["id"], dados)
        else:
            adicionar_produto(dados)

        ao_salvar(e)

    return ft.Column([
        ft.Text("✏️ Edição de Produto" if produto else "🆕 Cadastro de Produto", size=30, color=tema["texto"]),
        ft.Divider(),

        ft.Text("📋 Dados Básicos", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
        ft.Row([codigo_barras, nome], spacing=10),
        ft.Row([unidade, categoria], spacing=10),

        ft.Divider(),
        ft.Text("💰 Dados Financeiros", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
        ft.Row([custo, preco, margem_lucro], spacing=10),

        ft.Divider(),
        ft.Text("📦 Dados de Estoque", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
        ft.Row([estoque, estoque_minimo], spacing=10),

        ft.Divider(),
        ft.Text("🧩 Dados Complementares", size=16, weight=ft.FontWeight.BOLD, color=tema["texto"]),
        ft.Row([
            ativo,
            ft.ElevatedButton(
                text="📁 Selecionar Imagem",
                icon=ft.Icons.UPLOAD_FILE,
                bgcolor=tema["botao_azul"],
                color=tema["texto_botao"],
                on_click=lambda _: picker.pick_files(allow_multiple=False)
            )
        ], spacing=10),
        ft.Row([imagem_exibida, imagem_path, botao_remover_imagem], spacing=10),

        erro,
        ft.Divider(),
        ft.Row([
            ft.ElevatedButton("💾 Salvar", bgcolor=tema["botao_verde"], color=tema["texto_botao"],
                              height=45, on_click=salvar),
            ft.ElevatedButton("X Cancelar", bgcolor=tema["botao_vermelho"], color=tema["texto_botao"],
                              height=45, on_click=ao_cancelar),
        ], spacing=10)
    ], scroll=ft.ScrollMode.AUTO)
