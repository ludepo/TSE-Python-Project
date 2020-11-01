# EXAM PROJECT PYTHON

This project was realized as part of the Python class for EEE Master.  

## Project description

This project consists in modelling a coffee bar that sells drinks and food, for different
types of customers.

### Prerequisites

To run this project, you will need to instal Python

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
and the purchase object.

Finally, the "simulation.py" Code regroups functions that allows to create a five year span of 
customers' purchases.

Please run the Codes in the following order: Exploratory, Customer and Simulation. 

The Results folder contains the datasets created for the project.


## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
