from pydantic import BaseModel

class Passenger(BaseModel):
    Age: float
    Sex: str
    Embarked: str
