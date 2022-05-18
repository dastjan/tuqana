# Stock Press Release Scraper

This code scrapes the latest press release from any stock on [Yahoo! Finance](https://finance.yahoo.com/)

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install newspaper & beautifulsoup4.

```bash
pip install newspaper
pip install bs4
```

## Usage

Find the ticker of the stock you want to scrape on [Yahoo! Finance](https://finance.yahoo.com/) and enter the ticker in the code that you can find in the bottom of the file. 

It returns a tuple with 5 elements:
1. Ticker;
2. Timestamp;
3. Title;
4. Content;
5. URL.


Run and see!

```python
if __name__ == '__main__':
    news = find_press_release('TSLA')
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
