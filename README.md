# txpoloniex
Minimalist Twisted wrapper for the Poloniex API

API: https://poloniex.com/support/api/

# Example use
```python
from twisted.internet import task

from txpoloniex import Poloniex

p = Poloniex(api_key='', secret=b'')

def balances(reactor):
    d = p.completeBalances()
    d.addCallback(print)
    return d

task.react(balances)
```
