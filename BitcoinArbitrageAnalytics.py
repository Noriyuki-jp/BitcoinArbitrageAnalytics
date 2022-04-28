# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:16:46 2022

@author: Noriyuki
"""

#import(モジュールを宣言)
import ccxt #複数の仮想通貨取引所のAPIライブラリ
import time #sleep関数を使用する為
from pprint import pprint #処理内容をコンソールに出力する為
import csv #ビットコインの価格をCSVファイルへ書込む為
import datetime #日時取得の為
import requests #Get関数でHTMLデータを読込む為
import sys #終了処理の為

#定数定義
CYCLESLEEP = 5 #スリープ秒
CYCLEEND = 60 #繰返す回数 5秒×60回 = 300秒 (5分)
FILEPATH = 'TickerData.csv' #ファイル名

#CCXTの情報取得
bitbankCCXT = ccxt.bitbank()    #ビットバンク
bitflyerCCXT = ccxt.bitflyer()  #ビットフライヤー
liquidCCXT = ccxt.liquid()      #リキッド
coincheckCCXT = ccxt.coincheck() #コインチェック
zaifCCXT = ccxt.zaif() #ザイフ
 #GMOcoin,BITBOXはCCXTが用意されていない為、URL指定
urlGmo = 'https://api.coin.z.com/public/v1/ticker?symbol=BTC_JPY'#GMOコイン
urlBitbox = 'https://www.btcbox.co.jp/api/v1/tickers'#ビットボックス

def main(argv):
    # 引数の処理
    Cycleend = 0
    if len(argv) >= 2:
        Cycleend = argv[1]
    else:
        Cycleend = CYCLEEND
        
    Cyclesleep = 0
    if len(argv) >= 3:
        Cyclesleep = argv[2]
    else:
        Cyclesleep = CYCLESLEEP   

    print('繰返し回数:' + str(Cycleend))
    print('待機秒:' + str(Cyclesleep))

    #csvモジュールで書込み
    with open(FILEPATH, 'a', newline='') as f: #ファイルオープン
        writer = csv.writer(f)
        #CSVヘッダー
        writer.writerow(['時刻', 'bitbank', 'bitFlyer', 'liquid', 'Coincheck', 'Zaif', 'GMOcoin' ,'BITBOX'])
        
        #カウント初期化
        cycleCount = 1
        while cycleCount <= int(Cycleend): #定数定義された回数までループ
            #ビットコインの値取得
            bitbank = bitbankCCXT.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" }) #CCXTでビットバンクの価格取得
            bitflyer = bitflyerCCXT.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" }) #CCXTでビットフライヤーの価格取得
            liquid = liquidCCXT.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" }) #CCXTでリキッドの価格取得
            coincheck = coincheckCCXT.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" }) #CCXTでコインチェックの価格取得
            zaif = zaifCCXT.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" }) #CCXTでザイフの価格取得
            gmoRes = requests.get(urlGmo) #GMOコインのAPIでGMOコインの価格取得
            bitboxRes = requests.get(urlBitbox) #ビットボックスのAPIでビットボックスの価格取得
            
            dt = datetime.datetime.now().strftime('%H:%M:%S') #時刻を変数に代入
            bitbankLast = int(bitbank["last"]) #ビットバンクの終値を変数に代入
            bitflyerLast = int(bitflyer["last"]) #ビットフライヤーの終値を変数に代入
            liquidLast = int(liquid["last"]) #リキッドの終値を変数に代入
            coincheckLast = int(coincheck["last"]) #コインチェックの終値を変数に代入
            zaifLast = int(zaif["last"]) #ザイフの終値を変数に代入
            gmoLast = int(gmoRes.json()["data"][0]["last"]) #GMOコインの終値を変数に代入
            bitboxLast = int(bitboxRes.json()["BTC_JPY"]["last"]) #ビットボックスの終値を変数に代入
            
            #csvファイルへ書込み
            writer.writerow([dt, bitbankLast, bitflyerLast, liquidLast, coincheckLast, zaifLast, gmoLast, bitboxLast])
                
            #csvファイルへ書込まれた値をコンソールで確認用
            pprint(str(cycleCount) + " [" + str(dt) + "] [" + str(bitbankLast) + "] [" + str(bitflyerLast) + "] [" + str(liquidLast) + "] [" + str(coincheckLast) + "] [" + str(zaifLast) + "] [" + str(gmoLast) + "] [" + str(bitboxLast) + "]")
            #回数をカウントアップ
            cycleCount += 1
            #5秒待機
            time.sleep(int(Cyclesleep))
    #終了
    sys.exit()
    
if __name__ == '__main__':
    choice = input("実行します。よろしいですか？ [y/n]: ").lower()
    if choice in ['y', 'Y']:
        main(sys.argv)
    elif choice in ['n', 'N']:
        sys.exit()
    