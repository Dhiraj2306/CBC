import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing

df = pd.read_csv('Bank_Personal_Loan_Modelling_PGM_3.csv')
df.head()
df.shape
df.info()
df.isnull().values.any()

X = df.drop('Personal Loan', axis=1)
y = df['Personal Loan']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

print('X training data size:', X_train.shape)
print('y training data size:', y_train.shape)
print('X testing data size:', X_test.shape)
print('y testing data size:', y_test.shape)

print("Data in training set:", (len(X_train) / len(df.index)) * 100)
print("Data in test set:", (len(X_test) / len(df.index)) * 100)

# a) Unscaled data

gnb_model = GaussianNB()
gnb_model.fit(X_train, y_train)
gnb_pred = gnb_model.predict(X_test)

cm = metrics.confusion_matrix(y_test, gnb_pred, labels=[1, 0])

df_cm = pd.DataFrame(
    cm,
    index=[i for i in ["Actual 1", "Actual 0"]],
    columns=[i for i in ["Predict 1", "Predict 0"]]
)

plt.title('Naive Bayes Confusion Matrix without scaling')
sns.heatmap(df_cm, annot=True, fmt='g')

TP = cm[0, 0]
FP = cm[0, 1]
FN = cm[1, 0]
TN = cm[1, 1]

classification_accuracy = (TP + TN) / float(TP + TN + FP + FN)

print(f'Classification accuracy without scaling: {classification_accuracy:.4f}')

# b) Scaled data

X_train_scaled = preprocessing.scale(X_train)
X_test_scaled = preprocessing.scale(X_test)

s_gnb_model = GaussianNB()
s_gnb_model.fit(X_train_scaled, y_train)
s_gnb_pred = s_gnb_model.predict(X_test_scaled)

cm = metrics.confusion_matrix(y_test, s_gnb_pred, labels=[1, 0])

df_cm = pd.DataFrame(
    cm,
    index=[i for i in ["Actual 1", "Actual 0"]],
    columns=[i for i in ["Predict 1", "Predict 0"]]
)

plt.title('Naive Bayes Confusion Matrix after scaling')
sns.heatmap(df_cm, annot=True, fmt='g')

TP = cm[0, 0]
FP = cm[0, 1]
FN = cm[1, 0]
TN = cm[1, 1]

classification_accuracy = (TP + TN) / float(TP + TN + FP + FN)

print(f'Classification accuracy without scaling: {classification_accuracy:.4f}')