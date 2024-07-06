import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
import joblib


# Function to extract Mel-frequency cepstral coefficients (MFCC) features from audio
def extract_features(audio_file, max_length=100):
    y, sr = librosa.load(audio_file, sr=None)
    mfcc_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    # Standardize feature length (pad or trim)
    if mfcc_features.shape[1] < max_length:
        mfcc_features = np.pad(mfcc_features, ((0, 0), (0, max_length - mfcc_features.shape[1])), mode='constant')
    else:
        mfcc_features = mfcc_features[:, :max_length]
    return mfcc_features


# Function to load and preprocess data
def load_data(data_dir, max_length=100):
    X = []
    y = []
    for label in os.listdir(data_dir):
        label_dir = os.path.join(data_dir, label)
        for audio_file in os.listdir(label_dir):
            audio_file_path = os.path.join(label_dir, audio_file)
            try:
                features = extract_features(audio_file_path, max_length=max_length)
                X.append(features)
                if label == "human":
                    y.append(0)  # 0 for human
                else:
                    y.append(1)  # 1 for AI
            except Exception as e:
                print(f"Error processing {audio_file_path}: {e}")
    return np.array(X), np.array(y)


# Load data
data_dir = "D:\\python\\miniconda\\voice\\audio"  # Replace with the path to your labeled data directory
X, y = load_data(data_dir)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define model architecture
model = models.Sequential([
    layers.Input(shape=(20, 100)),
    layers.Conv1D(32, 3, activation='relu'),
    layers.MaxPooling1D(2),
    layers.Conv1D(64, 3, activation='relu'),
    layers.MaxPooling1D(2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Save trained model for future use
model.save("audio_type_classification.h5")
