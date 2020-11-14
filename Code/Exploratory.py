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
exportpath_data = os.path.abspath("./Results/coffeebar_prices.csv")

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
    data['RET'] = (data.duplicated(keep=False, subset=['CUSTOMER'])) * 1
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
# -- Count number of each drinks and food sold over the 5 years span
plt.figure(figsize=(12,7))
plt.title('Number of each drinks and food sold over 5 years')
plt.bar(df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).DRINKS,
        df.groupby(by="DRINKS", as_index=False).count().sort_values(by='TIME', ascending=False).TIME)
plt.xticks(rotation=45)

plt.bar(df.groupby(by="FOOD", as_index=False).count().sort_values(by='TIME', ascending=False).FOOD,
        df.groupby(by="FOOD", as_index=False).count().sort_values(by='TIME', ascending=False).TIME)
plt.xticks(rotation=45)
plt.savefig('./Results/FoodDrinksSold_Bar.png')
plt.show()

# -- Graph for food and drinks depending on the week day
df['WEEKDAY'] = pd.Categorical(df['WEEKDAY'],
                               categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                               ordered=True)
df.groupby(['WEEKDAY', 'DRINKS']).count()['YEAR'].unstack().plot.bar(figsize=(12,7))
plt.title('Drinks bought by day of the week')
plt.xticks(rotation=45)
plt.savefig('./Results/DrinksDay_Bar.png')
plt.show()

df.groupby(['WEEKDAY', 'FOOD']).count()['YEAR'].unstack().plot.bar(figsize=(12,7))
plt.title('Food bought by day of the week')
plt.xticks(rotation=45)
plt.savefig('./Results/FoodDay_Bar.png')
plt.show()

## *********************************************************************************************************************
## III: Obtain time probabilities   ************************************************************************************
## *********************************************************************************************************************

# 3.1) Determine the average that a customer buys a certain food or drink at any given time:

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

# Dataframe for probabilities of buying certain food depending on the time of the day
dfpropfood = dfprob[['FOOD_cookie', 'FOOD_muffin', 'FOOD_nothing', 'FOOD_pie', 'FOOD_sandwich']]


# 3.2) Graphics on the probabilities of buying different items depending on the time of the day
dfpropdrink.plot.area(figsize=(10,6))
plt.legend(bbox_to_anchor=(0.77, 0.85), loc="center left", borderaxespad=0)
plt.title('Probabilities of buying different drinks over the day')
plt.savefig('./Results/DrinksProb_initial.png')
plt.show()

dfpropfood.plot.area(figsize=(10,6))
plt.legend(bbox_to_anchor=(0.77, 0.85), loc="center left", borderaxespad=0)
plt.title('Probabilities of buying different food over the day')
plt.savefig('./Results/FoodProb_initial.png')
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


def total(data):  # function that merge turnover and tips in the same dataset
    data = pd.merge(data, df_tips, how='left', on='CUSTOMER')
    data['TIPS'] = data['TIPS'].fillna(0)
    return data


coffee_bar_prices = total(df_prices)

## *********************************************************************************************************************
## V: Export Data ******************************************************************************************************
## *********************************************************************************************************************
# Export the databases that will be used later

dfprob.to_csv(exportpath_probs, sep=";", index=False)
coffee_bar_prices.to_csv(exportpath_data, sep=";", index=False)
