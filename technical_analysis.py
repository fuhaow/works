import indicators
import tushare as ts

# 蜡烛的颜色;
def colour(data):
    if data.close[0] > data.open[0]:
        return 'red'
    elif data.close[0] < data.open[0]:
        return 'blue'
    elif data.close[0] == data.open[0]:
        return 'star'

# 判断所处趋势的位置：
def position(data):
    if data.open[2] > data.open[0] or data.close[2] > data.open[0]:
        return 'trough'
    else:
        return 'peak'

# 计算蜡烛的大小：
def size(data):
    max = data.high.max()
    candle_size = abs(data.close[0] - data.open[0]) / max
    return candle_size

# MACD dif 大于 0 且 dif 大于 dea
def weekly_MACD(data):
    if indicators.MACD_diff(data)[0] > 0 and indicators.MACD_diff(data)[0] > indicators.MACD_dea(data)[0]:
        return True
    else:
        return False

# 跳空高开
def jump(data, n):
    if data.low[0] > data.high[1]:
        if (data.open[0]-data.close[1] / data.close[1]) * 100 > n:
            return True

# 站上250MA：
def MA250(data):
    ma250 = indicators.MA(data.close, 250)
    if data.low > ma250[0]:
        return True

# 锤子线和上吊线
def hammer_hanging(data):
    if position(data) == 'trough':
        if colour(data) == 'red' and abs(data.open[0] - data.low[0]) / abs(data.close[0] - data.open[0]) >= 2 and abs(data.close[0] - data.high[0]) / abs(data.close[0] - data.open[0]) <= 0.5:
            return 'hammer'
        elif colour(data) == 'blue' and abs(data.close[0] - data.low[0]) / abs(data.close[0] - data.open[0]) >= 2 and abs(data.open[0] - data.high[0]) / abs(data.close[0] - data.open[0]) <= 0.5:
            return 'hammer'
        elif colour(data) == ' star':
            return 'hammer'
    elif position(data) == 'peak':
        if colour(data) == 'red' and abs(data.open[0] - data.low[0]) / abs(data.close[0] - data.open[0]) >= 2 and abs(data.close[0] - data.high[0]) / abs(data.close[0] - data.open[0]) <= 0.5:
            return 'hanging'
        elif colour(data) == 'blue' and abs(data.close[0] - data.low[0]) / abs(data.close[0] - data.open[0]) >= 2 and abs(data.open[0] - data.high[0]) / abs(data.close[0] - data.open[0]) <= 0.5:
            return 'hanging'
        elif colour(data):
            return 'hanging'

# 吞没形态

def engulf(data):
    if size(data) >= 0.05:
        if position(data) == 'trough':
            if data.close[0] >= data.open[1] >= data.close[1] >= data.open[0]:
                return '看涨吞没'
            elif data.open[1] >= data.close[0] >= data.open[0] >= data.close[1]:
                return '看涨吞没'
            elif data.close[0] >= data.close[1] >= data.open[1] >= data.open[0] and (data.close[0] - data.open[0]) / (data.close[1] - data.open[1]) >= 3:
                return '看涨吞没'
            elif data.open[0] < data.close[1] < data.close[0] < data.open[1]:
                return '刺进形态'
            elif data.close[1] > data.open[0] > data.close[0] > data.open[1]:
                return '刺进形态'

        elif position(data) == 'peak':
            if data.open[0] >= data.close[1] >= data.open[1] >= data.close[0]:
                return '看跌吞没'
            elif data.close[1] >= data.open[0] >= data.close[0] >= data.open[1]:
                return '看跌吞没'
            elif data.open[0] >= data.open[1] >= data.close[1] >= data.close[0] and (data.open[0] - data.close[0]) / (data.open[1] - data.close[1]) >= 3:
                return '看跌吞没'
            elif data.open[1] < data.close[0] < data.close[1] < data.open[0]:
                return '乌云盖顶'
            elif data.close[1] > data.open[0] > data.open[1] > data.close[0]:
                return '乌云盖顶'
