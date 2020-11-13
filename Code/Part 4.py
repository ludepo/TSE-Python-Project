import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Code.Class import ReturningCust, Tripadvised

## *********************************************************************************************************************
## Part I: Show some buying histories of returning customers for your simulations **************************************
## *********************************************************************************************************************

ReturningCust[555].purchase_history()
ReturningCust[999].purchase_history()

## *********************************************************************************************************************
## Part II: Analysis of returning customers of the given dataset *******************************************************
## *********************************************************************************************************************

# load dataframe
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
df = pd.read_csv(importpath, sep=";")


# Data cleaning
def Cleandata(dataframe):  # function serves to show dataframe without objects but human-readable data
    dataframe['DATETIME'] = pd.to_datetime(dataframe['TIME'])
    dataframe['YEAR'] = dataframe.DATETIME.dt.year
    dataframe['WEEKDAY'] = dataframe.DATETIME.dt.day_name()
    dataframe['WEEKDAY'] = dataframe.DATETIME.dt.day_name()
    dataframe['TIME'] = dataframe.DATETIME.dt.time
    dataframe['DATE'] = dataframe.DATETIME.dt.date
    dataframe['FOOD'] = dataframe['FOOD'].fillna('nothing')
    return dataframe

df = Cleandata(df)

## 2.1) How many returning customers?
print(df.CUSTOMER.nunique())  ## carefull, here we count the number of purchases made by returners
returners = df[df['CUSTOMER'].duplicated(keep=False)]
returners = returners.drop_duplicates(subset=['CUSTOMER'])
print(len(returners))  ## there are 1000 customers that are returners

## 2.2) Do returners have specific time when they show up more?

returners = df[df['CUSTOMER'].duplicated(keep=False)]  # dataset with observations of returners only
returners = returners.assign(prob_returners=returners.TIME.map(returners.TIME.value_counts(normalize=True)))
returners.drop_duplicates(keep=False)  # dataset with probabilities for returners at each time

# -- Graph of returning customers over time
returners[['TIME', 'prob_returners']].plot('TIME', figsize=(15, 8))

# 2.3) Probability of having a onetimer or a returning customer at a given time
def Time(df):
    df['RET'] = (df.duplicated(keep=False, subset=['CUSTOMER'])) * 1
    time = df.drop(['CUSTOMER', 'DRINKS', 'FOOD', 'DATETIME', 'YEAR', 'WEEKDAY', 'DATE'], axis=1)
    time = pd.get_dummies(time, columns=["RET"], prefix=["RET"]).groupby('TIME').mean()
    time = time.reset_index()
    return time

time=Time(df)

# -- Graphic for probability of having a returner or a onetimer
time[['TIME', 'RET_1', 'RET_0']].plot('TIME', figsize=(15, 8))

