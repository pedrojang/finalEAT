from numpy.core.einsumfunc import _einsum_path_dispatcher
from numpy.core.fromnumeric import trace
import pandas as pd
import ccxt
import numpy as np
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
import requests
apiKey = 'Y3dcAaJ0BtLZdQpk9YTryEaft7wQQNMPZc7UJcZAGLKRbDFbtvw2GkRGVeadkvsL'
secKey = 'DA9aVE2d9fs7QWL6YfDs7Q3mJYHblnhJoPdO4tWjbDw4kGJCXviTSlZNroF99Dk9'



lastBol_low = 0.0
lastBol_high = 0.0
binanceFUTURE = ccxt.binance(config={
    'apiKey': apiKey,
    'secret': secKey,
    'enableRateLimit': True, 
})

binanceFR = ccxt.binance(config={
    'apiKey': apiKey, 
    'secret': secKey,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

markets = binanceFR.load_markets()
symbol = "ETH/USDT"
market = binanceFR.market(symbol)
leverage = 20

resp = binanceFR.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage
})


balance = binanceFUTURE.fetch_balance(params={"type": "future"})


def btcc(day):
    btc = binanceFR.fetch_ohlcv(
        symbol="ETH/USDT", 
        timeframe='15m', 
        since=None, 
        limit=int(24*4*day+26))


    return btc

def btcc_1h():
    btc = binanceFR.fetch_ohlcv(
        symbol="ETH/USDT", 
        timeframe='1h', 
        since=None, 
        limit=61)


    return btc

