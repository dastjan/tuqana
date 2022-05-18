from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from newspaper import Article

def get_article_info(url):
    req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
    resp = urlopen(req)    
    publish_date = BeautifulSoup(resp, features="lxml").find('time')['datetime']
    a = Article(url)
    a.download()
    a.parse()
    return publish_date, a.title, a.text

def find_press_release(ticker):
    print(f'Retrieve most recent press release of {ticker}')
    url = f"https://finance.yahoo.com/quote/{ticker}/press-releases?p={ticker}"
    base_url = "https://finance.yahoo.com"    
    req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
    resp = urlopen(req)    
    html = BeautifulSoup(resp, features="lxml")
    news_table = html.find(id='summaryPressStream-0-Stream')
    if len(news_table.find_all(href=True)) > 0:        
            href_tags = news_table.find_all(href=True)
            tag = href_tags[0]
            url = base_url + tag['href']
            publish_date, title, text = get_article_info(url)
            articles = ticker, publish_date, title, text, url
            return articles
    else:
        return None   
    
if __name__ == '__main__':
    news = find_press_release('TSLA')
    
