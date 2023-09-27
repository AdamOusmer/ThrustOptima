"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the code for the GUI and it is use for all user's interactions excluding the request for the path
of the dicomdir file when the Scan object is being initialized.
"""

from flask import Flask, render_template

def main():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.run(debug=True)

main()
