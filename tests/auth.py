import pytest
from fastapi.testclient import TestClient
from faker import Faker

from main import app

def test_login():
    client = TestClient(app)
    faker = Faker()

    request_payload = {
        'name': 'John',
        'age': 25,
        'email': faker.email(),
        'password': 'Asdfghjk1'
    }   

    response = client.post('/api/v1/auth/login', json={
        'email': request_payload['email'],
        'password': request_payload['password']
    })
    
    assert response.status_code == 404

    response = client.post('/api/v1/passengers/', json=request_payload)
    
    assert response.status_code == 201
    assert response.json()['success'] == True

    passenger_id = response.json()['data']['passenger']['id']

    response = client.post('/api/v1/auth/login', json={
        'email': request_payload['email'],
        'password': 'Asdfghjk11'
    })

    assert response.status_code == 401
    assert response.json()['message'] == 'Invalid password'

    response = client.post('/api/v1/auth/login', json={
        'email': request_payload['email'],
        'password': request_payload['password']
    })

    assert response.status_code == 200
    assert response.json()['success'] == True
    assert 'token' in response.json()['data']

    response = client.delete(f'/api/v1/passengers/{passenger_id}', headers={
        'Authorization': f'Bearer {response.json()["data"]["token"]}'
    })

    assert response.status_code == 204
