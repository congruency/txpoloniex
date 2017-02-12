"""
Summarize deposits, withdrawals, and trade history.
"""

from decimal import *
from datetime import datetime, timedelta
from time import mktime

from twisted.internet import task, defer

from txpoloniex import Poloniex

def balancesBTCTotal(balances):
    btc_values = (Decimal(b['btcValue']) for b in balances.values())
    return sum(btc_values)

def balancesTotals(entries):
    totals = {}

    for currency in entries:
        entry = entries[currency]
        orders = Decimal(entry['onOrders'])
        available = Decimal(entry['available'])
        btc_value = Decimal(entry['btcValue'])
        totals[currency] = {
            'amount': orders + available,
            'btcValue': btc_value,
        }

    return totals

def depositWithdrawalTotals(entries):
    totals = {
        'total': {}
    }

    for method in ['deposits', 'withdrawals']:

        totals[method] = {}

        for entry in entries[method]:
            currency = entry['currency']
            amount = Decimal(entry['amount'])

            if not currency in totals[method]:
                totals[method][currency] = 0

            totals[method][currency] += amount

            if not currency in totals['total']:
                totals['total'][currency] = 0

            if method == 'deposits':
                totals['total'][currency] += amount
            else:
                totals['total'][currency] -= amount

    return totals

def tradeHistoryTotals(entries):
    totals = {}

    for pair in entries:
        primary, secondary = pair.split('_')

        for currency in (primary, secondary):
            if not currency in totals:
                totals[currency] = {
                    'amount': 0,
                    'fees': 0,
                }

        for trade in entries[pair]:
            trade_type = trade['type']
            amount = Decimal(trade['amount'])
            total = Decimal(trade['total'])

            if trade_type == 'buy':
                fees = amount * Decimal(trade['fee'])
                totals[primary]['amount'] -= total
                totals[secondary]['amount'] += amount - fees
                totals[secondary]['fees'] += fees

            elif trade_type == 'sell':
                fees = total * Decimal(trade['fee'])
                totals[primary]['amount'] += total - fees
                totals[primary]['fees'] += fees
                totals[secondary]['amount'] -= amount

            else:
                print('Encountered unknown trade type')

    return totals

def totals(balances, deposits_withdrawals, trade_history, show=True):
    dw_totals = depositWithdrawalTotals(deposits_withdrawals)

    th_totals = tradeHistoryTotals(trade_history)

    bal_totals = balancesTotals(balances)

    return dw_totals, th_totals, bal_totals

def display(dw_totals, th_totals, bal_totals):
    dw_title = '{:>6}{:>20}{:>20}{:>20}'
    dw_row = '{:>6}{: 20.8f}{: 20.8f}{: 20.8f}'
    print('\nDeposit and withdrawal totals:')
    print(dw_title.format('Name', 'Deposits', 'Withdrawals', 'Total'))
    for currency in sorted(dw_totals['total'].keys()):
        d_total = dw_totals['deposits'].get(currency, 0)
        w_total = dw_totals['withdrawals'].get(currency, 0)
        total = dw_totals['total'][currency]
        print(dw_row.format(currency, d_total, w_total, total))

    print('\n--------------------------\n')

    print('Trade totals:')
    th_title = '{:>6}{:>20}{:>20}{:>20}'
    th_row = '{:>6}{: 20.8f}{: 20.8f}{: 20.8f}'
    print(th_title.format('Name', 'Amount', 'Fees paid', 'Discrepancy'))
    for currency in sorted(th_totals.keys()):
        total = th_totals[currency]
        profits = total['amount'] + dw_totals['total'].get(currency, 0)

        if bal_totals[currency]:
            profits -= bal_totals[currency]['amount']

        print(th_row.format(currency, total['amount'], total['fees'], profits))

    print('\nNOTE: Discrepancy is likely due to rounding errors')

    print('\n--------------------------\n')

    print('Balances totals:')
    bt_title = '{:>6}{:>20}{:>20}'
    bt_row = '{:>6}{: 20.8f}{: 20.8f}'
    print(bt_title.format('Name', 'Amount', 'BTC value'))
    for currency in bal_totals:
        total = bal_totals[currency]

        if not total['amount']:
            continue

        print(bt_row.format(currency, total['amount'], total['btcValue']))

    print('{:>6}{: 40.8f}'.format('Total:', balancesBTCTotal(bal_totals)))

@defer.inlineCallbacks
def acquire(reactor, start='0000000000', end='9999999999'):
    api_key = 'YOUR_API_KEY'
    secret = 'YOUR_SECRET'

    p = Poloniex(api_key, secret)

    balances = yield p.completeBalances(account='all')
    deposits_withdrawals = yield p.depositsWithdrawals(start=start, end=end)
    trade_history = yield p.tradeHistory(currencyPair='all', start=start, end=end)

    display(*totals(balances, deposits_withdrawals, trade_history))

task.react(acquire)
