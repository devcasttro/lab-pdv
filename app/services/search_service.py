import unicodedata

def normalizar(texto: str) -> str:
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.lower().strip()

def filtrar_lista(lista, termo_busca, campos):
    termo_normalizado = normalizar(termo_busca)
    resultado = []

    for item in lista:
        for campo in campos:
            # Suporta tanto objetos quanto dicionários
            valor = ""
            if isinstance(item, dict):
                valor = item.get(campo, "")
            else:
                valor = getattr(item, campo, "")

            if termo_normalizado in normalizar(str(valor)):
                resultado.append(item)
                break

    return resultado
