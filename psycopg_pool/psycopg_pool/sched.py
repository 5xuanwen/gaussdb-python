# WARNING: this file is auto-generated by 'async_to_sync.py'
# from the original file 'sched_async.py'
# DO NOT CHANGE! Change the original file instead.
"""
A minimal scheduler to schedule tasks to run in the future (sync version).

Inspired to the standard library `sched.scheduler`, but designed for
multi-thread usage from the ground up, not as an afterthought. Tasks can be
scheduled in front of the one currently running and `Scheduler.run()` can be
left running without any tasks scheduled.

Tasks are called "Task", not "Event", here, because we actually make use of
`[threading/asyncio].Event` and the two would be confusing.
"""

# Copyright (C) 2021 The Psycopg Team

from __future__ import annotations

import logging
from time import monotonic
from heapq import heappop, heappush
from typing import Any, Callable

from ._task import Task
from ._acompat import Event, Lock

logger = logging.getLogger(__name__)


class Scheduler:

    def __init__(self) -> None:
        self._queue: list[Task] = []
        self._lock = Lock()
        self._event = Event()

    EMPTY_QUEUE_TIMEOUT = 600.0

    def enter(self, delay: float, action: Callable[[], Any] | None) -> Task:
        """Enter a new task in the queue delayed in the future.

        Schedule a `!None` to stop the execution.
        """
        time = monotonic() + delay
        return self.enterabs(time, action)

    def enterabs(self, time: float, action: Callable[[], Any] | None) -> Task:
        """Enter a new task in the queue at an absolute time.

        Schedule a `!None` to stop the execution.
        """
        task = Task(time, action)
        with self._lock:
            heappush(self._queue, task)
            first = self._queue[0] is task

        if first:
            self._event.set()

        return task

    def run(self) -> None:
        """Execute the events scheduled."""
        q = self._queue
        while True:
            with self._lock:
                now = monotonic()
                task = q[0] if q else None
                if task:
                    if task.time <= now:
                        heappop(q)
                    else:
                        delay = task.time - now
                        task = None
                else:
                    delay = self.EMPTY_QUEUE_TIMEOUT
                self._event.clear()

            if task:
                if not task.action:
                    break
                try:
                    task.action()
                except Exception as e:
                    logger.warning(
                        "scheduled task run %s failed: %s: %s",
                        task.action,
                        e.__class__.__name__,
                        e,
                    )
            else:
                # Block for the expected timeout or until a new task scheduled
                self._event.wait(delay)
