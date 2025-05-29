from datetime import datetime, timedelta


def test_complete_booking_flow(client, mock_clubs, mock_competitions):
    """Test the complete booking flow from login to booking page"""
    # Start at index page
    response = client.get("/")
    assert response.status_code == 200

    # Login with a club that has points
    club = next(club for club in mock_clubs if int(club["points"]) > 0)
    response = client.post(
        "/showSummary", data={"email": club["email"]}, follow_redirects=True
    )
    assert response.status_code == 200
    assert f"Points available: {club['points']}" in response.data.decode()

    # Find a future competition
    future_competition = next(
        comp
        for comp in mock_competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    )

    # Try to book the competition
    response = client.get(
        f'/book/{future_competition["name"]}/{club["name"]}', follow_redirects=True
    )
    assert response.status_code == 200
    assert b"How many places" in response.data
    assert future_competition["name"].encode() in response.data
    assert str(future_competition["numberOfPlaces"]).encode() in response.data
