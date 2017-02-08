Twisted wrapper for the Poloniex API
====================================

- **code**: https://github.com/congruency/txpoloniex
- Apache License 2.0
- Tested with Python 3.5.2
- depends on `Twisted 16.6 <https://twistedmatrix.com>`_

Introduction
------------

txpoloniex is a lightweight wrapper for the `Poloniex API
<https://poloniex.com/support/api/>`_. Endpoints are mapped
to functions in an instantiated Poloniex class. Parameters to these
endpoints are *not* mapped. However, you can specify any parameter
as a keyword argument and they will be passed.

Calls are queued after 6 per second, but otherwise execute as quickly as possible.

Example use
-----------

.. sourcecode:: python

    from twisted.internet import task

    from txpoloniex import Poloniex

    p = Poloniex(api_key='', secret='')

    def balances(reactor):
        d = p.availableAccountBalances()
        d.addCallback(print)
        return d

    task.react(balances)

.. code-block:: shell-session

    % python3 examples/balance.py
    {'exchange': {'ZEC': '0.00199121', 'ETH': '4.00199121', 'BTC': '0.79774165'}}

Donate
------

- BTC: 12BBRhcyZtzSYQ45pvuyWBsDjM9hmxNLrY
- ETH: 0x32320d939c9f715f9edb9ec725b013b551dc6ebd
- ZEC: t1c5dxfN8L3EfUFSGn4zLBBLByvLwi5gQiR
