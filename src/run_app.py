"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This script runs the graph app.
"""
from graphapp import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)