from datetime import datetime


def test_book_valid_competition(client, mock_clubs, mock_competitions):
    """Test booking a valid competition"""
    club = next(club for club in mock_clubs if int(club["points"]) > 0)

    # Try to book a future competition
    future_competition = next(
        comp
        for comp in mock_competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    )

    response = client.get(
        f'/book/{future_competition["name"]}/{club["name"]}', follow_redirects=True
    )
    assert response.status_code == 200
    assert b"How many places" in response.data


def test_book_past_competition(client, mock_clubs, mock_competitions):
    """Test booking a past competition"""
    club = next(club for club in mock_clubs if int(club["points"]) > 0)

    # Use the past competition from mock data
    past_competition = next(
        comp
        for comp in mock_competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") < datetime.now()
    )

    response = client.get(
        f'/book/{past_competition["name"]}/{club["name"]}', follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Cannot book places for past competitions" in response.data
