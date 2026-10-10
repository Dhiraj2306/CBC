# Write a program to implement the K-Nearest 
#    Neighbour classifier for a sample training data set stored as a .CSV file. 
#      Find the optimal number of neighbours

# Import the necessary libraries

# Numbers
import numpy as np
import pandas as pd

# linear algebra
# Data processing, CSV file I/O (e.g. pd.read_csv)

# Plots
import seaborn as sns

# importing seaborn for statistical plots
import matplotlib.pyplot as plt

# matplotlib.pyplot plots data

# Train test split
from sklearn.model_selection import train_test_split

# Sklearn package's randomized data splitting function

# Model
from sklearn.neighbors import KNeighborsClassifier

# To model the KNN classifier

# Metrics
from sklearn import metrics

# sklearn metrics module implements utility functions to
# measure classification performance
from sklearn.metrics import confusion_matrix

# Computes confusion matrix to evaluate the accuracy of a classification

from sklearn import preprocessing

# Provides several common utility functions:
# standardization of the data set
from sklearn.preprocessing import StandardScaler

# Standardizes features by removing the mean and scaling to unit variance
from sklearn.metrics import accuracy_score

# Performance measure – Accuracy

# Reading the data as a dataframe
df = pd.read_csv('diabetes.csv')

# Checking the number of rows and columns in the data frame
df.shape

# Displaying the first five records of the dataframe
df.head()

# Information about the data
df.info()

# Checking if there are any null values in the dataset
df.isnull().values.any()

# Separating the target variable
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1
)  # 1 is just any random seed number

# Checking split of data
print('X training data size: {}'.format(X_train.shape))
print('y training data size: {}'.format(y_train.shape))
print('X testing data size: {}'.format(X_test.shape))
print('y testing data size: {}'.format(y_test.shape))

print("{0:0.2f}% of data is in training set".format(
    (len(X_train) / len(df.index)) * 100
))

print("{0:0.2f}% of data is in test set".format(
    (len(X_test) / len(df.index)) * 100
))

# Creating number list from range 1 to 20 of K for KNN with
# X_train, X_test, y_train, y_test

numberList = list(range(1, 20))

neighbors = list(filter(lambda x: x % 2 != 0, numberList))
# subsetting just the odd ones

# Declaring an empty list that will hold the accuracy scores
ac_scores = []

# performing accuracy metrics for value from 1,3,5....19
for k in neighbors:
    knn = KNeighborsClassifier(n_neighbors=k)

    # predict the response
    knn.fit(X_train, y_train.values.ravel())
    y_pred = knn.predict(X_test)

    # evaluate accuracy
    scores = accuracy_score(y_test, y_pred)

    # insert scores to the list
    ac_scores.append(scores)

# changing to misclassification error
MSE = [1 - x for x in ac_scores]

# determining best k
optimal_k = neighbors[MSE.index(min(MSE))]

print('Odd Neighbors : \n', neighbors)
print('\nAccuracy Score : \n', ac_scores)
print('\nMisclassification error :\n', MSE)
print("\nThe optimal number of neighbor is k=", optimal_k)

# plot misclassification error vs k
plt.plot(neighbors, MSE)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error')
plt.show()

# Model building using X_train, X_test, y_train, y_test
# with obtained optimal_k

knn_model = KNeighborsClassifier(
    n_neighbors=optimal_k,
    weights='uniform',
    metric='euclidean'
)

knn_model.fit(X_train, y_train)

knn_pred = knn_model.predict(X_test)

# Confusion matrix
cm = metrics.confusion_matrix(y_test, knn_pred, labels=[1, 0])

df_cm = pd.DataFrame(
    cm,
    index=[i for i in ["Actual 1", "Actual 0"]],
    columns=[i for i in ["Predict 1", "Predict 0"]]
)

plt.title('KNN Confusion Matrix')
sns.heatmap(df_cm, annot=True, fmt='g')

# Accuracy
TP = cm[0, 0]
FP = cm[0, 1]
FN = cm[1, 0]
TN = cm[1, 1]

# Print classification accuracy
classification_accuracy = (TP + TN) / float(TP + TN + FP + FN)

print(
    'Classification accuracy: {0:0.4f}'.format(
        classification_accuracy
    )
)