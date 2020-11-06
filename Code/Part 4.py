#1. Show some buying histories of returning customers for your simulations

#2.From the provided datast:
#how many returning cust?
#specific time for returning?
 #   prob of 1 timer at a given time
  #  prob of returning at a given time?
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

#Returning customer table
returners=df[df['CUSTOMER'].duplicated(keep=False)]
returners=returners.assign(pro=returners.TIME.map(returners.TIME.value_counts(normalize=True)))

returners.drop_duplicates(subset=['CUSTOMER'], keep=False)
returners[['TIME','pro']].plot('TIME', figsize=(15,8))#graph for returners

#One-time customer
onetimer= df.drop_duplicates(subset= ['CUSTOMER'],keep=False)
onetimer=onetimer.assign(pro=onetimer.TIME.map(onetimer.TIME.value_counts(normalize=True)))
onetimer[['TIME','pro']].plot('TIME', figsize=(15,8)) #graph for onetime customers



#
df['RET']=(df.duplicated(keep=False, subset=['CUSTOMER']))*1
df['RET'] = 'returner' if df['RET'] == 1 else 'onetimer'
test=returners.groupby(['TIME', 'FOOD'], axis=1).count()