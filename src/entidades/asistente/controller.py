from fastapi import WebSocket, WebSocketDisconnect
from openai import OpenAI
from database import SqlDB
from entidades.documentos.schema import DocumentoDB
import json
from collections import namedtuple

# Variables globales
client = OpenAI()
auditor = client.beta.assistants.retrieve("asst_VU2eGpeR7rbfJ8e7rOxqeIJ9")


def crear_conversacion():
    return client.beta.threads.create()


def enviar_mensaje(conversacion, mensaje):
    return client.beta.threads.messages.create(
        thread_id=conversacion.id, role="user", content=mensaje
    )


async def stream_respuesta(conversacion, websocket):
    stream = client.beta.threads.runs.create(
        thread_id=conversacion.id, assistant_id=auditor.id, stream=True
    )
    for event in stream:
        if event.event == "thread.message.delta":
            delta = event.data.delta.content[0].text.value
            # print(f"{delta!r}")
            if "【" not in delta:
                await websocket.send_text(delta)


# @app.websocket("/ws")
async def consultar_asistente(websocket: WebSocket):
    # Se acepta la conexion
    await websocket.accept()
    conversacion = crear_conversacion()

    try:
        while True:
            prompt = await websocket.receive_text()
            print("Prompt:", prompt)
            # await websocket.send_text(prompt)
            enviar_mensaje(conversacion, prompt)
            await stream_respuesta(conversacion, websocket)
            await websocket.send_text("ACK:FIN")

    except WebSocketDisconnect:
        ...


# Manejo de archivos
store = client.beta.vector_stores.retrieve("vs_pl0l2GU3S8XpNqp8veSxnmXi")
FORMATO_TIMESTAMP = "%Y%m%d%H%M%S"


DocumentoStore = namedtuple("DocumentoStore", ["id", "filename", "idDoc", "timestamp"])
DocumentoCargar = namedtuple("DocumentoCargar", ["id", "timestamp", "obj"])


def listar_archivos_store() -> set[DocumentoStore]:
    archivos_store = client.beta.vector_stores.files.list(vector_store_id=store.id)
    out = set()
    for archivo_store in archivos_store.data:
        archivo = client.files.retrieve(archivo_store.id)
        out.add(
            DocumentoStore(
                archivo.id,
                archivo.filename,
                int(archivo.filename.split("_")[0].replace("Doc", "")),
                int(archivo.filename.split("_")[1].replace(".txt", "")),
            )
        )

    return out


def buscar_doc_store(id: int, documentos_store: set[DocumentoStore]):
    for doc_st in documentos_store:
        if doc_st.idDoc == id:
            return doc_st


def determinar_acciones(
    documentos_db: list[DocumentoDB], documentos_store: set[DocumentoStore]
):
    eliminar, subir = set(), set()

    for doc_db in documentos_db:
        doc_car = DocumentoCargar(
            doc_db.id, int(doc_db.actualizacion.strftime(FORMATO_TIMESTAMP)), doc_db
        )

        asociado_en_store = buscar_doc_store(doc_car.id, documentos_store)

        if not asociado_en_store:
            subir.add(doc_car)
        else:
            if doc_car.timestamp > asociado_en_store.timestamp:
                subir.add(doc_car)
                eliminar.add(asociado_en_store)

    return eliminar, subir


def guardar_documento(doc: DocumentoCargar):
    nombre = f"Doc{doc.id}_{doc.timestamp}.txt"
    path = f"files/tmp/asistente/{nombre}"
    parseado = json.loads(doc.obj.contenido.replace(r"\\n", ""))

    with open(path, mode="w", encoding="utf-8") as f:
        f.write(f"titulo:::{doc.obj.relevamiento.nombre}\n")
        f.write(f"timestap:::{doc.timestamp}\n")
        for block in parseado["blocks"]:
            tipo, data = block["type"], block["data"]

            if tipo == "mermaid" or not data:
                continue
            f.write(f"|type:{tipo}|{data}")

    return path


def eliminar_doc_store(iterable):
    for archivo in iterable:
        client.files.delete(archivo.id)
        print(f"Eliminado de OpenAI: {archivo.id}")


def cargar_doc_store(iterable):
    file_paths = []
    for doc in iterable:
        path = guardar_documento(doc)
        file_paths.append(path)

    file_streams = [open(path, "rb") for path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=store.id, files=file_streams
    )

    # You can print the status and the file counts of the batch to see the result of this operation.
    print(file_batch.status)
    print(file_batch.file_counts)


async def actualizar_contenido(db: SqlDB):
    documentos_db = db.query(DocumentoDB).all()
    documentos_store = listar_archivos_store()

    eliminar, subir = determinar_acciones(documentos_db, documentos_store)
    print(f"Se eliminarán {len(eliminar)} archivos del store de OpenAI.")
    print(f"Se agregarán {len(subir)} archivos al store de OpenAI.")
    eliminar_doc_store(eliminar)
    cargar_doc_store(subir)
    # TODO eliminar archivos, ver porque se siguen subiendo siempre 17
    return None
