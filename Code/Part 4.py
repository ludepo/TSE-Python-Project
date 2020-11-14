import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.pyplot import *

## *********************************************************************************************************************
## 0: Define path and import data  *************************************************************************************
## *********************************************************************************************************************
importpath = os.path.abspath("./Results/coffeebar_prices.csv")

PIKdata = "./Data/transactionsDF.dat"
PIKreturn = "./Data/ReturningCust.dat"
PIKdata4month = "./Data/data4month.dat"
PIKreturn4month = "./Data/Cust4month.dat"

df = pd.read_csv(importpath, sep=";")

## *********************************************************************************************************************
## I: Show some buying histories of returning customers for your simulations *******************************************
## *********************************************************************************************************************

# call method to tell history from customer object for two randomly chosen customers
ReturningCust[555].purchase_history()
ReturningCust[999].purchase_history()

## *********************************************************************************************************************
## II: Analysis of returning customers of the given dataset ************************************************************
## *********************************************************************************************************************

## 2.1) How many returning customers?
print(df.CUSTOMER.nunique())  # This is the number of purchases made by returners
returners = df[df.RET == 1]
print(len(returners.drop_duplicates(subset=['CUSTOMER'])))  # There are 1000 customers that are returners

## 2.2) Do returners have specific time when they show up more?
returners = returners[['TIME', 'RET']]
prob_returners = returners.groupby('TIME').count()  # dataset with probabilities for returners at each time
prob_returners['prob'] = prob_returners['RET'] / len(returners)
prob_returners = prob_returners.reset_index()

# -- Graph of returning customers over time
prob_returners[['TIME', 'prob']].plot('TIME', figsize=(15, 8))


# 2.3) Probability of having a onetimer or a returning customer at a given time
def time(dataframe):  # function to obtain a dataset with probabilities of returners and onetimers at each time
    dataframe = dataframe.drop(['CUSTOMER', 'DRINKS', 'FOOD', 'DATETIME', 'YEAR', 'WEEKDAY', 'DATE'], axis=1)
    dataframe = pd.get_dummies(dataframe, columns=["RET"], prefix=["RET"]).groupby('TIME').mean()
    dataframe = dataframe.reset_index()
    dataframe = dataframe[['TIME', 'RET_0', 'RET_1']]
    return dataframe


time = time(df)

# -- Graphic for probability of having a returner or a onetimer
ax = time.plot()
ax.legend(["One time customers", "Returners"])


