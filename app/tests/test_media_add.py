from os.path import abspath, dirname, join

from fastapi.testclient import TestClient

from ..main import appFastAPI as app

abs_path_file = dirname(abspath(__file__))
abs_path_file = join(abs_path_file, "app", "medias", "test.png")
file_name = "test.png"


def test_add_media():
    with TestClient(app) as client:
        test_file = abs_path_file
        files = {"file": (file_name, open(test_file, "rb"))}
        response = client.post(url="/api/medias", files=files, headers={"api-key": "1"})
        assert response.status_code == 201
        assert response.json()["result"] == True
        assert response.json()["media_id"] == 3


def test_get_media():
    with TestClient(app) as client:
        response = client.get(url="/api/medias/Poker-Playing-Cards-tall-l.jpg")
        assert response.status_code == 200
