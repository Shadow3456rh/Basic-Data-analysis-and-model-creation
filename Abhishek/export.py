import joblib

def model_download(model, scaler):
    joblib.dump(model, "Model.pkl")
    joblib.dump(scaler, "Scaler.pkl")
