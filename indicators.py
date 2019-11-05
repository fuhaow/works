import tushare as ts
import numpy as np
# indicators

class MACD:
    def __init__(self, values):
        self.values = values
        self.MACD_diff = self.MACD_diff_cal()
        self.MACD_dea = self.MACD_dea_cal()

    def EMA_cal(self, values, window):
        if window == 1:
            return values[0]
        else:
            if isinstance(values, list):
                return (2 * values[0] + (window - 1) * self.EMA_cal(values[1:], window - 1)) / (window + 1)
            else:
                return (2 * values[0] + (window - 1) * self.EMA_cal(values[1:].reset_index(drop=True), window - 1)) / (window + 1)

    def MACD_diff_cal(self):
        diff = []
        for i in range(9):
            EMA_short = self.EMA_cal(self.values[i:].reset_index(drop=True), 12)
            EMA_long = self.EMA_cal(self.values[i:].reset_index(drop=True), 26)
            dif = EMA_short - EMA_long
            diff.append(dif)
        return diff

    def MACD_dea_cal(self):
        return self.EMA_cal(self.MACD_diff_cal(), 9)


class Mean:
    def __init__(self, data):
        self.close = data
        self.MA5 = self.Mean(5)
        self.MA10 = self.Mean(10)
        self.MA20 = self.Mean(20)
        self.MA60 = self.Mean(60)
        self.MA250 = self.Mean(250)

    def Mean(self, window):
        weights = np.repeat(1.0, window) / window
        ma = np.convolve(self.close, weights, 'valid')
        return ma

class KDJ:
    def __init__(self, data):
        self.data = data
        self.K = self.K_cal()[0]
        self.K_lst = self.K_cal()
        self.D = self.D_cal()
        self.J = self.J_cal()



    def RSU_cal(self, data):
        RSU = (data.close[0] - data.low.min()) / (data.high.max() - (data.low[:9]).min()) * 100
        return RSU

    def SMA_cal(self, values, window):
        if window == 1:
            return values[0]
        else:
            return (values[0] + (window - 1) * self.SMA_cal(values[1:], window - 1)) / window

    # test:
    def K_cal(self):
        RSU_lst = []
        K_lst = []
        for i in range(5):
            data = self.data[i:].reset_index(drop=True)
            data = data[:9].reset_index(drop=True)
            RSU = self.RSU_cal(data)
            RSU_lst.append(RSU)

        for j in range(3):
            K = self.SMA_cal(RSU_lst[j:], 3)
            K_lst.append(K)
        return K_lst

    def D_cal(self):
        return self.SMA_cal(self.K_lst, 3)

    def J_cal(self):
        return 3 * self.K - 2 * self.D

def golden_cross(data):
    time_list=[]
    i = 0
    while i in range(len(data)):
        true_data_1 = data[i:].reset_index(drop=True)
        true_data_2 = data[i + 1:].reset_index(drop=True)
        late_KDJ_value = KDJ(true_data_1)
        early_KDJ_value = KDJ(true_data_2)

        # 金叉：
        if early_KDJ_value.K < early_KDJ_value.D and late_KDJ_value.K > late_KDJ_value.D:
            return True

        i += 1
