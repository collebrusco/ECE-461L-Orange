"""
We can use any file structure we want, I just saw this app/views.py structure
on a couple of tutorials I was looking at. For now this is a placeholder
to see that flask is serving from a container.
"""

from pathlib import Path
from app import app, send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(path)
    if path != "" and Path(app.static_folder + '/' + path).exists():
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
