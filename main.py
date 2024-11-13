import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

model = LinearRegression()




df = pd.read_csv('C:\\Tensorflow\\Middle\\energo.txt', sep=",", header=0)
df['datetime'] = df['<DATE>']*100 + df['<TIME>']/10000
df['middle'] = (df['<HIGH>'] + df['<LOW>'])/2
df['middle2'] = df['middle'].rolling(10).mean()

# numbers = [x for x in range(df.shape[0])]
# df['id'] = numbers
# y = df['middle']
# x = df[['id']]
#
# model.fit(x, y)
# # Creating a list of numbers from 0 to 9
#
#
# r2_score = model.score(x, y)
#
# lmao = df['datetime'][0].reshape(1, -1)
# print(f"R-squared value: {r2_score}")
#
# df['ans'] = df['id'].map(lambda x: model.predict([[x]])[0])
# print("kek")
#
df["middle"].plot()
df["middle2"].plot()
# df["ans"].plot()
# <Axes: xlabel='datetime'>

plt.show()


#----------------------------------------------------------------------------------------------------------------------

class Broker():
    def __init__(self, money: float):
        self.money = money
        self.actions = 0
        self.bought_price = 1
        self.sold_price = 1
    def Buy(self, price, comission, amount = 1):
        total_price = price*amount*(1+comission)
        if total_price <= self.money:
            self.money -= total_price
            self.actions += amount
            self.bought_price = price
            return True
        return False
    def sell(self, price, comission, amount = 1):
        total_price = price*amount*(1-comission)
        if amount <= self.actions:
            self.money += total_price
            self.actions -= amount
            self.sold_price = price
            return True
        return False

money = 20000
comission = 0.035
comission = comission/100
stock = df['middle2']
stock = stock.fillna(method='bfill')
drop_flag = False
raise_flag = False
old_price = stock[9]
amount = 5
Bro = Broker(money = money)
Bro.Buy(old_price, 0, amount*2)
Bro.sell(old_price, 0, amount)
true_price = 0
buy_tolerance = 0.1
sell_tolerance = 0.1
initial_buy_tolerance = 0.1
initial_sell_tolerance = 0.1
cooldown = 0
initial_cooldown = 10
print((Bro.bought_price))
for i, price in enumerate(stock):
    cooldown -= 1
    true_price = stock = df['middle'][i]
    if price < old_price and raise_flag and cooldown <= 0:
        # print("try sell")
        # print(price)
        # print(Bro.bought_price)
        if price/Bro.bought_price >= 1 + buy_tolerance:
            flag = Bro.sell(true_price, comission, amount)
            if flag:
                print('sell')
                print(true_price)
                cooldown = initial_cooldown
    elif price > old_price and drop_flag and cooldown <= 0:
        if price/Bro.sold_price < 1 - sell_tolerance:
            flag = Bro.Buy(true_price, comission, amount)
            if flag:
                print('buy')
                print(true_price)
                cooldown = initial_cooldown
    if price > old_price:
        raise_flag = True
        drop_flag = False
    elif price < old_price:
        drop_flag = True
        raise_flag = False
    old_price = price
print(Bro.actions)
Bro.sell(true_price, comission, Bro.actions)
print(Bro.money)
print(Bro.actions)

