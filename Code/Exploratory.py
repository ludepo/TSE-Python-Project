# 0) Import libraries and data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# define inupt and output path
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
exportpath = os.path.abspath("../Results/Outputdata.csv")

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
df.groupby(df['YEAR']).count()
plt.show()

a = df['FOOD'].groupby(df[['YEAR', 'FOOD']]).count()
plt.show()

df['DRINKS'].groupby(df['TIME']).count().plot()
plt.bar.show()

df['DRINKS'].groupby(df['WEEKDAY']).count().plot()
plt.show()

df['FOOD'].groupby(df['DATE']).count().plot()
plt.show()

df['DRINKS'].groupby(df['DATE']).count().plot()
plt.show()

# 3) Determine the average that a customer buys a certain food or drink at any given time:
dfprob = df.drop(['CUSTOMER', 'DATETIME', 'YEAR', 'WEEKDAY', 'DATE'], axis=1)
dfprob = pd.get_dummies(dfprob, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"]).\
                 groupby('TIME').\
                 sum()
drinks = ['DRINK_coffee', 'DRINK_frappucino', 'DRINK_milkshake', 'DRINK_soda', 'DRINK_tea', 'DRINK_water']
food =  ['FOOD_cookie', 'FOOD_muffin', 'FOOD_nothing', 'FOOD_pie', 'FOOD_sandwich']
dfprob['totalDrinks'] = dfprob[drinks].sum(axis=1)
dfprob['totalFood'] = dfprob[food].sum(axis=1)

for i in drinks:
    dfprob[i] = round(dfprob[i]/dfprob['totalDrinks']*100)
for i in food:
    dfprob[i] = round(dfprob[i]/dfprob['totalFood']*100)
dfprob['ID'] = dfprob.index

for index,row in dfprob.iterrows():
    print("On average the probability of a costumer at %s buying coffee, soda and water is %s, %s, %s and for "
          "food %s sandwiches, %s muffins and %s nothing."
          %(row['ID'], row['DRINK_coffee'], row['DRINK_soda'], row['DRINK_water'],
            row['FOOD_sandwich'], row['FOOD_muffin'], row['FOOD_nothing']))

dfprob[drinks].plot()
plt.show()
dfprob[['FOOD_cookie', 'FOOD_muffin', 'FOOD_pie', 'FOOD_sandwich']].plot()
plt.show()




df.groupby(['TIME', 'FOOD']).count()['YEAR'].unstack()



    plot()
plt.show()
df['DATETIME'][df['FOOD'] == "sandwich"].dt.hour.describe()
df[df['FOOD'] != 'sandwich'].groupby(['TIME', 'FOOD']).count()['YEAR'].unstack().plot()
plt.show()

df.groupby(['TIME', 'DRINKS']).count()['YEAR'].unstack().plot()
plt.show()

df[df['DRINKS'] != 'soda'].groupby(['TIME', 'FOOD']).count()['YEAR'].unstack().plot()
plt.show()
df[df['DRINKS'] == 'soda'].groupby(['TIME', 'FOOD']).count()['YEAR'].unstack().plot()
plt.show()
df['DRINKS'][df['DRINKS'] == 'soda'].corr([df['FOOD'] != 'sandwich'], method='pearson')

df[df['DRINKS'] != 'soda'].groupby(['TIME', 'DRINKS']).count()['YEAR'].unstack().plot()
plt.show()
