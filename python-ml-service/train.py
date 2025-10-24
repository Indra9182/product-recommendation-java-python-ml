import os, json
import numpy as np

MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

def generate_synthetic_interactions(num_users=50, num_items=60, density=0.08, seed=42):
    rng = np.random.default_rng(seed)
    mat = (rng.random((num_users, num_items)) < density).astype(float)
    # add some popularity signal
    pop = rng.random(num_items) * 0.5
    mat += pop
    mat = (mat > 0.6).astype(float)  # binarize interactions
    return mat

def train_model():
    user_item = generate_synthetic_interactions()
    # compute item-item cosine sim using normalized columns
    norms = (np.linalg.norm(user_item, axis=0, keepdims=True) + 1e-9)
    normalized = user_item / norms
    item_sim = normalized.T @ normalized

    num_users, num_items = user_item.shape
    user_index = {str(uid): uid for uid in range(num_users)}
    item_index = {str(iid): iid for iid in range(num_items)}

    np.save(os.path.join(MODELS_DIR, "user_item.npy"), user_item)
    np.save(os.path.join(MODELS_DIR, "item_sim.npy"), item_sim)
    with open(os.path.join(MODELS_DIR, "user_index.json"), "w") as f:
        json.dump(user_index, f)
    with open(os.path.join(MODELS_DIR, "item_index.json"), "w") as f:
        json.dump(item_index, f)
    print("✅ Trained CF model. Users:", num_users, "Items:", num_items)

if __name__ == "__main__":
    train_model()
