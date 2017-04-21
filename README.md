# General Project Description

* Note: to learn about the purpose of each class please read the assignment readme before.

We divide the project into several differet sections:

 1. DB section - creation and data insertion
 2. Accessor APIs - caching (notice if needed disk cache has to be manually deleted)
 3. Classifier implementation 
 4. Experiments 
 
## DB section
The data that we use can be found at YahStocks folder.
The project is based on mongodb server. 
The non-relational DB is very convenient for the 
creation of the DB.

All the data in the first phase (inserting the stock data) is either a 
Dictionary or a list of double and dates. 

In the second phase (creating the market data) we are also taking advantage of LearningData 
(which is explained later on)
as its API is using caches.

## Accessor APIs
All of the classes are in orginizers file under the Utilities package.

The cache class is called DataAccessor and is used mostly internally.
The class implements the python Mapping interface by using the pickle
library. 

The LearningData class uses the DataAccessor as cache and the main
data structure used is the pandas.DataFrame. All functions take
advantage of the fast pandas API.

The TrainingData class uses the LearningData API to provide a fluent
API for deciding how to classify, which features to put, on what
dates to work and so on.

## Classifier implementation 
To get the correlation strength between a given stock and a market we implemented 
StrengthCalc class which uses sklearn's KMeans for a better clustering and numpy in his matrix manipulation. This class also uses DataAccessor in order to cache his results and save some running time and LearningData to access the stocks data.

ConnectionStrengthClassifier is implementing sklearn's classifier API and is using the 
results that returned from StrengthCalc in his classifications.
It uses the API inherited from sklearn base and a base estimator received
and uses the predict_proba method for copies of the classifier.

## Experiments
To conduct our experiments we used the framework of jupyter notebooks.
This frameworks runs python kernel so we used our previous parts instantiations to run the experiments.

We use pyplotlib to create the graphs of the results in the report.
    



 