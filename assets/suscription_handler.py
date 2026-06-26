import asyncio
from assets.funcions.func import create_queue_item, local_datetime_text, set_fatal_error
from config import EVENT_QUEUE_MAX_SIZE, PRINT_EACH_EVENT


class SubscriptionHandler:
    def __init__(self, tag_by_node_id, event_queue, fatal_event, fatal_state,):
        self.tag_by_node_id = (tag_by_node_id)
        self.event_queue    = event_queue
        self.fatal_event    = fatal_event
        self.fatal_state    = fatal_state
        self.active         = True

    def datachange_notification(self, node, value, data,):
        if (not self.active or self.fatal_event.is_set()):
            return

        try:
            node_id = (node.nodeid.to_string())
            tag     = self.tag_by_node_id.get(node_id)

            if tag is None:
                print(
                    f"{local_datetime_text(milliseconds=False)} "
                    f"Nodo desconocido: "
                    f"{node_id}"
                )

                return

            data_value = (data.monitored_item.Value)

            item = create_queue_item(
                tag=tag,
                value=value,
                source_timestamp=(data_value.SourceTimestamp),
                status_code=(data_value.StatusCode),
            )

            try:
                self.event_queue.put_nowait(item)

            except asyncio.QueueFull:
                self.active = False

                set_fatal_error(
                    fatal_event=(self.fatal_event),
                    fatal_state=(self.fatal_state),
                    message=(
                        "La cola de escritura ha "
                        "alcanzado el máximo de "
                        f"{EVENT_QUEUE_MAX_SIZE} "
                        "eventos. El proceso se "
                        "detiene para evitar agotar "
                        "la memoria RAM."
                    ),
                )

                return

            if PRINT_EACH_EVENT:
                print(
                    f"{local_datetime_text()} "
                    f"{tag} = {value!r}"
                )

        except Exception as error:
            self.active = False

            set_fatal_error(
                fatal_event=(
                    self.fatal_event
                ),
                fatal_state=(
                    self.fatal_state
                ),
                message=(
                    "Error procesando una "
                    "notificación OPC UA: "
                    f"{error!r}"
                ),
            )