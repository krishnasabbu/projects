import pandas as pd
import numpy as np
import os
# import seaborn as sns
# import matplotlib.pyplot as plt
import librosa
# import librosa.display
# from IPython.display import Audio
import warnings
from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

warnings.filterwarnings('ignore')

paths = []
labels = []
for dirname, _, filenames in os.walk('D:\\Downloads\\Converted_Certificates\\Bills\\emotion\\dataset'):
    for filename in filenames:
        paths.append(os.path.join(dirname, filename))
        label = filename.split('_')[-1]
        label = label.split('.')[0]
        labels.append(label.lower())
    if len(paths) == 2800:
        break
print('Dataset is Loaded')

len(paths)

df = pd.DataFrame()
df['speech'] = paths
df['label'] = labels
df.head()

print(f"count == {df['label'].value_counts()}")


def extract_mfcc(filename):
    y, sr = librosa.load(filename, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    return mfcc


X_mfcc = df['speech'].apply(lambda x: extract_mfcc(x))
X = [x for x in X_mfcc]
X = np.array(X)

enc = OneHotEncoder()
y = enc.fit_transform(df[['label']])
y = y.toarray()

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

history = model.fit(X, y, validation_split=0.2, epochs=50, batch_size=64)

print(f"history === {history}")

model.save("speaker_emotional_model.h5")
