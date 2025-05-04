import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier  # Changed from SVC to KNN
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler  # Important for KNN
from sklearn.model_selection import learning_curve
import seaborn as sns
import matplotlib.pyplot as plt
import joblib


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

# Feature scaling - CRUCIAL for KNN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train KNN model
knn_model = KNeighborsClassifier(
    n_neighbors=5,  # Start with 5 neighbors (can be tuned)
    weights='distance',  # Closer neighbors have more influence
    metric='euclidean'  # Distance metric
)
knn_model.fit(X_train_scaled, y_train)

# Predict
y_pred = knn_model.predict(X_test_scaled)

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

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt='g',
            xticklabels=['sitting_still', 'sitting_nodding_up_and_down',
                         'sitting_nodding_side_to_side', 'sitting_nodding_diagonal'],
            yticklabels=['sitting_still', 'sitting_nodding_up_and_down',
                         'sitting_nodding_side_to_side', 'sitting_nodding_diagonal'])
plt.title('KNN Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# Optional: Find optimal k value
accuracies = []
k_values = range(1, 15)
for k in k_values:
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    knn_temp.fit(X_train_scaled, y_train)
    accuracies.append(knn_temp.score(X_test_scaled, y_test))

# Plot learning curves
train_sizes, train_scores, test_scores = learning_curve(
    knn_model, X_train, y_train, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 5))

joblib.dump(knn_model, "knn_model.pk1")
joblib.dump(scaler, "knn_scaler.pkl")  # This is the new line you need to add
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Training score')
plt.plot(train_sizes, np.mean(test_scores, axis=1), label='Cross-validation score')
plt.xlabel("Training examples")
plt.ylabel("Accuracy")
plt.legend()
plt.title("Learning Curves")
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(k_values, accuracies, marker='o')
plt.title('Finding Optimal k Value')
plt.xlabel('Number of Neighbors (k)')
plt.ylabel('Accuracy')
plt.xticks(k_values)
plt.grid()
plt.show()