import datetime
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel, Text, Scrollbar, END

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
            if dates[i].month != dates[i - 1].month:  # Detect new month
                growth = (prices[i] - prices[i - 1]) / prices[i - 1]
                monthly_growth.append(growth)
        return monthly_growth

    def simulate_purchases(self, months):
        stock_choices = self.get_stock_choices()
        start_date = datetime.datetime.now()
        growth_rates = {}
        prices = {}

        # Calculate growth rates for each stock based on historical monthly patterns
        for stock_symbol in stock_choices:
            stock_prices, stock_dates = self.get_stock_prices_last_year(stock_symbol)
            growth_rates[stock_symbol] = self.calculate_monthly_growth(stock_prices, stock_dates)
            prices[stock_symbol] = stock_prices[-1]  # Last known price for reference

            # Save all trends for graphing
            for month in range(months):
                growth_rate = growth_rates[stock_symbol][month % len(growth_rates[stock_symbol])]
                self.all_trends.append({
                    'date': (start_date + datetime.timedelta(days=30 * month)).strftime('%Y-%m-%d'),
                    'stock': stock_symbol,
                    'growth': growth_rate * 100
                })

        # Determine best stock each month based on past patterns
        for month in range(months):
            purchase_date = start_date + datetime.timedelta(days=30 * month)
            best_stock = None
            best_growth = float('-inf')

            for stock_symbol in stock_choices:
                # Repeat growth rates if months exceed 12 (for predictions beyond a year)
                growth_rate = growth_rates[stock_symbol][month % len(growth_rates[stock_symbol])]
                if growth_rate > best_growth:
                    best_growth = growth_rate
                    best_stock = stock_symbol

            # Calculate price and shares based on growth rate
            predicted_price = prices[best_stock] * (1 + best_growth)
            shares = self.calculate_shares(self.monthly_investment, predicted_price)
            prices[best_stock] = predicted_price  # Update price for next prediction

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

    def plot_trends(self):
        dates = [trend['date'] for trend in self.all_trends]
        growths = [trend['growth'] for trend in self.all_trends]
        stocks = [trend['stock'] for trend in self.all_trends]

        plt.figure(figsize=(10, 6))
        for stock in set(stocks):
            stock_dates = [dates[i] for i in range(len(stocks)) if stocks[i] == stock]
            stock_growths = [growths[i] for i in range(len(stocks)) if stocks[i] == stock]
            plt.plot(stock_dates, stock_growths, marker='o', linestyle='-', label=stock)

        plt.xlabel('Date')
        plt.ylabel('Growth Percentage (%)')
        plt.title('Predicted Growth Trends by Symbol')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def display_summary(self):
        summary_window = Toplevel()
        summary_window.title("Investment Summary")

        text_area = Text(summary_window, wrap='none', height=20, width=80)
        scrollbar_y = Scrollbar(summary_window, orient='vertical', command=text_area.yview)
        scrollbar_x = Scrollbar(summary_window, orient='horizontal', command=text_area.xview)
        text_area.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        text_area.insert(END, f"{'Date':<15}{'Stock':<10}{'Growth %':<10}{'Price':<10}{'Shares':<10}\n")
        text_area.insert(END, f"{'-'*60}\n")
        for record in self.history:
            text_area.insert(END, f"{record['date']:<15}{record['stock']:<10}{record['growth']:<10.2f}${record['price']:<10.2f}{record['shares']:<10.4f}\n")

        text_area.pack(side='left', fill='both', expand=True)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')

# GUI Application
class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Stock Trader")

        Label(root, text="Monthly Investment ($):").grid(row=0, column=0)
        Label(root, text="Risk Level (0.5-2.0):").grid(row=1, column=0)
        Label(root, text="Months to Simulate:").grid(row=2, column=0)

        self.investment_entry = Entry(root)
        self.risk_entry = Entry(root)
        self.months_entry = Entry(root)

        self.investment_entry.grid(row=0, column=1)
        self.risk_entry.grid(row=1, column=1)
        self.months_entry.grid(row=2, column=1)

        Button(root, text="Simulate", command=self.run_simulation).grid(row=3, column=0, columnspan=2)

    def run_simulation(self):
        try:
            investment = float(self.investment_entry.get())
            risk = float(self.risk_entry.get())
            months = int(self.months_entry.get())

            trader = AutoStockTrader(investment, risk)
            trader.simulate_purchases(months)
            trader.plot_trends()
            trader.display_summary()

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = Tk()
    app = StockApp(root)
    root.mainloop()
