from Code.Customers import *
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from itertools import repeat

# define paths:
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
import_dfprob = os.path.abspath("./Results/dfprobs.csv")

# define paths for pickle files
PIKdata = "./Data/transactionsDF.dat"
PIKreturn = "./Data/ReturningCust.dat"
PIKdata4month = "./Data/data4month.dat"
PIKreturn4month = "./Data/Cust4month.dat"
PIKdata_fifty = "./Data/transactionsDF_fifty.dat"
PIKreturn_fifty = "./Data/ReturningCust_fifty.dat"
PIKdata_inflat = "./Data/transactionsDF_inflat.dat"
PIKreturn_inflat = "./Data/ReturningCust_inflat.dat"
PIKdata_budget = "./Data/transactionsDF_budget.dat"
PIKreturn_budget = "./Data/ReturningCust_budget.dat"
PIKdata_lottery = "./Data/transactionsDF_lottery.dat"
PIKreturn_lottery = "./Data/ReturningCust_lottery.dat"

## *********************************************************************************************************************
## I: Show some buying histories of returning customers for your simulations *******************************************
## *********************************************************************************************************************

# call method to tell history from customer object for two randomly chosen customers
ReturningCust[555].purchase_history()
ReturningCust[999].purchase_history()




## *********************************************************************************************************************
## II: Analysis of returning customers of the given dataset ************************************************************
## *********************************************************************************************************************

# load dataframe
df = pd.read_csv(importpath, sep=";")

# Add columns to simplify analysis
def AddColumns(dataframe):  # function serves to add variables for easier grouping of data
    data = dataframe.copy(deep=True)  # Make a copy so dataframe not overwritten
    data['DATETIME'] = pd.to_datetime(data['TIME'])
    data['YEAR'] = data.DATETIME.dt.year
    data['WEEKDAY'] = data.DATETIME.dt.day_name()
    data['TIME'] = data.DATETIME.dt.time
    data['DATE'] = data.DATETIME.dt.date
    data['FOOD'] = data['FOOD'].fillna('nothing')
    return data

df = AddColumns(df)


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

# TODO: what should we do here?

########################################################################################################################
## For the following sections we will re-run the simulation so we have to define the inputs again                     ##
########################################################################################################################
# create items that are sold in cafe: item(name, price, type)
items = [item("coffee", 3, "drink"),
         item("frappucino", 4, "drink"),
         item("milkshake", 5, "drink"),
         item("soda", 3, "drink"),
         item("tea", 3, "drink"),
         item("water", 2, "drink"),
         item("cookie", 2, "food"),
         item("muffin", 3, "food"),
         item("pie", 3, "food"),
         item("sandwich", 2, "food"),
         item("nothing", 0, "food")]

# load dataframe with probabilities obtained from Exploratory.py
dfprob = pd.read_csv(import_dfprob, sep=";")
dfprob.index = dfprob['ID']
dfprob['HOUR'] = dfprob.ID.str.slice(stop=2)
dfprob['MINUTE'] = dfprob.ID.str.slice(start=3, stop=5)

# import pickle file of original simulation for comparison
transactions = pickle.load(open(PIKdata4month, "rb")) # TODO erase 4month



## *********************************************************************************************************************
## III: What would happen if we lower the returning customers to 50 and simulate the same period? **********************
## *********************************************************************************************************************
# note that the code would crash if we do not make the additional assumption that once all returning customers
# are bankrupt, only 90% normal one-time customers or 10% tripadvised customers would enter the cafe
# (see ChooseCustomers())

# create list of fifty returning customers
ReturningCust_fifty = [Returner() for i in range(34)]  # prob = 2/3 for being normal returning customer
ReturningCust_fifty.extend([Hipster() for i in range(16)])  # prob = 1/3 for being hipster

# again, define whether simulation should be run or pickle file should be loaded
# Input mask to specify option
answer = input("Variation I: \n Do you want to run full simulation (approx. 40min) or load pickle files of full"
               " simulation and run \n representative (four month) simulation instead to see that code works? If "
               "run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    # simulate specified range (by default set to five years)
    transactionsAll_fifty = SimulateRange(dfprob, ReturningCust_fifty, items)  # run full simulation
    # transform created data to show objects along with their attributes
    transactions_fifty = NoObjects(transactionsAll_fifty)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_fifty, open(PIKdata_fifty, "wb"))
    pickle.dump(ReturningCust_fifty, open(PIKreturn_fifty, "wb"))

