# model_utils.py
import os
import numpy as np
from tensorflow.keras.models import load_model
from skimage.feature import hog, local_binary_pattern
import cv2

# Handcrafted feature settings
LBP_P = 8
LBP_R = 1
HOG_PIXELS_PER_CELL = (8, 8)    # smaller cells are okay for 64x64
HOG_CELLS_PER_BLOCK = (2, 2)

def load_deep_model(path='models/BrainTumor10Epochs.h5'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Deep model not found at {path}.")
    model = load_model(path, compile=False)
    # model.input_shape is (None, H, W, C)
    input_shape = model.input_shape
    # Ensure channels-last
    if len(input_shape) == 4:
        target_h = int(input_shape[1])
        target_w = int(input_shape[2])
        target_c = int(input_shape[3])
    else:
        # sensible fallback
        target_h, target_w, target_c = 64, 64, 3
    return model, (target_h, target_w, target_c)

def preprocess_for_deep(img, model_expected_shape):
    """
    img: BGR image from cv2.imread
    model_expected_shape: (H, W, C)
    returns: array shape (1, H, W, C) scaled to [0,1]
    """
    target_h, target_w, target_c = model_expected_shape

    # If image has alpha channel drop it
    if img is None:
        raise ValueError("Input image is None")

    if img.ndim == 3 and img.shape[2] == 4:
        img = img[..., :3]

    # Convert BGR->RGB for color models
    if target_c == 3:
        if img.ndim == 2:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(img_rgb, (target_w, target_h))
        arr = resized.astype('float32') / 255.0
    else:
        # single-channel expected
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        resized = cv2.resize(gray, (target_w, target_h))
        arr = resized.astype('float32') / 255.0
        arr = np.expand_dims(arr, axis=-1)

    return np.expand_dims(arr, axis=0)  # (1,H,W,C)

def extract_handcrafted_features(img, resize_shape=(64,64)):
    """
    HOG + LBP + simple stats. Default resize set to 64x64 for compatibility.
    """
    if img is None:
        raise ValueError("Input image is None")
    if img.ndim == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    gray = cv2.resize(gray, resize_shape)

    hog_feat = hog(gray,
                   pixels_per_cell=HOG_PIXELS_PER_CELL,
                   cells_per_block=HOG_CELLS_PER_BLOCK,
                   feature_vector=True,
                   block_norm='L2-Hys')

    lbp = local_binary_pattern(gray, P=LBP_P, R=LBP_R, method="uniform")
    (lbp_hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, LBP_P + 3),
                                 range=(0, LBP_P + 2))
    lbp_hist = lbp_hist.astype("float")
    lbp_hist /= (lbp_hist.sum() + 1e-7)

    mean = np.mean(gray)
    std = np.std(gray)
    mn = np.min(gray)
    mx = np.max(gray)

    features = np.concatenate([hog_feat, lbp_hist, [mean, std, mn, mx]])
    return features
