from functools import partial

from txpoloniex import base, commands, queue, util

class ConfigError(Exception):
    def __init__(self, api_key, secret):

        missing = []

        if not api_key:
            missing.append('api_key')

        if not secret:
            missing.append('secret')

        self.message = 'Missing necessary {missing}'.format(
            missing=' and '.join(missing)
        )

    def __str__(self):
        return self.message

class Poloniex(base.PoloniexBase, queue.RateLimitMixin):

    MAX_REQS_PER_SECOND = 6

    def __init__(self, api_key='', secret=''):
        base.PoloniexBase.__init__(self, api_key, secret)

        self.setLimit(self.MAX_REQS_PER_SECOND)
        self.addHandler(self.requestPublic, commands.PUBLIC)

        def error(*args, **kwargs):
            raise ConfigError(api_key, secret)

        if not api_key or not secret:
            self.addHandler(error, commands.PRIVATE)
        else:
            self.addHandler(self.requestPrivate, commands.PRIVATE)

    def addHandler(self, handler, endpoints):
        """
        Add all endpoints as functions
        """
        for endpoint in endpoints:
            name = util.format_function(endpoint)
            self.log.trace('Adding {name} handler', name=name)
            func = partial(self.addQueue, handler, endpoint)
            setattr(self, name, func)
