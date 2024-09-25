import yfinance as yf
from datetime import datetime
import time
from notification import send_line_notify

from dotenv import load_dotenv
import os
load_dotenv()

name = os.getenv("STOCK_NAME")
ticker = os.getenv("STOCK_TICKER")

start_time = 1
end_time = 24

# 設置一個字典來追蹤每個漲跌幅的通知狀態
notified = {
    0.5: False,
    1.0: False,
    1.5: False,
    2.0: False,
    2.5: False,
    3.0: False,
    3.5: False,
    4.0: False,
    4.5: False,
    5.0: False
}

# 抓取台灣加權指數資料 (台股指數的代碼 "^TWII")
def get_twii_data():
    global ticker
    twii = yf.Ticker(ticker)
    data = twii.history(period="5d")
    return data

# 計算漲跌幅百分比
def calculate_price_change(data):
    if len(data) < 2:
        return None, None
    open_price = data['Close'].iloc[-2]  # 上一個交易日的收盤價
    close_price = data['Close'].iloc[-1]  # 當前的收盤價
    price_change = ((close_price - open_price) / open_price) * 100
    return price_change, close_price

# 檢查漲跌幅並通知
def check_price_change(price_change, current_index):
    global notified, name
    if price_change is None:
        print("無法獲取資料")
        return

    # 獲取當前時間
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 確認漲幅或跌幅，並通知各個門檻
    for threshold in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        if abs(price_change) >= threshold and not notified[threshold]:
            if price_change > 0:
                msg = f"{name} {current_index:.2f} 漲幅達到 {price_change:.2f}%，門檻：{threshold}% (數據有15分鐘延遲)"
                print(f"通知: {msg}")
                send_line_notify(msg)
            else:
                msg = f"{name} {current_index:.2f} 跌幅達到 {price_change:.2f}%，門檻：{threshold}% (數據有15分鐘延遲)"
                print(f"通知: {msg}")
                send_line_notify(msg)
            notified[threshold] = True  # 設定該門檻為已通知
    print(f"檢查時間: {current_time} {name}: {current_index:.2f}, 漲跌幅: {price_change:.2f}%")

def main():
    global notified, start_time, end_time
    # 每分鐘檢查一次
    while True:
        now = datetime.now()
        if now.hour >= start_time and now.hour < end_time:
            data = get_twii_data()
            price_change, current_index = calculate_price_change(data)
            check_price_change(price_change, current_index)
        else:
            # 超過交易時間後，重置通知狀態，準備第二天的通知
            notified = {0.5: False, 1.0: False, 1.5: False, 2.0: False, 2.5: False, 3.0: False, 3.5: False, 4.0: False, 4.5: False, 5.0: False}
            print("非交易時間，通知狀態已重置。")
        
        time.sleep(60)  # 每分鐘檢查一次

if __name__ == "__main__":
    main()