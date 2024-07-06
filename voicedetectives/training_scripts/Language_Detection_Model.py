import numpy as np
import os
import librosa
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


# Function to extract features from audio files
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    return np.mean(mfcc, axis=1)


# Directory containing audio files for each language
data_dir = "D:\\python\\miniconda\\voice\\lang"
languages = os.listdir(data_dir)

X, y = [], []

# Extract features and labels from audio files
for language in languages:
    language_dir = os.path.join(data_dir, language)
    for audio_file in os.listdir(language_dir):
        audio_file_path = os.path.join(language_dir, audio_file)
        features = extract_features(audio_file_path)
        X.append(features)
        y.append(language)

# Convert lists to numpy arrays
X = np.array(X)
y = np.array(y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# Save the trained model
joblib.dump(model, "language_model.pkl")

# Save the label encoder classes
label_encoder = LabelEncoder()
label_encoder.fit(languages)
np.save("label_encoder_classes.npy", label_encoder.classes_)
