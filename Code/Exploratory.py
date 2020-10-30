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
dfaverages = pd.get_dummies(df, columns=["DRINKS", "FOOD"], prefix=["DRINK", "FOOD"])
df.groupby(['TIME', 'FOOD']).count()['YEAR'].unstack().plot()
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