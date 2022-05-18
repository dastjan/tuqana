# Discounted Cashflow Analysis

This simple code calculates the discounted cashflow (DCF) and the intrinsic value of stocks. A company is subjective to the DCF calculation if it meets one of the following citeria ([source](https://investorsgrow.com/)):

1. Company does not pay dividends
2. Company pays dividend, but dividends are very different from the company's ability to pay
3. Free cash flow aligns with profitability
4. Investor is taking a control perspective

Based on the last 4 years, the annual revenue growth is estimated and projected over 5 years. With this growth, the DCF and intrinsic share value is calculated.
## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install yfinance.

```bash
pip install yfinance
```

## Usage

Find the ticker(s) of the stock(s) you want to analyze on [Yahoo! Finance](https://finance.yahoo.com/) and enter the tickers in the code that you can find in the bottom of the file. Run and see!
```python
if __name__ == '__main__':
    # Enter your ticker(s) in the list below
    tickers = ['AAPL', 'ASML.AS']
    msg = analyze(tickers)
    print(msg)
```
## License
[MIT](https://choosealicense.com/licenses/mit/)
