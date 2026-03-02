# train_traditional.py
import os
import glob
import joblib
import numpy as np
from tqdm import tqdm
from model_utils import extract_handcrafted_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_dataset_folder(data_dir):
    # Expecting structure: data/yes/*.jpg (tumor), data/no/*.jpg (no tumor)
    X = []
    y = []
    for label_name, label in [('no',0), ('yes',1)]:
        folder = os.path.join(data_dir, label_name)
        if not os.path.exists(folder):
            print("Missing folder:", folder)
            continue
        for img_path in glob.glob(os.path.join(folder, '*.*')):
            import cv2
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            feat = extract_handcrafted_features(img)
            X.append(feat)
            y.append(label)
    return np.array(X), np.array(y)

if __name__ == "__main__":
    data_dir = "data/brain_tumor_dataset"  # set to your downloaded dataset folder
    X, y = load_dataset_folder(data_dir)
    print("Features shape:", X.shape, "Labels shape:", y.shape)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))

    os.makedirs('models', exist_ok=True)
    joblib.dump(clf, 'models/rf_model.joblib')
    print("Saved rf model to models/rf_model.joblib")
