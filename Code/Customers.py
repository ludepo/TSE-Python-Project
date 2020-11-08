import uuid
import random
import pandas as pd
from progressbar import progressbar
from itertools import product, repeat
import os


## *********************************************************************************************************************
##     Part I: Objects           ***************************************************************************************
## *********************************************************************************************************************

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
        print("The customer %s had a %s." % (self.ID, beverages))  # to improve: print not list but elements alone

    # method for telling what food has been bought in the past
    def food_bought(self):
        snacks = []
        for i in range(len(self.purchases)):
            snacks.append(self.purchases[i].food.name)
        print("The customer %s had a %s." % (self.ID, snacks))  # to improve: print not list but elements alone

    # method for telling complete history of purchases
    def purchase_history(self):
        history = []
        for i in range(len(self.purchases)):
            history.append(["At", self.purchases[i].time, "o'clock a", self.purchases[i].drink.name, "and",
                            self.purchases[i].food.name, "for", self.purchases[i].value, "€"])
        print("The customer %s has made the following purchases: %s" % (self.ID, " ".join(i)) for i in history))


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
    def __init__(self, customer, hour, minute, probabilities): # probabilities is dataframe obtained in Exploratory.py
        self.customer = customer # note that customer will be an object
        self.time = [hour, minute]

        # get the probabilities for the respective items at the given hour and minute
        prob = probabilities.drop('ID', axis=1)
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
        self.payment = food[0].price + drink[0].price + customer.tip # payment might differ from value as tip is possible
        self.tip = customer.tip

    def describe_purchase(self):
        print("The purchase of %s of type %s at %s:%s o'clock was a %s with %s "
              "to eat and had an overall value of %s€ with %s€ tips."
              % (self.customer.ID, self.customer.type, self.time[0], self.time[1],
                 self.drink.name, self.food.name, self.value, self.tip))





## *********************************************************************************************************************
##     Part II: Functions        ***************************************************************************************
## *********************************************************************************************************************

# create function that defines what type of customer enters the cafe for a given time (robust version)
def ChooseCustomer():
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if ReturningCust[i].budget > 8]  # is returner solvent?
    if liquid != []:
        returner = random.choice(liquid)  # define type of returner (normal/hipster)
        customer = random.choices([returner, Customer(), Tripadvised()],
                                    weights=[20, 72, 8],  # 20% chance for returner, 72% normal one time customer,
                                    k=1)  # 8% tripadvisor customer
    else:
        customer = random.choices([Customer(), Tripadvised()], weights=[90,10], k=1) # if all returners bankrupt

    return customer[0]


# create function that will assign a purchase object for a given customer at a given hour and minute
def MakePurchase(customer, hour, minute, probabilities): # probabilities refers to dataframe obtained in Exploratory.py
    purchase = Purchase(customer, hour, minute, probabilities) # create purchase object given customer, hour and minute
    customer.money_spent += purchase.payment # update money_spent attribute of chosen customer
    customer.budget -= purchase.payment # update budget of chosen customer
    customer.purchases.append(purchase) # update purchase history of chosen customer
    return purchase


# create function to simulate five years (or different if specified in input)
def SimulateRange(probabilities, start = "2016-01-01", end = "2020-12-31"):
    ## !!! Important !!! function needs around 40 minutes if simulation for five years.
    #                     Progress bar will give progress and estimate of overall time
    daterange = pd.date_range(start=start,end=end).strftime("%Y-%m-%d").to_list() # define range of date
    time = probabilities['ID']
    transactions = pd.DataFrame({'DATETIME' : [pd.to_datetime(" ".join(i)) for i in product(daterange, time)]})
    transactions['HOUR'] = transactions['DATETIME'].dt.strftime("%H") # get hour from datetime column
    transactions['MINUTE'] = transactions['DATETIME'].dt.strftime("%M") # get minute from datetime column
    transactions['CUSTOMER'] = None
    transactions['PURCHASE'] = None
    for i in progressbar(range(0, len(transactions))): # *** see comment below
        transactions['CUSTOMER'][i] = ChooseCustomer() # assign customer object for given time
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i], # assign purchase object
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities)
    return transactions
# *** the structure of looping through every row to change value in columns is slow but here necessary since the
#     chosen customer attributes need to be updated before the selection of the customer in the next slot


