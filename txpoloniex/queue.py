from twisted.internet import reactor, task, defer

class RateLimit(defer.DeferredLock):
    """
    Mixin for classes to rate limit function calls
    """
    _times = []

    _expirations = []

    reactor = reactor

    def __init__(self, maxPerSecond=0):
        self.maxPerSecond = maxPerSecond

        defer.DeferredLock.__init__(self)

    def _nextDelay(self):
        """
        Returns the amount of time to delay the next call
        """

        length = len(self._times)

        limit = self.maxPerSecond

        remainder = length % limit

        difference = 0

        base = length // self.maxPerSecond

        if not limit or not length or not base:
            return 0.0

        last = self._times[-1]

        i = length - limit

        difference = last - self._times[i]

        return 1.0 - difference

    def _called(self, ignoredResult):
        """
        Record the time that the deferred was called
        """
        self._times.append(self.reactor.seconds())

        # Once a second has passed, remove the recorded time
        de = self.reactor.callLater(1.0, self._expire)

        self._expirations.append(de)

    def _expire(self):
        """
        Called to remove the time from calculations after a second has expired
        """
        self._times.pop(0)

    def _cancel(self, d):
        """
        Remove d from waiting and cancel the expiration
        """
        i = self.waiting.index(d)

        self.waiting.pop(i)

        df = self._expirations.pop(i)

        df.cancel()

    def acquire(self):

        d = defer.Deferred(canceller=self._cancel)

        d.addCallback(self._called)

        if self.locked:
            self.waiting.append(d)
        else:
            self.locked = True
            d.callback(self)

        return d

    def release(self):

        delay = self._nextDelay()

        self.reactor.callLater(delay, defer.DeferredLock.release, self)

    def clear(self):
        """
        Cancel all pending calls and flush state
        """
        
        for d in self.waiting:
            self._cancel(d)

        for d in self._expirations:
            d.cancel()

        self._times = []
        self._expirations = []
