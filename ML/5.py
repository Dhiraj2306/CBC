# For the iris dataset, Implement Logistic Regression 
#   and Linear Regression. Plot the following graphs: Accuracy and 
#     Loss values per iteration


# Import the necessary libraries

# Numbers
import numpy as np
import pandas as pd

# Plots
import seaborn as sns
import matplotlib.pyplot as plt

# linear algebra
# Data processing, CSV file I/O (e.g. pd.read_csv)

# importing seaborn for statistical plots
# matplotlib.pyplot plots data

# Train test split
from sklearn.model_selection import train_test_split

# Sklearn package's randomized data splitting function

# Scaling related
from sklearn import preprocessing

# Provides several common utility functions:
# standardization of the data set

from scipy.stats import zscore

# Computes standard score relative to the sample mean
# and standard deviation

# Models
from sklearn.linear_model import LinearRegression

# To model the ordinary least squares Linear Regression

from sklearn.linear_model import Ridge

# To model Linear least squares with l2 regularization

from sklearn.linear_model import Lasso

# Linear Model trained with L1 prior as regularizer

# Metrics
from sklearn import metrics

# sklearn metrics module implements utility functions
# to measure classification performance

from sklearn.metrics import mean_squared_error

# Determines mean squared error regression loss

from sklearn.metrics import mean_absolute_error

# Determines mean absolute error regression loss

# Reading the data as a dataframe
df = pd.read_csv('concrete.csv')

# Checking the number of rows and columns in the data frame
df.shape

# Displaying the first five records of the dataframe
df.head()

# Data type of each attribute
df.dtypes

# Information about the data
df.info()

# Checking if there are any null values in the dataset
df.isnull().values.any()

# Copying all the predictor variables into X dataframe.
# Since 'strength' is dependent variable dropping it

X = df.drop(['strength'], axis=1)

# Copying the 'strength' column alone into the y dataframe.
# This is the dependent variable

y = df['strength']

# Scaling the attributes using Z score
XScaled = X.apply(zscore)

XScaled.head()

# Splitting the scaled data into training and test set
# in the ratio of 70:30 respectively

X_train, X_test, y_train, y_test = train_test_split(
    XScaled,
    y,
    test_size=0.30,
    random_state=1
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

# a) Linear Regression

# Fitting a simple linear model
lr = LinearRegression()

# Fitting the model on Training data
lr.fit(X_train, y_train)

# Making predictions on Test data
y_pred_lr = lr.predict(X_test)

# Printing the coefficients
print("Linear Regression model coefficients:", (lr.coef_))

print('\nLR R2_score on training data:', lr.score(X_train, y_train))
print('LR R2_score on test data:', lr.score(X_test, y_test))

print(
    'LR Mean Square Error:',
    mean_squared_error(y_test, y_pred_lr)
)

print(
    'LR Root Mean Square Error :',
    np.sqrt(mean_squared_error(y_test, y_pred_lr))
)

print(
    'LR Mean Absolute Error :',
    mean_absolute_error(y_test, y_pred_lr)
)
