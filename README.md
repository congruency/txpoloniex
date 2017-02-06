# txpoloniex
Minimalist Twisted wrapper for the Poloniex API

API: https://poloniex.com/support/api/

# Rate limiting

Calls are queued after 6 per second, but otherwise execute as quickly as possible.

# Example use
```python
from twisted.internet import task

from txpoloniex import Poloniex

p = Poloniex(api_key='', secret='')

def balances(reactor):
    d = p.availableAccountBalances()
    d.addCallback(print)
    return d

task.react(balances)
```

```bash
% python3 test.py
{'exchange': {'ZEC': '0.00199121', 'ETH': '4.00199121', 'BTC': '0.79774165'}}
```

# Donate

BTC: 12BBRhcyZtzSYQ45pvuyWBsDjM9hmxNLrY
ETH: 0x32320d939c9f715f9edb9ec725b013b551dc6ebd
ZEC: t1c5dxfN8L3EfUFSGn4zLBBLByvLwi5gQiR
