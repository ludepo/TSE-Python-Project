# 0) Import libraries and data
import pandas as pd
import os
import matplotlib.pyplot as plt
from numpy import cov

# define input and output path
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
exportpath = os.path.abspath("./Results/dfprobs.csv")

# load dataframe
df = pd.read_csv(importpath, sep=";")

# explore data
print(df.head())
print(df.dtypes)

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

# 1) What food and drinks are sold by the coffee bar? How many unique customers did the bar have?
print(df.DRINKS.value_counts())
print(df.FOOD.value_counts())
print(df.CUSTOMER.count())
print(df.CUSTOMER.nunique())

# 2) Create (at least) a bar plot of total amount of sold foods (plot1) and drinks (plot2) over the five years

# -- Count number of each food/drik sold over the 5 years span
plt.bar(df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).DRINKS,
        df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).TIME)

plt.bar(df.groupby(by="FOOD", as_index=False).count().sort_values(by='TIME', ascending=False).FOOD,
        df.groupby(by="FOOD", as_index=False).count().sort_values(by='TIME', ascending=False).TIME)

# -- Does the time of the day impact the choice of food/drinks? SURPRISE...: Yes it does
df.groupby(['TIME', 'FOOD']).count()['YEAR'].unstack().plot()
df.groupby(['TIME', 'DRINKS']).count()['YEAR'].unstack().plot()

# -- Graph for food and drinks depending on the day: the day as no impact on the chosen food
df.groupby(['WEEKDAY', 'DRINKS']).count()['YEAR'].unstack().plot.bar()
df.groupby(['WEEKDAY', 'FOOD']).count()['YEAR'].unstack().plot.bar()

# 3) Determine the average that a customer buys a certain food or drink at any given time:
dfprob = df.drop(['CUSTOMER', 'DATETIME', 'YEAR', 'WEEKDAY', 'DATE'], axis=1)
dfprob = pd.get_dummies(dfprob, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"]). \
    groupby('TIME'). \
    mean()
for i in dfprob.columns:
    dfprob[i] = round(dfprob[i] * 100)

dfprob = dfprob.astype(int)
dfprob['ID'] = dfprob.index

for index, row in dfprob.iterrows():
    print("On average the probabilities of a costumer buying the following drinks at %s are: "
          "coffee %s, soda %s, water %s, tea %s, milkshake %s, frappucino %s and for food: "
          "sandwich %s, muffin %s, cookie %s, pie %s or nothing %s."
          % (row['ID'], row['DRINK_coffee'], row['DRINK_soda'], row['DRINK_water'], row['DRINK_tea'],
             row['DRINK_milkshake'], row['DRINK_frappucino'],
             row['FOOD_sandwich'], row['FOOD_muffin'], row['FOOD_cookie'], row['FOOD_pie'], row['FOOD_nothing']))

dfpropdrink = dfprob[['DRINK_coffee', 'DRINK_soda', 'DRINK_frappucino', 'DRINK_milkshake', 'DRINK_tea', 'DRINK_water']]
dfpropdrink.plot.area()

dfpropfood = dfprob[['FOOD_cookie', 'FOOD_muffin', 'FOOD_nothing', 'FOOD_pie', 'FOOD_sandwich']]
dfpropfood.plot.area()

dfprob.to_csv(exportpath, sep=";", index=False)
