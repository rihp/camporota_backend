import json

import pytest
from flask_jwt_extended import create_access_token

import api.server.start as app
from tests.integration import app, mocked_db
import api.utils.algolia as test

mock_property =  {
    "title": "Top floor",
    "description": "Amazing stuff",
    "kind": "floor",
    "price": 45,
    "state": "Maracaibo",
    "sale": True,
    "property_id": 'ca1ea042-e5db-4746-b453-4a39b832b7fe',
    "rooms": 1,
    "bathrooms": 1,
    "address": "Calle Adrada de Haza",
    "square_meters": 100,
    "heating": True,
    "community_fees": 100,
    "orientation": "Ni idea",
    "furnished": True,
    "equipped_kitchen": False,
    "floor_number": "Bajo",
    "common_zones": "Muchas",
    "pets": True,
    "contract_time": "1 ano",
    "bond": "2 meses"
}

def test_create_property(mocked_db, mocker):
    json_body = json.dumps(mock_property)
    access_token = create_access_token('test@gmail.com')
    mocker.patch('api.models.property.create_or_update_property', return_value=True)
    mocker.patch('api.models.property.upload_images', return_value=[{'url':'first/path.jpg'}, {'url':'second/path.jpg'}])
    request = mocked_db.app.test_client().post(
        'api/properties',
        data=json_body,
        content_type='application/json',
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert True == json.loads(request.data)['success']

def test_search_property(mocked_db, mocker):
    mock_property['images'] = []
    value = dict(hits=[mock_property])
    value['hits'][0]['objectID'] = 'ca1ea042-e5db-4746-b453-4a39b832b7fe'
    mocker.patch('api.models.property.search_property', return_value=value)
    request = mocked_db.app.test_client().get('/api/properties')
    del value['hits'][0]['objectID']
    assert json.loads(request.data)[0] == mock_property

# def test_update_property(mocked_db, mocker):
#     json_body = json.dumps(dict(property_id='ca1ea042-e5db-4746-b453-4a39b832b7fe', title="new title"))
#     access_token = create_access_token('test@gmail.com')
#     mocker.patch('api.models.property.create_or_update_property', return_value=True)
#     request = mocked_db.app.test_client().put(
#         'api/properties',
#         data=json_body,
#         content_type='application/json',
#         headers = {
#             "Authorization": f"Bearer {access_token}"
#         }
#     )
#     print(request.data)
#     assert True == json.loads(request.data)['success']


def test_delete_property(mocked_db, mocker):
    mocker.patch('api.models.property.delete_property', return_value=True)
    access_token = create_access_token('test@gmail.cmom')
    request = mocked_db.app.test_client().delete(
        'api/properties?property_id=ca1ea042-e5db-4746-b453-4a39b832b7fe',
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert True == json.loads(request.data)['success']
