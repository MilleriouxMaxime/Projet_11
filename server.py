import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        email = request.form.get("email")
        if not email:
            flash("Please enter your email")
            return redirect(url_for("index"))

        club = next((club for club in clubs if club["email"] == email), None)
        if not club:
            flash("Email not found")
            return redirect(url_for("index"))

        return render_template("welcome.html", club=club, competitions=competitions)
    except Exception as e:
        flash("An error occurred. Please try again.")
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        # Find club and competition
        foundClub = next((c for c in clubs if c["name"] == club), None)
        foundCompetition = next(
            (c for c in competitions if c["name"] == competition), None
        )

        if not foundClub:
            flash("Club not found")
            return redirect(url_for("index"))

        if not foundCompetition:
            flash("Competition not found")
            return redirect(url_for("index"))

        # Check if competition is in the past
        competition_date = datetime.strptime(
            foundCompetition["date"], "%Y-%m-%d %H:%M:%S"
        )
        if competition_date < datetime.now():
            flash("Cannot book places for past competitions")
            return render_template(
                "welcome.html", club=foundClub, competitions=competitions
            )

        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    except Exception as e:
        flash("An error occurred. Please try again.")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])

    # Check if club has enough points
    if int(club["points"]) < placesRequired:
        flash("Cannot book more places than available points")
        return render_template("welcome.html", club=club, competitions=competitions)

    # Check if trying to book more than 12 places
    if placesRequired > 12:
        flash("Cannot book more than 12 places per competition")
        return render_template("welcome.html", club=club, competitions=competitions)

    # Check if competition has enough places
    if int(competition["numberOfPlaces"]) < placesRequired:
        flash("Not enough places available in the competition")
        return render_template("welcome.html", club=club, competitions=competitions)

    # Update competition places
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired

    # Update club points
    club["points"] = str(int(club["points"]) - placesRequired)

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
