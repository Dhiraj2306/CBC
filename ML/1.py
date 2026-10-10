#Write a program to implement different data imputations in Machine Learning using Python.

#a) Mean

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

dataset = pd.read_csv('pima-indians-diabetes.csv', header=None)

print('Missing values before imputation:', dataset.isnull().sum())

values = dataset.values
print('\nValues before imputation:\n', values)

imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
transformed_values = imputer.fit_transform(values)

print('\nValues after imputation:\n', transformed_values)

print('\nMissing values after imputation:', np.isnan(transformed_values).sum())