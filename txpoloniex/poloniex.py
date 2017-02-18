from functools import partial

from txpoloniex import base, const, queue, util

class Poloniex:

    def __init__(self, api_key='', secret=''):

        self.public = base.PoloniexPublic()
        self.private = base.PoloniexPrivate(api_key, secret)

        self.addHandlers(self.public, const.PUBLIC_COMMANDS)
        self.addHandlers(self.private, const.PRIVATE_COMMANDS)

    def addHandlers(self, cls, endpoints):
        """
        Add all endpoints as functions
        """

        for endpoint in endpoints:
            name = util.format_function(endpoint)
            func = partial(cls.addQueue, cls.request, endpoint)
            setattr(self, name, func)
