from fastapi import FastAPI, HTTPException
from schemas.passenger import Passenger
from pydantic import BaseModel
import pandas as pd
import joblib


model = joblib.load('./models/model.pkl')

app = FastAPI()


@app.post("/predict")
def predict(passengers: list[Passenger]):
    # Convert input data to DataFrame
    data = pd.DataFrame([p.dict() for p in passengers])

    predictions = model.predict(data)

    return {"predictions": predictions.tolist()}
