from functools import partial

from txpoloniex import base, commands, queue, util

class Poloniex(base.PoloniexBase, queue.RateLimitMixin):

    MAX_REQS_PER_SECOND = 6

    def __init__(self, *args, **kwargs):
        base.PoloniexBase.__init__(self, *args, **kwargs)

        self.setLimit(self.MAX_REQS_PER_SECOND)

        # Add all commands as functions
        for command in commands.PUBLIC:
            name = util.format_function(command)
            self.log.trace('Adding {name} handler', name=name)
            func = partial(self.addQueue, self.requestPublic, command)
            setattr(self, name, func)

        for command in commands.PRIVATE:
            name = util.format_function(command)
            self.log.trace('Adding {name} handler', name=name)
            func = partial(self.addQueue, self.requestPrivate, command)
            setattr(self, name, func)


