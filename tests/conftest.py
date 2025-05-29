import pytest
from datetime import datetime, timedelta
from server import app

@pytest.fixture
def mock_clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "0"
        }
    ]

@pytest.fixture
def mock_competitions():
    now = datetime.now()
    return [
        {
            "name": "Spring Festival",
            "date": (now + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": (now + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "6"
        },
        {
            "name": "Past Competition",
            "date": (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "0"
        }
    ]

@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    })
    with app.test_client() as client:
        yield client

# Monkey patch the loadClubs and loadCompetitions functions
@pytest.fixture(autouse=True)
def mock_load_functions(monkeypatch, mock_clubs, mock_competitions):
    def mock_load_clubs():
        return mock_clubs
    
    def mock_load_competitions():
        return mock_competitions
    
    monkeypatch.setattr('server.loadClubs', mock_load_clubs)
    monkeypatch.setattr('server.loadCompetitions', mock_load_competitions)
    monkeypatch.setattr('server.clubs', mock_clubs)
    monkeypatch.setattr('server.competitions', mock_competitions) 