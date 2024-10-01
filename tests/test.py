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
            "Age": 22.0,
            "Sex": "male",
            "Embarked": "S"
        },
        {
            "Age": 38.0,
            "Sex": "female",
            "Embarked": "C"
        }
    ]

    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/predict", json=passengers)
    
    logging.info(f"Request sent, status code: {response.status_code}")
    logging.info(f"Response content: {response.content}")  # Log para revisar el contenido de la respuesta

    assert response.status_code == 200
    json_response = response.json()

    logging.info(f"Response received: {json_response}")
    
    assert "predictions" in json_response
    assert len(json_response["predictions"]) == len(passengers)
    
    logging.info("test_predict passed successfully")
    print('TEST FINALIZADO')
