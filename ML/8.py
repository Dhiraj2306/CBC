# For the given dataset, develop the recommendation system using PCA.

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

loan = pd.read_csv("loan_dataset.csv")

features = [
    'ApplicantIncome',
    'CoapplicantIncome',
    'LoanAmount',
    'Loan_Amount_Term',
    'Credit_History'
]

loan_features = loan[features].fillna(loan[features].mean())

scaler = StandardScaler()
scaled_data = scaler.fit_transform(loan_features)

pca = PCA(n_components=2)
pca_components = pca.fit_transform(scaled_data)
pca_df = pd.DataFrame(pca_components, columns=['PC1', 'PC2'])

similarity = cosine_similarity(pca_df)

def recommend_similar_applicants(applicant_index, top_n=3):
    scores = list(enumerate(similarity[applicant_index]))
    
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    return scores[1:top_n+1]

recommend_similar_applicants(0)