from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def find_insider_trades(ticker):
    try:
        url = f"https://finviz.com/quote.ashx?t={ticker}"    
        req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
        resp = urlopen(req)    
        html = BeautifulSoup(resp, features="lxml")
        rows = html.find_all(class_='insider-row')    
        entries = []
        for row in rows:
            hrefs = row.find_all(href=True)
            href = [href['href'] for href in hrefs if 'sec' in href['href']]
            columns = row.find_all('td')
            entry = [c.text for c in columns]
            entry.append(href[0])
            entries.append(entry)            
    except:
        entries = None
    return entries

if __name__ == '__main__':
    insider_trades = find_insider_trades('TSLA')
