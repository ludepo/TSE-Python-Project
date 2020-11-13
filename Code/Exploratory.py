# 0) Import libraries and data
import pandas as pd
import os
import matplotlib.pyplot as plt
from numpy import cov

# TODO: clean file

## *********************************************************************************************************************
## I: Define Inputs and prepare data  **********************************************************************************
## *********************************************************************************************************************

# define input and output path
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
exportpath = os.path.abspath("./Results/dfprobs.csv")

# load dataframe
df = pd.read_csv(importpath, sep=";")

# explore data
print(df.head())
print(df.dtypes)

# add variables for analysis

def AddColumns(dataframe):  # function serves to add variables for easier grouping of data
    data = dataframe.copy(deep=True)  # Make a copy so dataframe not overwritten
    data['DATETIME'] = pd.to_datetime(data['TIME'])
    data['YEAR'] = data.DATETIME.dt.year
    data['WEEKDAY'] = data.DATETIME.dt.day_name()
    data['TIME'] = data.DATETIME.dt.time
    data['DATE'] = data.DATETIME.dt.date
    data['FOOD'] = data['FOOD'].fillna('nothing')
    return data

df = AddColumns(df)

## *********************************************************************************************************************
## II: Insight of the data  ********************************************************************************************
## *********************************************************************************************************************

# 1) What food and drinks are sold by the coffee bar?
print(df.DRINKS.value_counts())
print(df.FOOD.value_counts())

# -- How many unique customers did the bar have?
print(df.CUSTOMER.count())
print(df.CUSTOMER.nunique())

# 2) Create (at least) a bar plot of total amount of sold foods (plot1) and drinks (plot2) over the five years

# -- Count number of each food/drik sold over the 5 years span
plt.bar(df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).DRINKS,
        df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).TIME)
plt.show()

plt.bar(df.groupby(by="FOOD", as_index=False).count().sort_values(by='TIME', ascending=False).FOOD,
        df.groupby(by="FOOD", as_index=False).count().sort_values(by='TIME', ascending=False).TIME)
plt.show()

# -- Different foods and drinks sold depending on the time of the day
df.groupby(['TIME', 'FOOD']).count()['YEAR'].unstack().plot()
plt.show()
df.groupby(['TIME', 'DRINKS']).count()['YEAR'].unstack().plot()
plt.show()

# -- Graph for food and drinks depending on the week day
df.groupby(['WEEKDAY', 'DRINKS']).count()['YEAR'].unstack().plot.bar()
plt.show()
df.groupby(['WEEKDAY', 'FOOD']).count()['YEAR'].unstack().plot.bar()
plt.show()

## *********************************************************************************************************************
## III: Obtain time probabilities   ************************************************************************************
## *********************************************************************************************************************

# Determine the average that a customer buys a certain food or drink at any given time:


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

# Dataframe for probabilities of buying certain drink depending on the time of the day
dfpropdrink = dfprob[['DRINK_coffee', 'DRINK_soda', 'DRINK_frappucino', 'DRINK_milkshake', 'DRINK_tea', 'DRINK_water']]
dfpropdrink.plot.area()
plt.show()

# Dataframe for probabilities of buying certain food depending on the time of the day
dfpropfood = dfprob[['FOOD_cookie', 'FOOD_muffin', 'FOOD_nothing', 'FOOD_pie', 'FOOD_sandwich']]
dfpropfood.plot.area()
plt.show()

dfprob.to_csv(exportpath, sep=";", index=False)
