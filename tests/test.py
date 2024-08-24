import pytest
import httpx

@pytest.mark.asyncio
async def test_read_item():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "name": "The Answer"}

@pytest.mark.asyncio
async def test_read_item_not_found():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
