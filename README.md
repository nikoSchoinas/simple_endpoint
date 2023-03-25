# Simple Endpoint

This is a small project that returns an endpoint with sales information for a given date.

The code is developed in Linux operating system. If you use any other operating system is highly recomended to use Anaconda or Docker. 

## Installation
You can clone the repository by going to your prefered directory, open a terminal and run

```console
~$ git clone https://github.com/nikoSchoinas/simple_endpoint.git
```

Before you run the code you need to install the dependencies.
```concole
~$ cd simple_endpoint
~$ pip3 install -r requirements.txt
```

Then, run the main script to launch the application.
```console
~$ python3 main.py
```

Now, if you go to http://localhost:5000/ in your web browser, you should see a form where you can choose a date. When you submit the form, the browser will make a request and the Flask endpoint will generate a report for the chosen date.

## Testing
To run the tests you need to have pytest install (it's  included to the requirements.txt). Navigate to the directory where the test files are and run:
```console
~$ cd simple_endpoint/tests
pytest -q
```