# 2.4) How does this impact their buying history?
def buy(df):
    buy = pd.get_dummies(df, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"]).groupby('RET').mean()
    buy = buy.transpose()
    buy = buy.drop('YEAR')
    buy = buy.rename(columns={buy.columns[0]: "onetimer", buy.columns[1]: "returner"})
    return buy

buy = buy(df)

# -- Graphic comparing probabilities of buying each item by type of customer
list_onet = buy['onetimer'].values.tolist()
list_ret = buy['returner'].values.tolist()

barWidth = 0.3
r1 = np.arange(len(list_onet))
r2 = [x + barWidth for x in r1]

plt.bar(r1, list_onet, width=barWidth, color='blue', edgecolor='black', capsize=7, label='onetimers')
plt.bar(r2, list_ret, width=barWidth, color='cyan', edgecolor='black', capsize=7, label='returners')
plt.xticks([r + barWidth for r in range(len(list_onet))],
           ['coffee', 'frappucino', 'milkshake', 'soda', 'tea', 'water', 'cookie', 'muffin', 'nothing', 'pie',
            'sandwich'])
plt.ylabel('prob')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# 2.5) Do you see correlations between what returning customers buy and one-timers?
#function to create dataset with probabilities of buying different items depending on type
def divide(df,x):
    df['RET'] = (df.duplicated(keep=False, subset=['CUSTOMER'])) * 1
    df = df[df['RET'] == x]
    df = df.drop(['CUSTOMER', 'DATETIME', 'WEEKDAY', 'YEAR', 'DATE', 'RET'], axis=1)
    df = pd.get_dummies(df, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"])
    df = df.groupby('TIME').mean()
    df = df.reset_index()
    return df

returners = divide(df,1)
onetimers = divide(df,0)

# -- Graphs for drinks
onetimers[['TIME', 'DRINK_coffee','DRINK_water', 'DRINK_frappucino', 'DRINK_milkshake', 'DRINK_soda', 'DRINK_tea']].plot('TIME', figsize=(15, 8))
returners[['TIME', 'DRINK_coffee','DRINK_water', 'DRINK_frappucino', 'DRINK_milkshake', 'DRINK_soda', 'DRINK_tea']].plot('TIME', figsize=(15, 8))

# -- Graphs for food
onetimers[['TIME', 'FOOD_cookie','FOOD_muffin', 'FOOD_nothing', 'FOOD_pie', 'FOOD_sandwich']].plot('TIME', figsize=(15, 8))
returners[['TIME', 'FOOD_cookie','FOOD_muffin', 'FOOD_nothing', 'FOOD_pie', 'FOOD_sandwich']].plot('TIME', figsize=(15, 8))

# 2.6) Comparison of returners of our generated dataset
PIK = "./Data/transactionsDF.dat"
transactions = pickle.load(open(PIK, "rb"))



## *********************************************************************************************************************
## PartIII: What would happen if we lower the returning customers to 50 and simulate the same period? ******************
## *********************************************************************************************************************

## the code would crash if we do not make the additional assumption that once all returning customers are bankrupt,
## only 90% normal one-time customers or 10% tripadvised customers would enter the cafe (see ChooseCustomers())

## *********************************************************************************************************************
## PartIV: The prices change from the beginning of 2018 and go up by 20%  **********************************************
## *********************************************************************************************************************

# create function that will assign a purchase object for a given customer at a given hour and minute
def MakePurchase(customer, hour, minute, probabilities,
                 date):  # probabilities refers to dataframe obtained in Exploratory.py
    purchase = Purchase(customer, hour, minute, probabilities)  # create purchase object given customer, hour and minute
    if (date.astype('datetime64[D]') > np.datetime64("2017-12-31").astype('datetime64[D]')):
        purchase.value = purchase.value * 1.2
    else:
        None
    customer.money_spent += purchase.payment  # update money_spent attribute of chosen customer
    customer.budget -= purchase.payment  # update budget of chosen customer
    customer.purchases.append(purchase)  # update purchase history of chosen customer

    return purchase


def SimulateRange(probabilities, start="2016-01-01", end="2020-12-31"):
    daterange = pd.date_range(start=start, end=end).strftime("%Y-%m-%d").to_list()  # define range of date
    time = probabilities['ID']
    transactions = pd.DataFrame({'DATETIME': [pd.to_datetime(" ".join(i)) for i in product(daterange, time)]})
    transactions['HOUR'] = transactions['DATETIME'].dt.strftime("%H")  # get hour from datetime column
    transactions['MINUTE'] = transactions['DATETIME'].dt.strftime("%M")  # get minute from datetime column
    transactions['CUSTOMER'] = None
    transactions['PURCHASE'] = None
    for i in progressbar(range(0, len(transactions))):  # *** see comment below
        transactions['CUSTOMER'][i] = ChooseCustomer()  # assign customer object for given time
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i],  # assign purchase object
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities,
                                                   transactions['DATETIME'].values[i])
    return transactions


# run a new simulation for comparison (smaller time horizon)
transactions_inflat = SimulateRange(dfprob, start="2017-11-01", end="2018-02-10")
transactions_inflat = NoObjects(transactions_inflat)


## *********************************************************************************************************************
## PartV: What would happen if the budget of hipsters drops to 40?  ****************************************************
## *********************************************************************************************************************

## the same as if we would only have 50 returning customers, since the budget of the hipsters would be zero rather
## quickly. Therefore, the normal returning customers would compensate and also be bankrupt soon. Once all returning
## customers are bankrupt the code would crash without the additional assumption.



## *********************************************************************************************************************
## PartVI: Open Question ***********************************************************************************************
## *********************************************************************************************************************

## Impact of: changing assumption that 20% chance for returner even when most returners are bankrupt (instead 0.02%
#             chance per solvent returner

# ChooseCust() with assumption that returners will not go more often if another returner is bankrupt but instead go
#     like before
def ChooseCustomer():
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if
              ReturningCust[i].budget > 8]  # is returner solvent?
    allcust = [Customer(), Tripadvised()]  # create list for possible customers (note we do not care what Customer() or
    allcust.extend(liquid)  # Tripadvised() comes, but for Returner() and Hipster() we want to keep track
    weights = [72, (100 - 72 - len(liquid) * (
            20 / len(ReturningCust)))]  # bankrupt returning customers are replaced by Tripadvised
    weights.extend(
        list(repeat((20 / len(ReturningCust)), len(liquid))))  # prob. of repeating returner dependen on overall nr.
    if liquid != []:
        customer = random.choices(allcust, weights=weights, k=1)  # 8% tripadvisor customer
    else:
        customer = random.choices([Customer(), Tripadvised()], weights=[72, 28], k=1)  # if all returners bankrupt
    return customer[0]