# reformat dataframe to match it with initial data (show attribute instead of object)
def NoObjects(dataframe): # function serves to show dataframe without objects but human-readable data
    dataframe['CUSTOMER_ID'] = dataframe['CUSTOMER'].apply(lambda x: x.ID)
    dataframe['CUSTOMER_TYPE'] = dataframe['CUSTOMER'].apply(lambda x: x.type)
    dataframe['DRINKS'] = dataframe['PURCHASE'].apply(lambda x: x.drink.name)
    dataframe['FOOD'] = dataframe['PURCHASE'].apply(lambda x: x.food.name)
    dataframe['TURNOVER'] = dataframe['PURCHASE'].apply(lambda x: x.value)
    dataframe['TIPS'] = dataframe['PURCHASE'].apply(lambda x: x.tip)
    dataframe['TIME'] = dataframe['DATETIME'].dt.time
    dataframe['DATE'] = dataframe['DATETIME'].dt.date
    dataframe = dataframe.drop(['HOUR', 'MINUTE'], axis = 1)
    return dataframe








##### SIMULATION FILE ##################################################################################################

## *********************************************************************************************************************
## Part I: Define Inputs                         ***********************************************************************
## *********************************************************************************************************************

# Import and export path
importpath = os.path.abspath("./Results/dfprobs.csv")
exportpath = os.path.abspath("./Results/transactionsAll.csv")


# create items that are sold in cafe: item(name, price, type)
items = [item("coffee", 3, "drink"),
         item("frappucino", 4, "drink"),
         item("milkshake", 5, "drink"),
         item("soda", 3, "drink"),
         item("tea", 3, "drink"),
         item("water", 2, "drink"),
         item("cookie", 2, "food"),
         item("muffin", 3, "food"),
         item("pie", 3, "food"),
         item("sandwich", 2, "food"),
         item("nothing", 0, "food")]

# print the items with their prices
for i in items:
    print("Delicious %s, just %s€" %(i.name, i.price))


# load dataframe with probabilities obtained from Exploratory.py
dfprob = pd.read_csv(importpath, sep=";")
dfprob.index = dfprob['ID']
dfprob['HOUR'] = dfprob.ID.str.slice(stop=2)
dfprob['MINUTE'] = dfprob.ID.str.slice(start=3, stop=5)


# create list of returning customers
ReturningCust = [Returner() for i in range(667)]  # prob = 2/3 for being normal returning customer(out of 1000 returning)
ReturningCust.extend([Hipster() for i in range(333)])  # prob = 1/3 for being hipster




## *********************************************************************************************************************
## Part II: Simulation                           ***********************************************************************
## *********************************************************************************************************************
import pickle

# simulate two month to see that program works fine
transactionsTwoMonths = SimulateRange(dfprob,start = "2020-11-01")

# # simulate specified range (by default set to five years)
transactionsAll = SimulateRange(dfprob) # note that command will run approx. 60 min (8GB Ram)

# the data can be transformed to show objects and attributes:
#transactions = NoObjects(transactionsAll)

# save simulated data as pickle in order to access objects later again
# PIK = "Data/transactionsDF.dat"
# with open(PIK, "wb") as f:
#     pickle.dump(transactions, f)

# alternatively, simulated data can be loaded from pickle:
transactions = pickle.load(open(PIK, "rb"))




## *********************************************************************************************************************
## Part III: Visualize and discuss simulation    ***********************************************************************
## *********************************************************************************************************************
import matplotlib.pyplot as plt
import numpy as np

# Give examples of purchases
transactions['PURCHASE'][0].describe_purchase()
transactions['PURCHASE'][100].describe_purchase()
transactions['PURCHASE'][1500].describe_purchase()

# How much money was spent by returning customers?
moneyspent = [ReturningCust[i].money_spent for i in range(len(ReturningCust))]
print("The average amount spent by a returning customer was %s" %(sum(moneyspent)/len(moneyspent)))

# How much budget do returning customers have left?
budgets = [ReturningCust[i].budget for i in range(len(ReturningCust))]
print("The average budget left for a normal returning customer was %s€ and for a hipster %s€" %(round(sum(budgets[:666])/len(budgets[:666])), round(sum(budgets[667:])/len(budgets[667:]))))




# -- average income during day
trans_mean_day = transactions.groupby(by='TIME').mean()
trans_std_day = transactions.groupby(by='TIME').std()

plt.figure()
plt.plot(trans_mean_day.index, trans_mean_day)
plt.fill_between(trans_std_day.index, trans_mean_day - 2 * trans_std_day,trans_mean_day + 2 * trans_std_day, alpha=0.2)

# -- average income by types per day


