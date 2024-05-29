import json
import hashlib


def extraer_medio(buscar, texto, longitud=80):
    indices = []
    start = 0

    # Encuentra todas las posiciones de la buscar en el texto
    while start < len(texto):
        indice = texto.find(buscar, start)
        if indice == -1:
            break
        indices.append(indice)
        start = indice + len(buscar)

    subcadenas = []
    for indice in indices:
        start_index = max(indice - (longitud - len(buscar)) // 2, 0)
        end_index = start_index + longitud

        # Ajusta el final si excede la longitud del texto
        if end_index > len(texto):
            end_index = len(texto)
            start_index = max(end_index - longitud, 0)

        subcadena = texto[start_index:end_index]

        # Añade puntos suspensivos si no es el principio o el fin del texto
        if start_index > 0:
            subcadena = "..." + subcadena
        if end_index < len(texto):
            subcadena = subcadena + "..."

        subcadenas.append(subcadena)

    return subcadenas


def extraer_elementos(items, nivel=0):
    result = ""
    for item in items:
        result += "-" * (nivel + 1) + " " + item["content"] + "\n"
        result += extraer_elementos(item["items"], nivel + 1)
    return result


def bloque_to_text(block: dict) -> str:
    tipo, data = block["type"], block["data"]

    match block["type"]:
        case "header":
            return data["text"]
        case "paragraph":
            return data["text"]
        case "control" | "riesgo" | "normativa" | "aplicacion" | "organigrama":
            return f"[{tipo}] {data['nombre']}: {data['descripcion']}"
        case "checklist":
            return " ".join([f"- {i['text']}" for i in data["items"]])
        case "list":
            return extraer_elementos(data["items"])
        case "delimiter":
            return ""
        case "table":
            return " ".join([elem for li in data["content"] for elem in li])
        case "alert":
            return data["message"]
        case "toggle":
            return data["text"]

        case "mermaid":
            return data["caption"]
        case _:
            print(data)
            raise Exception(
                f"Tipo de bloque EditorJS no reconocido: {tipo}.\n  Data: {data}"
            )


def editorjs_to_text(contenido: str) -> str:
    contenido = json.loads(contenido.replace("\n", " ").lower())

    lineas = [
        bloque_to_text(block)
        .strip()
        .lower()
        .replace("\n", " ")
        .replace("<b>", "")
        .replace("</b>", "")
        .replace("<i>", "")
        .replace("</i>", "")
        for block in contenido["blocks"]
    ]

    return " ".join(lineas)


def hash_string(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()
