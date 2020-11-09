import Customer
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

## *********************************************************************************************************************
## Part I: Define Inputs                         ***********************************************************************
## *********************************************************************************************************************

# import and export path
importpath = os.path.abspath("./Results/dfprobs.csv")
exportpath = os.path.abspath("./Results/transactionsAll.csv")


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

# print the items with their prices
for i in items:
    print("Delicious %s, just %s€" %(i.name, i.price))


# load dataframe with probabilities obtained from Exploratory.py
dfprob = pd.read_csv(importpath, sep=";")
dfprob.index = dfprob['ID']
dfprob['HOUR'] = dfprob.ID.str.slice(stop=2)
dfprob['MINUTE'] = dfprob.ID.str.slice(start=3, stop=5)


# create list of returning customers
ReturningCust = [Returner() for i in range(667)]  # prob = 2/3 for being normal returning customer(out of 1000 returning)
ReturningCust.extend([Hipster() for i in range(333)])  # prob = 1/3 for being hipster




## *********************************************************************************************************************
## Part II: Simulation                           ***********************************************************************
## *********************************************************************************************************************


# simulate four month to see that program works fine
transactionsFourMonths = SimulateRange(dfprob,start = "2017-11-01", end = "2018-02-10")

# transform created data to show objects along with their attributes
transactions = NoObjects(transactionsFourMonths)

# # simulate specified range (by default set to five years)
# transactionsAll = SimulateRange(dfprob) # note that command will run approx. 60 min (8GB Ram) alternatively load pickle

# transform created data to show objects along with their attributes
transactions = NoObjects(transactionsAll)

# save simulated data as pickle in order to access objects later again
PIKdata = "Data/transactionsDF.dat"
PIKreturn = "Data/transactionsDF.dat"
# pickle.dump(transactions, open(PIKdata, "wb"))
# pickle.dump(ReturningCust, open(PIKreturn, "wb"))

# get full simulation stored in pickle file
transactions = pickle.load(open(PIKdata, "rb"))
ReturningCust = pickle.load(open(PIKreturn, "rb"))




## *********************************************************************************************************************
## Part III: Visualize and discuss simulation    ***********************************************************************
## *********************************************************************************************************************


# Give examples of purchases
transactions['PURCHASE'][0].describe_purchase()
transactions['PURCHASE'][100].describe_purchase()
transactions['PURCHASE'][1500].describe_purchase()

# How much money was spent by returning customers?
moneyspent = [ReturningCust[i].money_spent for i in range(len(ReturningCust))]
print("The average amount spent by a returning customer was %s" %(sum(moneyspent)/len(moneyspent)))

# How much budget do returning customers have left?
budgets = [ReturningCust[i].budget for i in range(len(ReturningCust))]
print("The average budget left for a normal returning customer was %s€ and for a hipster %s€"
      %(round(sum(budgets[:666])/len(budgets[:666])), round(sum(budgets[667:])/len(budgets[667:]))))



# -- average income during day
trans_mean_day = transactionsFourMonths.groupby(by='TIME').mean().reset_index()
trans_std_day = transactionsFourMonths.groupby(by='TIME').std().reset_index()

plt.figure()
plt.plot(trans_mean_day.TIME, trans_mean_day.TURNOVER, trans_mean_day.TIPS)
plt.fill_between(trans_std_day.TIME,
                 trans_mean_day.TURNOVER - 2 * trans_std_day.TURNOVER,
                 trans_mean_day.TURNOVER + 2 * trans_std_day.TURNOVER,
                 color = "b", alpha = 0.2)
plt.fill_between(trans_std_day.TIME,
                     trans_mean_day.TIPS - 2 * trans_std_day.TIPS,
                     trans_mean_day.TIPS + 2 * trans_std_day.TIPS,
                     color="r", alpha=0.2)


# -- average income by types per day


trans_mean_type = transactions.groupby(by=['TIME', 'CUSTOMER_TYPE']).mean().reset_index()
trans_std_type = transactions.groupby(by=['TIME', 'CUSTOMER_TYPE']).std().reset_index()

trans_mean_type.plot()

plt.figure()
plt.plot(trans_mean_type.index, trans_mean_type.TURNOVER, ax = plt.subplots())
plt.fill_between(trans_std_type.index, trans_mean_type - 2 * trans_std_type, trans_mean_type + 2 * trans_std_type,
                     alpha=0.2)
# -- average income by type over years

