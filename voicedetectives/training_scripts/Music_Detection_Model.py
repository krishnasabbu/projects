import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib


# Function to extract audio features
def extract_features(audio_file):
    y, sr = librosa.load(audio_file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)

    # Calculate mean of each feature individually
    mfcc_mean = np.mean(mfcc) if mfcc.size > 0 else 0
    spectral_centroid_mean = np.mean(spectral_centroid) if spectral_centroid.size > 0 else 0
    spectral_bandwidth_mean = np.mean(spectral_bandwidth) if spectral_bandwidth.size > 0 else 0

    # Concatenate the means
    features = np.array([mfcc_mean, spectral_centroid_mean, spectral_bandwidth_mean])
    return features


# Directory containing labeled audio files
data_dir = "D:\\python\\miniconda\\voice\\train"

# Initialize lists to store features and labels
X = []
y = []

# Iterate over labeled audio files
for label in os.listdir(data_dir):
    label_dir = os.path.join(data_dir, label)
    for audio_file in os.listdir(label_dir):
        audio_file_path = os.path.join(label_dir, audio_file)
        try:
            features = extract_features(audio_file_path)
            if features is not None:
                X.append(features)
                y.append(label)
        except Exception as e:
            print(f"Error processing {audio_file_path}: {e}")

# Convert lists to numpy arrays
X = np.array(X)
y = np.array(y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define pipeline with feature scaling and random forest classifier
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])

# Define hyperparameters grid for grid search
param_grid = {
    'classifier__n_estimators': [100, 200, 300],  # Number of trees in the forest
    'classifier__max_depth': [None, 10, 20, 30],  # Maximum depth of the tree
    'classifier__min_samples_split': [2, 5, 10],  # Minimum number of samples required to split a node
    'classifier__min_samples_leaf': [1, 2, 4],    # Minimum number of samples required at each leaf node
    'classifier__bootstrap': [True, False]        # Whether bootstrap samples are used when building trees
}

# Initialize grid search with 5-fold cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)

# Perform grid search on the training data
grid_search.fit(X_train, y_train)

# Print the best hyperparameters found by grid search
print("Best Hyperparameters:")
print(grid_search.best_params_)

# Evaluate the best model on the test data
accuracy = grid_search.best_estimator_.score(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# Save the best model for future use
model_filename = "music_classification_model.joblib"
joblib.dump(grid_search.best_estimator_, model_filename)
print(f"Model saved as {model_filename}")
