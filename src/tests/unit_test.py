import json

from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)

def authorization():
    token = client.post("/login", data={'username': 'qwer@mail.ru',
                                        'password': 'qwer'})
    return json.loads(token.content.decode('utf-8'))

def test_list_image():
    access_token = authorization()
    response = client.get("/image", headers={"Authorization": f"Bearer "
                                                              f"{access_token['access_token']}"})
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_add_image():
    access_token = authorization()
    files = {'file': open('src/tests/test.jpg', 'rb')}
    response = client.post("/image", files=files, data = {'text':'value'},
                           headers={"Authorization": f"Bearer {access_token['access_token']}"})
    assert response.status_code == 200
    assert {"message": response.json()["message"]}== {"message":
                                                          "Photo saved successfully"}

def test_err_add_image():
    access_token = authorization()
    files = {'file': open('src/tests/test1.txt', 'rb')}
    response = client.post("/image", files=files, data = {'text':'value'},
                           headers={"Authorization": f"Bearer "
                                                     f"{access_token['access_token']}"})
    assert response.status_code == 400
    assert response.json() == {"message":
                                   "Photo saved error. Incorrect image format"}

def test_show_image_noauthorization():
    response = client.get("/image/5")
    assert response.status_code == 401

def test_err_show_image():
    access_token = authorization()
    response = client.get("/image/1000", headers={"Authorization":
                                                      f"Bearer {access_token['access_token']}"})
    assert response.status_code == 400
    assert response.json() == {"message":
                                   "Incorrect Data. This id is not in the database"}

def test_err_show_image_nonumber():
    access_token = authorization()
    response = client.get("/image/e", headers={"Authorization":
                                                   f"Bearer {access_token['access_token']}"})
    assert response.status_code == 422

def test_err_delete_image():
    access_token = authorization()
    response = client.delete("/image/r", headers={"Authorization":
                                                      f"Bearer {access_token['access_token']}"})
    assert response.status_code == 422

def test_err_update_image_nonumber():
    access_token = authorization()
    files = {'file': open('src/tests/test.jpg', 'rb')}
    response = client.put("/image/r", files=files, data={'text': 'value'},
                          headers={"Authorization": f"Bearer "
                                                    f"{access_token['access_token']}"})
    assert response.status_code == 422

def test_err_update_image_incorect_number():
    access_token = authorization()

    response = client.put("/image/6", params={'id': 9, 'text': 'test'},
                          headers={"Authorization": f"Bearer "
                                                    f"{access_token['access_token']}"})
    assert response.status_code == 400
    assert response.json() == {"message": "Incorrect Data. Error id"}