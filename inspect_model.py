# inspect_model.py
from tensorflow.keras.models import load_model

m = load_model('models/BrainTumor10Epochs.h5', compile=False)
print("Model input_shape:", m.input_shape)   # usually (None, H, W, C) or (None, C, H, W)
print("Model output_shape:", m.output_shape)
print("\n--- Model summary ---")
m.summary()
