# -*- coding: utf-8 -*-
"""Speech Emotion Recognition

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19_hveImjx48b9YQ4yNQ6OEUzkReCrrCD

##Speech Emotion Recognition

#Import Modules
"""

import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import librosa
import librosa.display
from IPython.display import Audio
import warnings
warnings.filterwarnings('ignore')

"""##Load the Dataset"""

import zipfile
import os

zip_path = "/content/drive/MyDrive/Data_Science/TESS_Toronto_emotional_speech_set_data.zip"
extract_path = "/content/drive/MyDrive/Data_Science/TESS_Toronto_emotional_speech_set_data/"

# Create the extraction directory if it doesn't exist
os.makedirs(extract_path, exist_ok=True)

# Unzip the file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Display the path of the extracted folder
extracted_folder_path = os.path.join(extract_path, os.path.splitext(os.path.basename(zip_path))[0])
print("Path of the extracted folder:", extracted_folder_path)

paths = []
labels = []
for dirname, _, filenames in os.walk('/content/drive/MyDrive/Data_Science/TESS_Toronto_emotional_speech_set_data/TESS_Toronto_emotional_speech_set_data'):
    for filename in filenames:
        paths.append(os.path.join(dirname, filename))
        label = filename.split('_')[-1]
        label = label.split('.')[0]
        labels.append(label.lower())
    if len(paths) == 2800:
        break
print('Dataset is Loaded')

len(paths)

paths[:5]

labels[:5]

## Create a dataframe
df = pd.DataFrame()
df['speech'] = paths
df['label'] = labels
df.head()

df['label'].value_counts()

"""##Exploratory Data Analysis"""

sns.countplot(data=df, x='label')

def waveplot(data, sr, emotion):
    plt.figure(figsize=(10,4))
    plt.title(emotion, size=20)
    librosa.display.waveshow(data, sr=sr)
    plt.show()

def spectogram(data, sr, emotion):
    x = librosa.stft(data)
    xdb = librosa.amplitude_to_db(abs(x))
    plt.figure(figsize=(11,4))
    plt.title(emotion, size=20)
    librosa.display.specshow(xdb, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar()

emotion = 'fear'
path = np.array(df['speech'][df['label']==emotion])[0]
data, sampling_rate = librosa.load(path)
waveplot(data, sampling_rate, emotion)
spectogram(data, sampling_rate, emotion)
print('---------------------------------')
print('Audio:\n')

Audio(path)

emotion = 'angry'
path = np.array(df['speech'][df['label']==emotion])[1]
data, sampling_rate = librosa.load(path)
waveplot(data, sampling_rate, emotion)
spectogram(data, sampling_rate, emotion)
print('---------------------------------')
print('Audio:\n')

Audio(path)

emotion = 'disgust'
path = np.array(df['speech'][df['label']==emotion])[0]
data, sampling_rate = librosa.load(path)
waveplot(data, sampling_rate, emotion)
spectogram(data, sampling_rate, emotion)
print('---------------------------------')
print('Audio:\n')

Audio(path)

emotion = 'neutral'
path = np.array(df['speech'][df['label']==emotion])[0]
data, sampling_rate = librosa.load(path)
waveplot(data, sampling_rate, emotion)
spectogram(data, sampling_rate, emotion)
print('---------------------------------')
print('Audio:\n')

Audio(path)

emotion = 'sad'
path = np.array(df['speech'][df['label']==emotion])[0]
data, sampling_rate = librosa.load(path)
waveplot(data, sampling_rate, emotion)
spectogram(data, sampling_rate, emotion)
print('---------------------------------')
print('Audio:\n')

Audio(path)

emotion = 'ps'
path = np.array(df['speech'][df['label']==emotion])[0]
data, sampling_rate = librosa.load(path)
waveplot(data, sampling_rate, emotion)
spectogram(data, sampling_rate, emotion)
print('---------------------------------')
print('Audio:\n')

Audio(path)

emotion = 'happy'
path = np.array(df['speech'][df['label']==emotion])[0]
data, sampling_rate = librosa.load(path)
waveplot(data, sampling_rate, emotion)
spectogram(data, sampling_rate, emotion)
print('---------------------------------')
print('Audio:\n')

Audio(path)

"""* Waveplot and spectrogram of an audio file from each class is plotted

* Sample audio of emotion speech from each class is displayed

* Lower pitched voices have darker colors

* Higher pitched voices have more brighter colors

##Feature Extraction
"""

def extract_mfcc(filename):
    y, sr = librosa.load(filename, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    return mfcc

"""* Audio duration capped to max 3 seconds for equal duration of file size

* It will extract the Mel-frequency cepstral coefficients (MFCC) features with the limit of 40 and take the mean as the final feature
"""

extract_mfcc(df['speech'][0])

X_mfcc = df['speech'].apply(lambda x: extract_mfcc(x))

"""* Returns extracted features from all the audio files"""

X_mfcc

"""* Visualization of the features extracted from the data

* The more samples in the dataset, the longer the processing time
"""

X = [x for x in X_mfcc]
X = np.array(X)
X.shape

"""* Conversion of the list into a single dimensional array"""

## input split
X = np.expand_dims(X, -1)
X.shape

"""* The shape represents the number of samples in the dataset and features in a single dimension array"""

from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()
y = enc.fit_transform(df[['label']])

y = y.toarray()

y.shape

"""* The shape represents the number of samples and number of output classes

##Create the LSTM Model
"""

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import ReduceLROnPlateau


model = Sequential([
    LSTM(256, return_sequences=False, input_shape=(40,1)),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(7, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

"""##LSTM Model Summary
* Dense - single dimension linear layer with hidden units

* Dropout - used to add regularization to the data, avoiding over fitting & dropping out a fraction of the data

* Loss='sparse_categorical_crossentropy' - computes the cross-entropy loss between true labels and predicted labels.

* Optimizer='adam' - automatically adjust the learning rate for the model over the number of epochs
"""

# Train the model
# history = model.fit(X, y, validation_split=0.2, epochs=50, batch_size=64)
# Assuming X, y are your training data
rlrp = ReduceLROnPlateau(monitor='loss', factor=0.4, verbose=0, patience=2, min_lr=0.0000001)
history = model.fit(X, y, validation_split=0.2, epochs=50, batch_size=64, callbacks=[rlrp])

# Print final training and validation accuracy
train_accuracy = history.history['accuracy'][-1]
val_accuracy = history.history['val_accuracy'][-1]

print(f"Final Training Accuracy: {train_accuracy}")
print(f"Final Validation Accuracy: {val_accuracy}")

"""**Best val_accuracy was: *70.36***

##Plot the results
"""

epochs = list(range(50))
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

plt.plot(epochs, acc, label='train accuracy')
plt.plot(epochs, val_acc, label='val accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.plot(epochs, loss, label='train loss')
plt.plot(epochs, val_loss, label='val loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()