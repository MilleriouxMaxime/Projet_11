from datetime import datetime, timedelta


def test_points_update_after_booking(client, mock_clubs, mock_competitions):
    """Test that club points are updated after booking places"""
    # Login with a club that has points
    club = next(club for club in mock_clubs if int(club["points"]) > 0)
    initial_points = int(club["points"])

    # Find a future competition
    future_competition = next(
        comp
        for comp in mock_competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    )

    # Book 2 places
    places_to_book = 2
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": future_competition["name"],
            "club": club["name"],
            "places": places_to_book,
        },
        follow_redirects=True,
    )

    # Check that points were deducted
    assert response.status_code == 200
    assert (
        f"Points available: {initial_points - places_to_book}" in response.data.decode()
    )


def test_cannot_book_more_than_points(client, mock_clubs, mock_competitions):
    """Test that a club cannot book more places than they have points"""
    # Login with a club that has points
    club = next(club for club in mock_clubs if int(club["points"]) > 0)
    initial_points = int(club["points"])

    # Find a future competition
    future_competition = next(
        comp
        for comp in mock_competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    )

    # Try to book more places than available points
    places_to_book = initial_points + 1
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": future_competition["name"],
            "club": club["name"],
            "places": places_to_book,
        },
        follow_redirects=True,
    )

    # Check that points were not deducted
    assert response.status_code == 200
    assert f"Points available: {initial_points}" in response.data.decode()
    assert "Cannot book more places than available points" in response.data.decode()


def test_cannot_book_more_than_available_places(client, mock_clubs, mock_competitions):
    """Test that a club cannot book more places than available in the competition"""
    # Login with a club that has enough points
    club = next(club for club in mock_clubs if int(club["points"]) > 0)
    initial_points = int(club["points"])

    # Find a Fall Classic competition that has 6 places
    competition = next(
        comp for comp in mock_competitions if comp["name"] == "Fall Classic"
    )

    # Try to book more places than available in the competition
    places_to_book = int(competition["numberOfPlaces"]) + 1
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": places_to_book,
        },
        follow_redirects=True,
    )

    # Check that points were not deducted
    assert response.status_code == 200
    assert f"Points available: {initial_points}" in response.data.decode()
    print(response.data.decode())
    assert "Not enough places available in the competition" in response.data.decode()
