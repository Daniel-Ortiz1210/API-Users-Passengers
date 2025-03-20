import pytest
from fastapi.testclient import TestClient
from faker import Faker

from main import app


def test_passenger_endpoints():
    client = TestClient(app)
    faker = Faker()

    request_payload = {
        'name': 'John',
        'email': faker.email(),
        'age': 25,
        'password': 'Abchyxcfat!*90Ax'
    }   

    response = client.post('/api/v1/passengers/', json={
        **request_payload,
        'password': '123'
        }
    )

    assert response.status_code == 400

    response = client.post('/api/v1/passengers/', json={
        **request_payload,
        'email': 'test_email@mail'
        }
    )

    assert response.status_code == 400

    response = client.post('/api/v1/passengers/', json=request_payload)

    assert response.status_code == 201
    assert response.json()['success'] == True

    passenger_id = response.json()['data']['passenger']['id']
    passenger_email = response.json()['data']['passenger']['email']
    token = response.json()['data']['token']

    
    # Test get passenger by id
    response = client.get('/api/v1/passengers/6456482840', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 403
    assert response.json()['message'] == 'passenger logged in does not have access to this resource'

    response = client.get(f'/api/v1/passengers/{passenger_id}', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 200
    assert response.json()['success'] == True
    assert response.json()['data']['id'] == passenger_id

    # Test update passenger

    updated_payload = {
        'name': 'Jane',
        'email': faker.email(),
        'password': 'New3241!*',
        'age': 55
        }
    response = client.put(f'/api/v1/passengers/1000000', json=updated_payload,
        headers={
            'Authorization': f"Bearer {token}"
        })

    assert response.status_code == 403
    assert response.json()['message'] == 'passenger logged in does not have access to this resource'

    response = client.put(f'/api/v1/passengers/{passenger_id}', json={**updated_payload, 'email': 'vtrcavue'}, headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 400

    response = client.put(f'/api/v1/passengers/{passenger_id}', json=updated_payload, headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 201
    assert response.json()['success'] == True
    assert response.json()['data']['passenger']['email'] == updated_payload['email']

    token = response.json()['data']['token']

    # Test delete passenger
    response = client.delete('/api/v1/passengers/7365448204', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 403

    response = client.delete(f'/api/v1/passengers/{passenger_id}', headers={
        'Authorization': f"Bearer {token}"
    })

    assert response.status_code == 204
    