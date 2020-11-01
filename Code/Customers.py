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

    #def drinks_bought(self):
    #def food_bought(self):
    #def purchase_history(self):
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
        self.customer = customer
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

    def describe_purchase(self):
        print("The purchase of %s at %s:%s o'clock was a %s with %s to eat and had an overall value of %s€."
              %(self.customer.ID, self.time[0], self.time[1], self.drink[0], self.food[0], self.value))



###### Simulations file #################################################################################################

# Prepare dtataframe that will associate a purchase object to a customer object at given times
transactions = dfprob[['HOUR', 'MINUTE']]
transactions['CUSTOMER'] = ""
transactions['PURCHASE'] = ""

# Create list of returning customers
ReturningCust = [Returner()]*667 # probability 2/3 for being normal returning customer (out of 1000 returning)
ReturningCust.extend([Hipster()]*333) # probability 1/3 for being hipster

# Create function that defines what type of customer enters the cafe for a given time
def ChooseCustomer(time):
    customer = random.choices([random.choice(ReturningCust), Customer(), Tripadvised()],
                              weights = [20, 72, 8], # 20% chance for random draw of returning,
                              k = 1)                 # 72% normal one time customer, 8% tripadvisor customer
    return customer[0]

# Assign type of customer per timeslot
for i in range(0, len(transactions)):
    transactions['CUSTOMER'][i] = ChooseCustomer(i)

# Find purchase object of the respective customer at a given time
for i in range(0, len(transactions)):
    transactions['PURCHASE'][i] = Purchase(transactions['CUSTOMER'].values[i],
                                           transactions['HOUR'].values[i],
                                           transactions['MINUTE'].values[i])

# Give examples of purchases
print(transactions['PURCHASE'][0].describe_purchase(),
      transactions['PURCHASE'][1].describe_purchase(),
      transactions['PURCHASE'][2].describe_purchase())








trans = []
for i in range(0, len(transactions)):
    trans.append(Purchase(transactions['CUSTOMER'].values[i],
                          transactions['HOUR'].values[i],
                          transactions['MINUTE'].values[i]))




tran = []
tran = Purchase(transactions['CUSTOMER'], transactions['HOUR'], transactions['MINUTE'])

for index,row in transactions.iterrows():
    .extend(Purchase(row['CUSTOMER'], row['HOUR'], row['MINUTE']))






# -> 0.2* randomly from ReturningCust
# -> 0.8* (0.1* Tripadvised() or 0.9*Customer())



test = [Customer()]*6
test.extend([Tripadvised()]*5)

