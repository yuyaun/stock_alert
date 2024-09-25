import yfinance as yf
from datetime import datetime
import time
from notification import send_line_notify

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
    twii = yf.Ticker("^TWII")
    data = twii.history(period="1d")
    return data

# 計算漲跌幅百分比
def calculate_price_change(data):
    if len(data) == 0:
        return None, None
    open_price = data['Open'].iloc[0]  # 使用 iloc[0] 表示第一個位置
    close_price = data['Close'].iloc[0]  # 使用 iloc[0] 表示第一個位置
    price_change = ((close_price - open_price) / open_price) * 100
    return price_change, close_price

# 檢查漲跌幅並通知
def check_price_change(price_change, current_index):
    global notified
    if price_change is None:
        print("無法獲取資料")
        return

    # 獲取當前時間
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 確認漲幅或跌幅，並通知各個門檻
    for threshold in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        if abs(price_change) >= threshold and not notified[threshold]:
            if price_change > 0:
                msg = f"{current_time} 台灣加權指數 {current_index:.2f} 漲幅達到 {price_change:.2f}%，門檻：{threshold}%"
                print(f"通知: {msg}")
                send_line_notify(msg)
            else:
                msg = f"{current_time} 台灣加權指數 {current_index:.2f} 跌幅達到 {price_change:.2f}%，門檻：{threshold}%"
                print(f"通知: {msg}")
                send_line_notify(msg)
            notified[threshold] = True  # 設定該門檻為已通知
    print(f"檢查時間: {current_time} 台灣加權指數: {current_index:.2f}, 漲跌幅: {price_change:.2f}%")

def main():
    global notified
    # 每分鐘檢查一次
    while True:
        now = datetime.now()
        # 每天早上9點至下午1點之間執行檢查 (假設為台股交易時間)
        if now.hour >= 9 and now.hour < 14:
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