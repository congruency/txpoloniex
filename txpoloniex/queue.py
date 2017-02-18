from time import time

from twisted.internet import reactor, task

class RateLimitMixin:
    """
    Mixin for classes to rate limit function calls
    """
    maxPerSecond = 0

    _queue = []

    _wait = 0.0

    def addQueue(self, func, *args, **kwargs):
        """
        Add to queue
        """
        self.purgeOld()
        
        length = len(self._queue)

        limit = self.maxPerSecond

        before_limit = length % limit

        if limit and length and not before_limit:
            i = length - limit

            distance = self._queue[-1] - self._queue[i]

            duration = 1.0 - distance

            # Increase wait time by 1 second, less the time already transpired
            self._wait += duration

            # Purge the queue once the wait has expired
            reactor.callLater(self._wait, self.deQueue, duration)

        self._queue.append(time())

        if not self._wait:
            return func(*args, **kwargs)
        else:
            return task.deferLater(
                reactor, self._wait,
                func, *args, **kwargs
            )

    def deQueue(self, duration):
        """
        Remove from the queue
        """
        self.purgeOld()

        self._wait -= 1.0

    def purgeOld(self):
        """
        Purge old entries from queue
        """
        now = time()

        for entry in self._queue:
            distance = now - entry

            if distance < 1.0:
                continue

            self._queue.remove(entry)
    
