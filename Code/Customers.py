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
        self.type = "normal one time"
        self.money_spent = 0
        self.budget = 100
        self.purchases = []
        self.tip = 0

    def drinks_bought(self):
        beverages = []
        for i in range(len(self.purchases)):
            beverages.append(self.purchases[i].drink[0])
        print("The customer %s has bought %s." %(self.ID, beverages)) # to improve: print not list but elements alone

    def food_bought(self):
        snacks = []
        for i in range(len(self.purchases)):
            snacks.append(self.purchases[i].food[0])
        print("The customer %s has bought %s." % (self.ID, snacks))  # to improve: print not list but elements alone

    def purchase_history(self):
        history = []
        for i in range(len(self.purchases)):
            history.append([self.purchases[i].time, self.purchases[i].drink[0],
                            self.purchases[i].food[0], self.purchases[i].value])
        print("The customer %s has made the following purchases: %s" %(self.ID, history))

class Tripadvised(Customer):
    def __init__(self):
        super().__init__()
        self.type = "tripadvisor one time"
        self.tip = random.choice(range(100, 1001))/100

class Returner(Customer):
    def __init__(self):
        super().__init__()
        self.type = "normal returning"
        self.budget = 250

class Hipster(Customer):
    def __init__(self):
        super().__init__()
        self.type = "hipster returning"
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
        #self.payment = different from value as tips might be given

    def describe_purchase(self):
        print("The purchase of %s at %s:%s o'clock was a %s with %s to eat and had an overall value of %s€."
              %(self.customer.ID, self.time[0], self.time[1], self.drink[0], self.food[0], self.value))



###### Simulations file #################################################################################################

# Prepare dtataframe that will associate a purchase object to a customer object at given times
transactions = dfprob[['HOUR', 'MINUTE']]
transactions['CUSTOMER'] = ""
transactions['PURCHASE'] = ""
transactions['CUSTBUDG'] = ""
transactions['MONEYSPENT'] = ""

# Create list of returning customers
ReturningCust = [Returner() for i in range(667)] # probability 2/3 for being normal returning customer (out of 1000 returning)
ReturningCust.extend([Hipster() for i in range(333)]) # probability 1/3 for being hipster

# Create function that defines what type of customer enters the cafe for a given time
def ChooseCustomer(time):
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if ReturningCust[i].budget > 8] # is returner solvent?
    returner = random.choice(liquid)                                         # define type of returner (normal/hipster)
    customer = random.choices([returner, Customer(), Tripadvised()],
                              weights = [20, 72, 8], # 20% chance for returner, 72% normal one time customer,
                              k = 1)                 #  8% tripadvisor customer
    return customer[0]

# Assign type of customer per timeslot, find purchase object of the respective customer
for i in range(0, len(transactions)):
    # define customer of transaction and purchase object
    transactions['CUSTOMER'][i] = ChooseCustomer(i)
    transactions['PURCHASE'][i] = Purchase(transactions['CUSTOMER'].values[i],
                                           transactions['HOUR'].values[i],
                                           transactions['MINUTE'].values[i])
    # update attributes of customer that did the purchase
    transactions['CUSTOMER'][i].money_spent += transactions['PURCHASE'][i].value # change to payment once tips are done
    transactions['CUSTOMER'][i].budget -= transactions['PURCHASE'][i].value
    transactions['CUSTOMER'][i].purchases.append(transactions['PURCHASE'][i])

test = []
for i in range(0,len(ReturningCust)):
    test.append(ReturningCust[i].money_spent)

test2 = []
for i in range(0,len(ReturningCust)):
    test2.append(ReturningCust[i].budget)

test3 = []
for i in range(0,len(ReturningCust)):
    test3.append(ReturningCust[i].purchases)

# Give examples of purchases
print(transactions['PURCHASE'][0].describe_purchase(),
      transactions['PURCHASE'][1].describe_purchase(),
      transactions['PURCHASE'][2].describe_purchase())




