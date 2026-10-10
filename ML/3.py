# Write a program to implement the Naive Bayesian classifier 
#   for a sample training data set stored as a .CSV file

# Import the necessary libraries

# Numbers
import numpy as np
import pandas as pd

# Plots
import matplotlib.pyplot as plt
import seaborn as sns

# Train test split function
from sklearn.model_selection import train_test_split

# Model
from sklearn.naive_bayes import GaussianNB

# Metrics
from sklearn import metrics

# To model the Gaussian Naive Bayes classifier
# Implements utility functions to measure classification performance
# Computes confusion matrix
from sklearn.metrics import confusion_matrix

# Provides several common utility functions
from sklearn import preprocessing

# Reading the data as a dataframe
df = pd.read_csv('Bank_Personal_Loan_Modelling_PGM_3.csv')

# Displaying first 5 rows of the dataframe
df.head()

# Checking the number of columns and rows in data frame
df.shape

# Information about the data
df.info()

# Checking if there are any null values in the dataset
df.isnull().values.any()

# Separating the target variable
X = df.drop('Personal Loan', axis=1)

# Input variables
y = df['Personal Loan']

# Target variable

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1
)  # 1 is just any random seed number

# Checking split of data
print('X training data size:', X_train.shape)
print('y training data size:', y_train.shape)
print('X testing data size:', X_test.shape)
print('y testing data size:', y_test.shape)

print("Data in training set:", (len(X_train) / len(df.index)) * 100)
print("Data in test set:", (len(X_test) / len(df.index)) * 100)

# a) Unscaled data

# Model building without scaling
gnb_model = GaussianNB()
gnb_model.fit(X_train, y_train)
gnb_pred = gnb_model.predict(X_test)

# gnb_cm = metrics.confusion_matrix(y_test, gnb_pred)

# Confusion matrix
cm = metrics.confusion_matrix(y_test, gnb_pred, labels=[1, 0])

df_cm = pd.DataFrame(
    cm,
    index=[i for i in ["Actual 1", "Actual 0"]],
    columns=[i for i in ["Predict 1", "Predict 0"]]
)

plt.title('Naive Bayes Confusion Matrix without scaling')
sns.heatmap(df_cm, annot=True, fmt='g')

# Accuracy
TP = cm[0, 0]
FP = cm[0, 1]
FN = cm[1, 0]
TN = cm[1, 1]

# Print classification accuracy
classification_accuracy = (TP + TN) / float(TP + TN + FP + FN)

print(
    'Classification accuracy without scaling: {0:0.4f}'.format(
        classification_accuracy
    )
)

# b) Scaled data

# Scaling the attributes
X_train_scaled = preprocessing.scale(X_train)
X_test_scaled = preprocessing.scale(X_test)

# Model building after scaling
scaled_gnb_model = GaussianNB()
scaled_gnb_model.fit(X_train_scaled, y_train)

scaled_gnb_pred = scaled_gnb_model.predict(X_test_scaled)

# scaled_gnb_cm = metrics.confusion_matrix(y_test, scaled_gnb_pred)

# Confusion matrix
cm = metrics.confusion_matrix(y_test, scaled_gnb_pred, labels=[1, 0])

df_cm = pd.DataFrame(
    cm,
    index=[i for i in ["Actual 1", "Actual 0"]],
    columns=[i for i in ["Predict 1", "Predict 0"]]
)

plt.title('Naive Bayes Confusion Matrix after scaling')
sns.heatmap(df_cm, annot=True, fmt='g')

# Accuracy
TP = cm[0, 0]
FP = cm[0, 1]
FN = cm[1, 0]
TN = cm[1, 1]

# Print classification accuracy
classification_accuracy = (TP + TN) / float(TP + TN + FP + FN)

print(
    'Classification accuracy after scaling: {0:0.4f}'.format(
        classification_accuracy
    )
)