from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.dicitionary import create_random_dictionary


def test_create_word(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    dictionary = create_random_dictionary(db, owner_id=current_user["id"])

    print("dictionary", dictionary)

    data = {"word_rus": "word_rus_test", "word_eng": "word_eng_test", "dictionary_id": dictionary.id}
    response = client.post(
        f"{settings.API_V1_STR}/words/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["word_rus"] == data["word_rus"]
    assert content["word_eng"] == data["word_eng"]
    assert "id" in content