# Insider trades

This code scrapes insider trades from [finviz](https://finviz.com/):

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install beautifulsoup.

```bash
pip install bs4
```

## Usage

Find the ticker of the stock you want to scrape on [finviz](https://finviz.com/) and enter the tickers in the code that you can find in the bottom of the file. Run and see!
```python
if __name__ == '__main__':
    insider_trades = find_insider_trades('TSLA')
```
## License
[MIT](https://choosealicense.com/licenses/mit/)
