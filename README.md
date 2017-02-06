# txpoloniex
Minimalist Twisted wrapper for the Poloniex API

API: https://poloniex.com/support/api/

# Rate limiting

Calls are queued after 6 per second, but otherwise execute as quickly as possible.

# Example use
```python
from twisted.internet import task

from txpoloniex import Poloniex

p = Poloniex(api_key='', secret=b'')

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
