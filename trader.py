import datetime
import yfinance as yf
import numpy as np

class AutoStockTrader:
    def __init__(self, monthly_investment, risk_level):
        self.monthly_investment = monthly_investment
        self.risk_level = risk_level
        self.history = []
        self.predictions = []
        self.all_trends = []
        self.stocks = {
            'low_risk': ['JNJ', 'PG', 'KO', 'PEP', 'WMT', 'UNH'],
            'medium_risk': ['AAPL', 'MSFT', 'V', 'GOOGL', 'MA', 'HD'],
            'high_risk': ['TSLA', 'NVDA', 'AMD', 'NFLX', 'SQ', 'CRWD']
        }

    def get_stock_prices_last_year(self, stock_symbol):
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1y")
        return data['Close'].tolist(), data.index.tolist()

    def calculate_monthly_growth(self, prices, dates):
        monthly_growth = []
        for i in range(1, len(prices)):
            if dates[i].month != dates[i - 1].month:
                growth = (prices[i] - prices[i - 1]) / prices[i - 1]
                monthly_growth.append(growth)
        return monthly_growth

    def simulate_purchases(self, months):
        stock_choices = self.get_stock_choices()
        start_date = datetime.datetime.now()
        growth_rates = {}
        prices = {}

        for stock_symbol in stock_choices:
            stock_prices, stock_dates = self.get_stock_prices_last_year(stock_symbol)
            growth_rates[stock_symbol] = self.calculate_monthly_growth(stock_prices, stock_dates)
            prices[stock_symbol] = stock_prices[-1]

            for month in range(months):
                growth_rate = growth_rates[stock_symbol][month % len(growth_rates[stock_symbol])]
                self.all_trends.append({
                    'date': (start_date + datetime.timedelta(days=30 * month)).strftime('%Y-%m-%d'),
                    'stock': stock_symbol,
                    'growth': growth_rate * 100
                })

        for month in range(months):
            purchase_date = start_date + datetime.timedelta(days=30 * month)
            best_stock = None
            best_growth = float('-inf')

            for stock_symbol in stock_choices:
                growth_rate = growth_rates[stock_symbol][month % len(growth_rates[stock_symbol])]
                if growth_rate > best_growth:
                    best_growth = growth_rate
                    best_stock = stock_symbol

            predicted_price = prices[best_stock] * (1 + best_growth)
            shares = self.calculate_shares(self.monthly_investment, predicted_price)
            prices[best_stock] = predicted_price

            self.history.append({
                'date': purchase_date.strftime('%Y-%m-%d'),
                'stock': best_stock,
                'price': predicted_price,
                'growth': best_growth * 100,
                'shares': shares
            })

    def calculate_shares(self, investment, price):
        return investment / price if price else 0

    def get_stock_choices(self):
        if self.risk_level < 1:
            return self.stocks['low_risk']
        elif self.risk_level == 1:
            return self.stocks['medium_risk']
        else:
            return self.stocks['high_risk']