# If data should be loaded instead, following commands will be run
elif answer == "load":
    # simulate four month to see that program works fine
    ReturningCustFourMonth_fifty = ReturningCust_fifty.copy() # copy list of returning customers just to show changes
    transactionsFourMonths_fifty = SimulateRange(dfprob, ReturningCustFourMonth_fifty, items, start="2016-11-01", end="2018-02-10") # TODO change to 4 month
    # transform created data to show objects along with their attributes
    transactionsFourMonths_fifty = NoObjects(transactionsFourMonths_fifty)
    # get full simulation stored in pickle file
    transactions_fifty = pickle.load(open(PIKdata_fifty, "rb"))
    ReturningCust_fifty = pickle.load(open(PIKreturn_fifty, "rb"))

# If input is not specified correctly, this message will appear
else:
    print("Either 'run' or 'load' needs to be specified!")


# -- compare aggregated income by types per day
# create function to aggregate data by type per day
def sumtype(dataframe):
    data = dataframe.copy(deep=True)
    data = data.groupby(by=['DATE', 'CUSTOMER_TYPE']).sum().reset_index()
    data['TOTAL'] = data['TURNOVER'] + data['TIPS']
    data = data.pivot(index="DATE", columns="CUSTOMER_TYPE", values="TOTAL")
    return data

# modify variables needed to plot
trans_sum_type = sumtype(transactions)
trans_sum_type_fifty = sumtype(transactions_fifty)


# plot
fig, ax = plt.subplots(2, sharex='col', sharey='row')
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (returners=1000)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_fifty.index,  trans_sum_type_fifty['tripadvisor_one_time'], trans_sum_type_fifty['normal_one_time'],
              trans_sum_type_fifty['hipster_returning'], trans_sum_type_fifty['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (returners=50)', ylabel='Value in €', xlabel='Date')




## *********************************************************************************************************************
## IV: The prices change from the beginning of 2018 and go up by 20%  **************************************************
## *********************************************************************************************************************
# in order to address this change, we first modify the relevant functions and re-run the simulation after
# modify MakePurchase() function with if else statement; if date after 2017, prices 20% higher
def MakePurchase(customer, hour, minute, probabilities, items, date):  # additional input "date" required
    purchase = Purchase(customer, hour, minute, probabilities, items)
    if (date.astype('datetime64[D]') > np.datetime64("2017-12-31").astype('datetime64[D]')):
        purchase.value = purchase.value * 1.2 # if date is after 2017, value of purchase increased 20%
    else:
        None # if date is before 2018, nothing changes
    customer.money_spent += purchase.payment
    customer.budget -= purchase.payment
    customer.purchases.append(purchase)

    return purchase

# the SimulateRange() function needs to be modified too since MakePurchase() now requires date input
def SimulateRange(probabilities, ReturningCust, items, start = "2016-01-01", end = "2020-12-31"):
    daterange = pd.date_range(start=start, end=end).strftime("%Y-%m-%d").to_list()
    time = probabilities['ID']
    transactions = pd.DataFrame({'DATETIME': [pd.to_datetime(" ".join(i)) for i in product(daterange, time)]})
    transactions['HOUR'] = transactions['DATETIME'].dt.strftime("%H")
    transactions['MINUTE'] = transactions['DATETIME'].dt.strftime("%M")
    transactions['CUSTOMER'] = None
    transactions['PURCHASE'] = None
    for i in progressbar(range(0, len(transactions))):
        transactions['CUSTOMER'][i] = ChooseCustomer(ReturningCust)
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i],
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities,
                                                   items,
                                                   transactions['DATETIME'].values[i]) # date passed to function
    return transactions

# create individual list of returning customers
ReturningCust_inflat = [Returner() for i in range(66)]  # prob = 2/3 for being normal returning customer # TODO change
ReturningCust_inflat.extend([Hipster() for i in range(33)])  # prob = 1/3 for being hipster

# again, define whether simulation should be run or pickle file should be loaded
# Input mask to specify option
answer = input("Variation I: \n Do you want to run full simulation (approx. 40min) or load pickle files of full"
               " simulation and run \n representative (four month) simulation instead to see that code works? If "
               "run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    transactionsAll_inflat = SimulateRange(dfprob, ReturningCust_inflat, items)  # run full simulation
    transactions_inflat = NoObjects(transactionsAll_inflat)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_inflat, open(PIKdata_inflat, "wb"))
    pickle.dump(ReturningCust_inflat, open(PIKreturn_inflat, "wb"))

