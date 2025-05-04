import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier  # Import Random Forest
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score  # For cross-validation
import seaborn as sns
import matplotlib.pyplot as plt

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

# Train Random Forest model
rf_model = RandomForestClassifier(
    n_estimators=100,  # Number of trees in the forest
    max_depth=None,    # Let trees grow to full depth (can tune this)
    min_samples_split=2,  # Minimum samples required to split a node
    min_samples_leaf=1,   # Minimum samples required at each leaf node
    max_features='sqrt',  # Number of features to consider at each split
    random_state=42,      # For reproducibility
    n_jobs=-1            # Use all available cores
)

rf_model.fit(X_train, y_train)

# Predict
y_pred = rf_model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Cross-validation (optional but recommended)
cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5)
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV accuracy: {np.mean(cv_scores)*100:.2f}%")

# Classification Report
print("\nClassification Report:")
print(classification_report(
    y_test, y_pred,
    target_names=['sitting_still', 'sitting_nodding_up_and_down',
                  'sitting_nodding_side_to_side', 'sitting_nodding_diagonal']
))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt='g',
            xticklabels=['still', 'up_down', 'side_to_side', 'diagonal'],
            yticklabels=['still', 'up_down', 'side_to_side', 'diagonal'])
plt.title('Random Forest Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# Feature Importance
feature_names = [
    'accel_x_mean', 'accel_x_std',
    'accel_y_mean', 'accel_y_std',
    'accel_z_mean', 'accel_z_std',
    'gyro_x_mean', 'gyro_x_std',
    'gyro_y_mean', 'gyro_y_std',
    'gyro_z_mean', 'gyro_z_std'
]

importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X_train.shape[1]), importances[indices], align="center")
plt.xticks(range(X_train.shape[1]), [feature_names[i] for i in indices], rotation=90)
plt.xlim([-1, X_train.shape[1]])
plt.tight_layout()
plt.show()