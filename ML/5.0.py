import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('concrete.csv')
df.shape
df.head()
df.dtypes
df.info()
df.isnull().values.any()

X = df.drop(['strength'], axis=1)
y = df['strength']

XScaled = X.apply(zscore)

XScaled.head()

X_train, X_test, y_train, y_test = train_test_split(
    XScaled,
    y,
    test_size=0.30,
    random_state=1
)

print('X training data size: {}'.format(X_train.shape))
print('y training data size: {}'.format(y_train.shape))
print('X testing data size: {}'.format(X_test.shape))
print('y testing data size: {}'.format(y_test.shape))
print(f"{len(X_train) / len(df) * 100:.2f}% of data is in training set")
print(f"{len(X_test) / len(df) * 100:.2f}% of data is in test set")


lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

print("Linear Regression model coefficients:", (lr.coef_))

print('\nLR R2_score on training data:', lr.score(X_train, y_train))
print('LR R2_score on test data:', lr.score(X_test, y_test))

print('LR Mean Square Error:',mean_squared_error(y_test, y_pred_lr))
print('LR Root Mean Square Error :',np.sqrt(mean_squared_error(y_test, y_pred_lr)))
print('LR Mean Absolute Error :',mean_absolute_error(y_test, y_pred_lr))