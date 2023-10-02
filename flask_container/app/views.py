"""
We can use any file structure we want, I just saw this app/views.py structure
on a couple of tutorials I was looking at. For now this is a placeholder
to see that flask is serving from a container.
"""

from app import app

@app.route('/')
def hello_world():
	return "hello world! seeing this means flask is working."