# If data should be loaded instead, following commands will be run
elif answer == "load":
    ReturningCustFourMonth_inflat = ReturningCust_inflat.copy() # copy list of returning customers just to show changes
    transactionsFourMonths_inflat = SimulateRange(dfprob, ReturningCustFourMonth_inflat, items, start="2016-11-01", end="2018-02-10") #TODO change to 4 month
    transactionsFourMonths_inflat = NoObjects(transactionsFourMonths_inflat)
    # get full simulation stored in pickle file
    transactions_inflat = pickle.load(open(PIKdata_inflat, "rb"))
    ReturningCust_inflat = pickle.load(open(PIKreturn_inflat, "rb"))

# If input is not specified correctly, this message will appear
else:
    print("Either 'run' or 'load' needs to be specified!")


# -- compare aggregated income by types per day
# modify variables needed to plot
trans_sum_type = sumtype(transactions)
trans_sum_type_inflat = sumtype(transactions_inflat)

# plot
fig, ax = plt.subplots(2, sharex='col', sharey='row')
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (steady prices)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_inflat.index,  trans_sum_type_inflat['tripadvisor_one_time'], trans_sum_type_inflat['normal_one_time'],
              trans_sum_type_inflat['hipster_returning'], trans_sum_type_inflat['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (prices increase 20% in 2018)', ylabel='Value in €', xlabel='Date')





# in order to not have the inflation in the following simulations, we will re-run the standard versions of the functions
# create function that will assign a purchase object for a given customer at a given hour and minute
def MakePurchase(customer, hour, minute, probabilities, items): # probabilities refers to dfobtained in Exploratory.py
    purchase = Purchase(customer, hour, minute, probabilities, items) # create purchase object
    customer.money_spent += purchase.payment # update money_spent attribute of chosen customer
    customer.budget -= purchase.payment # update budget of chosen customer
    customer.purchases.append(purchase) # update purchase history of chosen customer
    return purchase


# create function to simulate five years (or different if specified in input)
def SimulateRange(probabilities, ReturningCust, items, start = "2016-01-01", end = "2020-12-31"):
    ## !!! Important !!! function needs around 40 minutes if simulation for five years.
    #                     Progress bar will give progress and estimate of overall time
    daterange = pd.date_range(start=start,end=end).strftime("%Y-%m-%d").to_list() # define range of date
    time = probabilities['ID']
    transactions = pd.DataFrame({'DATETIME' : [pd.to_datetime(" ".join(i)) for i in product(daterange, time)]})
    transactions['HOUR'] = transactions['DATETIME'].dt.strftime("%H") # get hour from datetime column
    transactions['MINUTE'] = transactions['DATETIME'].dt.strftime("%M") # get minute from datetime column
    transactions['CUSTOMER'] = None
    transactions['PURCHASE'] = None
    for i in progressbar(range(0, len(transactions))): # *** see comment below
        transactions['CUSTOMER'][i] = ChooseCustomer(ReturningCust) # assign customer object for given time
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i], # assign purchase object
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities,
                                                   items)
    return transactions


## *********************************************************************************************************************
## V: What would happen if the budget of hipsters drops to 40?  ********************************************************
## *********************************************************************************************************************
# in order to account for the change in the initial budget of the hipsters, we first update their attribute "budget"
# before running the simulation again (note that also here the additional assumption is needed)

# create individual list of returning customers
ReturningCust_budget = [Returner() for i in range(66)]  # prob = 2/3 for being normal returning customer # TODO change
ReturningCust_budget.extend([Hipster() for i in range(33)])  # prob = 1/3 for being hipster
# update change in initial budget
for i in ReturningCust_budget:
    if i.type == "hipster_returning":
        i.budget = 40

# now run the simulation again
# again, define whether simulation should be run or pickle file should be loaded
# Input mask to specify option
answer = input("Variation I: \n Do you want to run full simulation (approx. 40min) or load pickle files of full"
               " simulation and run \n representative (four month) simulation instead to see that code works? If "
               "run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    transactionsAll_budget = SimulateRange(dfprob, ReturningCust_budget, items)  # run full simulation
    transactions_budget = NoObjects(transactionsAll_budget)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_budget, open(PIKdata_budget, "wb"))
    pickle.dump(ReturningCust_budget, open(PIKreturn_budget, "wb"))

# If data should be loaded instead, following commands will be run
elif answer == "load":
    ReturningCustFourMonth_budget = ReturningCust_budget.copy() # copy list of returning customers just to show changes
    transactionsFourMonths_budget = SimulateRange(dfprob, ReturningCustFourMonth_budget, items, start="2016-11-01", end="2018-02-10") #TODO change to 4 month
    transactionsFourMonths_budget = NoObjects(transactionsFourMonths_budget)
    # get full simulation stored in pickle file
    transactions_budget = pickle.load(open(PIKdata_budget, "rb"))
    ReturningCust_budget = pickle.load(open(PIKreturn_budget, "rb"))

