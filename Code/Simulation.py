from Code.Customers import *
import pickle
import matplotlib.pyplot as plt
import os

## *********************************************************************************************************************
## Part I: Define Inputs ***********************************************************************************************
## *********************************************************************************************************************

# import and export path
import_dfprob = os.path.abspath("../Results/dfprobs.csv")
exportpath_sim = os.path.abspath("../Results/Simulation.csv")

# define path where pickle file of full simulation should be saved/ loaded from
PIKdata = "../Data/transactionsDF.dat"
PIKreturn = "../Data/ReturningCust.dat"
PIKdata4month = "../Data/data4month.dat"
PIKreturn4month = "../Data/Cust4month.dat"

# create list of item objects that are sold in cafe: item(name, price, type)
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

# load dataframe with choice probabilities obtained from Exploratory.py
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
    # save simulated data as csv for completeness
    transactions.to_csv(exportpath_sim, sep=";", index=False)

# If data should be loaded instead, following commands will be run
elif answer == "load":
    # simulate four month to see that program works fine
    ReturningCustFourMonth = ReturningCust.copy()  # copy list of returning customers just to show changes
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

# Give examples of purchases (random)
transactions['PURCHASE'][1].describe_purchase()
transactions['PURCHASE'][11].describe_purchase()
transactions['PURCHASE'][996].describe_purchase()

# How much money was spent by returning customers?
moneyspent = [ReturningCust[i].money_spent for i in range(len(ReturningCust))]
print("The average amount spent by a returning customer was %s" % (sum(moneyspent) / len(moneyspent)))

# How much budget do returning customers have left?
budgets = [ReturningCust[i].budget for i in range(len(ReturningCust))]
print("The average budget left for a normal returning customer was %s??? and for a hipster %s???"
      % (round(sum(budgets[:666]) / len(budgets[:666])), round(sum(budgets[666:]) / len(budgets[666:]))))

# -- average income during day
trans_mean_day = transactions.groupby(by='TIME').mean().reset_index()

plt.figure()
plt.plot(trans_mean_day.TIME, trans_mean_day.TURNOVER, label='Turnover mean')
plt.plot(trans_mean_day.TIME, trans_mean_day.TIPS, label='Tips mean')
plt.xticks(trans_mean_day['TIME'][::30], trans_mean_day['TIME'][::30])
plt.legend(frameon=False, loc='center right')
plt.xlabel('Hour of the day')
plt.ylabel('Values in ???')
plt.title('Average income during day own simulation')
plt.savefig('../Results/MeanIncomeDay.png')
plt.show()


# -- aggregated income by types per day
# create function to aggregate data by type per day
def sumtype(dataframe):
    data = dataframe.copy(deep=True)
    data = data.groupby(by=['DATE', 'CUSTOMER_TYPE']).sum().reset_index()
    data['TOTAL'] = data['TURNOVER'] + data['TIPS']
    data = data.pivot(index="DATE", columns="CUSTOMER_TYPE", values="TOTAL")
    return data


trans_sum_type = sumtype(transactions)

plt.figure(figsize=(12, 4.5))
plt.stackplot(trans_sum_type.index, trans_sum_type['tripadvisor_one_time'], trans_sum_type['normal_one_time'],
              trans_sum_type['hipster_returning'], trans_sum_type['normal_returning'],
              labels=['Tripadvised', 'Normal one-time', 'Hipster', 'Normal returning'])
plt.legend(bbox_to_anchor=(0.01, .925, .98, 1.5), loc='lower left', mode="expand", ncol=4, borderaxespad=0.)
plt.ylabel('Value in ???')
plt.xlabel('Date')
plt.title('Aggregated turnover per day by customer type own simulation')
plt.savefig('../Results/IncomeDaySim.png')
plt.show()

## *********************************************************************************************************************
## Part IV: Comparison with given data *********************************************************************************
## *********************************************************************************************************************

# load dataframe
importpath = os.path.abspath("../Results/coffeebar_prices.csv")
df = pd.read_csv(importpath, sep=";")

# -- average income during day
trans_mean_day = df.groupby(by='TIME').mean().reset_index()

plt.figure()
plt.plot(trans_mean_day.TIME, trans_mean_day.TURNOVER, label='Turnover mean')
plt.plot(trans_mean_day.TIME, trans_mean_day.TIPS, label='Tips mean')
plt.xticks(trans_mean_day['TIME'][::30], trans_mean_day['TIME'][::30])
plt.legend(frameon=False, loc='center right')
plt.xlabel('Hour of the day')
plt.ylabel('Values in ???')
plt.title('Average income during day given data')
plt.savefig('../Results/MeanIncomeDayOriginalData.png')
plt.show()

# -- aggregated income by types per day
# create function to aggregate data by type per day: in the given dataset we only identify returners ans onetimers
def aggregate(dataframe):
    data = dataframe.copy(deep=True)
    data = data.groupby(by=['DATE', 'RET']).sum().reset_index()
    data['TOTAL'] = data['TURNOVER'] + data['TIPS']
    data = data.pivot(index="DATE", columns="RET", values="TOTAL")
    data = data.rename(columns={data.columns[0]: "onetimer", data.columns[1]: "returner"})
    return data


by_type = aggregate(df)

plt.figure(figsize=(12, 7))
plt.stackplot(by_type.index, by_type['onetimer'], by_type['returner'],
              labels=['Onetimer', 'Returner'])
plt.legend(bbox_to_anchor=(0.85, 0.95), loc="center left", borderaxespad=0)
plt.ylabel('Value in ???')
plt.xlabel('Date')
plt.xticks(by_type.index[::100], by_type.index[::100])
plt.title('Aggregated turnover per day by customer type given data')
plt.xticks(rotation=45)
plt.savefig('../Results/IncomeDaySimOriginalData.png')
plt.show()