# 星线
def star(data):
    if size(data) <= 0.05 and size(data[1:].reset_index(drop=True)) >= 0.05:
        if position(data) == 'peak' and abs(data.close[1] - data.open[1]) / abs(data.close[0] - data.open[0]) >= 2 and data.close[1] < data.open[0] and data.close[1] < data.close[0]:
            return '黄昏星'
        elif position(data) == 'trough' and abs(data.close[1] - data.open[1]) / abs(data.close[0] - data.open[0]) >= 2 and data.close[1] > data.open[0] and data.close[1] > data.close[0]:
            return '启明星'

#倒锤子
def long_tail(data):
    if size(data[1:].reset_index(drop=True)) >= 0.05:
        if position(data) == 'trough':
            if colour(data) == 'red' and abs(data.high[0] - data.close[0]) / abs(data.close[0] - data.open[0]) >= 2 and abs(data.low[0] - data.open[0]) / abs(data.close[0] - data.open[0]) <= 0.5:
                return '倒锤子'
            elif colour(data) == 'blue' and abs(data.high[0] - data.open[0]) / abs(data.close[0] - data.open[0]) >= 2 and abs(data.low[0] - data.close[0]) / abs(data.close[0] - data.open[0]) <= 0.5:
                return '倒锤子'
            elif colour(data) == ' star':
                return '倒锤子'
        elif position(data) == 'peak':
            if colour(data) == 'red' and abs(data.high[0] - data.close[0]) / abs(data.close[0] - data.open[0]) >= 2:
                return '流星'
            elif colour(data) == 'blue' and abs(data.high[0] - data.open[0]) / abs(data.close[0] - data.open[0]) >= 2:
                return '流星'
            elif colour(data) == 'star':
                return '流星'

