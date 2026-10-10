# =========================================================
# IMPORTING LIBRARIES
# =========================================================

import os
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

from sklearn.decomposition import PCA

# =========================================================
# OUTPUT FOLDER
# =========================================================

output_path = r"D:\Applications\CODES\Python"

# =========================================================
# LOADING DATASET
# =========================================================

df = pd.read_csv(r"D:\PDFzzz\Data Sets\Spotify track dataset.csv")

# =========================================================
# BASIC DATASET INFORMATION
# =========================================================

print("\nDataset Shape:\n")
print(df.shape)

print("\nFirst 5 Rows:\n")
print(df.head())

print("\nDataset Info:\n")
print(df.info())

print("\nChecking Null Values:\n")
print(df.isnull().sum())

# =========================================================
# CLEANING DATA
# =========================================================

df = df.dropna()

df = df.drop_duplicates()

df = df.reset_index(drop=True)

print("\nDataset Shape After Cleaning:\n")
print(df.shape)

# =========================================================
# SELECTING IMPORTANT FEATURES
# =========================================================

X = df[[
    'popularity',
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo'
]]

# =========================================================
# TARGET VARIABLE
# =========================================================

y = df['track_genre']

# =========================================================
# FEATURE SCALING
# =========================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=1
)

print('\nX training data size: {}'.format(X_train.shape))
print('y training data size: {}'.format(y_train.shape))
print('X testing data size: {}'.format(X_test.shape))
print('y testing data size: {}'.format(y_test.shape))

# =========================================================
# FINDING BEST K VALUE
# =========================================================

numberList = list(range(1, 31))

neighbors = list(filter(lambda x: x % 2 != 0, numberList))

ac_scores = []

for k in neighbors:

    knn = KNeighborsClassifier(
        n_neighbors=k,
        weights='distance'
    )

    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    scores = accuracy_score(y_test, y_pred)

    ac_scores.append(scores)

# =========================================================
# MISCLASSIFICATION ERROR
# =========================================================

MSE = [1 - x for x in ac_scores]

optimal_k = neighbors[MSE.index(min(MSE))]

print('\nOdd Neighbors :\n', neighbors)

print('\nAccuracy Scores :\n', ac_scores)

print('\nMisclassification Error :\n', MSE)

print("\nOptimal K Value =", optimal_k)

# =========================================================
# PLOT ERROR VS K
# =========================================================

plt.figure(figsize=(8, 5))

plt.plot(neighbors, MSE, marker='o')

plt.xlabel('Number of Neighbors K')

plt.ylabel('Misclassification Error')

plt.title('K Value vs Error')

plt.grid(True)

