from Code.Customers import *
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from itertools import repeat

## *********************************************************************************************************************
## 0: Define path and import data  *************************************************************************************
## *********************************************************************************************************************

# define paths:
importpath = os.path.abspath("./Results/coffeebar_prices.csv")
import_dfprob = os.path.abspath("./Results/dfprobs.csv")

exportpath_fifty = os.path.abspath("./Results/Simulation_fifty.csv")
exportpath_inflat = os.path.abspath("./Results/Simulation_inflat.csv")
exportpath_budget = os.path.abspath("./Results/Simulation_budget.csv")
exportpath_lottery = os.path.abspath("./Results/Simulation_lottery.csv")

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

# load given dataset
df = pd.read_csv(importpath, sep=";")

# load full simulation pickle file for comparison
transactions = pickle.load(open(PIKdata, "rb"))
ReturningCust = pickle.load(open(PIKreturn, "rb"))

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
plt.xlabel('Time')
plt.ylabel('Prob')
plt.title('Probability of Customer being Returner throughout day')
plt.savefig('./Results/CustomerReturnerProb.png')
plt.show()


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
plt.xlabel('Time slot')
plt.ylabel('Probability')
plt.title('Probability of type of customer')
plt.savefig('./Results/CustomerTypeProb.png')
plt.show()


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

plt.figure()
plt.bar(r1, list_onet, width=barWidth, color='blue', edgecolor='black', capsize=7, label='onetimers')
plt.bar(r2, list_ret, width=barWidth, color='cyan', edgecolor='black', capsize=7, label='returners')
plt.xticks([r + barWidth for r in range(len(list_onet))],
           ['coffee', 'frappucino', 'milkshake', 'soda', 'tea', 'water', 'cookie', 'muffin', 'nothing', 'pie',
            'sandwich'])
plt.ylabel('prob')
plt.xticks(rotation=45)
plt.legend()
plt.savefig('./Results/OneTimers_Returners_comparison.png')
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
fig1, ax = plt.subplots(2, sharex='col', sharey='row', figsize=(12,7))
plt.title('Comparison in probabilities of buying different drinks for one time customers and returners')

