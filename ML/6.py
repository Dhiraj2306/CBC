# Implement ID3 decision tree algorithm using Python.


# Import the necessary libraries

# Numerical computation
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt

# Train-test split
from sklearn.model_selection import train_test_split

# ID3 Decision Tree (Entropy-based)
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Reading the data
df = pd.read_csv('fertility.csv')

# Checking dataset shape
print("Dataset shape:", df.shape)

# Display first five records
print(df.head())

# Dataset information
print(df.info())

# Checking for missing values
print("Any missing values:", df.isnull().values.any())

# Feature selection and target variable
X = df.drop('output', axis=1)
y = df['output']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# Checking data split
print('X training data size:', X_train.shape)
print('y training data size:', y_train.shape)
print('X testing data size:', X_test.shape)
print('y testing data size:', y_test.shape)

print("{0:0.2f}% of data is in training set".format(
    (len(X_train) / len(df)) * 100
))

print("{0:0.2f}% of data is in test set".format(
    (len(X_test) / len(df)) * 100
))

# Model building using ID3 (Entropy)
id3_tree = DecisionTreeClassifier(
    criterion='entropy',   # ID3 uses entropy
    random_state=1
)

id3_tree.fit(X_train, y_train)

# Model evaluation
print(
    'Test accuracy before feature removal:',
    id3_tree.score(X_test, y_test)
)

# Visualizing the ID3 Decision Tree
feature_names = list(X_train.columns)

# Ensure these match actual class labels
class_names = ['N', 'O']

plt.figure(figsize=(6, 6), dpi=300)

plot_tree(
    id3_tree,
    feature_names=feature_names,
    class_names=class_names,
    filled=True
)

plt.show()

# Feature importance (Information Gain based)
fi = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': id3_tree.feature_importances_
})

fi = fi.sort_values(
    by='Importance',
    ascending=False,
    ignore_index=True
)

print(fi)

# Removing low-importance features
X_train_new = X_train.drop(
    columns=[
        'sitting',
        'surgical-intervention',
        'childish-disease',
        'fevers'
    ]
)

X_test_new = X_test.drop(
    columns=[
        'sitting',
        'surgical-intervention',
        'childish-disease',
        'fevers'
    ]
)

# Rebuilding ID3 model with selected features
id3_tree_new = DecisionTreeClassifier(
    criterion='entropy',
    random_state=1
)

id3_tree_new.fit(X_train_new, y_train)

# Model evaluation after feature removal
print(
    'Test accuracy after feature removal:',
    id3_tree_new.score(X_test_new, y_test)
)