# If input is not specified correctly, this message will appear
else:
    print("Either 'run' or 'load' needs to be specified!")


# -- compare aggregated income by types per day
# modify variables needed to plot
trans_sum_type = sumtype(transactions)
trans_sum_type_budget = sumtype(transactions_budget)

# plot
fig, ax = plt.subplots(2, sharex='col', sharey='row')
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (Hipster budget 250€)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_budget.index,  trans_sum_type_budget['tripadvisor_one_time'], trans_sum_type_budget['normal_one_time'],
              trans_sum_type_budget['normal_returning'], trans_sum_type_budget['hipster_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (Hipster budget 40€)', ylabel='Value in €', xlabel='Date')



## *********************************************************************************************************************
## VI: Open Question ***************************************************************************************************
## *********************************************************************************************************************

## Impact of: changing assumption that 20% chance for returner even when most returners are bankrupt (instead 0.02%
## chance per solvent returner); in order assess the impact, the lottery for the customer has to be adopted
## accordingly before we can run the simulation again. Additionally, we make the assumption that returners that are
## bankrupt are replaced by tripadvised customers, as it might be seen as an indicator for a good cafe that the returners
## spent all their money there so the cafe should have a good rating and attract more customers from tripadvisor. This
## is also beneficial for the cafe as the tripadvisor customers are the only ones giving tips.

# TODO: Try run with full sample to see if problem still there, it seems like function is not called (change in weights desnt change anything)

# ChooseCustomer() with assumption that returners will not go more often if another returner is bankrupt but instead go
# at same frequency
def ChooseCustomer(ReturningCust):
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if
              ReturningCust[i].budget > 8]  # is returner solvent?
    allcust = [Customer(), Tripadvised()]  # create list for possible customers (note we do not care what Customer() or
    allcust.extend(liquid)  # Tripadvised() comes, but for Returner() and Hipster() we want to keep track
    weights = [7, (100 - 72 - len(liquid) * (20 / len(ReturningCust)))]  # bankrupt returning customers are replaced by Tripadvised
    weights.extend(
        list(repeat((20 / len(ReturningCust)), len(liquid))))  # prob. of repeating returner dependen on overall nr.
    if liquid == []:
        customer = random.choices([Customer(), Tripadvised()], weights=[72, 28], k=1)  # if all returners bankrupt

    else:
        customer = random.choices(allcust, weights=weights, k=1)
    return customer[0]

# create individual list of returning customers
ReturningCust_lottery = [Returner() for i in range(66)]  # prob = 2/3 for being normal returning customer # TODO change
ReturningCust_lottery.extend([Hipster() for i in range(33)])  # prob = 1/3 for being hipster

# now run the simulation again
# again, define whether simulation should be run or pickle file should be loaded
# Input mask to specify option
answer = input("Variation I: \n Do you want to run full simulation (approx. 40min) or load pickle files of full"
               " simulation and run \n representative (four month) simulation instead to see that code works? If "
               "run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    transactionsAll_lottery = SimulateRange(dfprob, ReturningCust_lottery, items)  # run full simulation
    transactions_lottery = NoObjects(transactionsAll_lottery)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_lottery, open(PIKdata_lottery, "wb"))
    pickle.dump(ReturningCust_lottery, open(PIKreturn_lottery, "wb"))

# If data should be loaded instead, following commands will be run
elif answer == "load":
    ReturningCustFourMonth_lottery = ReturningCust_lottery.copy()
    transactionsFourMonths_lottery = SimulateRange(dfprob, ReturningCustFourMonth_lottery, items, start="2017-11-01", end="2018-02-10") #TODO change to 4 month
    transactionsFourMonths_lottery = NoObjects(transactionsFourMonths_lottery)
    # get full simulation stored in pickle file
    transactions_lottery = pickle.load(open(PIKdata_lottery, "rb"))
    ReturningCust_lottery = pickle.load(open(PIKreturn_lottery, "rb"))

# If input is not specified correctly, this message will appear
else:
    print("Either 'run' or 'load' needs to be specified!")


# -- compare aggregated income by types per day
# modify variables needed to plot
trans_sum_type = sumtype(transactions)
trans_sum_type_lottery = sumtype(transactionsFourMonths_lottery)

# plot
fig, ax = plt.subplots(2, sharex='col', sharey='row')
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (other returners compensate for bankrupt ones)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_lottery.index,  trans_sum_type_lottery['tripadvisor_one_time'], trans_sum_type_lottery['normal_one_time'],
                trans_sum_type_lottery['hipster_returning'], trans_sum_type_lottery['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (no change in visit frequency depending on other returners)', ylabel='Value in €', xlabel='Date')

