# EXAM PROJECT PYTHON

This project was realized as part of the Python class for EEE Master.  

## Project description

This project consists in modelling a coffee bar that sells drinks and food, for different
types of customers.

### Prerequisites

To run this project, you will need to install Python. Before running any piece of code, please make sure that 
you imported the packaged specified at the top of each file. 

### Files decription
The project is structured in 4 folders: one for the documentation, one for the data, 
one with our code and one with the results.

The Documentation folder contains a PowerPoint file, "ExamProjectTSE_2020-21.pptx", 
describing in detail the assignment. 

The Data folder contains a simulated dataset, "Coffeebar_2016-2020.csv" of customers 
that we use in the first part of the project.

The Code folder contains the three python files used to solve the project. This 
"Exploratory.py" file responds to the first part of the assignment. With this code, we 
explore the "Coffeebar_2016-2020.csv" dataset in order to determine what the shop is 
selling and to obtain probabilities for orders at each given time of the day. This code 
allows to obtain a csv dataset, "dfprobs.csv"  with cross probabilities between time of the day and order of
different items. 

The second Code file, "Customer.py", creates the different classes of objects that are needed in the simulation. 
It creates the different types of customers with given attributes, the food and drinks objects 
and the purchase object. It also defines the functions that will generate a list of customer and assign a specific
 purchase to each customer, based on the probabilities obtained previously. 

Finally, the "Simulation.py" allows to obtain a 5 years span of customer based on the class and functions created previously. 

Please run the Codes in the following order: Exploratory.py, Customer.py and Simulation.py. 

The Results folder contains the datasets created for the project.


## Authors
**Luca POLL**, lupoll208@gmail.com, git account: Lupoll

**Camille CALANDRE**, calandre.camille@hotmail.fr, git account: CamilleCalandre