plt.savefig(
    os.path.join(output_path, "K_Value_vs_Error.png"),
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# =========================================================
# FINAL KNN MODEL
# =========================================================

knn_model = KNeighborsClassifier(
    n_neighbors=optimal_k,
    weights='distance',
    metric='euclidean'
)

knn_model.fit(X_train, y_train)

knn_pred = knn_model.predict(X_test)

# =========================================================
# CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(y_test, knn_pred)

plt.figure(figsize=(12, 10))

sns.heatmap(cm, annot=False)

plt.title('KNN Confusion Matrix')

plt.savefig(
    os.path.join(output_path, "Confusion_Matrix.png"),
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# =========================================================
# FINAL ACCURACY
# =========================================================

classification_accuracy = accuracy_score(y_test, knn_pred)

print('\nClassification Accuracy: {0:0.4f}'.format(
    classification_accuracy
))

# =========================================================
# CLASSIFICATION REPORT
# =========================================================

print("\nClassification Report:\n")

print(classification_report(y_test, knn_pred))

# =========================================================
# =========================================================
# FEATURE 1 : MUSIC RECOMMENDATION SYSTEM
# =========================================================
# =========================================================

print("\n=================================================")

print("MUSIC RECOMMENDATION SYSTEM")

print("=================================================\n")

# =========================================================
# FEATURES FOR RECOMMENDATION
# =========================================================

feature_columns = [
    'popularity',
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo'
]

recommendation_features = df[feature_columns]

recommendation_features_scaled = scaler.fit_transform(
    recommendation_features
)

# =========================================================
# RECOMMENDATION MODEL
# =========================================================

recommendation_model = NearestNeighbors(
    n_neighbors=11,
    metric='euclidean'
)

recommendation_model.fit(recommendation_features_scaled)

# =========================================================
# FUNCTION TO RECOMMEND SONGS
# =========================================================

def recommend_songs(song_name):

    matching_songs = df[
        df['track_name'].str.lower().str.contains(
            song_name.lower(),
            na=False
        )
    ]

    if matching_songs.empty:

        print("Song not found in dataset")

        return

    song_index = matching_songs.index[0]

    distances, indices = recommendation_model.kneighbors(
        recommendation_features_scaled[song_index].reshape(1, -1)
    )

    print("\nRecommended Songs for:",
          df.iloc[song_index]['track_name'])

    print("\n")

    for i in indices[0][1:6]:

        print(
            "Track:", df.iloc[i]['track_name'],
            "| Artist:", df.iloc[i]['artists'],
            "| Genre:", df.iloc[i]['track_genre']
        )

# =========================================================
# SAMPLE RECOMMENDATION
# =========================================================

recommend_songs('love')

# =========================================================
# =========================================================
# FEATURE 2 : SONG CLUSTERING
# =========================================================
# =========================================================

print("\n=================================================")

print("SONG CLUSTERING")

print("=================================================\n")

# =========================================================
# ELBOW METHOD
# =========================================================

inertia_values = []

for k in range(1, 11):

    kmeans_test = KMeans(
        n_clusters=k,
        random_state=1,
        n_init=10
    )

    kmeans_test.fit(recommendation_features_scaled)

    inertia_values.append(kmeans_test.inertia_)

plt.figure(figsize=(8, 5))

plt.plot(range(1, 11), inertia_values, marker='o')

plt.xlabel('Number of Clusters')

plt.ylabel('Inertia')

plt.title('Elbow Method')

plt.grid(True)

plt.savefig(
    os.path.join(output_path, "Elbow_Method.png"),
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# =========================================================
# FINAL KMEANS MODEL
# =========================================================

kmeans = KMeans(
    n_clusters=8,
    random_state=1,
    n_init=10
)

clusters = kmeans.fit_predict(recommendation_features_scaled)

df['Cluster'] = clusters

print("\nCluster Counts:\n")

print(df['Cluster'].value_counts())

# =========================================================
# PCA CLUSTER VISUALIZATION WITH MEANINGFUL LABELS
# =========================================================

# Creating readable labels for clusters

cluster_labels = {
    0: 'Workout / Energetic',
    1: 'Dance / Party',
    2: 'Pop / Trending',
    3: 'Chill / Relax',
    4: 'Emotional / Soft',
    5: 'Acoustic / Calm',
    6: 'Live / Instrumental',
    7: 'Mixed Vibes'
}

# PCA Transformation

pca = PCA(n_components=2)

pca_features = pca.fit_transform(
    recommendation_features_scaled
)

plt.figure(figsize=(12, 7))

scatter = plt.scatter(
    pca_features[:, 0],
    pca_features[:, 1],
    c=df['Cluster'],
    cmap='viridis',
    alpha=0.7
)

plt.xlabel('PCA Component 1')

plt.ylabel('PCA Component 2')

plt.title('PCA Visualization of Spotify Song Clusters')

# Creating custom legend labels

handles = scatter.legend_elements()[0]

labels = [
    cluster_labels[i]
    for i in range(len(handles))
]

plt.legend(
    handles,
    labels,
    title='Song Clusters',
    loc='upper left',
    bbox_to_anchor=(1.02, 1)
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(output_path, "PCA_Cluster_Visualization.png"),
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# =========================================================
# =========================================================
# FEATURE 3 : MOOD DETECTION SYSTEM
# =========================================================
# =========================================================

print("\n=================================================")

print("MOOD DETECTION SYSTEM")

print("=================================================\n")

# =========================================================
# MOOD FILTERS
# =========================================================

happy_songs = df[
    (df['valence'] > 0.6) &
    (df['energy'] > 0.5)
]

sad_songs = df[
    (df['valence'] < 0.4) &
    (df['energy'] < 0.5)
]

energetic_songs = df[
    (df['energy'] > 0.8)
]

calm_songs = df[
    (df['acousticness'] > 0.7) &
    (df['energy'] < 0.4)
]

# =========================================================
# FUNCTION TO SUGGEST SONGS BASED ON MOOD
# =========================================================

def suggest_songs_by_mood(mood):

    print("\nSuggested Songs for Mood:", mood)

    print("\n")

    if mood.lower() == 'happy':

        sample = happy_songs.sample(
            min(5, len(happy_songs))
        )

    elif mood.lower() == 'sad':

        sample = sad_songs.sample(
            min(5, len(sad_songs))
        )

    elif mood.lower() == 'energetic':

        sample = energetic_songs.sample(
            min(5, len(energetic_songs))
        )

    elif mood.lower() == 'calm':

        sample = calm_songs.sample(
            min(5, len(calm_songs))
        )

    else:

        print("Mood not found")

        return

    for index, row in sample.iterrows():

        print(
            "Track:", row['track_name'],
            "| Artist:", row['artists'],
            "| Genre:", row['track_genre']
        )

# =========================================================
# SAMPLE MOOD DETECTION
# =========================================================

suggest_songs_by_mood('happy')

# =========================================================
# PROJECT COMPLETED
# =========================================================

print("\n=================================================")

print("PROJECT COMPLETED SUCCESSFULLY")

print("=================================================\n")

print("\nGraphs saved successfully in:")
print(output_path)