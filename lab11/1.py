import os
import numpy as np
import keras
from keras.datasets import reuters, imdb
from keras.models import Sequential
from keras.layers import LSTM, SimpleRNN, GRU, Dense, Dropout, Activation, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
import pandas as pd

EMBEDDING_DIM = 50
# load in training/test set
data = pd.read_csv('tweets.160k.random.csv', encoding='utf-8')
data.head()

data['label'].value_counts()

vocab_size = 20000
tokenizer = Tokenizer(num_words= vocab_size)
tokenizer.fit_on_texts(data['text'])
sequences = tokenizer.texts_to_sequences(data['text'])
word_index = tokenizer.word_index
tweets = sequence.pad_sequences(sequences, padding='post', maxlen=50)


labels = data['label']
labels = labels.replace(4,1) # replace label '4' with '1' to facilitate one-hot encoding
x_train, x_test, y_train, y_test = train_test_split(tweets, labels, test_size=0.2)

print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')

y_train = keras.utils.to_categorical(y_train) # 2 classes
y_test = keras.utils.to_categorical(y_test)

embeddings_index = {}
GLOVE_DIR = "/Users/soujanyaporia/Downloads/"
f = open(os.path.join(GLOVE_DIR, 'glove.6B.50d.txt'))
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))

embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

model = Sequential()
model.add(Embedding(len(word_index)+1, EMBEDDING_DIM, weights=[embedding_matrix], trainable=False))
model.add(SimpleRNN(128))
model.add(Dense(2))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(x_train, y_train, batch_size=128, epochs=3, verbose=1, validation_split=0.2)

score = model.evaluate(x_test, y_test, batch_size=128, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])

