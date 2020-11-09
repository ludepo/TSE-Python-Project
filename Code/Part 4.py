import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import cov




#1. Show some buying histories of returning customers for your simulations
ReturningCust[555].purchase_history()
ReturningCust[999].purchase_history()

#2.From the provided datast:
#how many returning cust?
#specific time for returning?
 #   prob of 1 timer or returner at a given time?
   # how does this impact their buying history?
    #correlation?



# define input and output path
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
exportpath = os.path.abspath("./Results/dfprobs.csv")

# load dataframe
df = pd.read_csv(importpath, sep=";")

#Data cleaning
df['DATETIME'] = pd.to_datetime(df['TIME'])
df['YEAR'] = df.DATETIME.dt.year
df['WEEKDAY'] = df.DATETIME.dt.day_name()
df['TIME'] = df.DATETIME.dt.time
df['DATE'] = df.DATETIME.dt.date
print(df.dtypes)

df['CUSTOMER'].isnull().sum()
df['DRINKS'].isnull().sum()
df['FOOD'].isnull().sum()
df = df.fillna('nothing')

#specific time for returning customers?
returners=df[df['CUSTOMER'].duplicated(keep=False)]
returners=returners.assign(prob_returners=returners.TIME.map(returners.TIME.value_counts(normalize=True)))
returners.drop_duplicates( keep=False) #dataset with probabilities for returners at each time
returners[['TIME','prob_returners']].plot('TIME', figsize=(15,8))#graph for returners: We observe that returners
##have specific showing time: they show in the marning, up to 11 am. Then few returners between 11 and 13.
###Then the main time for returners is between 13 and 18

#specific time for one-time customers?
onetimer= df.drop_duplicates(subset= ['CUSTOMER'],keep=False)
onetimer=onetimer.assign(prob_onetimer=onetimer.TIME.map(onetimer.TIME.value_counts(normalize=True)))
onetimer.drop_duplicates( keep=False) #dataset with probabilities for onetimers at each time
onetimer[['TIME','prob_onetimer']].plot('TIME', figsize=(15,8)) #graph for onetime customers: One timers also have
## specific showing time: they come mainly between 11 and 13, and are very few to come after 13

#
df['RET']=(df.duplicated(keep=False, subset=['CUSTOMER']))*1 #dummy variable for returners

time=df.groupby(['TIME', 'RET']).count()['CUSTOMER'].unstack(level=0) #count each type of customer at each period
time=time.transpose()
time= time.rename(columns={time.columns[0]: "onetimer",time.columns[1]:"returner"})
time['prob_onetimer']=time['onetimer']/(time['onetimer']+time['returner'])
time['prob_returner']=time['returner']/(time['onetimer']+time['returner']) # we have the probability at each given time that the consumer is onetimer or returner
time.reset_index(inplace=True)


time[['TIME','prob_returner']].plot('TIME', figsize=(15,8))#graph for returners : 20% of customers are returners
##from 8 to 11, then 10% up to 13h, then 30% after 13
time[['TIME','prob_onetimer']].plot('TIME', figsize=(15,8))#graph for onetimers: 80% from 8 to 11, 90% from 11 to 13,
### 70% rest of the day

# graph food and drinks
df.groupby(['TIME', 'DRINKS']).count()['YEAR'].unstack().plot()
plt.show() ## coffee is mainly drink before 11, soda alsmost exclusively between 11 and 13

df.groupby(['TIME', 'FOOD']).count()['YEAR'].unstack().plot()
plt.show() #nothing is ordered as food before 11. sandwiches are only ordered between 13 and 18

