from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_create_dictionary(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    data = {"dictionary_name": "dictionary_name_test", "owner_id": current_user["id"]}
    response = client.post(
        f"{settings.API_V1_STR}/dictionaries/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["dictionary_name"] == data["dictionary_name"]
    assert "id" in content