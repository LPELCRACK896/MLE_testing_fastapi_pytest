import pytest
import httpx
import logging

# Configurar logging
logging.basicConfig(filename="test_log.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

@pytest.mark.asyncio
async def test_predict():
    logging.info("Starting test_predict")
    
    passengers = [
        {
            "Pclass": 3,
            "Name": "John Doe",
            "Sex": "male",
            "Age": 22,
            "Siblings/Spouses Aboard": 1,
            "Parents/Children Aboard": 0,
            "Fare": 7.25
        },
        {
            "Pclass": 1,
            "Name": "Jane Doe",
            "Sex": "female",
            "Age": 38,
            "Siblings/Spouses Aboard": 1,
            "Parents/Children Aboard": 0,
            "Fare": 71.2833
        }
    ]

    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/predict", json=passengers)
    
    logging.info(f"Request sent, status code: {response.status_code}")
    
    assert response.status_code == 200
    json_response = response.json()
    
    logging.info(f"Response received: {json_response}")
    
    assert "predictions" in json_response
    assert len(json_response["predictions"]) == len(passengers)
    
    logging.info("test_predict passed successfully")
