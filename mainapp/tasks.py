from celery import shared_task
import finnhub
from concurrent.futures import ThreadPoolExecutor, as_completed
from decouple import config
from mainapp.views import fetch_stock_data  # make sure this is not request-dependent
from channels.layers import get_channel_layer
import asyncio
import simplejson as json

@shared_task(bind=True)
def update_stock(self, stockpicker):
    stocks_data = {}
    finnhub_client = finnhub.Client(api_key=config('finhub_api_key'))

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_stock_data, finnhub_client, stock) for stock in stockpicker]

        for future in as_completed(futures):
            try:
                name, data = future.result()
                if data:
                    stocks_data[name] = data
            except Exception as e:
                print(f"Error fetching stock data: {e}")

    # You could optionally save stocks_data to your DB or cache here
    # print("Updated stock data:", stocks_data)
     # send data to group
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type': 'send_stock_update',
        'data': stocks_data,
    }))
    
    return "Done"
