from Code.Customers import *
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

## *********************************************************************************************************************
## Part I: Define Inputs ***********************************************************************************************
## *********************************************************************************************************************

# import and export path
import_dfprob = os.path.abspath("./Results/dfprobs.csv")
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

# load dataframe with probabilities obtained from Exploratory.py
dfprob = pd.read_csv(import_dfprob, sep=";")
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
## Following choice has to be taken: Either full simulation in line 68 can be run which will take approx. 40min (8GB ram)
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
    # simulate four month to see that program works fine
    ReturningCustFourMonth = ReturningCust.copy() # copy list of returning customers just to show changes
    transactionsFourMonths = SimulateRange(dfprob, ReturningCustFourMonth, items, start="2017-11-01", end="2018-02-10")
    # transform created data to show objects along with their attributes
    transactionsFourMonths = NoObjects(transactionsFourMonths)
    # save simulated data as pickle in order to access objects later again
    pickle.dump(transactionsFourMonths, open(PIKdata4month, "wb"))
    pickle.dump(ReturningCustFourMonth, open(PIKreturn4month, "wb"))
    # get full simulation stored in pickle file
    transactions = pickle.load(open(PIKdata, "rb"))
    ReturningCust = pickle.load(open(PIKreturn, "rb"))

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
      %(round(sum(budgets[:666])/len(budgets[:666])), round(sum(budgets[666:])/len(budgets[666:]))))

# -- average income during day
trans_mean_day = transactions.groupby(by='TIME').mean().reset_index()

plt.figure()
plt.plot(trans_mean_day.TIME, trans_mean_day.TURNOVER, label='Turnover mean')
plt.plot(trans_mean_day.TIME, trans_mean_day.TIPS, label='Tips mean')
plt.xticks(trans_mean_day['TIME'][::30], trans_mean_day['TIME'][::30])
plt.legend(frameon=False, loc='center right')
plt.xlabel('Hour of the day')
plt.ylabel('Values in €')
plt.title('Average income during day')



# -- aggregated income by types per day
# create function to aggregate data by type per day
def sumtype(dataframe):
    data = dataframe.copy(deep=True)
    data = data.groupby(by=['DATE', 'CUSTOMER_TYPE']).sum().reset_index()
    data['TOTAL'] = data['TURNOVER'] + data['TIPS']
    data = data.pivot(index="DATE", columns="CUSTOMER_TYPE", values="TOTAL")
    return data

trans_sum_type = sumtype(transactions)

plt.figure()
plt.stackplot(trans_sum_type.index,  trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels = ['Tripadvised','Normal one-time','Hipster','Normal returning'])
plt.legend(bbox_to_anchor=(0.01, .925, .98, 1.5), loc='lower left', mode="expand", ncol=4, borderaxespad=0.)
plt.ylabel('Value in €')
plt.xlabel('Date')
plt.title('Aggregated turnover per day by customer type')






## *********************************************************************************************************************
## Part VI: Comparison with given data *********************************************************************************
## *********************************************************************************************************************

# load dataframe

df = pd.read_csv(import_sim_old, sep=";")


# Data cleaning
def cleandata(dataframe):
    dataframe['DATETIME'] = pd.to_datetime(dataframe['TIME'])
    dataframe['YEAR'] = dataframe.DATETIME.dt.year
    dataframe['WEEKDAY'] = dataframe.DATETIME.dt.day_name()
    dataframe['WEEKDAY'] = dataframe.DATETIME.dt.day_name()
    dataframe['TIME'] = dataframe.DATETIME.dt.time
    dataframe['DATE'] = dataframe.DATETIME.dt.date
    dataframe['FOOD'] = dataframe['FOOD'].fillna('nothing')
    return dataframe


df = cleandata(df)

# Assign price to each item
prices_drinks = {'DRINKS': ['coffee', 'frappucino', 'milkshake', 'soda', 'tea', 'water'],
                 'PRICE_DRINKS': [3, 4, 5, 3, 3, 2]}
prices_drinks = pd.DataFrame(prices_drinks)

prices_food = {'FOOD': ['cookie', 'muffin', 'pie', 'sandwich', 'nothing'],
               'PRICE_FOOD': [2, 3, 3, 2, 0]}
prices_food = pd.DataFrame(prices_food)


# function for turnover
def prices(dataframe):
    dataframe = pd.merge(dataframe, prices_drinks, how='left', on='DRINKS')
    dataframe = pd.merge(dataframe, prices_food, how='left', on='FOOD')
    dataframe['TURNOVER'] = dataframe['PRICE_FOOD'] + dataframe['PRICE_DRINKS']
    return dataframe


df_prices = prices(df)


# function for tips : we don't know who are the tripadvised customers, so we randomly select 8% of the customers that
##will pay a tip
def tips(dataframe):
    dataframe = dataframe.sample(frac=.08)
    dataframe['TIPS'] = (np.random.randint(0, 11, size=len(dataframe)))
    dataframe = dataframe[['CUSTOMER', 'TIPS']]
    dataframe['TIPS'] = dataframe['TIPS'].astype(int)
    dataframe = dataframe.drop_duplicates(subset=['CUSTOMER'])
    return dataframe


df_tips = tips(df)


# function for all prices
def total(df_prices):
    df_prices = pd.merge(df_prices, df_tips, how='left', on='CUSTOMER')
    df_prices['TIPS'] = df_prices['TIPS'].fillna(0)
    return df_prices


df_prices = total(df_prices)
