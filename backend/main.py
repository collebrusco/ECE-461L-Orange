"""
Main entry point for the backend
"""

from app import app
if __name__ == '__main__':
	app.run(port=5000, host='0.0.0.0', debug=True)