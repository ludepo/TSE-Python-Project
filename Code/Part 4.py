#1. Show some buying histories of returning customers for your simulations

#2.From the provided datast:
#how many returning cust?
#specific time for returning?
 #   prob of 1 timer or returner at a given time?
   # how does this impact their buying history?
    #correlation?

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import cov

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

barWidth = 0.1
r1 = np.arange(len(list_onet))
r2 = [x + barWidth for x in r1]

plt.bar(r1, list_onet, width = barWidth, color = 'blue', edgecolor = 'black',  capsize=7, label='onetimers')
plt.bar(r2, list_ret, width = barWidth, color = 'cyan', edgecolor = 'black',  capsize=7, label='returners')
plt.xticks([r + barWidth for r in range(len(list_onet))], ['coffee', 'frappucino', 'milkshake','soda','tea','water','cookie','muffin','nthing','pie','sandwich'])
plt.ylabel('prob')
plt.legend()
plt.show()




##bar graph comparing probs

##
import pickle
PIK = "Data/transactionsDF.dat"
transactions = pickle.load(open(PIK, "rb"))



#impact of: unlimited budget for returners? possibility of buying 2 drinks?