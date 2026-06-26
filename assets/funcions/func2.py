import asyncio
from datetime import datetime
import signal

from config import QUEUE_DRAIN_TIMEOUT_SECONDS


def configure_stop_signals(stop_event,):
    """
    Configura Ctrl+C y la parada enviada
    por systemd mediante SIGTERM.
    """
    loop = asyncio.get_running_loop()

    def stop_handler(signum, frame,):
        print("Orden de parada recibida...")

        loop.call_soon_threadsafe(stop_event.set)

    signal.signal(signal.SIGINT, stop_handler,)
    signal.signal( signal.SIGTERM, stop_handler,)



async def stop_writer_normally(event_queue, writer_task,):
    """
    Vacía la cola y detiene el escritor
    durante una parada normal.
    """
    print("Guardando los eventos pendientes...")

    await asyncio.wait_for(
        event_queue.join(),
        timeout=QUEUE_DRAIN_TIMEOUT_SECONDS,
    )

    if not writer_task.done():
        await event_queue.put(None)
        await writer_task



def local_datetime_text(moment=None, milliseconds=True,):
    """
    Devuelve la fecha local en formato:

        YYYY-MM-DD HH:MM:SS.mmm

    O sin milisegundos cuando:

        milliseconds=False
    """
    if moment is None:
        moment = (datetime.now().astimezone())

    if milliseconds:
        return moment.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    return moment.strftime("%Y-%m-%d %H:%M:%S")

