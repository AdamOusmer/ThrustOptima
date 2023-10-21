"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************


"""
from thrust_optima import app
from waitress import serve
import sys

if __name__ == '__main__':
    print("Starting server...", file=sys.stdout)
    sys.stdout.flush()
    serve(app, host='localhost', port=5000)