# 2.4) How does this impact their buying history?
def buy(dataframe):  # function to obtain dataset with probabilities of buying the different items for each type
    dataframe = dataframe.drop(['PRICE_DRINKS', 'PRICE_FOOD', 'TURNOVER', 'TIPS', 'YEAR'], axis=1)
    dataframe = pd.get_dummies(dataframe, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"]).groupby('RET').mean()
    dataframe = dataframe.transpose()
    # dataframe = dataframe.drop('YEAR')
    dataframe = dataframe.rename(columns={dataframe.columns[0]: "onetimer", dataframe.columns[1]: "returner"})
    return dataframe


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
def divide(dataframe, x):  # function to create dataset with probabilities of buying different items depending on type
    dataframe = dataframe[dataframe['RET'] == x]
    dataframe = dataframe.drop(['CUSTOMER', 'DATETIME', 'WEEKDAY', 'YEAR', 'DATE', 'RET'], axis=1)
    dataframe = pd.get_dummies(dataframe, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"])
    dataframe = dataframe.groupby('TIME').mean()
    dataframe = dataframe.reset_index()
    return dataframe


returners = divide(df, 1)
onetimers = divide(df, 0)

# -- Graphs for drinks
fig1, ax = plt.subplots(2, sharex='col', sharey='row')
plt.title('Comparison in probabilities of buying different drinks for one time customers and returners')

ax[0].stackplot(onetimers['TIME'], onetimers['DRINK_coffee'], onetimers['DRINK_water'],
                onetimers['DRINK_frappucino'], onetimers['DRINK_milkshake'], onetimers['DRINK_soda'],
                onetimers['DRINK_tea'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[0].set(title='Choice of drinks for one time customers', ylabel='%')

ax[1].stackplot(returners['TIME'], returners['DRINK_coffee'], returners['DRINK_water'],
                returners['DRINK_frappucino'], returners['DRINK_milkshake'], returners['DRINK_soda'],
                returners['DRINK_tea'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[1].set(title='Choice of drinks for returners', ylabel='%')
plt.xticks(returners['TIME'][::30], returners['TIME'][::30])
plt.legend(bbox_to_anchor=(0.85, 1), loc="center left", borderaxespad=0)

# -- Graphs for food
fig2, ax = plt.subplots(2, sharex='col', sharey='row')
plt.title('Comparison in probabilities of buying different foods for one time customers and returners')
ax[0].stackplot(onetimers['TIME'], onetimers['FOOD_cookie'], onetimers['FOOD_muffin'],
                onetimers['FOOD_nothing'], onetimers['FOOD_pie'], onetimers['FOOD_sandwich'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[0].set(title='Choice of food for one time customers', ylabel='%')

ax[1].stackplot(returners['TIME'], returners['FOOD_cookie'], returners['FOOD_muffin'],
                returners['FOOD_nothing'], returners['FOOD_pie'], returners['FOOD_sandwich'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[1].set(title='Choice of food for returners', ylabel='%')
plt.xticks(returners['TIME'][::30], returners['TIME'][::30])
plt.legend(bbox_to_anchor=(0.85, 1), loc="center left", borderaxespad=0)

## *********************************************************************************************************************
## III: What would happen if we lower the returning customers to 50 and simulate the same period? **********************
## *********************************************************************************************************************

## the code would crash if we do not make the additional assumption that once all returning customers are bankrupt,
## only 90% normal one-time customers or 10% tripadvised customers would enter the cafe (see ChooseCustomers())

# TODO: add simulation and comparison graph

transactionsFourMonths = pickle.load(open(PIKdata, "rb"))
ReturningCustFourMonths = pickle.load(open(PIKreturn, "rb"))


## *********************************************************************************************************************
## IV: The prices change from the beginning of 2018 and go up by 20%  **************************************************
## *********************************************************************************************************************

# modify MakePurchase() function with if else statement; if date after 2017, prices 20% higher
def MakePurchase(customer, hour, minute, probabilities, date):  # additional input "date" required
    purchase = Purchase(customer, hour, minute, probabilities)
    if (date.astype('datetime64[D]') > np.datetime64("2017-12-31").astype('datetime64[D]')):
        purchase.value = purchase.value * 1.2  # if date is after 2017, value of purchase increased 20%
    else:
        None  # if date is before 2018, nothing changes
    customer.money_spent += purchase.payment
    customer.budget -= purchase.payment
    customer.purchases.append(purchase)

    return purchase


# the SimulateRange() function needs to be modified too since MakePurchase() now requires date input
def SimulateRange(probabilities, start="2016-01-01", end="2020-12-31"):
    daterange = pd.date_range(start=start, end=end).strftime("%Y-%m-%d").to_list()
    time = probabilities['ID']
    transactions = pd.DataFrame({'DATETIME': [pd.to_datetime(" ".join(i)) for i in product(daterange, time)]})
    transactions['HOUR'] = transactions['DATETIME'].dt.strftime("%H")
    transactions['MINUTE'] = transactions['DATETIME'].dt.strftime("%M")
    transactions['CUSTOMER'] = None
    transactions['PURCHASE'] = None
    for i in progressbar(range(0, len(transactions))):
        transactions['CUSTOMER'][i] = ChooseCustomer()
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i],
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities,
                                                   transactions['DATETIME'].values[i])  # date passed to function
    return transactions


# run a new simulation (four month time horizon) to compare to four month simulation
transactions_inflat = SimulateRange(dfprob, start="2017-11-01", end="2018-02-10")
transactions_inflat = NoObjects(transactions_inflat)


# TODO: compare both simulations with comparison graph


## *********************************************************************************************************************
## V: What would happen if the budget of hipsters drops to 40?  ********************************************************
## *********************************************************************************************************************

## the same as if we would only have 50 returning customers, since the budget of the hipsters would be zero rather
## quickly. Therefore, the normal returning customers would compensate and also be bankrupt soon. Once all returning
## customers are bankrupt the code would crash without the additional assumption.

# TODO: add simulation and comparison graph


## *********************************************************************************************************************
## VI: Open Question ***************************************************************************************************
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

# TODO: add comparison graph