ax[0].stackplot(onetimers['TIME'], onetimers['DRINK_coffee'], onetimers['DRINK_water'],
                onetimers['DRINK_frappucino'], onetimers['DRINK_milkshake'], onetimers['DRINK_soda'],
                onetimers['DRINK_tea'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[0].set(title='Choice of drinks for one time customers', ylabel='Probability in %')

ax[1].stackplot(returners['TIME'], returners['DRINK_coffee'], returners['DRINK_water'],
                returners['DRINK_frappucino'], returners['DRINK_milkshake'], returners['DRINK_soda'],
                returners['DRINK_tea'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[1].set(title='Choice of drinks for returners', ylabel='Probability in %', xlabel='Time')
plt.xticks(returners['TIME'][::30], returners['TIME'][::30])
plt.legend(bbox_to_anchor=(0.85, 1), loc="center left", borderaxespad=0)
plt.savefig('./Results/DrinkProbs.png')
plt.show()

# -- Graphs for food
fig2, ax = plt.subplots(2, sharex='col', sharey='row', figsize=(12,7))
plt.title('Comparison in probabilities of buying different foods for one time customers and returners')
ax[0].stackplot(onetimers['TIME'], onetimers['FOOD_cookie'], onetimers['FOOD_muffin'],
                onetimers['FOOD_nothing'], onetimers['FOOD_pie'], onetimers['FOOD_sandwich'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[0].set(title='Choice of food for one time customers', ylabel='Probability in %')

ax[1].stackplot(returners['TIME'], returners['FOOD_cookie'], returners['FOOD_muffin'],
                returners['FOOD_nothing'], returners['FOOD_pie'], returners['FOOD_sandwich'],
                labels=['Coffee', 'Water', 'Frappucino', 'Milkshake', 'Soda', 'Tea'])
ax[1].set(title='Choice of food for returners', ylabel='Probability in %', xlabel='Time')
plt.xticks(returners['TIME'][::30], returners['TIME'][::30])
plt.legend(bbox_to_anchor=(0.85, 1), loc="center left", borderaxespad=0)
plt.savefig('./Results/FoodProbs.png')
plt.show()



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
answer = input("Variation I (fifty returners): \n Do you want to run full simulation (approx. 40min) or load pickle "
               "files of full simulation and run \n representative (four month) simulation instead to see that "
               "code works? If run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    # simulate specified range (by default set to five years)
    transactionsAll_fifty = SimulateRange(dfprob, ReturningCust_fifty, items)  # run full simulation
    # transform created data to show objects along with their attributes
    transactions_fifty = NoObjects(transactionsAll_fifty)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_fifty, open(PIKdata_fifty, "wb"))
    pickle.dump(ReturningCust_fifty, open(PIKreturn_fifty, "wb"))
    # save simulated data as csv for completeness
    transactions.to_csv(exportpath_fifty, sep=";", index=False)

# If data should be loaded instead, following commands will be run
elif answer == "load":
    # simulate four month to see that program works fine
    ReturningCustFourMonth_fifty = ReturningCust_fifty.copy() # copy list of returning customers just to show changes
    transactionsFourMonths_fifty = SimulateRange(dfprob, ReturningCustFourMonth_fifty,
                                                 items, start="2017-11-01", end="2018-02-10")
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
fig, ax = plt.subplots(2, sharex='col', sharey='row', figsize=(12,7))
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (returners=1000)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_fifty.index,  trans_sum_type_fifty['tripadvisor_one_time'],
                trans_sum_type_fifty['normal_one_time'], trans_sum_type_fifty['hipster_returning'],
                trans_sum_type_fifty['normal_returning'],
                labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (returners=50)', ylabel='Value in €', xlabel='Date')
plt.savefig('./Results/FiftySim.png')
plt.show()



## *********************************************************************************************************************
## IV: The prices change from the beginning of 2018 and go up by 20%  **************************************************
## *********************************************************************************************************************
# in order to address this change, we first modify the relevant functions and re-run the simulation after
# modify MakePurchase() function with if else statement; if date after 2017, prices 20% higher
def MakePurchase(customer, hour, minute, probabilities, items, date):  # additional input "date" required
    purchase = Purchase(customer, hour, minute, probabilities, items)
    if (date.astype('datetime64[D]') > np.datetime64("2017-12-31").astype('datetime64[D]')):
        purchase.value = purchase.value * 1.2  # if date is after 2017, value of purchase increased 20%
    else:
        None  # if date is before 2018, nothing changes
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
                                                   transactions['DATETIME'].values[i])  # date passed to function
    return transactions

# create individual list of returning customers
ReturningCust_inflat = [Returner() for i in range(667)]  # prob = 2/3 for being normal returning customer
ReturningCust_inflat.extend([Hipster() for i in range(333)])  # prob = 1/3 for being hipster

# again, define whether simulation should be run or pickle file should be loaded
# Input mask to specify option
answer = input("Variation II (prices change): \n Do you want to run full simulation (approx. 40min) or load pickle "
               "files of full simulation and run \n representative (four month) simulation instead to see that "
               "code works? If run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    transactionsAll_inflat = SimulateRange(dfprob, ReturningCust_inflat, items)  # run full simulation
    transactions_inflat = NoObjects(transactionsAll_inflat)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_inflat, open(PIKdata_inflat, "wb"))
    pickle.dump(ReturningCust_inflat, open(PIKreturn_inflat, "wb"))
    # save simulated data as csv for completeness
    transactions.to_csv(exportpath_inflat, sep=";", index=False)

# If data should be loaded instead, following commands will be run
elif answer == "load":
    ReturningCustFourMonth_inflat = ReturningCust_inflat.copy() # copy list of returning customers just to show changes
    transactionsFourMonths_inflat = SimulateRange(dfprob, ReturningCustFourMonth_inflat,
                                                  items, start="2017-11-01", end="2018-02-10")
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
fig, ax = plt.subplots(2, sharex='col', sharey='row', figsize=(12,7))
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
                trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
                labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (steady prices)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_inflat.index,  trans_sum_type_inflat['tripadvisor_one_time'],
                trans_sum_type_inflat['normal_one_time'], trans_sum_type_inflat['hipster_returning'],
                trans_sum_type_inflat['normal_returning'],
                labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (prices increase 20% in 2018)', ylabel='Value in €', xlabel='Date')
plt.savefig('./Results/InflatSim.png')
plt.show()


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
ReturningCust_budget = [Returner() for i in range(667)]  # prob = 2/3 for being normal returning customer
ReturningCust_budget.extend([Hipster() for i in range(333)])  # prob = 1/3 for being hipster
# update change in initial budget
for i in ReturningCust_budget:
    if i.type == "hipster_returning":
        i.budget = 40

# now run the simulation again
# again, define whether simulation should be run or pickle file should be loaded
# Input mask to specify option
answer = input("Variation III (different hipster budget): \n Do you want to run full simulation (approx. 40min) or load"
               " pickle files of full simulation and run \n representative (four month) simulation instead to see that "
               "code works? If run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    transactionsAll_budget = SimulateRange(dfprob, ReturningCust_budget, items)  # run full simulation
    transactions_budget = NoObjects(transactionsAll_budget)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_budget, open(PIKdata_budget, "wb"))
    pickle.dump(ReturningCust_budget, open(PIKreturn_budget, "wb"))
    # save simulated data as csv for completeness
    transactions.to_csv(exportpath_budget, sep=";", index=False)

# If data should be loaded instead, following commands will be run
elif answer == "load":
    ReturningCustFourMonth_budget = ReturningCust_budget.copy() # copy list of returning customers just to show changes
    transactionsFourMonths_budget = SimulateRange(dfprob, ReturningCustFourMonth_budget,
                                                  items, start="2017-11-01", end="2018-02-10")
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
fig, ax = plt.subplots(2, sharex='col', sharey='row', figsize=(12,7))
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (Hipster budget 250€)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_budget.index,  trans_sum_type_budget['tripadvisor_one_time'],
                trans_sum_type_budget['normal_one_time'], trans_sum_type_budget['normal_returning'],
                trans_sum_type_budget['hipster_returning'],
                labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (Hipster budget 40€)', ylabel='Value in €', xlabel='Date')
plt.savefig('./Results/BudgetSim.png')
plt.show()


## *********************************************************************************************************************
## VI: Open Question ***************************************************************************************************
## *********************************************************************************************************************

## Impact of: changing assumption that 20% chance for returner even when most returners are bankrupt (instead 0.02%
## chance per solvent returner); in order assess the impact, the lottery for the customer has to be adopted
## accordingly before we can run the simulation again. Additionally, we make the assumption that returners that are
## bankrupt are replaced by tripadvised customers, as it might be seen as an indicator for a good cafe that the returners
## spent all their money there so the cafe should have a good rating and attract more customers from tripadvisor. This
## is also beneficial for the cafe as the tripadvisor customers are the only ones giving tips.

# ChooseCustomer() with assumption that returners will not go more often if another returner is bankrupt but instead go
# at same frequency
def ChooseCustomer(ReturningCust):
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if
              ReturningCust[i].budget > 8]  # is returner solvent?
    allcust = [Customer(), Tripadvised()]  # create list for possible customers (note we do not care what Customer() or
    allcust.extend(liquid)  # Tripadvised() comes, but for Returner() and Hipster() we want to keep track
    weights = [72, (100 - 72 - len(liquid) * (20 / len(ReturningCust)))]  # bankrupt ret. cust. are repl. by Tripadvised
    weights.extend(list(repeat((20 / len(ReturningCust)), len(liquid))))  # prob. of repeating ret. dep. on overall nr.

    if liquid == []:  # if all returners are bankrupt
        customer = random.choices([Customer(), Tripadvised()], weights=[72, 28], k=1)  # if all returners bankrupt

    else:  # if there are still liquid returners
        customer = random.choices(allcust, weights=weights, k=1)
    return customer[0]

# create individual list of returning customers
ReturningCust_lottery = [Returner() for i in range(667)]  # prob = 2/3 for being normal returning customer
ReturningCust_lottery.extend([Hipster() for i in range(333)])  # prob = 1/3 for being hipster

# now run the simulation again
# again, define whether simulation should be run or pickle file should be loaded
# Input mask to specify option
answer = input("Variation IV (returner assumption): \n Do you want to run full simulation (approx. 40min) or load pickle"
               " files of full simulation and run \n representative (four month) simulation instead to see that code "
               "works? If run full simulation, \n input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    transactionsAll_lottery = SimulateRange(dfprob, ReturningCust_lottery, items)  # run full simulation
    transactions_lottery = NoObjects(transactionsAll_lottery)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions_lottery, open(PIKdata_lottery, "wb"))
    pickle.dump(ReturningCust_lottery, open(PIKreturn_lottery, "wb"))
    # save simulated data as csv for completeness
    transactions.to_csv(exportpath_lottery, sep=";", index=False)

# If data should be loaded instead, following commands will be run
elif answer == "load":
    ReturningCustFourMonth_lottery = ReturningCust_lottery.copy()
    transactionsFourMonths_lottery = SimulateRange(dfprob, ReturningCustFourMonth_lottery,
                                                   items, start="2017-11-01", end="2018-02-10")
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
trans_sum_type_lottery = sumtype(transactions_lottery)

# plot
fig, ax = plt.subplots(2, sharex='col', sharey='row', figsize=(12,7))
plt.title('Aggregated turnover per day by customer type')

ax[0].stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[0].set(title='Original simulation (other returners compensate for bankrupt ones)', ylabel='Value in €')


ax[1].stackplot(trans_sum_type_lottery.index,  trans_sum_type_lottery['tripadvisor_one_time'],
                trans_sum_type_lottery['normal_one_time'], trans_sum_type_lottery['hipster_returning'],
                trans_sum_type_lottery['normal_returning'],
                labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
ax[1].set(title='Changed simulation (no change in visit frequency depending on other returners)',
          ylabel='Value in €', xlabel='Date')
plt.savefig('./Results/LotterySim.png')
plt.show()

