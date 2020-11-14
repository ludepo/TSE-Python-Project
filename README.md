# EXAM PROJECT PYTHON

This project was realized as part of the Python class for EEE Master.  

## 1. Project description

This project consists in modelling a coffee bar that sells drinks and food, for different
types of customers. Based on information obtained from a given dataframe, the aim is to simulate 
the purchases made in a coffee-shop by different type of customers that have different behaviors.

## 2. Prerequisites
To run this project, you will need to install Python. Before running any piece of code, please make sure that 
you imported the packaged specified at the top of each file. 

**Please note that decisions must be taken while running the code. As running the full simulation uses 
approximatly 8BG of ram, which can be long, you will have the choice to either simulate the whole dataframe or to 
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
As the 5 years simulation takes about 40 minutes to run, this allows to do the later analysis 
without having to run the whole simulation. Those are actual simulations obtained from our code.
The general 5 year simulation is called "TransactionsDF.dat". The other databases correspond to 
different hypothesis that are made. 

### 3.3. Code
The Code folder contains the four python files used to solve the project. Each file correspond to a different part of 
the assignment. 

#### *Exploratory*
"Exploratory.py" file responds to the first part of the assignment. With this code, we  explore the 
"Coffeebar_2016-2020.csv" dataset in order to determine what the shop is selling and to obtain probabilities of
customers buying each items at each time of the day. This code allows to obtain a csv dataset, "dfprobs.csv"  
with cross probabilities between time of the day and order of different items.
The given dataset is also transformed in order to add prices and tips. This will be used for later comparisons. 

#### *Customers*
##### *Objects*
In a first part, this file creates the different classes of objects that are needed in the simulation. 
It first creates the different types of customers with given attributes and instance methods that will be used in
the simulation. It also creates the Purchase object that assign a purchase to customers depending on the time they show
up. Finally it creates the  class Items for food and drinks objects 

##### *Functions*
In a second part, we specify the functions needed for the simulation. 
The ChooseCustomer() function will allow to choose between the different type of customers, taking into account their 
solvability. 
The MakePurchase() function assign a purchase to the chosen customer, depending on the time of the day and on the 
probabilities obtained in the first part.
The SimulateRange() function will allow to obtain the final simulation by combining the chosen customer with its given 
purchase depending on the time of the day. It is created to simulate a 5 years span but a different time range can be 
specified in the input. 
Finally, the NoObjects() function allows to convert the object stored in the dataframe to human readable data.

#### *Simulation*
Finally, the "Simulation.py" allows to obtain a 5 years span of customer based on the class and functions created 
previously. **At this point, you will be asked to either run the simulation or instead used the pre-stored
simulation**
The simulation obtained is compared with the given dataset by the mean of different graphs.

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
using a pre-loaded simulation**

### Results
The Results folder contains the datasets created for the project and the different graphs.


## Authors
**Luca POLL**, lupoll208@gmail.com, git account: Lupoll

**Camille CALANDRE**, calandre.camille@hotmail.fr, git account: CamilleCalandre
