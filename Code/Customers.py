import uuid
import random
import pandas as pd
import numpy as np
import os

importpath = os.path.abspath("./Results/dfprobs.csv")
dfprob = pd.read_csv(importpath, sep=";")

dfprob.index = dfprob['ID']
dfprob['HOUR'] = dfprob.ID.str.slice(stop=2)
dfprob['MINUTE'] = dfprob.ID.str.slice(start=3, stop=5)

# create superclass for type of customer ("default customer" 0 normal one time customer)
class Customer(object):
    def __init__(self):
        self.ID = "CID" + str(uuid.uuid1()) # unique ID
        self.type = "normal one time"
        self.money_spent = 0
        self.budget = 100
        self.purchases = [] # note that appended purchases will be objects of class "Purchase()"
        self.tip = 0

    # method for telling what drinks have been bought in the past
    def drinks_bought(self):
        beverages = []
        for i in range(len(self.purchases)):
            beverages.append(self.purchases[i].drink.name)
        print("The customer %s has bought %s." % (self.ID, beverages))  # to improve: print not list but elements alone

    # method for telling what food has been bought in the past
    def food_bought(self):
        snacks = []
        for i in range(len(self.purchases)):
            snacks.append(self.purchases[i].food.name)
        print("The customer %s has bought %s." % (self.ID, snacks))  # to improve: print not list but elements alone

    # method for telling complete history of purchases
    def purchase_history(self):
        history = []
        for i in range(len(self.purchases)):
            history.append([self.purchases[i].time, self.purchases[i].drink.name,
                            self.purchases[i].food.name, self.purchases[i].value])
        print("The customer %s has made the following purchases: %s" % (self.ID, history))

# create subclass for customers from Tripadvisor (differs in propensity to give tips)
class Tripadvised(Customer):
    def __init__(self):
        super().__init__()
        self.type = "tripadvisor one time"
        self.tip = random.choice(range(100, 1001))/100

# create subclass for normal returning customer (differs in available budget)
class Returner(Customer):
    def __init__(self):
        super().__init__()
        self.type = "normal returning"
        self.budget = 250

# create subclass for normal returning Hipster customer(differs in available budget)
class Hipster(Customer):
    def __init__(self):
        super().__init__()
        self.type = "hipster returning"
        self.budget = 500

# create class do define items that are sold in cafe as objects
class item(object):
    def __init__(self, name, price, type):
        self.price = price
        self.name = name
        self.type = type

# create class for purchases that allows to create objects for the individual purchases
class Purchase(object):
    def __init__(self, customer, hour, minute):
        self.customer = customer # note that customer will be an object
        self.time = [hour, minute]

        # get the probabilities for the respective items at the given hour and minute
        prob = dfprob.drop('ID', axis=1)
        prob = prob[(prob['HOUR'] == hour) & (prob['MINUTE'] == minute)].drop(['HOUR', 'MINUTE'],axis=1)

        # match the items with the given probability for the hour and the minute
        assignedprob = []
        for i in items:
            for col in prob.columns:
                if i.name in col:
                    assignedprob.append([i, prob[col].values[0]])

        # distinguish between food and drinks and their respective probabilities, assign to respective list
        drinks = []; drinksprob = []; food = []; foodprob = []
        for i in assignedprob:
            if i[0].type == "food":
                food.append(i[0])
                foodprob.append(i[1])
            elif i[0].type == "drink":
                drinks.append(i[0])
                drinksprob.append(i[1])
            else:
                print("ERROR")

        # run lottery for what food and what drink is chosen given the items and their probabilities
        food = random.choices(food, weights = foodprob, k=1)
        drink = random.choices(drinks, weights = drinksprob, k=1)

        self.drink = drink[0] # note that drink will be an object
        self.food = food[0] # note that food will also be an object
        self.value = food[0].price + drink[0].price
        self.payment = self.value + self.customer.tip # not that payment might differ from value since tip is possible
        self.tip = self.payment - self.value

    def describe_purchase(self):
        print("The purchase of %s at %s:%s o'clock was a %s with %s to eat and had an overall value of %s€ with %s€ tips."
              % (self.customer.ID, self.time[0], self.time[1], self.drink.name, self.food.name, self.value, self.tip))


###### Simulations file ###############################################################################################

# create items that are sold in cafe: item(name, price, type)
items = [item("coffee", 3, "drink"),
         item("frappucino", 4, "drink"),
         item("milkshake", 5, "drink"),
         item ("soda", 3, "drink"),
         item("tea", 4, "drink"),
         item("water", 2, "drink"),
         item("cookie", 2, "food"),
         item("muffin", 3, "food"),
         item("pie", 3, "food"),
         item("sandwich", 2, "food"),
         item("nothing", 0, "food")]

for i in items:
    print("Item: %s, price: %s" %(i.name, i.price))

# Dataframe that will associate a purchase object to a customer object at given times
transactions = dfprob[['HOUR', 'MINUTE']]
transactions['CUSTOMER'] = ""
transactions['PURCHASE'] = ""
transactions['CUSTBUDG'] = ""
transactions['MONEYSPENT'] = ""

# Create list of returning customers
ReturningCust = [Returner() for i in
                 range(667)]  # probability 2/3 for being normal returning customer (out of 1000 returning)
ReturningCust.extend([Hipster() for i in range(333)])  # probability 1/3 for being hipster


# Create function that defines what type of customer enters the cafe for a given time
def ChooseCustomer(time):
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if
              ReturningCust[i].budget > 8]  # is returner solvent?
    returner = random.choice(liquid)  # define type of returner (normal/hipster)
    customer = random.choices([returner, Customer(), Tripadvised()],
                              weights=[20, 72, 8],  # 20% chance for returner, 72% normal one time customer,
                              k=1)  # 8% tripadvisor customer
    return customer[0]


# Assign type of customer per timeslot, find purchase object of the respective customer
for i in range(0, len(transactions)):
    # define customer of transaction and purchase object
    transactions['CUSTOMER'][i] = ChooseCustomer(i)
    transactions['PURCHASE'][i] = Purchase(transactions['CUSTOMER'].values[i],
                                           transactions['HOUR'].values[i],
                                           transactions['MINUTE'].values[i])
    # update attributes of customer that did the purchase
    transactions['CUSTOMER'][i].money_spent += transactions['PURCHASE'][i].payment  # change to payment once tips are done
    transactions['CUSTOMER'][i].budget -= transactions['PURCHASE'][i].payment
    transactions['CUSTOMER'][i].purchases.append(transactions['PURCHASE'][i])

test = []
for i in range(0, len(ReturningCust)):
    test.append(ReturningCust[i].money_spent)

test2 = []
for i in range(0, len(ReturningCust)):
    test2.append(ReturningCust[i].budget)

test3 = []
for i in range(0, len(ReturningCust)):
    test3.append(ReturningCust[i].purchases)

# Give examples of purchases
print(transactions['PURCHASE'][0].describe_purchase(),
      transactions['PURCHASE'][1].describe_purchase(),
      transactions['PURCHASE'][2].describe_purchase())