def GetPD(day):
    dff = pd.DataFrame(btcc(day), columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    dff['datetime'] = pd.to_datetime(dff['datetime'], unit='ms')
    dff['datetime1'] = dff['datetime']
    dff['dec'] = dff['high'] - dff['low']
    dff['RD'] = dff['close'] - dff['open']
    dff['GS'] = dff['dec']/dff['volume']
    dff['uptail'] = dff['high'] - ((dff['open'] + dff['close'])/2 + abs(dff['RD'])/2)
    dff['downtail'] = ((dff['open'] + dff['close'])/2 - abs(dff['RD'])/2) - dff['low']
    dff['open1'] = dff['open'].shift(1)
    dff['high1'] = dff['high'].shift(1)
    dff['low1'] = dff['low'].shift(1)
    dff['close1'] = dff['close'].shift(1)
    dff['volume1'] = dff['volume'].shift(1)
    dff['dec1'] = dff['dec'].shift(1)
    dff['RD1'] = dff['RD'].shift(1)
    dff['uptail1'] = dff['uptail'].shift(1)
    dff['downtail1'] = dff['downtail'].shift(1)
    dff['GS1'] = dff['GS'].shift(1)
    dff.set_index('datetime', inplace=True)
    dff['tMA1'] = dff['close1'].rolling(window=20).mean()
    dff['tMA1'] = dff['tMA1'].round(2)
    dff['std1'] = dff['close1'].rolling(window=20).std()
    dff['tMA2'] = dff['tMA1'].shift(1)
    dff['ttMA1'] = dff['close1'].rolling(window=10).mean()
    dff['ttMA1'] = dff['ttMA1'].round(2)
    dff['ttMA2'] = dff['ttMA1'].shift(1)
    dff['mid'] = dff['open']/2 + dff['close']/2
    dff['mid1'] = dff['mid'].shift(1)
    dff['tend1'] = dff['ttMA1'] - dff['ttMA2']
    dff['tend2'] = dff['tend1'].shift(1)
    dff['mMm'] = dff['mid'] - dff['mid1']
    dff1= dff.dropna()
    dff1['bollow1'] = dff1['tMA1'] - 2*dff1['std1']
    dff1['bollow1'] = dff1['bollow1'].round(2)
    dff1['bolhigh1'] = dff1['tMA1'] + 2*dff1['std1']
    dff1['bolhigh1'] = dff1['bolhigh1'].round(2)
    dff1['bollow11'] = dff1['tMA1'] - 1.8*dff1['std1']
    dff1['bollow11'] = dff1['bollow11'].round(2)
    dff1['bolhigh11'] = dff1['tMA1'] + 1.8*dff1['std1']
    dff1['bolhigh11'] = dff1['bolhigh11'].round(2)
    dff1.isnull().sum()
    return dff1

def GetPD1h():
    dff = pd.DataFrame(btcc_1h(), columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    dff['datetime'] = pd.to_datetime(dff['datetime'], unit='ms')
    dff['dec'] = dff['high'] - dff['low']
    dff['RD'] = dff['close'] - dff['open']
    dff['GS'] = dff['dec']/dff['volume']
    dff['uptail'] = dff['high'] - ((dff['open'] + dff['close'])/2 + abs(dff['RD'])/2)
    dff['downtail'] = ((dff['open'] + dff['close'])/2 - abs(dff['RD'])/2) - dff['low']
    dff['open1'] = dff['open'].shift(1)
    dff['high1'] = dff['high'].shift(1)
    dff['low1'] = dff['low'].shift(1)
    dff['close1'] = dff['close'].shift(1)
    dff['volume1'] = dff['volume'].shift(1)
    dff['dec1'] = dff['dec'].shift(1)
    dff['RD1'] = dff['RD'].shift(1)
    dff['uptail1'] = dff['uptail'].shift(1)
    dff['downtail1'] = dff['downtail'].shift(1)
    dff['GS1'] = dff['GS'].shift(1)
    dff.set_index('datetime', inplace=True)
    dff['tMA1'] = dff['close1'].rolling(window=20).mean()
    dff['tMA1'] = dff['tMA1'].round(2)
    dff['std1'] = dff['close1'].rolling(window=20).std()
    dff['tMA2'] = dff['tMA1'].shift(1)
    dff['ttMA1'] = dff['close1'].rolling(window=10).mean()
    dff['ttMA1'] = dff['ttMA1'].round(2)
    dff['ttMA2'] = dff['ttMA1'].shift(1)
    dff['mid'] = dff['open']/2 + dff['close']/2
    dff['mid1'] = dff['mid'].shift(1)
    dff['tend1'] = dff['ttMA1'] - dff['ttMA2']
    dff['tend2'] = dff['tend1'].shift(1)
    dff1= dff.dropna()
    dff1['bollow1'] = dff1['tMA1'] - 2*dff1['std1']
    dff1['bollow1'] = dff1['bollow1'].round(2)
    dff1['bolhigh1'] = dff1['tMA1'] + 2*dff1['std1']
    dff1['bolhigh1'] = dff1['bolhigh1'].round(2)
    dff1['mMm'] = dff1['mid'] - dff1['mid1']
    dff1.isnull().sum()
    return dff1

# 고가 - 저가 
def getdec():

    lst = GetPD().dec.tolist()
    return lst

# 시가 - 종가 리스트
def getRD():
    lst = GetPD().RD.tolist()
    return lst


def mail(text,PN):
    now = datetime.now()
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('pedrojang777@gmail.com','mpgzxiggfdjbarqz')

    msg =  MIMEText(text)
    msg['Subject'] = PN + str(now)

    s.sendmail('pedrojang777@gmail.com','peter000520@naver.com',msg.as_string())

    s.quit()

def nownow():
    now = datetime.now().minute

    return now
def nowsec():
    now = datetime.now().second
    return now
def nowhour():
    NH = datetime.now().hour

    return NH

# 선물 계좌 구하기 
def BGDF():
    balance = binanceFUTURE.fetch_balance(params={"type": "future"})

    return balance['USDT']['free']
# 현재가 구하기
def getcurrent():
    symbol = "ETH/USDT"
    btc = binanceFR.fetch_ticker(symbol)
    return btc['last']

def amountgetter():
    money = BGDF()
    if BGDF() > 50000:
        money = 50000
    amountget = round(money/getcurrent(),6)*0.985
    return amountget

#롱 - 풀매수 -
def buybit(a):
    order = binanceFR.create_market_buy_order(
    symbol=symbol,
    amount=a*leverage,
)

#숏 - 풀매도 -
def sellbit(a):
    order = binanceFR.create_market_sell_order(
    symbol=symbol,
    amount=a*leverage,
)
def sellmethod(i):
    
    stut = ls_mids[i] < ls_mids[i+1] and ls_mids[i+1] < ls_mids[i+2] and ls_mids[i+2] > ls_mids[i+3]  #and ls_mids[i+3] > ls_mids[i+4] 
    stut2 = ls_mids[i] < ls_mids[i+1] and ls_mids[i+1] < ls_mids[i+2] and ls_mids[i+2] > ls_mids[i+3] and ls_close[i+3] < ls_opens[i]
    # stut3 = abs(1-(ls_close[i+4]/ls_opens[i+4])) > 0.0047 or Longpossition == True
    laststut = stut or stut2
    stut4 = ls_opens[i+2] > ls_bolhigh[i+2] or ls_opens[i+3] > ls_bolhigh[i+3]
    return laststut and stut4
def buymethod(i):
    stut = ls_mids[i] > ls_mids[i+1] and ls_mids[i+1] > ls_mids[i+2] and ls_mids[i+2] < ls_mids[i+3] #and ls_mids[i+3] < ls_mids[i+4]
    stut2 = ls_mids[i] > ls_mids[i+1] and ls_mids[i+1] > ls_mids[i+2] and ls_mids[i+2] < ls_mids[i+3] and ls_close[i+3] > ls_opens[i]
    # stut3 = abs(1-(ls_close[i+4]/ls_opens[i+4])) > 0.0047 or Shortpossition == True
    laststut = stut or stut2
    stut4 = ls_opens[i+2] < ls_bollow[i+2] or ls_opens[i+3] < ls_bollow[i+3]
    return laststut and stut4

def timechecker_15min():
    now = datetime.now().minute
    hour = datetime.now().hour
    count_15min = now//15 + hour*4
    return count_15min

def timefinder_15min(a):
    day = 0
    if a < 0:
        while a < 0:
            a = a + 96
            day = day - 1
    t = a//4
    tt = a%4
    thattime = str(t)+ ':' + str(tt*15) + '  day from now...' +str(day)
    return thattime

def timechecker_5min():
    now = datetime.now().minute
    hour = datetime.now().hour
    count_15min = now//5 + hour*12
    return count_15min

def timefinder_5min(a):
    day = 0
    if a < 0:
        while a < 0:
            a = a + (96*3)
            day = day - 1
    t = a//12
    tt = a%12
    thattime = str(t)+ ':' + str(tt*5) + '  day from now...' +str(day)
    return thattime

def newSM(i):
    stut1 = ls_ochi[i+2] <= ls_ochi[i+1+2] and ls_ochi[i+2+2] >= ls_ochi[i+3+2]  and (ls_ochi[i+3] >= ls_bolhigh[i+3] or ls_ochi[i+4] >= ls_bolhigh[i+4]) 
    stut = (ls_mids[i+3] > ls_mids[i+4] or ls_oclo[i+2] > ls_oclo[i+5]) and ls_close[i+5] > ls_bollow[i+5] and ls_close[i+3] > ls_opens[i+3] and ls_close[i+4] < ls_opens[i+4] 
    stut2 = True
    stut3 = False
    stut4 = 1 - (ls_close[i+3]/ls_opens[i+3]) < 0.008 and 1 - (ls_close[i+5]/ls_opens[i+5]) < 0.008 and 1 - (ls_close[i+4]/ls_opens[i+4]) < 0.008#and ls_oclo[i+5] > ls_ma[i+5]
    # if ls_volchg[i+3] > ls_volchg[i+4] == True:
    #     stut3 = True
    k = 0
    p = 0
    ki = 1
    while ki < 6:
        if ls_ochi[i+ki] > ls_bolhigh[i+ki]:
            k = k + 1
        if ls_close[i+ki] > ls_opens[i+ki]:
            p = p + 1
        ki = ki + 1
    if k > 2 or p > 4:
        stut2 = False
    result = (stut and stut1 and stut2 and stut4 ) or stut3#(ls_ochi[i+2] <= ls_ochi[i+1+2] and ls_ochi[i+2+2] >= ls_ochi[i+3+2] == True and stut3)
    return result

def newBM(i):
    stut1 = ls_oclo[i+2] >= ls_oclo[i+1+2] and ls_oclo[i+2+2] <= ls_oclo[i+3+2]  and ((ls_oclo[i+3] <= ls_bollow[i+3]) or (ls_oclo[i+4] <= ls_bollow[i+4])) 
    stut = (ls_mids[i+3] < ls_mids[i+4] or ls_ochi[i+2] < ls_ochi[i+5]) and ls_close[i+5] < ls_bolhigh[i+5] and ls_close[i+3] < ls_opens[i+3] and ls_close[i+4] > ls_opens[i+4] 
    stut2 = True
    stut3 = False
    stut4 = (ls_opens[i+3]/ls_close[i+3]) - 1 < 0.008 and (ls_opens[i+5]/ls_close[i+5]) - 1 < 0.008 and (ls_opens[i+4]/ls_close[i+4]) - 1 < 0.008#and ls_ochi[i+5] < ls_ma[i+5]
    # if ls_volchg[i+3] < ls_volchg[i+4] == True:
    #     stut3 = True
    k = 0
    p = 0
    ki = 1
    while ki < 6:
        if ls_oclo[i+ki] < ls_bollow[i+ki]:
            k = k + 1
        if ls_close[i+ki] < ls_opens[i+ki]:
            p = p + 1
        ki = ki + 1
    if k > 2 or p > 4:
        stut2 = False
    result = (stut and stut1 and stut2 and stut4) or stut3 #(ls_oclo[i+2] >= ls_oclo[i+1+2] and ls_oclo[i+2+2] <= ls_oclo[i+3+2] == True and stut3)
    return result 

def newMTG(i):
    resultLP = (LP == True and ls_close[i+1] < ls_bollow[i+1] and ls_close[i+2] < ls_bollow[i+2] and ls_close[i+3] < ls_bollow[i+3] and ls_close[i+4] < ls_bollow[i+4] and ls_close[i+5] < ls_bollow[i+5])
    resultSP = (SP == True and ls_close[i+1] > ls_bolhigh[i+1] and ls_close[i+2] > ls_bolhigh[i+2] and ls_close[i+3] > ls_bolhigh[i+3] and ls_close[i+4] > ls_bolhigh[i+4] and ls_close[i+5] > ls_bolhigh[i+5])
    # 30K 이상 거래량 보일때 멈추는 것 만들기 
    result = resultLP or resultSP
    return result

def MTGGBM(i):
    stut1 = ls_ochi[i+5] > ls_bolhigh1[i+5] and ls_ochi[i+4] > ls_bolhigh1[i+4]#and ls_oclo[i+5] > ls_ma[i+5] 
    stut2 = (ls_close[i+5]/ls_opens[i+5]) > 1.008
    stut3 = LP == False and SP == False
    stut4 = ls_vol[i+5] < 150000
    return (stut1 and stut2) and stut3 and stut4

def MTGGSM(i):# 볼린저 넓이와 관련지어 설명해볼것
    stut1 = ls_oclo[i+5] < ls_bollow1[i+5] and ls_oclo[i+4] < ls_bollow1[i+4] #and ls_ochi[i+5] < ls_ma[i+5]
    stut2 = (ls_close[i+5]/ls_opens[i+5]) < 0.992
    stut3 = LP == False and SP == False
    stut4 = ls_vol[i+5] < 150000
    return stut1 and stut2 and stut3 and stut4
def stut3SM(i):
    stut3 = False
    if LP == True and (buynum*(1+dd) < getcurrent() or getcurrent() > ls_bolhigh1[i+5]) and MTGG == False and MTG == False:
        stut3 = True
    return stut3
def stut3BM(i):
    stut3 = False
    if SP == True and (sellnum*(1-dd) > getcurrent() or getcurrent() < ls_bollow1[i+5]) and MTGG == False and MTG == False:
        stut3 = True
    return stut3

dd = 0.02
ddd = 0.01
ddddd = 0.28
actiontime = -1
summary = ''
Shortpossition = False
Longpossition = False
nfornothing = 30000
STARTtime = datetime(1,1,1,9,30)
ENDtime = datetime(1,1,1,9,30)
ki = 0
proF = 1
proFP = 1
SP = False
LP = False
leverF = 20
MTG = False
MTGS = False
MTGG = False

actiontime = nownow()
etherinfo = GetPD(2)
ls_mids = etherinfo.mid.tolist()
ls_opens = etherinfo.open.tolist()
ls_close = etherinfo.close.tolist()
ls_mMm = etherinfo.mMm.tolist()
ls_bollow = etherinfo.bollow1.tolist()
ls_bolhigh = etherinfo.bolhigh1.tolist()
ls_bollow1 = etherinfo.bollow11.tolist()
ls_bolhigh1 = etherinfo.bolhigh11.tolist()
ls_ma = etherinfo.tMA1.tolist()
ls_ma2 = etherinfo.tMA2.tolist()
ls_tend1 = etherinfo.tend1.tolist()
ls_tend2 = etherinfo.tend2.tolist()
ls_high = etherinfo.high.tolist()
ls_low = etherinfo.low.tolist()
ls_vol = etherinfo.volume.tolist()
ls_DT = etherinfo.datetime1.tolist()
CTF = -1
while CTF > -1*len(ls_DT):
    asdf = datetime.now() - ls_DT[CTF] - (datetime(1,1,1,9) - datetime(1,1,1))
    if asdf < (datetime(1,1,1,9,30) - datetime(1,1,1,9)) and asdf >= (datetime(1,1,1,9,15) - datetime(1,1,1,9)):
        CorrectTime = CTF
        break
    else :
        CTF = CTF - 1
ls_ochi = []
ls_oclo = []
ki = 0
while ki < len(ls_opens):
    if ls_opens[ki] <= ls_close[ki]:
        ls_ochi.append(ls_close[ki])
        ls_oclo.append(ls_opens[ki])
    else:
        ls_ochi.append(ls_opens[ki])
        ls_oclo.append(ls_close[ki])
    ki = ki + 1

text = 'Good Luck!!'
title = 'Program started!!'
mail(text,title)
print('Program started!! \n Good Luck!!')
while True:
    try:
        if nownow()%15 == 0 :
            time.sleep(0.5)  # 15분마다 한번씩 행동하는 것 (15분으로 나누어 떨어지지 않을 시 행동하지 않음)
            if not(actiontime == nownow()):
                actiontime = nownow()
                etherinfo = GetPD(2)
                ls_mids = etherinfo.mid.tolist()
                ls_opens = etherinfo.open.tolist()
                ls_close = etherinfo.close.tolist()
                ls_mMm = etherinfo.mMm.tolist()
                ls_bollow = etherinfo.bollow1.tolist()
                ls_bolhigh = etherinfo.bolhigh1.tolist()
                ls_bollow1 = etherinfo.bollow11.tolist()
                ls_bolhigh1 = etherinfo.bolhigh11.tolist()
                ls_ma = etherinfo.tMA1.tolist()
                ls_ma2 = etherinfo.tMA2.tolist()
                ls_tend1 = etherinfo.tend1.tolist()
                ls_tend2 = etherinfo.tend2.tolist()
                ls_high = etherinfo.high.tolist()
                ls_low = etherinfo.low.tolist()
                ls_vol = etherinfo.volume.tolist()
                ls_DT = etherinfo.datetime1.tolist()
                CTF = -1
                while CTF > -1*len(ls_DT):
                    asdf = datetime.now() - ls_DT[CTF] - (datetime(1,1,1,9) - datetime(1,1,1))
                    if asdf < (datetime(1,1,1,9,30) - datetime(1,1,1,9)) and asdf >= (datetime(1,1,1,9,15) - datetime(1,1,1,9)):
                        CorrectTime = CTF
                        break
                    else :
                        CTF = CTF - 1
                ls_ochi = []
                ls_oclo = []
                ki = 0
                while ki < len(ls_opens):
                    if ls_opens[ki] <= ls_close[ki]:
                        ls_ochi.append(ls_close[ki])
                        ls_oclo.append(ls_opens[ki])
                    else:
                        ls_ochi.append(ls_opens[ki])
                        ls_oclo.append(ls_close[ki])
                    ki = ki + 1
                if MTG == False and MTGG == False:
                    if newBM(CorrectTime - 5):
                        if LP == False and SP == False and ENDtime + (datetime(1,1,1,9,30) - datetime(1,1,1,9)) <= datetime.now():
                            beforetrade = BGDF()
                            LP = True
                            PN = amountgetter()
                            buybit(PN)
                            buynum = getcurrent()
                            text = 'Before trade: ' + str(beforetrade) + '\n' + 'buynum: ' + str(buynum)
                            title = 'Long possiton started'
                            mail(text,title)
                            STARTtime = datetime.now()
                        if SP == True:
                            SP = False
                            buybit(PN)
                            buynum = getcurrent()
                            time.sleep(1)
                            aftertrade = BGDF()
                            text = 'After trade: ' + str(aftertrade) + '\n' + 'buynum: ' + str(buynum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                            title = 'Short possition Endded'
                            mail(text,title)
                            ENDtime = datetime.now()
                    if newSM(CorrectTime - 5):
                        if LP == False and SP == False and ENDtime + (datetime(1,1,1,9,30) - datetime(1,1,1,9)) <= datetime.now():
                            beforetrade = BGDF()
                            SP = True
                            PN = amountgetter()
                            sellbit(PN)
                            sellnum = getcurrent()
                            text = 'Before trade: ' + str(beforetrade) + '\n' + 'sellnum: ' + str(sellnum)
                            title = 'Short possiton started'
                            STARTtime = datetime.now()
                            mail(text,title)
                        if LP == True:
                            LP = False 
                            sellbit(PN)
                            sellnum = getcurrent()
                            time.sleep(1)
                            aftertrade = BGDF()
                            text = 'After trade: ' + str(aftertrade) + '\n' + 'sellnum: ' + str(sellnum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                            title = 'Long possition Endded'
                            mail(text,title)
                            ENDtime = datetime.now()
                    if newMTG(CorrectTime - 5):
                        MTG = True
                        MTGS = True
                        if LP == True:
                            LP = False 
                            sellbit(PN)
                            sellnum = getcurrent()
                            time.sleep(2)
                            aftertrade = BGDF()
                            text = 'After trade: ' + str(aftertrade) + '\n' + 'sellnum: ' + str(sellnum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                            title = 'MTG-L'
                            mail(text,title)
                            print('possition END')
                        if SP == True:
                            SP = False
                            buybit(PN)
                            buynum = getcurrent()
                            time.sleep(2)
                            aftertrade = BGDF()
                            text = 'After trade: ' + str(aftertrade) + '\n' + 'buynum: ' + str(buynum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                            title = 'MTG-S'
                            mail(text,title)
                if MTG == True:
                    if MTGS == True:
                        MTGtime = 0
                        MTGS = False
                    if MTGS == False and MTGtime > 5:
                        MTG = False
                    if MTGS == False:
                        MTGtime = MTGtime + 1
                if MTGG == True:
                    if (LP == True and (ls_ochi[CorrectTime] < ls_bolhigh1[CorrectTime] or ls_high[CorrectTime] > ls_bolhigh1[CorrectTime]*1.03)):
                        LP = False
                        MTGG = False
                        sellbit(PN)
                        sellnum = getcurrent()
                        aftertrade = BGDF()
                        text = 'After trade: ' + str(aftertrade) + '\n' + 'sellnum: ' + str(sellnum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                        title = 'P - sell'
                        mail(text,title)
                        print('possition END')
                    if (SP == True and (ls_oclo[CorrectTime] > ls_bollow1[CorrectTime]or ls_low[CorrectTime] < ls_bollow1[CorrectTime]*0.97)):
                        SP = False
                        MTGG = False
                        buybit(PN)
                        buynum = getcurrent()
                        aftertrade = BGDF()
                        text = 'After trade: ' + str(aftertrade) + '\n' + 'buynum: ' + str(buynum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                        title = 'P - buy'
                        mail(text,title)
                        print('possition END')
                if MTGGBM(CorrectTime - 5): 
                    LP = True
                    MTGG = True
                    beforetrade = BGDF()
                    PN = amountgetter()
                    buybit(PN)
                    buynum = getcurrent()
                    text = 'Before trade: ' + str(beforetrade) + '\n' + 'buynum: ' + str(buynum)
                    title = 'P-BUY'
                    mail(text,title)
                if MTGGSM(CorrectTime - 5):
                    SP = True
                    MTGG = True
                    beforetrade = BGDF()
                    PN = amountgetter()
                    sellbit(PN)
                    sellnum = getcurrent()
                    text = 'Before trade: ' + str(beforetrade) + '\n' + 'sellnum: ' + str(sellnum)
                    title = 'P-SELL'
                    mail(text,title)
                if LP == True and STARTtime + (datetime(1,1,1,9,30) - datetime(1,1,1,9)) > datetime.now() and STARTtime + (datetime(1,1,1,9,15) - datetime(1,1,1,9)) <= datetime.now() and ls_oclo[CorrectTime] < ls_oclo[CorrectTime]:
                    LP = False 
                    sellbit(PN)
                    sellnum = getcurrent()
                    time.sleep(1)
                    aftertrade = BGDF()
                    text = 'After trade: ' + str(aftertrade) + '\n' + 'sellnum: ' + str(sellnum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                    title = 'BD-S'
                    mail(text,title)
                if SP == True and STARTtime + (datetime(1,1,1,9,30) - datetime(1,1,1,9)) > datetime.now() and STARTtime + (datetime(1,1,1,9,15) - datetime(1,1,1,9)) <= datetime.now() and ls_ochi[CorrectTime] > ls_ochi[CorrectTime]:
                    SP = False
                    buybit(PN)
                    buynum = getcurrent()
                    time.sleep(1)
                    aftertrade = BGDF()
                    text = 'After trade: ' + str(aftertrade) + '\n' + 'buynum: ' + str(buynum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
                    title = 'BD-L'
                    mail(text,title)
                asdfasdfasdf = str(LP)+'|'+str(SP)+'|'+str(ls_close[CorrectTime])
                asdfasdfasdf = str(asdfasdfasdf)
                print(asdfasdfasdf)
        time.sleep(0.5)
        if LP == True and getcurrent() > ls_bolhigh[CorrectTime]*1.002 and getcurrent() > buynum*1.02:
            LP = False
            sellbit(PN)
            sellnum = getcurrent()
            time.sleep(1)
            aftertrade = BGDF()
            text = 'After trade: ' + str(aftertrade) + '\n' + 'sellnum: ' + str(sellnum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
            title = 'MAX get by long p'
            mail(text,title)
            print('possition END')
        if SP == True and getcurrent() < ls_bollow[CorrectTime]*0.998 and getcurrent() < sellnum*0.98:
            SP = False
            buybit(PN)
            buynum = getcurrent()
            time.sleep(1)
            aftertrade = BGDF()
            text = 'After trade: ' + str(aftertrade) + '\n' + 'buynum: ' + str(buynum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
            title = 'MAX get by short p'
            mail(text,title)
            print('possition END')
        if stut3SM(CorrectTime - 5): # 밖으로 빠져야함 
            LP = False 
            sellbit(PN)
            sellnum = getcurrent()
            time.sleep(1)
            aftertrade = BGDF()
            text = 'After trade: ' + str(aftertrade) + '\n' + 'sellnum: ' + str(sellnum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
            title = 'Long possition Endded'
            mail(text,title)
            ENDtime = datetime.now()
        if stut3BM(CorrectTime - 5):
            SP = False
            buybit(PN)
            buynum = getcurrent()
            time.sleep(1)
            aftertrade = BGDF()
            text = 'After trade: ' + str(aftertrade) + '\n' + 'buynum: ' + str(buynum) + '\n' + 'Profit: ' + str(aftertrade/beforetrade)
            title = 'Short possition Endded'
            mail(text,title)
            ENDtime = datetime.now()
    except Exception as e:
       print(e)
       time.sleep(1)

       # 코드 아이채크 할것-> 반복문이 일정 시간 이상 걸릴 경우 전봉이 나타나지 않고 다음봉이 나타나는 현상이 나타남 -> 일정한 정도 차이나는 범위에 있는 분봉을 가져 오도록 프로그래밍
       # 슬랙으로 15분 마다 알림 받을 수 있도록 설정할것 
       # MTGG and newBM 바꿀것
       
       