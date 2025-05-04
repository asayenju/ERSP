import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pickle


def load_and_extract_features(file_path):
    try:
        data = np.loadtxt(file_path, delimiter=',', skiprows=1)

        accel_x, accel_y, accel_z = data[:, 0], data[:, 1], data[:, 2]
        gyro_x, gyro_y, gyro_z = data[:, 3], data[:, 4], data[:, 5]

        features = [
            np.mean(accel_x), np.std(accel_x),
            np.mean(accel_y), np.std(accel_y),
            np.mean(accel_z), np.std(accel_z),
            np.mean(gyro_x), np.std(gyro_x),
            np.mean(gyro_y), np.std(gyro_y),
            np.mean(gyro_z), np.std(gyro_z)
        ]
        return features
    except Exception as e:
        print(f"Skipping file {file_path}: {e}")
        return None


def prepare_dataset(data_dir):
    X_train, X_test, y_train, y_test = [], [], [], []

    gesture_folders = {
        'sitting_still': 0,
        'sitting_nodding_up_down': 1,
        'sitting_nodding_side_to_side': 2,
        'sitting_nodding_diagonal': 3
    }

    for folder_name, label in gesture_folders.items():
        folder_path = os.path.join(data_dir, folder_name)

        if not os.path.exists(folder_path):
            print(f"Warning: Folder {folder_path} does not exist. Skipping...")
            continue

        files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        files = sorted(files)[:100]  # make sure it's always 100 files

        features_list = []
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            features = load_and_extract_features(file_path)
            if features is not None:
                features_list.append(features)

        # split into train and test within the class
        X_class_train, X_class_test = features_list[:70], features_list[70:]
        y_class_train, y_class_test = [label]*70, [label]*30

        X_train.extend(X_class_train)
        X_test.extend(X_class_test)
        y_train.extend(y_class_train)
        y_test.extend(y_class_test)

    return np.array(X_train), np.array(X_test), np.array(y_train), np.array(y_test)

# ========================= #
#      START OF SCRIPT      #
# ========================= #

# path to 'ersp' folder
data_directory = r"C:\Users\ashwi\OneDrive\Documents\UMass Amherst\ERSP"

# THIS returns X_train, X_test, y_train, y_test separately
X_train, X_test, y_train, y_test = prepare_dataset(data_directory)

print(f"Train set -> Features: {X_train.shape}, Labels: {y_train.shape}")
print(f"Test set -> Features: {X_test.shape}, Labels: {y_test.shape}")
# Check class distribution in train and test sets
print("\n=== Class Distribution ===")
print("Training set:")
print(np.unique(y_train, return_counts=True))
print("\nTest set:")
print(np.unique(y_test, return_counts=True))

# Visualize distribution
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.hist(y_train, bins=4, edgecolor='black')
plt.title("Training Set Class Distribution")
plt.subplot(1, 2, 2)
plt.hist(y_test, bins=4, edgecolor='black')
plt.title("Test Set Class Distribution")
plt.show()

# Check basic statistics of your features
print("\n=== Feature Statistics ===")
print("Feature means:")
print(np.mean(X_train, axis=0))
print("\nFeature standard deviations:")
print(np.std(X_train, axis=0))

# Check for NaN/infinite values
print("\nNaN values in training set:", np.isnan(X_train).sum())
print("Infinite values in training set:", np.isinf(X_train).sum())

from sklearn.model_selection import learning_curve


# Train SVM model
model = SVC(kernel='rbf')
model.fit(X_train, y_train)
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
# Predict
y_pred = model.predict(X_test)


# Plot learning curves
train_sizes, train_scores, test_scores = learning_curve(
    model, X_train, y_train, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 5))

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Training score')
plt.plot(train_sizes, np.mean(test_scores, axis=1), label='Cross-validation score')
plt.xlabel("Training examples")
plt.ylabel("Accuracy")
plt.legend()
plt.title("Learning Curves")
plt.show()

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Classification Report
print("Classification Report:")
print(classification_report(
    y_test, y_pred,
    target_names=['sitting_still', 'sitting_nodding_up_and_down',
                  'sitting_nodding_side_to_side', 'sitting_nodding_diagonal']
))

# Confusion Matrix with larger font
plt.figure(figsize=(10, 8))  # You can adjust the figure size if needed
conf_matrix = confusion_matrix(y_test, y_pred)

# Create the heatmap with larger font settings
ax = sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt='g',
            xticklabels=['sitting_still', 'sitting_nodding_up_and_down',
                         'sitting_nodding_side_to_side', 'sitting_nodding_diagonal'],
            yticklabels=['sitting_still', 'sitting_nodding_up_and_down',
                         'sitting_nodding_side_to_side', 'sitting_nodding_diagonal'],
            annot_kws={"size": 16})  # This controls the annotation font size

# Set larger font sizes for labels and title
ax.set_xlabel('Predicted Label', fontsize=14)
ax.set_ylabel('True Label', fontsize=14)
ax.set_title('Confusion Matrix', fontsize=16)

# Adjust tick label sizes
ax.set_xticklabels(ax.get_xticklabels(), fontsize=20)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)

plt.tight_layout()  # Ensures everything fits properly
plt.show()