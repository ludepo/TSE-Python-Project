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

    def make_payment(self, cost):
        self.budget -= cost


    #def drinks_bought(self):
    #def food_bought(self):
    #def purchase_history(self):
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
    transactions['CUSTOMER'][i] = ChooseCustomer(i)
    transactions['CUSTBUDG'][i] = transactions['CUSTOMER'][i].budget
    transactions['PURCHASE'][i] = Purchase(transactions['CUSTOMER'].values[i],
                                           transactions['HOUR'].values[i],
                                           transactions['MINUTE'].values[i])
    transactions['MONEYSPENT'][i] = transactions['PURCHASE'][i].value # TODO change to payment once tips are done
    transactions['CUSTOMER'][i].money_spent += transactions['PURCHASE'][i].value
    #transactions['CUSTOMER'][i].budget -= transactions['PURCHASE'][i].value
    transactions['CUSTOMER'][i].make_payment(transactions['PURCHASE'][i].value) # TODO problem: subtracts from all objects of same class

# F
for i in range(0, len(transactions)):
    transactions['PURCHASE'][i] = Purchase(transactions['CUSTOMER'].values[i],
                                           transactions['HOUR'].values[i],
                                           transactions['MINUTE'].values[i])

# Give examples of purchases
print(transactions['PURCHASE'][0].describe_purchase(),
      transactions['PURCHASE'][1].describe_purchase(),
      transactions['PURCHASE'][2].describe_purchase())

test = []

for i in range(0,len(ReturningCust)):
    test.append(ReturningCust[i].money_spent)


test2 = []

for i in range(0,len(ReturningCust)):
    test2.append(ReturningCust[i].budget)


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

