from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
import copy
class StockConsumer(AsyncWebsocketConsumer):
    def get_celery_models(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        return PeriodicTask, IntervalSchedule

    @sync_to_async
    def addToCeleryBeat(self, stockpicker):
        PeriodicTask,IntervalSchedule=self.get_celery_models()
        task = PeriodicTask.objects.filter(name = "every-10-seconds")
        if len(task)>0:
            print("hello")  # testing that task.first() will work or not
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in stockpicker:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(every=10, period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule, name='every-10-seconds', task="mainapp.tasks.update_stock", args = json.dumps([stockpicker]))

    @sync_to_async    
    def addToStockDetail(self, stock_list):
        from .models import StockDetail
        user = self.scope["user"]
        for stock in stock_list:
            # ticker,name=stock.split('|')
            stock, created = StockDetail.objects.get_or_create(stock = stock)
            stock.user.add(user)
            
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"WebSocket CONNECTED: {self.room_name}")
        query_string = self.scope['query_string'].decode()  # bytes to str
        query_params = parse_qs(query_string)

        # Now get the 'stocks' parameter
        stocks_param = query_params.get('stocks', [])
        if stocks_param:
            stock_list = stocks_param[0].split('-') 
            # add user to stockdetail
            await self.addToCeleryBeat(stock_list)
            await self.addToStockDetail(stock_list)
            
            
        else:
            print("No stocks provided in query string")
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': f"Welcome to {self.room_name}!"
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        # print(f"Received: {stocks}")
        
        # distributing the data across the rooms
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_stock_update',
                'data': data
            }
        )
    @sync_to_async   
    def helper_func(self):
        from .models import StockDetail
        PeriodicTask,IntervalSchedule=self.get_celery_models()
        user = self.scope["user"]
        stocks = StockDetail.objects.filter(user__id = user.id)
        task = PeriodicTask.objects.get(name = "every-10-seconds")
        args = json.loads(task.args)
        print(args)
        args = args[0]
        for i in stocks:
            i.user.remove(user)
            if i.user.count() == 0:
                args.remove(i.stock)
                i.delete()
        if args == None:
            args = []

        if len(args) == 0:
            task.delete()
        else:
            task.args = json.dumps([args])
            task.save()


    async def disconnect(self, close_code):
        print(f"WebSocket DISCONNECTED: {self.room_name}")
        await self.helper_func()
        
        # leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    @sync_to_async
    def selectUserStocks(self):
        user = self.scope["user"]
        user_stocks = user.stockdetail_set.values_list('stock', flat = True)
        return list(user_stocks)
    
    async def send_stock_update(self, event):
        stocks = event['data']
        stocks = copy.copy(stocks)

        user_stocks = await self.selectUserStocks()
        user_stocks=[stock.split('|')[1] for stock in user_stocks]
        keys = stocks.keys()
        for key in list(keys):
            if key in user_stocks:
                pass
            else:
                del stocks[key]

        # Send message to WebSocket
        print('i m sending data to websocket ')
        await self.send(text_data=json.dumps(stocks))