trans_mean_type = transactions.groupby(by=['TIME', 'CUSTOMER_TYPE']).mean()
trans_std_type = transactions.groupby(by=['TIME', 'CUSTOMER_TYPE']).std()

plt.figure()
plt.plot(trans_mean_type.index, trans_mean_type)
plt.fill_between(trans_std_type.index, trans_mean_type - 2 * trans_std_type, trans_mean_type + 2 * trans_std_type,
                     alpha=0.2)
# -- average income by type over years


# show some buying histories of returning customers for your simulations
ReturningCust[555].purchase_history()
ReturningCust[999].purchase_history()


# What would happen if we lower the returning customers to 50 and simulate the same period?
## the code would crash if we do not make the additional assumption that once all returning customers are bankrupt,
## only 90% normal one-time customers or 10% tripadvised customerss would enter the cafe (see ChooseCustomers())


# The budget of hipsters drops to 40
## the same as if we would only have 50 returning customers, since the budget of the hipsters would be zero rather
## quickly. Therefore, the normal returning customers would compensate and also be bankrupt soon. Once all returning
## customers are bankrupt the code would crash without the additional assumption.


# The prices change from the beginning of 2018 and go up by 20%
# create function that will assign a purchase object for a given customer at a given hour and minute
def MakePurchase(customer, hour, minute, probabilities, date):  # probabilities refers to dataframe obtained in Exploratory.py
    purchase = Purchase(customer, hour, minute, probabilities)  # create purchase object given customer, hour and minute
    if (date > "2017-12-31"):
        purchase.drink.price = purchase.drink.price * 1.2
        purchase.food.price = purchase.food.price * 1.2
    else:
        None
    customer.money_spent += purchase.payment  # update money_spent attribute of chosen customer
    customer.budget -= purchase.payment  # update budget of chosen customer
    customer.purchases.append(purchase)  # update purchase history of chosen customer

    return purchase


def SimulateRange(probabilities, start = "2016-01-01", end = "2020-12-31"):
    daterange = pd.date_range(start=start,end=end).strftime("%Y-%m-%d").to_list() # define range of date
    time = probabilities['ID']
    transactions = pd.DataFrame({'DATETIME' : [pd.to_datetime(" ".join(i)) for i in product(daterange, time)]})
    transactions['HOUR'] = transactions['DATETIME'].dt.strftime("%H") # get hour from datetime column
    transactions['MINUTE'] = transactions['DATETIME'].dt.strftime("%M") # get minute from datetime column
    transactions['CUSTOMER'] = None
    transactions['PURCHASE'] = None
    for i in progressbar(range(0, len(transactions))): # *** see comment below
        transactions['CUSTOMER'][i] = ChooseCustomer() # assign customer object for given time
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i], # assign purchase object
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities,
                                                   transactions['DATETIME'].values[i])
    return transactions

#Other approach: change the value of the purchase in the Purchase() function. But for that we need to have the year as
##parameter of the function and not only the time.



# ChooseCust() that does not crash if all returning are bankrupt
def ChooseCustomer():
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if ReturningCust[i].budget > 8]  # is returner solvent?
    if liquid != []:
        returner = random.choice(liquid)  # define type of returner (normal/hipster)
        customer = random.choices([returner, Customer(), Tripadvised()],
                                    weights=[20, 72, 8],  # 20% chance for returner, 72% normal one time customer,
                                    k=1)  # 8% tripadvisor customer
    else:
        customer = random.choices([Customer(), Tripadvised()], weights=[90,10], k=1) # if all returners bankrupt

    return customer[0]

# ChooseCust() with assumption that returners will not go more often if another returner is bankrupt but instead go
#     like before
def ChooseCustomer():
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if ReturningCust[i].budget > 8]  # is returner solvent?
    allcust = [Customer(), Tripadvised()] # create list for possible customers (note we do not care what Customer() or
    allcust.extend(liquid)                # Tripadvised() comes, but for Returner() and Hipster() we want to keep track
    weights = [72, (100-72-len(liquid)*(20/len(ReturningCust)))] # bankrupt returning customers are replaced by Tripadvised
    weights.extend(list(repeat((20/len(ReturningCust)), len(liquid)))) # prob. of repeating returner dependen on overall nr.
    if liquid != []:
        customer = random.choices(allcust, weights=weights, k=1)  # 8% tripadvisor customer
    else:
        customer = random.choices([Customer(), Tripadvised()], weights=[72, 28], k=1)  # if all returners bankrupt
    return customer[0]

