import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def extract_features(audio_file, mfcc=True, chroma=True, mel=True):
    y, sample_rate = librosa.load(audio_file)
    features = []
    if chroma:
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sample_rate)
        features.append(chroma_stft.T)
    if mel:
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sample_rate)
        features.append(mel_spectrogram.T)
    if mfcc:
        mfccs = librosa.feature.mfcc(y=y, sr=sample_rate)
        features.append(mfccs.T)
    return np.hstack(features)


# Directory containing labeled audio files
live_audio_dir = "D:\\python\\miniconda\\voice\\live\\live"
recorded_audio_dir = "D:\\python\\miniconda\\voice\\live\\recorded"

# Initialize lists to store features and labels
X = []
y = []

# Process live audio files
for audio_file in os.listdir(live_audio_dir):
    audio_file_path = os.path.join(live_audio_dir, audio_file)
    features = extract_features(audio_file_path)
    X.append(features)
    y.append("live")

# Process recorded audio files
for audio_file in os.listdir(recorded_audio_dir):
    audio_file_path = os.path.join(recorded_audio_dir, audio_file)
    features = extract_features(audio_file_path)
    X.append(features)
    y.append("recorded")

# Convert lists to numpy arrays
X = np.array(X)
y = np.array(y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Flatten the features
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Initialize and train the classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train_flat, y_train)

# Make predictions
y_pred = classifier.predict(X_test_flat)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the trained model
model_filename = "live_vs_recorded_model.joblib"
joblib.dump(classifier, model_filename)
print(f"Model saved as {model_filename}")
