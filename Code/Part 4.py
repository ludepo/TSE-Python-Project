#1. Show some buying histories of returning customers for your simulations

#2.From the provided datast:
#how many returning cust?
#specific time for returning?
 #   prob of 1 time ror returner at a given time?
   # how does this impact their buying history?
    #correlation?

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# define input and output path

importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
exportpath = os.path.abspath("./Results/dfprobs.csv")

# load dataframe
df = pd.read_csv(importpath, sep=";")

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
returners.drop_duplicates(subset=['CUSTOMER'], keep=False)
returners[['TIME','prob_returners']].plot('TIME', figsize=(15,8))#graph for returners

#specific time for one-time customers?
onetimer= df.drop_duplicates(subset= ['CUSTOMER'],keep=False)
onetimer=onetimer.assign(prob_onetimer=onetimer.TIME.map(onetimer.TIME.value_counts(normalize=True)))
onetimer[['TIME','prob_onetimer']].plot('TIME', figsize=(15,8)) #graph for onetime customers



#
df['RET']=(df.duplicated(keep=False, subset=['CUSTOMER']))*1 #dummy variable for returners

time=df.groupby(['TIME', 'RET']).count()['CUSTOMER'].unstack(level=0) #count each type of customer at each period
time=time.transpose()
time= time.rename(columns={time.columns[0]: "onetimer",time.columns[1]:"returner"})
time['prob_onetimer']=time['onetimer']/(time['onetimer']+time['returner'])
time['prob_returner']=time['returner']/(time['onetimer']+time['returner']) # we have the probability at each given time that the consumer is onetimer of returner

time.reset_index(inplace=True)
time[['TIME','prob_onetimer']].plot('TIME', figsize=(15,8))#graph for onetimers
time[['TIME','prob_returner']].plot('TIME', figsize=(15,8))#graph for returners

#TBD: function to integrate those prob

# graph test
df.groupby(['TIME', 'DRINKS']).count()['YEAR'].unstack().plot()
plt.show()


#function for change in price

#impact of: unlimited budget for returners? possibility of buying 2 drinks?