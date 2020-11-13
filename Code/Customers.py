import uuid
import random
import pandas as pd
from progressbar import progressbar
from itertools import product


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
            history.append([self.purchases[i].drink.name, self.purchases[i].food.name])
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
    def __init__(self, customer, hour, minute, probabilities, items): # probabilities is df obtained in Exploratory.py
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
        self.payment = self.value + customer.tip # payment might differ from value as tip is possible
        self.tip = customer.tip

    def describe_purchase(self):
        print("The purchase of %s of type '%s' at %s:%s o'clock was a %s with %s "
              "to eat and had an overall value of %s€ with %s€ tips."
              % (self.customer.ID, self.customer.type, self.time[0], self.time[1],
                 self.drink.name, self.food.name, self.value, self.tip))





## *********************************************************************************************************************
##     Part II: Functions        ***************************************************************************************
## *********************************************************************************************************************

# create function that defines what type of customer enters the cafe for a given time (robust version)
def ChooseCustomer(ReturningCust):
    liquid = [ReturningCust[i] for i in range(len(ReturningCust)) if ReturningCust[i].budget > 8]  # is returner solvent?
    if len(liquid) == 0:
        returner = random.choice(liquid)  # define type of returner (normal/hipster)
        customer = random.choices([returner, Customer(), Tripadvised()],
                                  weights=[20, 72, 8],  # 20% chance for returner, 72% normal one time customer,
                                  k=1)  # 8% tripadvisor customer
    else:
        customer = random.choices([Customer(), Tripadvised()], weights=[90,10], k=1) # if all returners bankrupt

    return customer[0]


# create function that will assign a purchase object for a given customer at a given hour and minute
def MakePurchase(customer, hour, minute, probabilities, items): # probabilities refers to dfobtained in Exploratory.py
    purchase = Purchase(customer, hour, minute, probabilities, items) # create purchase object
    customer.money_spent += purchase.payment # update money_spent attribute of chosen customer
    customer.budget -= purchase.payment # update budget of chosen customer
    customer.purchases.append(purchase) # update purchase history of chosen customer
    return purchase


# create function to simulate five years (or different if specified in input)
def SimulateRange(probabilities, ReturningCust, items, start = "2016-01-01", end = "2020-12-31"):
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
        transactions['CUSTOMER'][i] = ChooseCustomer(ReturningCust) # assign customer object for given time
        transactions['PURCHASE'][i] = MakePurchase(transactions['CUSTOMER'].values[i], # assign purchase object
                                                   transactions['HOUR'].values[i],
                                                   transactions['MINUTE'].values[i],
                                                   probabilities,
                                                   items)
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
    dataframe['TIME'] = dataframe['DATETIME'].dt.strftime("%H:%M:%S")
    dataframe['DATE'] = dataframe['DATETIME'].dt.strftime("%Y-%m-%d")
    dataframe = dataframe.drop(['HOUR', 'MINUTE'], axis = 1)
    return dataframe

