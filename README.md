# 📈 Auto Stock Trader (QuantModel)

This is an **automated stock trading simulation** that predicts stock growth trends and simulates purchases based on **monthly investments** and **risk levels**. The system utilizes **real-time stock data** via `yfinance` and visualizes predicted trends using `matplotlib`.

---

## 📌 Features
- **Automates stock selection** based on risk level.
- **Fetches real stock data** using `yfinance`.
- **Simulates monthly stock purchases** based on past performance.
- **Predicts and visualizes growth trends** using `matplotlib`.
- **User-friendly GUI** built with `tkinter`.

---

## 🏗️ Project Structure
```
quantmodel/
├── gui.py              # User interface with tkinter
├── trader.py           # AutoStockTrader logic
├── utils.py            # Helper functions (e.g., share calculations)
├── main.py             # Entry point for running the app
├── requirements.txt    # Dependencies list
└── README.md           # Project documentation
```

---

## ⚙️ Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/quantmodel.git
cd quantmodel
```

### 2️⃣ Install Dependencies
Make sure you have Python 3 installed. Then, install the required libraries:
```bash
pip install -r requirements.txt
```
Alternatively, install them manually:
```bash
pip install yfinance numpy matplotlib tkinter
```

### 3️⃣ Run the Application
```bash
python main.py
```

---

## 📂 Code Overview

### 🎛️ `main.py` (Application Entry)
```python
from gui import StockApp
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    app = StockApp(root)
    root.mainloop()
```
- Initializes the **tkinter GUI** for stock simulation.

---

### 🖥️ `gui.py` (Graphical User Interface)
Handles user input and displays results.
```python
import matplotlib.pyplot as plt
from tkinter import Label, Entry, Button, messagebox
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
```

---

### 📊 `trader.py` (Auto Stock Trading Logic)
Fetches stock data and simulates purchases.
```python
import datetime
import yfinance as yf
import numpy as np
from utils import calculate_shares

class AutoStockTrader:
    def __init__(self, monthly_investment, risk_level):
        self.monthly_investment = monthly_investment
        self.risk_level = risk_level
        self.history = []
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

        for stock_symbol in stock_choices:
            stock_prices, stock_dates = self.get_stock_prices_last_year(stock_symbol)
            growth_rates[stock_symbol] = self.calculate_monthly_growth(stock_prices, stock_dates)

            for month in range(months):
                growth_rate = growth_rates[stock_symbol][month % len(growth_rates[stock_symbol])]
                self.all_trends.append({
                    'date': (start_date + datetime.timedelta(days=30 * month)).strftime('%Y-%m-%d'),
                    'stock': stock_symbol,
                    'growth': growth_rate * 100
                })

    def get_stock_choices(self):
        if self.risk_level < 1:
            return self.stocks['low_risk']
        elif self.risk_level == 1:
            return self.stocks['medium_risk']
        else:
            return self.stocks['high_risk']
```

---

## 💡 Future Enhancements
✅ Add **real-time buy/sell execution**  
✅ Implement **stop-loss and take-profit strategies**  
✅ Integrate **machine learning for stock predictions**  

---

## 🏆 Contributors
- **Nate Cirino**  
- Open-source contributions are welcome! Feel free to submit a **pull request**.  

---

## 📜 License
This project is open-source and available under the **MIT License**.

---

### ⭐ Show Some Support!
If you found this useful, please **star** 🌟 this repository and **fork** 🍴 it to contribute!  
