# EXAM PROJECT PYTHON

This project was realized as part of the Python class for the EEE Master.  

## 1. Project description

This project consists in modelling a coffee bar that sells drinks and food, for different
types of customers. Based on information obtained from given data, the aim is to simulate 
the purchases made in a coffee-shop by different type of customers that have different behaviors.

## 2. Prerequisites
To run this project, you will need to install Python. Before running any piece of code, please make sure that
the libraries indicated at the top of each file are installed. 

Comment: **"progressbar2"** has to be installed, not library "progressbar".

**Please note that decisions must be taken while running the code. As running the full simulation takes 
approximatly one hour (with 8BG RAM), you will have the choice to either conduct the entire simulation or to 
load data that is already stored and simulate a shorter simulation. You will be indicated when needing to take 
decisions.**

The following question will display: 
*Do you want to run full simulation (approx. 40min) or load pickle files of full simulation and run 
 representative (four month) simulation instead to see that code works? If run full simulation, 
 input 'run', if load pickle file input 'load'.*

## 3. Structure
The project is structured in 4 folders: one for the documentation, one for the data, one with our code and one 
with the results.

### 3.1. Documentation
The Documentation folder contains a PowerPoint file, "ExamProjectTSE_2020-21.pptx", 
describing in detail the assignment. 

### 3.2. Data
The Data folder contains a given dataset, "Coffeebar_2016-2020.csv", containing a five years span of customers purchases. 
That dataset will be used in the first part of the project in order to explore the behavior of the customers in terms of 
consumption habits. 

In this folder, we also make available 5 years span simulations obtained with our code. 
As the 5 years simulation takes about 60 minutes to run, this allows to do the later analysis 
without having to run the whole simulation. Those are actual simulations obtained from our code.
The general 5 year simulation is called "TransactionsDF.dat" (or Simulation.csv). The other pickle/ .csv files correspond
to the variation in input parameters. 

### 3.3. Code
The Code folder contains the four python files used to solve the project. Each file corresponds to a different part of 
the assignment. 

#### *Exploratory*
The "Exploratory.py" file responds to the first part of the assignment. With this code, we  explore the 
"Coffeebar_2016-2020.csv" dataset in order to determine what the shop is selling and to obtain probabilities of
customers buying each items at each time of the day. This code allows to obtain and export a csv dataset, "dfprobs.csv" 
with cross probabilities between time of the day and order of different items.
The "Coffeebar_2016-2020.csv" dataset is also transformed in order to add prices and tips. This will be used for later 
comparisons. 

#### *Customers*
##### *Objects*
In a first part, this file defines the different classes of objects that are needed in the simulation. 
It first creates the different types of customers with given attributes and instance methods that will be used in
the simulation. It also creates the Purchase object that assigns a purchase to customers depending on the time they show
up. Finally, it creates the class Items for food and drinks.

##### *Functions*
In a second part, we specify the functions needed for the simulation. 

The ChooseCustomer() function will conduct the customer lottery given as input the list of returning customers
and outputs a chosen customer.

The MakePurchase() function takes as inputs the chosen customer object, the time slot (hour, minute), the choice probabilities,
as well as the list of item objects sold at the Cafe. It outputs a purchase object with attributes like 'food', 'drink', 
'value', 'tip', etc..

The SimulateRange() function will allow to obtain the final simulation by combining the chosen customer with its given 
purchase depending on the time of the day. It takes as input the choice probabilities, the list of returning customer 
objects, the list of item objects and optionally a start and end date (default five years).

Finally, the NoObjects() function takes as input the created dataframe with the customer object and the purchase object
assigned to each time slot and outputs the same dataframe with additional columns descriibing some attributes of the
respective objetcs.

#### *Simulation*
Finally, the "Simulation.py" allows to obtain a 5 years span of customer based on the class and functions created 
previously. **At this point, you will be asked to either run the simulation or instead used the pre-stored
simulation**

.The simulation obtained is compared with the given dataset by the mean of different graphs.

#### *Discussion*
Finally, this section correspond to part 4 of the assignment. We look at the datasets into more detail and make new
assumptions concerning the customers to see how it affects the simulation.
It analyses the 4 following assumptions: 
*What would happen if we lower the returning customers to 50 and simulate the same period?*
*The prices change from the beginning of 2018 and go up by 20%*
*What would happen if the budget of hipsters drops to 40?*
*Changing the assumption of 20% chance to have a returner even when most returners are bankrupt and instead assume
that bankrupt returners are replaced by tripavised customers*

**Each of these hypothesis requires a new simulation. You will again have to choose between running the simulation or
using a pre-stored simulation**

### Results
The Results folder contains the datasets created for the project and the different graphs.


## Authors
**Camille CALANDRE**, calandre.camille@hotmail.fr, git account: CamilleCalandre

**Luca POLL**, lupoll208@gmail.com, git account: Lupoll