# 寻找w底
'''
def w_bottom(data, len_of_period, N, difference, amount_of_change):
    regional_max_dict = {}
    regional_min_dict = {}
    max_lst = []
    min_lst = []
    period_time = {}

    # 找到每个周期内的最大值和最小值：
    for i in range(N):
        true_data = data[i * len_of_period:(i+1) * len_of_period].reset_index(drop=True)
        regional_max_dict[true_data.high.max()] = i
        regional_min_dict[true_data.low.min()] = i
        max_lst.append(true_data.high.max())
        min_lst.append(true_data.low.min())
        period_time[i] = true_data.loc[true_data.high == true_data.high.max(), 'trade_date'].iloc[0]
    i = 0
    time_list = {}

    # 找到最大值之间的关系
    while i in range(len(max_lst)):
        time_list[max_lst[i]] = []
        area = (max_lst[i] - difference * max_lst[i], max_lst[i] + difference * max_lst[i])
        deleted_num = max_lst[i]
        del max_lst[i]
        for value in max_lst:
            if area[0] < value < area[1]:
                time_list[deleted_num].append(regional_max_dict[value])
            time_list[deleted_num].sort(reverse=True)
        max_lst.insert(i, deleted_num)
        i += 1

    # 找到最小值之间的关系：
    i = 0
    while i in range(len(min_lst)):
        time_list[min_lst[i]] = []
        area = (min_lst[i] - difference * min_lst[i], min_lst[i] + difference * min_lst[i])
        deleted_num = min_lst[i]
        del min_lst[i]
        for value in min_lst:
            if area[0] < value < area[1]:
                time_list[deleted_num].append(regional_min_dict[value])
            time_list[deleted_num].sort(reverse=True)
        min_lst.insert(i, deleted_num)
        i += 1

    # 找到涨幅的大小
    tot_period_length = len_of_period * N
    true_data2 = data[:tot_period_length]
    amount = (true_data2.high.max() - true_data2.low.min()) / true_data2.high.max()

    # 测试是否满足条件
    for num in max_lst:
        index = 0
        if time_list[num]:
            while index in range(len(time_list[num])):
                time_list[num][index] = period_time[time_list[num][index]]
                index += 1
    if time_list[max_lst[0]] and time_list[min_lst[0]]and amount >= amount_of_change:
        return True



# 寻找w底2号
def w_bottom(data, len_of_period, difference, amount_of_change):
    regional_min_dict = {}
    min_lst = []

    # 找到每个周期内的最小值以及其时间：
    for i in range(2):
        true_data = data[i * len_of_period:(i+1) * len_of_period].reset_index(drop=True)
        regional_min = true_data.low.min()
        regional_min_time = true_data.loc[true_data.low == true_data.low.min(), 'trade_date'].iloc[0]

        # regional_min_dict = {0 : (regional_min, regional_min_time)}
        regional_min_dict[i] = (regional_min, regional_min_time)
        min_lst.append(true_data.low.min())


    # 最小值之间的关系:
    area1 = (min_lst[0] - difference * min_lst[0], min_lst[0] + difference * min_lst[0])
    area2 = (min_lst[1] - difference * min_lst[1], min_lst[1] + difference * min_lst[1])

    # 找到最小值之间的最大值：
    start = data[data['trade_date'] == regional_min_dict[0][1]].index.values.astype(int)[0]
    end = data[data['trade_date'] == regional_min_dict[1][1]].index.values.astype(int)[0]
    true_data2 = data[start : end]
    peak = true_data2.high.max()

    # 找到涨幅的大小
    amount = abs((min_lst[0] - peak) / peak)

    # 确认两个周期前的趋势是下降趋势
    true_data3 = data[2 * len_of_period : 3 * len_of_period].reset_index(drop=True)
    max_before_two_periods = true_data3.high.max()

    # 测试是否满足条件
    if (area2[0] <= min_lst[0] <= area2[1] or area1[0] <= min_lst[1] <= area1[1]) and amount >= amount_of_change and max_before_two_periods > peak:
        return True
    else:
        return False
'''
# 寻找w底3号：
def w_bottom(code, data, lenth_of_period):
    # 找到距离现在时间最新的最低点以及其时间：
    true_data_2 = data[:lenth_of_period]
    min_value_2 = true_data_2.low.min()
    min_value_2_time = true_data_2.loc[true_data_2.low == min_value_2, 'trade_date'].iloc[0]
    min_value_2_index = true_data_2[true_data_2['trade_date'] == min_value_2_time].index.values.astype(int)[0]

    # 在第二个最低点之前的30天内找到第一个最低点以及其时间
    true_data_1 = data[min_value_2_index+10 : min_value_2_index + 35]
    min_value_1 = true_data_1.low.min()
    min_value_1_time = true_data_1.loc[true_data_1.low == min_value_1, 'trade_date'].iloc[0]
    min_value_1_index = true_data_1[true_data_1['trade_date'] == min_value_1_time].index.values.astype(int)[0]

    # 在第一个最低点和第二个最低点之间找到中间的最高点，并计算其增长率和跌损率：
    true_data_3 = data[min_value_2_index : min_value_1_index]
    peak_1 = true_data_3.high.max()
    increase_amount_1 = (peak_1 - min_value_1) / min_value_1
    decrease_amount_1 = (peak_1 - min_value_2) / peak_1

    # 确认左边是下降趋势 （第一个低点后15天内的最高点大于peak）：
    true_data_4 = data[min_value_1_index : min_value_1_index + 15]
    left_side_value_1 = true_data_4.high.max()

    # 最低点价格差异：
    difference = abs(min_value_1 - min_value_2) / ((min_value_2 + min_value_1) / 2)



    # 三重底：
    true_data_5 = data[min_value_1_index + 10: min_value_1_index + 35]
    min_value_3 = true_data_5.low.min()
    min_value_3_time = true_data_5.loc[true_data_5.low == min_value_3, 'trade_date'].iloc[0]
    min_value_3_index = true_data_5[true_data_5['trade_date'] == min_value_3_time].index.values.astype(int)[0]

    # 确认左侧是下降趋势：
    true_data_6 = data[min_value_3_index : min_value_3_index + 15]
    left_side_value_2 = true_data_6.high.max()

    # 最低点价格差异：
    difference_1 = abs(min_value_1 - min_value_2) / ((min_value_2 + min_value_1 + min_value_3) / 3)
    difference_2 = abs(min_value_3 - min_value_2) / ((min_value_2 + min_value_1 + min_value_3) / 3)
    difference_3 = abs(min_value_3 - min_value_1) / ((min_value_2 + min_value_1 + min_value_3) / 3)

    # 在第3和第2个低点之间找到一个最高点。 并计算增长率和下降率
    true_data_7 = data[min_value_1_index : min_value_3_index]
    peak_2 = true_data_7.high.max()
    increase_amount_2 = (peak_2 - min_value_1) / min_value_1
    decrease_amount_2 = (peak_2 - min_value_2) / peak_2

    # KDJ在第二个低点+-5个index的周线和日线都发生金叉：
    daily_data_for_KDJ = data[min_value_2_index - 5 : min_value_2_index + 5]

    weekly_data_end_time = data.trade_date[0]
    weekly_data_start_time = data.trade_date[min_value_1_index + 30]
    pro = ts.pro_api('eeafdc95319fcce0ebd4a2ed3e5dbf8ff767c85e53affc867df701ce')
    weekly_data_for_KDJ = pro.weekly(ts_code = code, start_date= weekly_data_start_time, end_date=weekly_data_end_time,
                  fields='ts_code,trade_date,open,high,low,close,vol,amount')
    daily_golden_cross = indicators.golden_cross(daily_data_for_KDJ)
    weekly_golden_cross = indicators.golden_cross(weekly_data_for_KDJ)

    # 判断是否符合条件 (回调幅度和下降幅度大于10%； 第一个最低点左侧程下降趋势；两个最低点差异不超过6%；第一个最低点的交易量小于第二个最西点的交易量
    if (increase_amount_1 >= 0.1 and decrease_amount_1 >= 0.1 and ((left_side_value_1 - min_value_1) / (peak_1 - min_value_1)) >= 2
            and difference <= 0.06 and data.vol[min_value_1_index] < data.vol[min_value_2_index]
            and daily_golden_cross and weekly_golden_cross) or (difference_1 <= 0.06
            and difference_2 <= 0.06 and difference_3 <= 0.06 and increase_amount_2 >= 0.1 and decrease_amount_2 >= 0.1
            and ((left_side_value_2 - min_value_3) / (peak_2 - min_value_3)) >= 2 and daily_golden_cross and weekly_golden_cross):
        return True
    else:
        return False
