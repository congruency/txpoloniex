from __future__ import print_function

from twisted.internet import task, defer

from txpoloniex import Poloniex

@defer.inlineCallbacks
def ticker(reactor):
    """
    Print the last price for each symbol
    """
    tick = yield Poloniex().ticker()
    for pair in sorted(tick):
        last = tick[pair]['last']
        print('{pair}: {last}'.format(pair=pair, last=last))

task.react(ticker)
