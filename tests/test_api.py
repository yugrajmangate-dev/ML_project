import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'CACHE_TYPE': 'SimpleCache',
    })
    return app


def test_health_endpoint(app):
    client = app.test_client()
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'ok'


def test_recommend_endpoints(app):
    client = app.test_client()

    # Content endpoint should return JSON error for missing q
    r = client.get('/api/recommend/content')
    assert r.status_code == 400

    # Collab endpoint requires customer_id
    r2 = client.get('/api/recommend/collab')
    assert r2.status_code == 400
