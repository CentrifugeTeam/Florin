import pytest
from sqlmodel import select

from src.db import UserPlant


@pytest.fixture()
async def user(client):
    response = await client.post('/auth/signup', data={'username': 'dima', 'email': 'dima@mail.ru',
                                                       'password': 'password'})
    assert response.status_code == 200

    return response.json()


@pytest.fixture()
async def token(client, user):
    response = await client.post('/auth/login',  data={"username": 'dima@mail.ru', 'password': 'password'})
    assert response.status_code == 200
    return response.json()['access_token']


async def test_get_plants(client, session,
                          user, token):
    response = await client.get('/plants', params={'limit': 1})
    assert response.status_code == 200
    plant = response.json()[0]
    response = await client.post(f'/plants/{plant['id']}/attach', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    stmt = select(UserPlant).where(UserPlant.user_id == user['id']).where(
        UserPlant.plant_id == plant['id'])
    user_plant = (await session.exec(stmt)).one()
    assert user_plant
