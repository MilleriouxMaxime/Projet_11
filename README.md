# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called 
    [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.

    ### Running Tests

    The project uses pytest for testing. To run the tests:

    1. Make sure you're in your virtual environment:
       ```bash
       source bin/activate  # On Unix/Mac
       .\Scripts\activate   # On Windows
       ```

    2. Install test dependencies:
       ```bash
       pip install -r requirements.txt
       ```

    3. Run all tests:
       ```bash
       pytest
       ```

    4. Run tests with verbose output:
       ```bash
       pytest -v
       ```

    5. Run specific test files:
       ```bash
       pytest tests/unit_tests/test_login.py
       pytest tests/integration_tests/test_login_flow.py
       ```

6. Running the Flask Application

    To run the Flask application:

    1. Make sure you're in your virtual environment:
       ```bash
       source bin/activate  # On Unix/Mac
       .\Scripts\activate   # On Windows
       ```

    2. Set the Flask environment variable:
       ```bash
       # On Unix/Mac
       export FLASK_APP=server.py
       # On Windows
       set FLASK_APP=server.py
       ```

    3. Run the application:
       ```bash
       flask run
       ```
       or
       ```bash
       python -m flask run
       ```

    4. Access the application at http://127.0.0.1:5000 in your web browser

    Note: For development, you can enable debug mode:
    ```bash
    # On Unix/Mac
    export FLASK_DEBUG=1
    # On Windows
    set FLASK_DEBUG=1
    ```

## Running Tests with Coverage

To run the test suite with coverage reporting:

```bash
# Run all tests with coverage report
pytest --cov=server tests/

# Generate a detailed HTML coverage report
pytest --cov=server --cov-report=html tests/
```

The coverage report will show:
- Percentage of code covered by tests
- Which lines of code are covered/not covered
- Overall project coverage statistics

The HTML report will be generated in the `htmlcov` directory, where you can view a detailed, interactive coverage report in your browser.

## Load Testing with Locust

The project includes load testing capabilities using Locust. This helps simulate multiple users accessing the application simultaneously.

### Running Load Tests

There are two ways to run Locust tests:

#### 1. Using the Web Interface (Recommended for beginners)

1. Make sure you're in your virtual environment and have installed the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask application in one terminal:
   ```bash
   flask run
   ```

3. In another terminal, run Locust:
   ```bash
   locust
   ```

4. Open your browser and go to http://localhost:8089

5. Configure your test:
   - Number of users to simulate
   - Spawn rate (users per second)
   - Host (http://localhost:5000)

6. Click "Start swarming" to begin the load test

#### 2. Using Command Line (Advanced)

You can also run Locust directly from the command line with predefined parameters:

```bash
# Run with 10 users, spawn rate of 1 user/second
locust --users 10 --spawn-rate 1 --host http://localhost:5000

# Run in headless mode (no web interface)
locust --users 10 --spawn-rate 1 --host http://localhost:5000 --headless

# Run for a specific duration (e.g., 1 minute)
locust --users 10 --spawn-rate 1 --host http://localhost:5000 --headless --run-time 1m

# Run with a specific test file
locust -f locustfile.py --users 10 --spawn-rate 1 --host http://localhost:5000
```

Common command line options:
- `--users`: Number of users to simulate
- `--spawn-rate`: Users spawned per second
- `--host`: Target host URL
- `--headless`: Run without web interface
- `--run-time`: Duration of the test (e.g., 1m, 1h)
- `-f`: Specify the locustfile to use

### Test Scenarios

The load test simulates the following user behaviors:
- Viewing competitions (weight: 3)
- Booking places (weight: 2)
- Viewing points board (weight: 1)

The weights determine how frequently each action is performed relative to others.

### Understanding Results

Locust provides real-time metrics including:
- Requests per second
- Response times
- Number of users
- Failure rates

You can also download the test results in CSV format for further analysis.

