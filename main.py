"""
This  is the main script that executes the flask app. 
"""

from flask import Flask, render_template, request
import utils

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the index.html template.
    """
    return render_template('index.html')

@app.route('/report')
def generate_report():
    """
    Returns the endpoint report to the app
    """
    # Take the date after user clicks on submit button in the HTML form. 
    date_str = request.args.get('date')
    # Check if the date is valid and inform the user if not.
    if not utils.is_date_valid(date_str): return 'Input date is not valid'
    endpoint = utils.create_endpoint(date_str)
    return endpoint
    


if __name__ == '__main__':
    app.run()
