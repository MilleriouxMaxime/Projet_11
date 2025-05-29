import pytest
from flask import Flask
from server import app, loadClubs



def test_login_with_valid_email(client, mock_clubs):
    """Test login with a valid email"""
    response = client.post('/showSummary', data={'email': mock_clubs[0]['email']}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_login_with_invalid_email(client):
    """Test login with an invalid email"""
    response = client.post('/showSummary', data={'email': 'invalid@email.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email not found' in response.data

def test_login_with_empty_email(client):
    """Test login with an empty email"""
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Please enter your email' in response.data 