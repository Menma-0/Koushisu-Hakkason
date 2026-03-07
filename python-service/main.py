from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict():
    # TODO: YOLO推論を別担当が実装予定
    return {"message": "predict endpoint is not yet implemented", "predictions": []}
