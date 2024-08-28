from fastapi import FastAPI, HTTPException
from .schemas.passenger import Passenger
from pydantic import BaseModel
import pandas as pd
import joblib
from .functions.build_model import Model

model_builder = Model("model")
model = joblib.load('./models/model.pkl')

app = FastAPI()

@app.post("/predict")
def predict(passengers: list[Passenger]):

    data = pd.DataFrame([p.dict() for p in passengers])

    predictions = model.predict(data)

    return {"predictions": predictions.tolist()}

@app.put("/run-pipeline")
def run_pipeline():
    global model  
    model_builder.setup()
    model_builder.build()
    model_builder.dump(directory_to_save_model='./models/')
    model = joblib.load('./models/model.pkl')
    return {"msg": "Completed pipeline."}
