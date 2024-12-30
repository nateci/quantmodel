import matplotlib.pyplot as plt
from tkinter import Label, Entry, Button, messagebox, Toplevel, Text, Scrollbar, END
from trader import AutoStockTrader

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
            self.plot_trends(trader)
            self.display_summary(trader)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_trends(self, trader):
        dates = [trend['date'] for trend in trader.all_trends]
        growths = [trend['growth'] for trend in trader.all_trends]
        stocks = [trend['stock'] for trend in trader.all_trends]

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
