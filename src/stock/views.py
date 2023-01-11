from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import WlSearchForm
from django.http import HttpResponseRedirect

from .models import Stock, Trade
from .forms import StockSearchForm, TradeForm
import pandas as pd
from pandas_datareader import data as pdr
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from django.utils.timezone import make_aware
import datetime
import yfinance as yf
yf.pdr_override()


import json
from os.path import dirname
filename_STOCK_DIC = dirname(__file__) + '/stock_dic.json'
with open(filename_STOCK_DIC, 'rb') as f:
    STOCK_DIC = json.load(f)
filename_JAPANESE_TICKERS = dirname(__file__) + "/japanese_tickers.json"
JAPANESE_TICKERS = json.load(open(filename_JAPANESE_TICKERS,'r'))

def get_exchange_list():
    df = pdr.get_data_yahoo("USDJPY=X", period="max")
    l=[]
    ex = df["Close"].tolist()
    d = [ str(x).split(' ')[0] for x in df["Close"].index.tolist() ]
    l.append(ex)
    l.append(d)
    return l

def recent_rate(*args):
    now = datetime.date.today()
    yst = now - datetime.timedelta(days=5)
    tom = now + datetime.timedelta(days = 1)
    l = []
    for ticker in args:
        a = {}
        df = pdr.get_data_yahoo(ticker, start=yst, end=tom)
        cs = df.loc[:, "Close"].tolist()
        d = cs[-1] - cs[-2]
        t = d/cs[0]*100
        a["ticker"] = ticker
        a["fluc"] = t
        l.append(a)
    return l

class IndexView(TemplateView):
    template_name = 'stock/index.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        c["tab"] = int(self.request.GET.get('tab'))
        tradelist = Trade.objects.prefetch_related('stock').filter(user=self.request.user)
        buy_list = tradelist.filter(sell=False)
        sell_list = tradelist.filter(sell=True)
        total_buy = 0
        total_sell = 0
        for item in buy_list:
            total_buy += item.price * item.amount
        for item in sell_list:
            total_sell += item.price * item.amount
        c["total_buy"] = total_buy
        c["total_sell"] = total_sell
        c["total_asset"] = total_sell - total_buy
        assetlist = []     # for 保有銘柄 tab
        d={}
        dl = {}
        for item in tradelist:
            ss = {}
            j = json.loads(item.stock.json)
            ss["trade"] = item
            ss["json"] = j
            if j["ticker"]+".T" in JAPANESE_TICKERS: # if JPY
                ss["total"] = j["close"][-1] * item.amount
                ss["price_today"] = j["close"][-1]
                ss["profit"] = ss["total"] - item.price * item.amount
                ss["profit_percent"] = (ss["total"] - item.price * item.amount)*100 / (item.price * item.amount)
                ss["currency"] = "JPY"
            else:
                exl = get_exchange_list() # [[ex], [date]]
                ex = '1996-10-30'
                for i in range(7):
                    target_date = str(datetime.datetime.date(item.trade_date) - datetime.timedelta(-i))
                    b = target_date in exl[1] # その日付が存在すれば
                    if not b:
                        continue
                    else:
                        ex = exl[1].index(target_date)
                        break
                ss["total"] = j["close"][-1] * item.amount * exl[0][-1]
                ss["price_today"] = j["close"][-1]
                ss["profit"] = ss["total"] - item.price * item.amount * ex
                ss["profit_percent"] = (ss["total"] - item.price * item.amount * ex)*100 / (item.price * item.amount)
                ss["currency"] = "USD"
            assetlist.append(ss)
            # for tradingview graph
            for i,data in enumerate(j["close"]):
                date = j["date"][i].split("T")[0]
                if not dl.get(date):
                    dl[date] = data
        watchlist = []
        for x in Stock.objects.filter(watch_user = self.request.user):
            d = json.loads(x.json)
            if d["ticker"]+".T" in JAPANESE_TICKERS: # JPY-USD  hantei
                d["currency"] = 'JPY'
            else:
                d["currency"] = 'USD'
            watchlist.append(d)
        c["WlSearchForm"] = WlSearchForm
        c["TradeForm"] = TradeForm
        c["assetlist"] = assetlist
        c["watchlist"] = watchlist
        c["tradelist"] = tradelist
        c["data_list"] = dl # for tradingview graph
        return c

