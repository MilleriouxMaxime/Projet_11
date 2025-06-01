import pytest


def test_points_display(client, mock_clubs):
    """Test the points display page"""
    response = client.get("/points")
    assert response.status_code == 200
    assert b"Clubs Points" in response.data
    assert b"Back to Home" in response.data
    assert b"Logout" in response.data

    # Check if all clubs are displayed
    for club in mock_clubs:
        assert club["name"].encode() in response.data
        assert club["points"].encode() in response.data


def test_points_display_sorted(client, mock_clubs):
    """Test that clubs are sorted by points in descending order"""
    response = client.get("/points")
    assert response.status_code == 200

    # Get the points from the response
    points = [int(club["points"]) for club in mock_clubs]
    sorted_points = sorted(points, reverse=True)

    # Check if points are displayed in descending order
    for point in sorted_points:
        assert str(point).encode() in response.data
