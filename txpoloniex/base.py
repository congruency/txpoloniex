import hmac
from hashlib import sha512
from io import BytesIO
from time import time
from urllib.parse import urlencode

from twisted.logger import Logger
from twisted.internet import reactor, defer
from twisted.web.client import Agent, HTTPConnectionPool, \
     FileBodyProducer, ContentDecoderAgent, GzipDecoder
from twisted.web.http_headers import Headers

from txpoloniex import const, util, queue

class PoloniexBase(queue.RateLimitMixin):

    log = Logger()

    connectTimeout = 1.0

    maxPerSecond = 6

    pool = HTTPConnectionPool(reactor)

    agent = ContentDecoderAgent(
        Agent(
            reactor,
            connectTimeout=connectTimeout,
            pool=pool
        ),
        [(b'gzip', GzipDecoder)],
    )

class PoloniexPrivate(PoloniexBase):

    lock = defer.DeferredLock()

    def __init__(self, api_key, secret):

        self.api_key = api_key
        self.secret = secret
        self.nonce = int(time() * 1000)

    @util.to_json
    def request(self, command, **kwargs):
        """
        Submit a request to the private, authenticated, endpoint
        """
        if not self.api_key or not self.secret:
            raise

        self.nonce += 1

        kwargs.update({
            'command': command,
            'nonce': self.nonce,
        })

        method = 'POST'

        url = const.PRIVATE_API

        args = urlencode(kwargs).encode('utf-8')

        body = FileBodyProducer(BytesIO(args))

        sign = hmac.new(
            self.secret.encode('utf-8'),
            args,
            sha512
        )

        headers = {
            'Sign': [sign.hexdigest()],
            'Key': [self.api_key],
            'Content-Type': ['application/x-www-form-urlencoded'],
        }

        d = self.lock.run(self.agent.request,
            method.encode('utf-8'),
            url.encode('utf-8'),
            Headers(headers),
            body,
        )

        return d

class PoloniexPublic(PoloniexBase):

    @util.to_json
    def request(self, command, **kwargs):
        """
        Submit a request to the public endpoint
        """

        kwargs.update({'command': command})

        method = 'GET'

        args = urlencode(kwargs)

        url = '{uri}?{args}'.format(uri=const.PUBLIC_API, args=args)

        d = self.agent.request(
            method.encode('utf-8'),
            url.encode('utf-8'),
        )

        return d

