#!/usr/bin/env python3

import json
from functools import partial

from txpoloniex.base import PoloniexBase
from txpoloniex.queue import RateLimitMixin
from txpoloniex.commands import *
from txpoloniex.util import *

PUBLIC_API = 'https://poloniex.com/public'
TRADING_API = 'https://poloniex.com/tradingApi'

class Poloniex(PoloniexBase, RateLimitMixin):

    MAX_REQS_PER_SECOND = 6

    def __init__(self, *args, **kwargs):
        PoloniexBase.__init__(self, *args, **kwargs)

        self.setLimit(self.MAX_REQS_PER_SECOND)

        # Add all commands as functions
        for command in PUBLIC:
            name = format_function(command)
            self.log.trace('Adding {name} handler', name=name)
            func = partial(self.addQueue, self.requestPublic, command)
            setattr(self, name, func)

        for command in PRIVATE:
            name = format_function(command)
            self.log.trace('Adding {name} handler', name=name)
            func = partial(self.addQueue, self.requestPrivate, command)
            setattr(self, name, func)


