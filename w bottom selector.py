from multiprocessing.dummy import Pool
import tushare.pro
import technical_analysis as ta
import requests.exceptions
import time
from tqdm import tqdm

pro = tushare.pro_api('eeafdc95319fcce0ebd4a2ed3e5dbf8ff767c85e53affc867df701ce')


def get_data(code, end_date):
    while True:
        try:
            daily_data = pro.daily(ts_code=code, start_date='20180717', end_date=end_date,
                              fields='ts_code,trade_date,open,high,low,close,vol,amount')
            break
        except requests.exceptions.ReadTimeout:
            time.sleep(5)
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            pass
    return daily_data
end_date = input('您想选择的周期长度是：')


'''
len_of_period = int((input('您想选择的周期长度是：')))
difference = float(input('您想选择的两个周期的最低点差异大小是：'))
amount_of_change = float(input('您想选择的价格回调的程度是：'))
f = open('codes.txt', 'w')
content = f'您选择的周期长度是：{len_of_period} \n您选择的两个周期的最低点差异大小是：{difference} \n您选择的价格回调的程度是：{amount_of_change} \n'
f.write(content)
f.close()
'''

def searching(code):
    daily_data = get_data(code, end_date)
    try:
        result = ta.w_bottom(code, daily_data, lenth_of_period=15)

        if result:
            print(code)
            f = open('codes.txt', 'a')
            f.write(code + "\n\n")
            f.close()

    except:
        print(code)
        pass




pool = Pool()

print('600000——600499')
pool.map(searching, ['600' + str(x) + str(y) + str(z) + '.SH' for x in range(5) for y in range(10) for z in range(10)])

print('休息中')
time.sleep(70)
print('\n\n')

print('600500——600999')
pool.map(searching, ['600' + str(x) + str(y) + str(z) + '.SH' for x in range(5, 10) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('601000——601499')
pool.map(searching, ['601' + str(x) + str(y) + str(z) + '.SH' for x in range(5) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('601500——601999')
pool.map(searching, ['601' + str(x) + str(y) + str(z) + '.SH' for x in range(5, 10) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('300000——300799')
pool.map(searching, ['300' + str(x) + str(y) + str(z) + '.SZ' for x in range(8) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('000000——000499')
pool.map(searching, ['000' + str(x) + str(y) + str(z) + '.SZ' for x in range(5) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('000500——000999')
pool.map(searching, ['000' + str(x) + str(y) + str(z) + '.SZ'for x in range(5, 10) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('001000——001499')
pool.map(searching, ['001' + str(x) + str(y) + str(z) + '.SZ' for x in range(5) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('001500——001999')
pool.map(searching, ['001' + str(x) + str(y) + str(z) + '.SZ'for x in range(5, 10) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('002000——002499')
pool.map(searching, ['002' + str(x) + str(y) + str(z) + '.SZ'for x in range(5) for y in range(10) for z in range(10)])
print('休息中')
time.sleep(70)
print('\n\n')

print('002500——002999')
pool.map(searching, ['002' + str(x) + str(y) + str(z) + '.SZ'for x in range(5, 10) for y in range(10) for z in range(10)])
print('搜索完成')

