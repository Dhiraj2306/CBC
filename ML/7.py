from gensim.models import Word2Vec

import re

corpus = [
    "Machine learning is fascinating",
    "Deep learning is a subset of machine learning",
    "Natural language processing uses machine learning",
    "Word embeddings capture semantic meaning",
    "Word2Vec is a popular embedding technique"
]

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.split()

sentences = [preprocess(sentence) for sentence in corpus]

print("Tokenized Sentences:")
print(sentences)

model = Word2Vec(
    sentences=sentences,
    vector_size=50,
    window=3,
    min_count=1,
    workers=4,
    sg=1
)

print("\nVocabulary:")
print(model.wv.index_to_key)

vector = model.wv['learning']
print("\nWord Embedding for 'learning':")
print(vector)
print("\nEmbedding dimension:", len(vector))
similar_words = model.wv.most_similar('learning', topn=3)

print("\nWords similar to 'learning':")

for word, score in similar_words:
    print(word, ":", score)