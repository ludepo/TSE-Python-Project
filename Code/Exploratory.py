import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

## *********************************************************************************************************************
## 0: Import data ******************************************************************************************************
## *********************************************************************************************************************


# define input and output path
importpath = os.path.abspath("./Data/Coffeebar_2016-2020.csv")
exportpath_probs = os.path.abspath("./Results/dfprobs.csv")
exportpath_data = os.path.abspath("./Results/coffee_bar_prices.csv")

# load dataframe
df = pd.read_csv(importpath, sep=";")

## *********************************************************************************************************************
## I: Transformation of the Given Dataset ******************************************************************************
## *********************************************************************************************************************

# 1.1) explore data
print(df.head())
print(df.dtypes)


# 1.2) Add variables for analysis
def addcolumns(dataframe):  # function serves to add variables for easier grouping of data
    data = dataframe.copy(deep=True)  # Make a copy so dataframe not overwritten
    data['DATETIME'] = pd.to_datetime(data['TIME'])
    data['YEAR'] = data.DATETIME.dt.year
    data['WEEKDAY'] = data.DATETIME.dt.day_name()
    data['TIME'] = data.DATETIME.dt.time
    data['DATE'] = data.DATETIME.dt.date
    data['FOOD'] = data['FOOD'].fillna('nothing')
    return data


df = addcolumns(df)

## *********************************************************************************************************************
## II: Insight of the data  ********************************************************************************************
## *********************************************************************************************************************

# 2.1) What food and drinks are sold by the coffee bar?
print(df.DRINKS.value_counts())
print(df.FOOD.value_counts())

# -- How many unique customers did the bar have?
print(df.CUSTOMER.count())
print(df.CUSTOMER.nunique())

# 2.2) Create plots to illustrate the data
# -- Count number of each drinks sold over the 5 years span
plt.bar(df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).DRINKS,
        df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).TIME)
plt.show()

# -- Count number of each food sold over the 5 years span
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

## *********************************************************************************************************************
## IV: Add prices for later comparison *********************************************************************************
## *********************************************************************************************************************

# 4.1) Assign price to each item
prices_drinks = {'DRINKS': ['coffee', 'frappucino', 'milkshake', 'soda', 'tea', 'water'],
                 'PRICE_DRINKS': [3, 4, 5, 3, 3, 2]}
prices_drinks = pd.DataFrame(prices_drinks)

prices_food = {'FOOD': ['cookie', 'muffin', 'pie', 'sandwich', 'nothing'],
               'PRICE_FOOD': [2, 3, 3, 2, 0]}
prices_food = pd.DataFrame(prices_food)


# 4.2) Add turnover in the data
# function for turnover
def prices(dataframe):
    dataframe = pd.merge(dataframe, prices_drinks, how='left', on='DRINKS')
    dataframe = pd.merge(dataframe, prices_food, how='left', on='FOOD')
    dataframe['TURNOVER'] = dataframe['PRICE_FOOD'] + dataframe['PRICE_DRINKS']
    return dataframe


df_prices = prices(df)


# 4.2) Add tips in the data
# function for tips : we don't know who are the tripadvised customers in this dataset, only that they represent 10% of
# one-time customers. So we randomly select the 10% of the one-time customers that will pay a tip.
def tips(dataframe):  # function that takes a subsample of 10% of onetimers and assign them a tip
    dataframe = dataframe.drop_duplicates(subset=['CUSTOMER'], keep=False)
    dataframe = dataframe.sample(frac=.1)
    dataframe['TIPS'] = (np.random.randint(0, 11, size=len(dataframe)))
    dataframe = dataframe[['CUSTOMER', 'TIPS']]
    dataframe['TIPS'] = dataframe['TIPS'].astype(int)
    return dataframe


df_tips = tips(df)


def total(df_prices):  # function that merge turnover and tips in the same dataset
    df_prices = pd.merge(df_prices, df_tips, how='left', on='CUSTOMER')
    df_prices['TIPS'] = df_prices['TIPS'].fillna(0)
    return df_prices


coffee_bar_prices = total(df_prices)

## *********************************************************************************************************************
## V: Export Data ******************************************************************************************************
## *********************************************************************************************************************
# Export database that will be used later

dfprob.to_csv(exportpath_probs, sep=";", index=False)
coffee_bar_prices.to_csv(exportpath_data, sep=";", index=False)
