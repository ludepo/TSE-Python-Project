from Code.Customers import *
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

# define path where pickle file of full simulation should be saved/ loaded from
PIKdata = "./Data/transactionsDF.dat"
PIKreturn = "./Data/ReturningCust.dat"
PIKdata4month = "./Data/data4month.dat"
PIKreturn4month = "./Data/Cust4month.dat"


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

# # print the items with their prices
# for i in items:
#     print("Delicious %s, just %s€" %(i.name, i.price))


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

## Important note:
## Following choice has to be taken: Either full simulation in line 68 can be run which will take approx. 40 min (8GB ram)
## or the pickle file for the full simulation and the related updated list of returning customers can be loaded. If the
## second option is chosen, a simulation for four month will be executed in order to show that the code works.

# Input mask to specify option
answer = input("Do you want to run full simulation (approx. 40min) or load pickle files of full simulation and run \n "
               "representative (four month) simulation instead to see that code works? If run full simulation, \n "
               "input 'run', if load pickle file input 'load'.\n \n Answer:   ")

# If full simulation shall be run, this section of code is executed
if answer == "run":
    # simulate specified range (by default set to five years)
    transactionsAll = SimulateRange(dfprob, ReturningCust, items)  # run full simulation
    # transform created data to show objects along with their attributes
    transactions = NoObjects(transactionsAll)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactions, open(PIKdata, "wb"))
    pickle.dump(ReturningCust, open(PIKreturn, "wb"))

# If data should be loaded instead, following commands will be run
elif answer == "load":
    # get full simulation stored in pickle file
    transactions = pickle.load(open(PIKdata, "rb"))
    ReturningCust = pickle.load(open(PIKreturn, "rb"))
    # simulate four month to see that program works fine
    ReturningCustFourMonth = ReturningCust # copy list of returning customers just to show changes
    transactionsFourMonths = SimulateRange(dfprob, ReturningCustFourMonth, items, start="2017-11-01", end="2018-02-10")
    # transform created data to show objects along with their attributes
    transactionsFourMonths = NoObjects(transactionsFourMonths)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactionsFourMonths, open(PIKdata4month, "wb"))
    pickle.dump(ReturningCustFourMonths, open(PIKreturn4month, "wb"))

# If input is not specified correctly, this message will appear
else:
    print("Either 'run' or 'load' needs to be specified!")




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
transactions['TIME'] = transactions['TIME'].astype(str)
# TODO: plot is ugly but if we need a plot with confidence intervals thats the code
trans_mean_day = transactions.groupby(by='TIME').mean().reset_index()
trans_std_day = transactions.groupby(by='TIME').std().reset_index()

plt.figure()
plt.plot(trans_mean_day.TIME, trans_mean_day.TURNOVER, trans_mean_day.TIPS)
plt.fill_between(trans_std_day.TIME, trans_mean_day.TURNOVER - 2 * trans_std_day.TURNOVER, trans_mean_day.TURNOVER + 2 * trans_std_day.TURNOVER, color="b", alpha=0.2)
plt.fill_between(trans_std_day.TIME, trans_mean_day.TIPS - 2 * trans_std_day.TIPS, trans_mean_day.TIPS + 2 * trans_std_day.TIPS, color="r", alpha=0.2)


# -- aggregated income by types
trans_sum_type = transactions.groupby(by=['DATE', 'CUSTOMER_TYPE']).sum().reset_index()
trans_sum_type['TOTAL'] = trans_sum_type['TURNOVER'] + trans_sum_type['TIPS']
trans_sum_type = trans_sum_type.pivot(index="DATE", columns="CUSTOMER_TYPE", values="TOTAL")

plt.stackplot(trans_sum_type.index, trans_sum_type['hipster returning'], trans_sum_type['normal one time'],
              trans_sum_type['normal returning'], trans_sum_type['tripadvisor one time'],
              labels = ['Hipster','Normal one-time','Normal returning','Tripadvised'])
plt.legend(bbox_to_anchor=(0.01, .925, .98, 1.5), loc='lower left', mode="expand", ncol=4, borderaxespad=0.)
plt.ylabel('Value in €')
plt.xlabel('Date')
plt.title('Aggregated turnover per day by customer type')

#
# #-- average income by type over years
#
# #average income by day
# mean_day=transactionsFourMonths.groupby('DATE').sum().reset_index()
#
# mean_turn_day= (mean_day['TURNOVER']).mean() #mean turnover per day is 773$
# mean_tip_day= (mean_day['TIPS']).mean() #mean tips per day is $

data = data.copy(deep=True)  # Make a copy so dataframe not overwritten

## *********************************************************************************************************************
## Part VI: Comparison with given data *********************************************************************************
## *********************************************************************************************************************

# load dataframe
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
df = pd.read_csv(importpath, sep=";")

# Data cleaning
def Cleandata(dataframe):
    dataframe['DATETIME'] = pd.to_datetime(dataframe['TIME'])
    dataframe['YEAR'] = dataframe.DATETIME.dt.year
    dataframe['WEEKDAY'] = dataframe.DATETIME.dt.day_name()
    dataframe['WEEKDAY'] = dataframe.DATETIME.dt.day_name()
    dataframe['TIME'] = dataframe.DATETIME.dt.time
    dataframe['DATE'] = dataframe.DATETIME.dt.date
    dataframe['FOOD'] = dataframe['FOOD'].fillna('nothing')
    return dataframe

df = Cleandata(df)

# Assign price to each item
prices_drinks = {'DRINKS': ['coffee', 'frappucino', 'milkshake', 'soda', 'tea', 'water'],
          'PRICE_DRINKS': [3, 4, 5, 3, 3, 2]}
prices_drinks = pd.DataFrame(prices_drinks)

prices_food= {'FOOD': ['cookie', 'muffin', 'pie', 'sandwich', 'nothing'],
          'PRICE_FOOD': [2, 3, 3, 2, 0]}
prices_food = pd.DataFrame(prices_food)

# function for turnover
def prices(df):
    df_prices = pd.merge(df,prices_drinks, how='left', on='DRINKS')
    df_prices = pd.merge(df_prices, prices_food, how='left', on='FOOD')
    df_prices['TURNOVER']=df_prices['PRICE_FOOD']+df_prices['PRICE_DRINKS']
    return df_prices
df_prices = prices(df)

# function for tips : we don't know who are the tripadvised customers, so we randomly select 8% of the customers that
##will pay a tip
def tips(df):
    df_tips = df.sample(frac=.08)
    df_tips['TIPS'] = (np.random.randint(0, 11, size=len(df_tips)))
    df_tips = df_tips[['CUSTOMER', 'TIPS']]
    df_tips['TIPS'] = df_tips['TIPS'].astype(int)
    df_tips = df_tips.drop_duplicates(subset=['CUSTOMER'])
    return df_tips

df_tips=tips(df)

# function for all prices
def total(df_prices):
    df_prices = pd.merge(df_prices, df_tips, how='left', on='CUSTOMER')
    df_prices['TIPS'] = df_prices['TIPS'].fillna(0)
    return df_prices

df_prices = total(df_prices)
