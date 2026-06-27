import asyncio
import json
from datetime import datetime
from pathlib import Path

from assets.event_queue_file import EVENT_QUEUE



BASE_DIRECTORY = Path("/var/lib/froxa-opcua")
WRITE_RETRY_SECONDS = 5
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"



def append_event_jsonl(event):
    """
    Añade el evento como una línea JSON.

    Ejemplo:
    /var/lib/froxa-opcua/2026/06-all.json
    """


    year_directory = (
        BASE_DIRECTORY
        / f"{datetime.date.year:04d}"
    )

    year_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        year_directory
        / f"{datetime.date.month:02d}-all.json"
    )

    json_line = json.dumps(
        event,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )

    # Abre, escribe y cierra el archivo en cada evento.
    with file_path.open(
        mode="a",
        encoding="utf-8",
    ) as file:
        file.write(json_line)
        file.write("\n")
        file.flush()


async def jsonl_writer():
    """
    Consume permanentemente la cola global.
    """

    while True:
        event = await EVENT_QUEUE.get()

        try:
            while True:
                try:
                    await asyncio.to_thread(append_event_jsonl, event,)

                    break

                except Exception as e:
                    pass

        finally:
            EVENT_QUEUE.task_done()