#correlation
dftest = pd.get_dummies(df, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"]). \
    groupby('RET'). \
    mean()
dftest=dftest.transpose()
dftest=dftest.drop('YEAR')
dftest= dftest.rename(columns={dftest.columns[0]: "onetimer",dftest.columns[1]:"returner"})

list_onet=dftest['onetimer'].values.tolist()
list_ret=dftest['returner'].values.tolist()

##bar graph comparing probs for different items
barWidth = 0.1
r1 = np.arange(len(list_onet))
r2 = [x + barWidth for x in r1]

plt.bar(r1, list_onet, width = barWidth, color = 'blue', edgecolor = 'black',  capsize=7, label='onetimers')
plt.bar(r2, list_ret, width = barWidth, color = 'cyan', edgecolor = 'black',  capsize=7, label='returners')
plt.xticks([r + barWidth for r in range(len(list_onet))], ['coffee', 'frappucino', 'milkshake','soda','tea','water','cookie','muffin','nthing','pie','sandwich'])
plt.ylabel('prob')
plt.legend()
plt.show()



##
import pickle
PIK = "Data/transactionsDF.dat"
transactions = pickle.load(open(PIK, "rb"))



#impact of: unlimited budget for returners? possibility of buying 2 drinks?








# What would happen if we lower the returning customers to 50 and simulate the same period?
## the code would crash if we do not make the additional assumption that once all returning customers are bankrupt,
## only 90% normal one-time customers or 10% tripadvised customers would enter the cafe (see ChooseCustomers())


# The budget of hipsters drops to 40
## the same as if we would only have 50 returning customers, since the budget of the hipsters would be zero rather
## quickly. Therefore, the normal returning customers would compensate and also be bankrupt soon. Once all returning
## customers are bankrupt the code would crash without the additional assumption.


# The prices change from the beginning of 2018 and go up by 20%
# create function that will assign a purchase object for a given customer at a given hour and minute
def MakePurchase(customer, hour, minute, probabilities, date):  # probabilities refers to dataframe obtained in Exploratory.py
    purchase = Purchase(customer, hour, minute, probabilities)  # create purchase object given customer, hour and minute
    if (date.astype('datetime64[D]') > np.datetime64("2017-12-31").astype('datetime64[D]')):
        purchase.value = purchase.value * 1.2
    else:
        None
    customer.money_spent += purchase.payment  # update money_spent attribute of chosen customer
    customer.budget -= purchase.payment  # update budget of chosen customer
    customer.purchases.append(purchase)  # update purchase history of chosen customer

    return purchase


def SimulateRange(probabilities, start = "2016-01-01", end = "2020-12-31"):
    daterange = pd.date_range(start=start,end=end).strftime("%Y-%m-%d").to_list() # define range of date
    time = probabilities['ID']
    transactions = pd.DataFrame({'DATETIME' : [pd.to_datetime(" ".join(i)) for i in product(daterange, time)]})
    transactions['HOUR'] = transactions['DATETIME'].dt.strftime("%H") # get hour from datetime column
    transactions['MINUTE'] = transactions['DATETIME'].dt.strftime("%M") # get minute from datetime column
    transactions['CUSTOMER'] = None
    transactions['PURCHASE'] = None
    for i in progressbar(range(0, len(transactions))): # *** see comment below
        transactions['CUSTOMER'][i] = ChooseCustomer() # assign customer object for given time
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i], # assign purchase object
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities,
                                                   transactions['DATETIME'].values[i])
    return transactions


# run a new simulation for comparison (smaller time horizon)
transactions_inflat = SimulateRange(dfprob,start = "2017-11-01", end = "2018-02-10")
transactions_inflat = NoObjects(transactions_inflat)






## Impact of: changing assumption that 20% chance for returner even when most returners are bankrupt (instead 0.02%
#             chance per solvent returner

# ChooseCust() with assumption that returners will not go more often if another returner is bankrupt but instead go
#     like before
def ChooseCustomer():
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if ReturningCust[i].budget > 8]  # is returner solvent?
    allcust = [Customer(), Tripadvised()] # create list for possible customers (note we do not care what Customer() or
    allcust.extend(liquid)                # Tripadvised() comes, but for Returner() and Hipster() we want to keep track
    weights = [72, (100-72-len(liquid)*(20/len(ReturningCust)))] # bankrupt returning customers are replaced by Tripadvised
    weights.extend(list(repeat((20/len(ReturningCust)), len(liquid)))) # prob. of repeating returner dependen on overall nr.
    if liquid != []:
        customer = random.choices(allcust, weights=weights, k=1)  # 8% tripadvisor customer
    else:
        customer = random.choices([Customer(), Tripadvised()], weights=[72, 28], k=1)  # if all returners bankrupt
    return customer[0]



