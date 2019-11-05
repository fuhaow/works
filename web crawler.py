from selenium import webdriver
from time import sleep
from matplotlib import dates as dt
import matplotlib.pyplot as plt

# request for html
browser = webdriver.Chrome()
browser.get('https://www2.my.commbank.com.au/netbank/TransactionHistory/History.aspx?ACCOUNT_PRODUCT_TYPE=DDA&DEEPLINKING_WITH_CONTEXT=True&_e=MAhHTFdMd2s2anlrdDFMQVFpeDZlQ1M1QVRUSUw1YlQ5WVRqVUsrQTVnSk5lSVV3PT16JQpDPiZbaDMFGAPS0G3OBvOHAgm8zmRhj%2ffrAYsoOW4Z8kh1uuMnt2uib4KmNDrGwF5WssO%2byVkzpi7hjLPg9mIiGX20k%2bY%3d&RID=dY7_QztisUCP6ub6Cpw3vw&SID=U56%2bfQs%2fY%2f4%3d')
browser.implicitly_wait(3)
# input client number
CNinput = browser.find_element_by_name("txtMyClientNumber$field")
CNinput.send_keys('type your account number')

# input pin number
PNinput = browser.find_element_by_name('txtMyPassword$field')
PNinput.send_keys('type your key number')

# click log in
login = browser.find_element_by_name('btnLogon$field')
login.click()

# data sliders
preslider = browser.find_element_by_class_name('dateslider_previous')
postslider = browser.find_element_by_class_name('dateslider_next')

# adjusting
sleep(5)

while True:
    sleep(1)
    time = browser.find_elements_by_css_selector('.dateslider_labels li')[0]
    attribute = time.text
    if attribute == 'Feb 18':
        break
    preslider.click()
browser.find_elements_by_css_selector('.dateslider_labels li')[0].click()

final_dict = {'date':[], 'money':[]}
while True:
    # total amount of money:
    dates = browser.find_elements_by_css_selector('#transactionsTableBody .date')
    money_amounts = browser.find_elements_by_css_selector('.total.align_right')
    date_lst = []
    money_lst = []
    for i in dates:
        date = i.text
        date_lst.append(date)

    for j in money_amounts:
        money = j.text
        money_lst.append(money)
    date_lst = date_lst[::-1]

    for i in date_lst:
        final_dict['date'].append(i)

    money_lst = money_lst[::-1]
    for j in money_lst:
        final_dict['money'].append(j)
    if browser.find_elements_by_css_selector('.dateslider_labels li')[0].text == 'Apr 19':
        break
    postslider.click()
    sleep(1)
    time = browser.find_elements_by_css_selector('.dateslider_labels li')[0]
    sleep(1)
    time.click()



for i in range(1,5):
    sleep(1)
    time = browser.find_elements_by_css_selector('.dateslider_labels li')[i]
    sleep(1)
    time.click()
    dates = browser.find_elements_by_css_selector('#transactionsTableBody .date')
    money_amounts = browser.find_elements_by_css_selector('.total.align_right')
    date_lst = []
    money_lst = []
    for i in dates:
        date = i.text
        date_lst.append(date)

    for j in money_amounts:
        money = j.text
        money_lst.append(money)
    date_lst = date_lst[::-1]

    for i in date_lst:
        final_dict['date'].append(i)

    money_lst = money_lst[::-1]
    for j in money_lst:
        final_dict['money'].append(j)

# visualization of data
new_date_lst = []

for i in final_dict['date']:
    date = dt.datestr2num(i)
    new_date_lst.append(date)


new_money_lst = []
for money in final_dict['money']:
    money = money.replace(',', '')
    new_money = float(money[2:])
    new_money_lst.append(new_money)
final_dict['date'] = new_date_lst
final_dict['money'] = new_money_lst

date_lst = []
for date in final_dict['date']:
    new_date = dt.num2date(date)
    date_lst.append(new_date)
final_dict['date'] = date_lst
print(final_dict)

plt.plot(final_dict['date'], final_dict['money'])
plt.show()