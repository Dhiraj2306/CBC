import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


df = pd.read_csv('diabetes.csv')
df.shape
df.head()
df.info()
df.isnull().values.any()

X = df.drop('Outcome', axis=1)
y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

print('X training data size: {}'.format(X_train.shape))
print('y training data size: {}'.format(y_train.shape))
print('X testing data size: {}'.format(X_test.shape))
print('y testing data size: {}'.format(y_test.shape))
print(f"{len(X_train) / len(df) * 100:.2f}% of data is in training set")
print(f"{len(X_test) / len(df) * 100:.2f}% of data is in test set")

numberList = list(range(1, 20))
neighbors = [x for x in numberList if x % 2 != 0]
ac_scores = []

for k in neighbors:

    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train.values.ravel())
    y_pred = knn.predict(X_test)

    scores = accuracy_score(y_test, y_pred)
    ac_scores.append(scores)


error = [1 - x for x in ac_scores]
optimal_k = neighbors[error.index(min(error))]

print('Odd Neighbors : \n', neighbors)
print('\nAccuracy Score : \n', ac_scores)
print('\nMisclassification error :\n', error)
print("\nThe optimal number of neighbor is k=", optimal_k)


plt.plot(neighbors, error)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error')
plt.show()

knn_model = KNeighborsClassifier(n_neighbors=optimal_k, weights='uniform', metric='euclidean')
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