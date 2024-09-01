import joblib

def load_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load the model: {e}")
