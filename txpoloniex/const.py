"""
Constant values for the Poloniex API
"""

PUBLIC_API = 'https://poloniex.com/public'
PRIVATE_API = 'https://poloniex.com/tradingApi'

PUBLIC_COMMANDS = [
    'returnTicker',
    'return24hVolume',
    'returnOrderBook',
    'returnTradeHistory',
    'returnChartData',
    'returnCurrencies',
    'returnLoanOrders',
]

PRIVATE_COMMANDS = [
    'returnBalances',
    'returnCompleteBalances',
    'returnDepositAddresses',
    'generateNewAddress',
    'returnDepositsWithdrawals',
    'returnOpenOrders',
    'returnTradeHistory',
    'returnAvailableAccountBalances',
    'returnTradableBalances',
    'returnOpenLoanOffers',
    'returnOrderTrades',
    'returnActiveLoans',
    'returnLendingHistory',
    'createLoanOffer',
    'cancelLoanOffer',
    'toggleAutoRenew',
    'buy',
    'sell',
    'cancelOrder',
    'moveOrder',
    'withdraw',
    'returnFeeInfo',
    'transferBalance',
    'returnMarginAccountSummary',
    'marginBuy',
    'marginSell',
    'getMarginPosition',
    'closeMarginPosition',
]

DATE_FORMAT='%Y-%m-%d %H:%M:%S'
