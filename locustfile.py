from locust import HttpUser, task, between

class GUDLFTUser(HttpUser):
    host = "http://localhost:5000"  # Ajout de l'hôte de base
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Initialize user session"""
        # First get the index page
        self.client.get("/")
        # Then login with a test club
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
    
    @task(3)
    def view_competitions(self):
        """View competitions page"""
        # First get the index page
        self.client.get("/")
        # Then login to view competitions
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
    
    @task(2)
    def book_places(self):
        """Attempt to book places"""
        # First get the index page
        self.client.get("/")
        # Login
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        # Get a competition to book
        response = self.client.get("/book/Spring%20Festival/Simply%20Lift")
        if response.status_code == 200:
            # Try to book 2 places
            self.client.post("/purchasePlaces", data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "2"
            })
    
    @task(1)
    def view_points(self):
        """View points board"""
        self.client.get("/points") 