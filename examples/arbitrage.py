#!/usr/bin/env python
from __future__ import print_function

from decimal import *
from itertools import chain, permutations

from twisted.internet import task

from txpoloniex import Poloniex

getcontext().prec = 8
#getcontext().rounding = ROUND_FLOOR

TAKER_FEE = Decimal(0.0025)

def intertradeable(pairs):
    """
    Find all intertradeable currencies
    """
    secondaries = [x[1] for x in pairs]

    multiples = ((p, s) for p, s in pairs if secondaries.count(s) > 1)

    for primary, secondary in multiples:
        matching = [(p, s) for p, s in pairs if s == secondary]
        currencies = chain(*matching)
        yield currencies

def has_two_primary(primaries, chain):
    """
    Determine if there are two, or more, primary currencies in the chain
    """
    return len([entry for entry in chain if entry in primaries]) > 1

def valid_pairs(pairs, chain):
    """
    Determine if the chain contains any invalid pairs (e.g. ETH_XMR)
    """
    for primary, secondary in zip(chain[:-1], chain[1:]):
        if not (primary, secondary) in pairs and \
           not (secondary, primary) in pairs:
            return False
    return True

def find_routes(primaries, currencies, pairs):
    """
    Find all permutations of trade routes for pairs
    """
    discovered = []
    for c in currencies:

        for p in permutations(c, 3):

            # We want to end with the beginning currency
            p = p + (p[0],)

            if not p in discovered and \
               has_two_primary(primaries, p) and \
               valid_pairs(pairs, p):

                discovered.append(p)

                yield p

def calculate_profit(route, orderbook, pairs):
    """
    Calculate profit for a route assuming a starting amount of 1, ignoring the
    amount of coinage on the spread
    """
    amount = Decimal(1)

    def price_for(pair, trade_type):
        book = orderbook['_'.join(pair)]
        price, available = book[trade_type][0]
        return price

    for primary, secondary in zip(route[:-1], route[1:]):

        pair = (primary, secondary)

        if pair in pairs: # BUY
            price = price_for(pair, 'asks')
            amount = amount / Decimal(price) * (1 - TAKER_FEE)

        else: # SELL
            pair = (secondary, primary)
            price = price_for(pair, 'bids')
            amount = amount * Decimal(price) * (1 - TAKER_FEE)

    return amount

def calculate_arbitrage(orderbook):
    from time import time

    start = time()

    # Convert to tuple so later comparisons don't need conversion
    pairs = [tuple(x.split('_')) for x in orderbook.keys()]

    unique_primaries = set(x[0] for x in pairs)

    intertradeable_currencies = intertradeable(pairs)

    routes = find_routes(unique_primaries, intertradeable_currencies, pairs)

    for route in routes:
        route = list(route)
        amount = calculate_profit(route, orderbook, pairs)

        print('->'.join(route), amount)

    end = time()

    print('Took', int((end - start)*1000), 'ms to calculate')

def arbitrage(reactor):
    d = Poloniex().orderBook(
        currencyPair = 'all',
        depth = 1,
    )
    d.addCallback(calculate_arbitrage)
    return d

task.react(arbitrage)
