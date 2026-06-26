import asyncio
from assets.exceptions import FatalServiceError
from assets.funcions.func import configure_stop_signals, local_datetime_text, safe_write_health
from assets.service import run_service
from config import (TAGS, OTHER_TAGS,)


# Lista única de todos los tags suscritos.
ALL_TAGS = list(dict.fromkeys(TAGS + OTHER_TAGS))

# Los tags de esta lista se guardan:
#
# - En MM-all.json.
# - También en MM-stat.json.
STAT_TAGS = set(TAGS)



async def main():
    stop_event = asyncio.Event()
    configure_stop_signals(stop_event=stop_event)

    try:
        await run_service(stop_event=stop_event)

    except FatalServiceError as error:
        print(
            f"{local_datetime_text(milliseconds=False)} "
            f"[SERVICIO FINALIZADO POR ERROR] "
            f"{error}"
        )

        return 1

    except Exception as error:
        print(
            f"{local_datetime_text(milliseconds=False)} "
            f"[ERROR NO CONTROLADO] "
            f"{error!r}"
        )

        safe_write_health(status="fatal", detail=repr(error),)

        return 1

    print(
        "Servicio detenido correctamente"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        asyncio.run(main())
        )