'''
    if size(data[1:].reset_index(drop=True)) >= 0.05:
'''

def review(daily_data, weekly_data):
    # 第一个条件：T-1日的最高值小于250日均线

    daily_mean2 = indicators.Mean(daily_data.close)
    daily_mean1 = indicators.Mean(daily_data.close[1:].reset_index(drop=True))

    # 第二个条件：T日的涨幅为10%
    amount_of_increase = (daily_data.close[0] - daily_data.close[1]) / daily_data.close[1]

    # 第五个条件：VOL-TDX中的MA5大于MA10
    daily_vol_mean = indicators.Mean(daily_data.vol)

    if (daily_data.close[1] <= daily_mean1.MA250[0] or daily_data.close[0] >= daily_mean2.MA250[0]) and amount_of_increase >=0.09\
            and daily_vol_mean.MA5[0] > daily_vol_mean.MA10[0]:
        return True

    else:
        return False
# 去掉daily和weekly的macd
'''
daily_macd.MACD_diff[0] > daily_macd.MACD_dea and
weekly_macd.MACD_diff[0] > weekly_macd.MACD_dea
daily_macd.MACD_diff[0] > 0 and daily_macd.MACD_dea > 0 
and daily_KDJ.K >= daily_KDJ.D 
and daily_KDJ.K >= daily_KDJ.D 
'''
