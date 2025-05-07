from django.shortcuts import render
from django.http import HttpResponse
import finnhub
from decouple import config      
import time           
import requests             
from concurrent.futures import ThreadPoolExecutor, as_completed
from asgiref.sync import sync_to_async                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
# Create your views here.
def stock_picker(request):
    stocks=[]
    with open('popular_nasdaq_stocks.csv','r') as f:
        for line in f:
            name,ticker=line.split(',')
            ticker=ticker[:-1]
            stocks.append({name:ticker})
    # print(stocks)
    
    # nasdaq_stocks = [stock for stock in data if stock.get("mic") == "XNAS"]
    # print(nasdaq_stocks)
    # print(stock_tickers)
    context={
        'stock_tickers':stocks[1:]
    }
    return render(request,'stockpicker.html',context)

@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True

def format_market_cap(market_cap_millions):
    cap = market_cap_millions * 1_000_000  # Convert to actual number
    if cap >= 1_000_000_000_000:
        return f"${cap / 1_000_000_000_000:.2f}T"
    elif cap >= 1_000_000_000:
        return f"${cap / 1_000_000_000:.2f}B"
    elif cap >= 1_000_000:
        return f"${cap / 1_000_000:.2f}M"
    else:
        return f"${cap:,.0f}"  # Show full number if less than 1M

def fetch_stock_data(finnhub_client, stock):
    try:
        ticker, name = stock.split('|')
        details = finnhub_client.quote(ticker)
        profile = finnhub_client.company_profile2(symbol=ticker)
        marketcap = format_market_cap(profile.get('marketCapitalization'))

        return name, {
            'ticker': ticker,
            'price': details.get('c'),
            'change': round(details.get('c') - details.get('pc'), 2),
            'mcap': marketcap
        }
    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")
        return stock.split('|')[1], None

    
async def stock_tracker(request):
    is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
    stocks_data = {}
    if request.method == 'POST':
        stocks = request.POST.getlist('stocks')
        finnhub_client = finnhub.Client(api_key=config('finhub_api_key'))
        start_time=time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_stock_data, finnhub_client, stock) for stock in stocks]
            for future in as_completed(futures):
                name, data = future.result()
                if data:
                    stocks_data[name] = data
        end_time=time.time()
        # print(end_time-start_time)
    context = {
        'stocks_data': stocks_data,
        'room_name':'track',
        'stocks':stocks
        }
    return render(request, 'stocktracker.html', context)
