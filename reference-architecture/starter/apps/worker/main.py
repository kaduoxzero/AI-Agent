from __future__ import annotations

import asyncio
import logging
import signal

from packages.dependencies import container


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("agent-worker")


async def serve() -> None:
    await container.initialize()
    stopping = asyncio.Event()
    loop = asyncio.get_running_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stopping.set)
        except NotImplementedError:  # Windows event loop
            pass

    logger.info("worker started durable_mode=%s", container.settings.durable_mode)
    try:
        while not stopping.is_set():
            task_id = await container.queue.dequeue(container.settings.worker_poll_seconds)
            if task_id is None:
                continue
            try:
                logger.info("run task=%s", task_id)
                await container.runtime.run(task_id)
            except Exception:
                logger.exception("uncaught worker error task=%s", task_id)
    finally:
        await container.close()
        logger.info("worker stopped")


if __name__ == "__main__":
    asyncio.run(serve())
