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
            message = await container.queue.reserve(container.settings.worker_poll_seconds)
            if message is None:
                continue
            try:
                logger.info("run task=%s message=%s", message.task_id, message.message_id)
                await container.runtime.run(message.task_id)
                await container.queue.ack(message)
            except Exception:
                # Intentionally do not ACK. Redis Streams will expose the pending
                # message for XAUTOCLAIM after the stale timeout.
                logger.exception(
                    "uncaught worker error task=%s message=%s",
                    message.task_id,
                    message.message_id,
                )
    finally:
        await container.close()
        logger.info("worker stopped")


if __name__ == "__main__":
    asyncio.run(serve())
