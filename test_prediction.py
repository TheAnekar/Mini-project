import pickle
import numpy as np

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Test inputs
all_nines = np.array([[9]*10])
all_zeros = np.array([[0]*10])
medium_case = np.array([[4, 5, 3, 6, 3, 2, 5, 5, 4, 3]])

print("All 9s prediction:", model.predict(all_nines))
print("All 0s prediction:", model.predict(all_zeros))
print("Medium case prediction:", model.predict(medium_case))
