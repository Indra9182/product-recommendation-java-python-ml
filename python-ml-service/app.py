from flask import Flask, request, jsonify
import os, json
import numpy as np
import pandas as pd

MODELS_DIR = "models"
USER_INDEX_PATH = os.path.join(MODELS_DIR, "user_index.json")
ITEM_INDEX_PATH = os.path.join(MODELS_DIR, "item_index.json")
ITEM_SIM_PATH = os.path.join(MODELS_DIR, "item_sim.npy")
INTERACTIONS_PATH = os.path.join(MODELS_DIR, "user_item.npy")

app = Flask(__name__)

def ensure_trained():
    if not (os.path.exists(ITEM_SIM_PATH) and os.path.exists(USER_INDEX_PATH) and os.path.exists(ITEM_INDEX_PATH) and os.path.exists(INTERACTIONS_PATH)):
        from train import train_model
        train_model()

def load_artifacts():
    ensure_trained()
    with open(USER_INDEX_PATH) as f:
        user_index = json.load(f)
    with open(ITEM_INDEX_PATH) as f:
        item_index = json.load(f)
    item_sim = np.load(ITEM_SIM_PATH)
    user_item = np.load(INTERACTIONS_PATH)
    return user_index, item_index, item_sim, user_item

def recommend_for_user(user_id: int, k: int = 5):
    user_index, item_index, item_sim, user_item = load_artifacts()
    uid_str = str(user_id)
    if uid_str not in user_index:
        return []
    uidx = user_index[uid_str]
    user_vector = user_item[uidx]  # purchases/ratings row

    # Score items by similarity to items the user interacted with
    scores = user_vector @ item_sim  # (1 x items) * (items x items)
    # Avoid recommending items already consumed
    scores = np.where(user_vector > 0, -np.inf, scores)
    top_indices = np.argsort(-scores)[:k]
    # invert item_index dict
    inv_item_index = {v: int(k) for k, v in item_index.items()}
    return [{"item_id": int(inv_item_index[i]), "score": float(scores[i])} for i in top_indices if np.isfinite(scores[i])]

@app.route("/recommend", methods=["GET"])
def recommend():
    try:
        user_id = int(request.args.get("user_id"))
        k = int(request.args.get("k", 5))
        recs = recommend_for_user(user_id, k)
        return jsonify({"user_id": user_id, "recommendations": recs})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/train", methods=["POST"])
def train():
    try:
        from train import train_model
        train_model()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "up"})

if __name__ == "__main__":
    ensure_trained()
    app.run(host="0.0.0.0", port=5001)