def ticker_to_json(t):
    ticker = t[0]
    df = pdr.get_data_yahoo(ticker,period="max")
    data = {}
    d = df["Close"]
    close = list(d)
    date = [datetime.datetime.isoformat(x) for x in d.index.tolist()]
    p1 =  int(close[-1])
    p2 = int(close[-2])
    fluc = p1 - p2
    pfluc = fluc / p2
    data["ticker"] = ticker.split(".")[0]
    data["fluc"] = fluc
    data["pfluc"] = pfluc
    data["name"] = t[1]
    data["close"] = close
    data["date"] = date
    return data

def add_wl(request):
    sname = request.POST.get('stock_name')
    t = STOCK_DIC[sname]
    ticker = t[0] # xxxx.T など
    stock_name = t[1]
    if t:
        try:
            s = Stock.objects.get(stock_id=ticker)
        except:
            d = ticker_to_json(ticker) # get data from yahoo
            data = json.dumps(d)
            s = Stock.objects.create(stock_id = ticker, json = data)
        s.watch_user.add(request.user)
    else:
        r = "no ticker"
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def trade(request):
    sname = request.POST.get('stock_name')
    t = STOCK_DIC[sname]
    ticker = t[0]
    sell = request.GET.get('sell')
    trade_date = request.POST.get('trade_date')
    price = request.POST.get('price')
    if t:
        amount = request.POST.get('amount')
        try:
            s = Stock.objects.get(stock_id=ticker)
        except:
            d = ticker_to_json(t) # get data from yahoo
            data = json.dumps(d)
            s = Stock.objects.create(stock_id = ticker, json = data)
        Trade.objects.create(stock=s, amount=amount, user=request.user, price=price, sell=sell, trade_date=trade_date)
    else:
        r = "no ticker"
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_trade(request, pk):
    t = Trade.objects.get(pk=pk)
    if t.user == request.user:
        t.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class StockSearchView(FormView):
    form_class = StockSearchForm
    template_name = 'stock/search.html'
    success_url = reverse_lazy('stock:search')

    posted_data = {'stock_id': ""}

    def form_valid(self, form):
        self.posted_data['stock_id'] = form.data.get('stock_id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currdt = make_aware(datetime.datetime.now())
        now = str(currdt.year) + '-' + str(currdt.month) + '-' + str(currdt.day)
        try:
            ticker_info = yf.Ticker(self.posted_data['stock_id'])
            df = ticker_info.history(period='max')
            date = [d.strftime('%Y-%m-%d') for d in df.index]
            close = df.loc[:, 'Close'].tolist()
            a = []
            context["stock_id"] = self.posted_data['stock_id']
            for n in range(len(df)):
                b = {}
                b["date"] = date[n]
                b["close"] = close[n]
                a.append(b)
            context["data_list"] = a
        except:
            a = [{"date":now, "close":0}]
            context["data_list"] = a
            context["er"] = "sorry, there was no stock data you indicated"
        return context

def add_to_post(request):
    title = request.POST.get('title')
    category = request.POST.get('category')
    content = request.POST.get('content')
    form_data = {}
    form_data["title"] = title
    form_data["category"] = category
    form_data["content"] = content
    sname =  request.POST.get("tickerinput")
    t = STOCK_DIC[sname]
    ticker = t[0]
    if ticker+".T" in JAPANESE_TICKERS: # if JPY
        pass
    else:
        ticker = ticker.lower()
    with open(dirname(__file__) + "/jsons_close_only/" + str(ticker) + ".json") as f:
        j = json.load(f)
    del j[0]
    data_list = {}
    for item in j:
        date = list(item.items())[0][0]
        date = datetime.datetime.strptime(date, '%Y%m%d')
        date = format(date, '%Y-%m-%d')
        data_list[date] = list(item.items())[0][1]
    request.session["data_list"] = data_list
    request.session["form_data"] = form_data
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))