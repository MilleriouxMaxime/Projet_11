import pytest
from flask import Flask
from server import app, loadClubs

@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    })
    with app.test_client() as client:
        yield client

@pytest.fixture
def clubs():
    return loadClubs()

def test_complete_login_flow(client, clubs):
    """Test the complete login flow from index to welcome page"""
    # Start at index page
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal' in response.data
    
    # Login with valid email
    response = client.post('/showSummary', data={'email': clubs[0]['email']}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data
    
    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal' in response.data 