from twisted.trial import unittest
from twisted.internet import task, defer

from txpoloniex.queue import RateLimit

RATE_LIMIT=6

class RateLimitTests(unittest.TestCase):
    def setUp(self):
        self.clock = task.Clock()
        self.queue = RateLimit(RATE_LIMIT)
        self.queue.reactor = self.clock
        self.count = 0

    def _increment(self):
        self.count += 1
        #return defer.succeed(self.count)

    def _flush(self):
        """
        Flush state for a clean testing slate
        """
        self.count = 0
        self.queue.clear()

    def test_run(self):
        """
        Run a single job
        """
        self._flush()

        d = self.queue.run(self._increment)

        self.assertEqual(self.queue._times, [self.clock.seconds()])

        self.clock.advance(0.1)

        self.assertEqual(self.count, 1)

        return d

    def test_clear(self):
        """
        Add a job to the queue and test clearing
        """
        self._flush()
    
        d = self.queue.run(self._increment)

        self.queue.clear()

        self.assertEqual(self.queue.waiting, [])
        self.assertEqual(self.queue._times, []) 
        self.assertEqual(self.queue._expirations, []) 

    def test_wait(self):
        """
        Add enough jobs to induce a wait
        """
        self._flush()

        dl = []
        for i in range(RATE_LIMIT):
            d = self.queue.run(self._increment)
            dl.append(d)

        self.clock.advance(0.4)

        self.assertEqual(len(self.queue._times), RATE_LIMIT) 

        self.assertEqual(self.queue._nextDelay(), 0.6) 

        self.clock.advance(self.queue._nextDelay())

        self.assertEqual(self.queue._nextDelay(), 0.0) 
