import lxml
from lxml import html
import requests
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.expand_frame_repr', False)

def scrape_table(url):
    # Fetch the page that we're going to parse
    page = requests.get(url)
    tree = html.fromstring(page.content)
    tables = tree.findall('.//*/table')
    df = pd.read_html(lxml.etree.tostring(tables[0], method='html'))[0]
    return df

# macrotrend analysis
stock_list = ["AAPL/apple","MSFT/microsoft",'AMZN/amazon',"TSLA/tesla","NVDA/nvidia","FB/facebook","GOOGL/alphabe","JPM/jpmorgan-chase","C/citigroup","BCS/barclays","NFLX/netflix","BA/boeing"]
# ychart analysis
stocks = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA", "FB", "GOOG", "JPM", "C", "BCS", "NFLX","BA","PFE"]

# company is for decideing which website to take
# company 2 just the full for the company to plot the diagrams
def get_url(company,company2):
    for s in stock_list:
        if s == company:
            # macro
            url = ["https://www.macrotrends.net/stocks/charts/" + s + "/pe-ratio","https://www.macrotrends.net/stocks/charts/"+ s +"/eps-earnings-per-share-diluted","https://www.macrotrends.net/stocks/charts/"+s+"/price-book" ]
            for ll in url:
                if ll == "https://www.macrotrends.net/stocks/charts/" + s + "/pe-ratio":
                    data = requests.request("GET",ll)
                    url_completo = data.url
                    hist = scrape_table(url_completo)
                    hist = hist.sort_index(ascending=False)
                    print(hist)
                    # print the name of the columns
                    #print(hist.columns)
                    x =hist[company2+ ' PE Ratio Historical Data',        'Date']
                    y = hist[company2+' PE Ratio Historical Data',    'PE Ratio']
                    z= hist[company2+' PE Ratio Historical Data', 'Stock Price']
                    plt.plot(x,y, label = "P/E ratio")
                    plt.plot(x,z, label = "stock price")
                    plt.legend()
                    plt.title(s)
                    plt.show()
                elif ll == "https://www.macrotrends.net/stocks/charts/"+ s +"/eps-earnings-per-share-diluted":
                    data = requests.request("GET", ll)
                    url_completo = data.url
                    hist = scrape_table(url_completo)
                    hist = hist.sort_index(ascending=False)
                    print(hist)
                    # print the name of the columns
                    # print(hist.columns)
                    x = hist[company2+ " Annual EPS"]
                    y = hist[company2 +" Annual EPS.1"]
                    plt.bar(x, y, label = "Eps")
                    plt.legend()
                    plt.title(s)
                    plt.show()
                elif ll == "https://www.macrotrends.net/stocks/charts/"+s+"/price-book":
                    data = requests.request("GET", ll)
                    url_completo = data.url
                    hist = scrape_table(url_completo)
                    hist = hist.sort_index(ascending=False)
                    hist.dropna()
                    # print the name of the columns
                    # print(hist.columns)
                    x = hist[company2+' Price/Book Ratio Historical Data',                 'Date']
                    y = hist[company2+' Price/Book Ratio Historical Data',  'Price to Book Ratio']
                    z = hist[company2+' Price/Book Ratio Historical Data',          'Stock Price']
                    o = hist[company2+' Price/Book Ratio Historical Data', 'Book Value per Share']
                    bvpr = []
                    for gg in o:
                        if gg == str(gg):
                            gg = gg[1:]
                            gg = float(gg)
                            bvpr.append(gg)
                        else:
                            gg = 0
                            bvpr.append(gg)
                    hist["bvpr"] = bvpr
                    zz = hist["bvpr"]
                    plt.plot(x, y, label = "p/b")
                    plt.plot(x, z, label="stock price")
                    plt.legend()
                    plt.title(s)
                    plt.show()
                    plt.bar(x, zz, label="BVPS")
                    plt.show()
        else:
            for i in stocks:
                if i == company:
                    #ychart
                    url = "https://ycharts.com/companies/"+ i +"/profit_margin"
                    data = requests.request("GET", url)
                    url_completo = data.url
                    hist = scrape_table(url_completo)
                    # sorting the date from the beginning tell the end
                    hist = hist.sort_index(ascending=False)
                    print(hist)
                    #plotting the results
                    plt.bar(hist["Data for this Date Range"],hist["Unnamed: 1"])
                    plt.show()

print(get_url("TSLA",None))


