import asyncio


EVENT_QUEUE_MAX_SIZE = 50_000

EVENT_QUEUE = asyncio.Queue(maxsize=EVENT_QUEUE_MAX_SIZE,)