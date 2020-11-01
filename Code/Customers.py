import uuid
import random
import pandas as pd
import numpy as np
import os

importpath = os.path.abspath("./Results/dfprobs.csv")
dfprob = pd.read_csv(importpath, sep=";")

dfprob.index = dfprob['ID']
dfprob['HOUR'] = dfprob.ID.str.slice(stop=2)
dfprob['MINUTE'] = dfprob.ID.str.slice(start = 3, stop=5)

prices = {'PRODUCT': ['coffee', 'frappucino', 'milkshake', 'soda', 'tea', 'water',
                      'cookie', 'muffin', 'pie', 'sandwich', 'nothing'],
          'PRICE': [3, 4, 5, 3, 3, 2, 2, 3, 3, 2, 0]}
prices = pd.DataFrame(prices)



class Customer(object):
    def __init__(self):
        self.ID = "CID" + str(uuid.uuid1())
        self.budget = 100
        self.purchases = []
        self.money_spent = 0
        self.tip = 0

class Tripadvised(Customer):
    def __init__(self):
        super().__init__()
        self.tip = random.choice(range(100, 1001))/100

class Returner(Customer):
    def __init__(self):
        super().__init__()
        self.budget = 250

class Hipster(Customer):
    def __init__(self):
        super().__init__()
        self.budget = 500

class Purchase(object):
    def __init__(self, customer, hour, minute):
        self.customer = customer.ID
        self.time = [hour, minute]

        food = ['cookie', 'muffin', 'pie', 'sandwich', 'nothing']
        foodprob = dfprob[['FOOD_cookie', 'FOOD_muffin', 'FOOD_pie', 'FOOD_sandwich', 'FOOD_nothing', 'HOUR', 'MINUTE']]
        foodprob = foodprob[(foodprob['HOUR'] == hour) & (foodprob['MINUTE'] == minute)].drop(['HOUR', 'MINUTE'], axis=1)
        food = random.choices(food, weights=(foodprob.stack().tolist()), k=1)

        drink = ['coffee', 'frappucino', 'milkshake', 'soda', 'tea', 'water']
        drinkprob = dfprob[['DRINK_coffee', 'DRINK_frappucino', 'DRINK_milkshake', 'DRINK_soda',
                            'DRINK_tea', 'DRINK_water', 'HOUR', 'MINUTE']]
        drinkprob = drinkprob[(drinkprob['HOUR'] == hour) & (drinkprob['MINUTE'] == minute)].drop(['HOUR', 'MINUTE'], axis=1)
        drink = random.choices(drink, weights=(drinkprob.stack().tolist()), k=1)

        self.drink = drink
        self.food = food
        self.value = prices[prices['PRODUCT'] == food[0]]['PRICE'].values[0] + \
                     prices[prices['PRODUCT'] == drink[0]]['PRICE'].values[0]

    def describe(self):
        print("The purchase of %s at %s o'clock was a %s with %s to eat with an overall value of %s."
              %(self.customer, self.time, self.drink, self.food, self.value))



###### Simulations file #################################################################################################

times = dfprob[['HOUR','MINUTE']]
times['CUSTOMER'] = ""

ReturningCust = [Returner()]*667 # probability 2/3 for being normal returning customer (out of 1000 returning)
ReturningCust.extend([Hipster()]*333) # probability 1/3 for being hipster

def ChooseCustomer(time):
    # this function decides what customer enters the cafe at the respective time
    customer = random.choices([random.choice(ReturningCust), Customer(), Tripadvised()],
                              weights = [20, 72, 8], # 20% chance for random draw of returning,
                              k = 1)                 # 72% normal one time customer, 8% tripadvisor customer
    return customer

for i in range(0,len(times)):
    times['CUSTOMER'][i] = ChooseCustomer(i)

# TODO: Ask romain for best structure for list that combines time and customer which can be developed to purchase
# (Current problem that the objects attributes that are stored in cell can not be called (like line 46))

# make purchase
purchase = [Purchase(row['CUSTOMER'], row['HOUR'], row['MINUTE'])]
for index,row in times.iterrows():
    purchase.extend(Purchase(row['CUSTOMER'], row['HOUR'], row['MINUTE']))






# -> 0.2* randomly from ReturningCust
# -> 0.8* (0.1* Tripadvised() or 0.9*Customer())



test = [Customer()]*6
test.extend([Tripadvised()]*5)

