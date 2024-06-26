import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any

from database import SqlDB
from entidades.documentos.schema import DocumentoDB
from fastapi import WebSocket, WebSocketDisconnect
from openai import OpenAI
from pydantic import BaseModel

# Variables globales
client = OpenAI()
auditor = client.beta.assistants.retrieve("asst_VU2eGpeR7rbfJ8e7rOxqeIJ9")
store = client.beta.vector_stores.retrieve("vs_zsMbXAk9aLZ5btuwqzGc7aVU")


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
FORMATO_TIMESTAMP = "%Y%m%d%H%M%S"
CARPETA = Path("files/asistente")


class DocumentoRelevamiento(BaseModel):
    id: int
    fecha: datetime
    ubicacion: str
    accion: str = None
    archivo: Any

    def __repr__(self):
        return f"<DocRel {self.id} - {self.fecha} - {self.ubicacion} - {self.accion}>"

    def __hash__(self):
        return hash(f"{self.id}{self.fecha}{self.ubicacion}")

    def __lt__(self, other):
        return self.fecha < other.fecha

    def __gt__(self, other):
        return self.fecha > other.fecha

    def __eq__(self, other):
        return self.fecha == other.fecha

    def __ne__(self, other):
        return self.fecha != other.fecha

    def __le__(self, other):
        return self.fecha <= other.fecha

    def __ge__(self, other):
        return self.fecha >= other.fecha


def obtener_documentos_locales(db: SqlDB) -> list[DocumentoRelevamiento]:
    archivos_db = db.query(DocumentoDB).all()
    return [
        DocumentoRelevamiento(
            archivo=archivo,
            id=archivo.id,
            fecha=archivo.actualizacion.replace(microsecond=0),
            ubicacion="db",
        )
        for archivo in archivos_db
    ]


class CacheDocumentosOnline:
    archivo = CARPETA / "cache.pkl"

    @staticmethod
    def crear():
        documentos = consultar_documentos_online()
        with open(CacheDocumentosOnline.archivo, mode="wb") as f:
            pickle.dump(documentos, f)

    @staticmethod
    def cargar() -> list[DocumentoRelevamiento]:
        with open(CacheDocumentosOnline.archivo, mode="rb") as f:
            return pickle.load(f)

    @staticmethod
    def existe() -> bool:
        return CacheDocumentosOnline.archivo.exists()

    @staticmethod
    def eliminar():
        CacheDocumentosOnline.archivo.unlink()


def consultar_documentos_online() -> list[DocumentoRelevamiento]:
    archivos_store = client.beta.vector_stores.files.list(vector_store_id=store.id)

    files = []
    for pag in archivos_store.iter_pages():
        files.extend(pag.data)

    documentos_openai = [client.files.retrieve(file.id) for file in files]

    docs_online = []
    for archivo in documentos_openai:
        doc, fecha = archivo.filename.replace(".txt", "").split("_")
        doc = int(doc.replace("Doc", " "))
        fecha = datetime.strptime(fecha, FORMATO_TIMESTAMP)
        docs_online.append(
            DocumentoRelevamiento(
                archivo=archivo, id=doc, fecha=fecha, ubicacion="openai"
            )
        )

    return docs_online


def obtener_documentos_online() -> list[DocumentoRelevamiento]:
    if not CacheDocumentosOnline.existe():
        CacheDocumentosOnline.crear()

    return CacheDocumentosOnline.cargar()


def determinar_acciones_por_documento(
    archivos_online: list[DocumentoRelevamiento],
    archivos_locales: list[DocumentoRelevamiento],
) -> set[DocumentoRelevamiento]:
    set_online = set(archivos_online)
    set_locales = set(archivos_locales)

    todos = set_online | set_locales

    for donline in set_online:
        # Se comprueba si es el último disponible
        filtro = set(filter(lambda x: x.id == donline.id, todos))
        ultimo = max(filtro)

        if ultimo == donline:
            donline.accion = "mantener"
        else:
            donline.accion = "eliminar"

    for dlocal in set_locales:
        # Se comprueba si es el último disponible
        filtro_id = set(filter(lambda x: x.id == dlocal.id, todos))
        ultimo = max(filtro_id)

        # Verificar si se mantiene el online
        hay_mantener = any(filter(lambda x: x.accion == "mantener", filtro_id))

        if hay_mantener:
            dlocal.accion = "nada"
        else:
            if ultimo == dlocal:
                dlocal.accion = "subir"
            else:
                dlocal.accion = "nada"

    return todos


def contar_cantidad_pendientes(db: SqlDB) -> int:
    # Determinación de documentos
    documentos_locales = obtener_documentos_locales(db)
    documentos_online = obtener_documentos_online()

    # Determinar acciones por documento
    acciones = determinar_acciones_por_documento(documentos_online, documentos_locales)

    # Determinar cantidad de archivos pendientes
    pendientes = set(filter(lambda x: x.accion == "subir", acciones))

    return len(pendientes)


def generar_archivo_local(doc: DocumentoRelevamiento) -> str:
    fecha = doc.fecha.strftime(FORMATO_TIMESTAMP)
    nombre = f"Doc{doc.id}_{fecha}.txt"
    path = CARPETA / nombre
    parseado = json.loads(doc.archivo.contenido.replace(r"\\n", ""))

    with open(path, mode="w", encoding="utf-8") as f:
        f.write(f"titulo:::{doc.archivo.relevamiento.nombre}\n")
        f.write(f"timestamp:::{doc.fecha}\n")

        for block in parseado["blocks"]:
            tipo, data = block["type"], block["data"]

            if tipo == "mermaid" or not data:
                continue

            f.write(f"|type:{tipo}|{data}")

    return path


def cargar_archivos_online(archivos: set[DocumentoRelevamiento]):
    subir = filter(lambda x: x.accion == "subir", archivos)

    archivos_subir = {doc: generar_archivo_local(doc) for doc in subir}

    if not archivos_subir:
        return None

    print(f"Cargando {len(archivos_subir)} archivos a OpenAI:")
    for doc in archivos_subir:
        print(doc.archivo)

    file_streams = [open(path, "rb") for path in archivos_subir.values()]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=store.id, files=file_streams
    )

    # You can print the status and the file counts of the batch to see the result of this operation.
    print("Status:", file_batch.status)
    print("Conteo:", file_batch.file_counts)

    # Cerrado de archivos
    for file in file_streams:
        file.close()

    # Eliminar archivos locales
    for path in archivos_subir.values():
        Path(path).unlink()

    # Eliminar cache
    CacheDocumentosOnline.eliminar()

    # Generar nuevo caché
    CacheDocumentosOnline.crear()


def eliminar_archivos_antiguos(archivos: set[DocumentoRelevamiento]):
    eliminar = filter(lambda x: x.accion == "eliminar", archivos)

    for doc in eliminar:
        client.files.delete(doc.archivo.id)
        print(f"Eliminado de OpenAI: {doc.archivo.id}")


def sincronizar(db: SqlDB):
    # Determinación de documentos
    documentos_locales = obtener_documentos_locales(db)
    documentos_online = obtener_documentos_online()

    # Determinar acciones por documento
    acciones = determinar_acciones_por_documento(documentos_online, documentos_locales)

    cargar_archivos_online(acciones)
    eliminar_archivos_antiguos(acciones)
