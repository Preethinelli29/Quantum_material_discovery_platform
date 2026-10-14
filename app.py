import glob
import os

from flask import Flask, send_file

BASE = os.path.dirname(os.path.abspath(__file__))

# static_folder=None so app.py / requirements.txt are NOT publicly served
app = Flask(__name__, static_folder=None)


def find_page():
    """Serve index.html if present, otherwise the first .html file next to app.py."""
    preferred = os.path.join(BASE, "index.html")
    if os.path.exists(preferred):
        return preferred
    matches = sorted(glob.glob(os.path.join(BASE, "*.html")))
    return matches[0] if matches else None


@app.route("/")
def home():
    page = find_page()
    if page is None:
        files = ", ".join(sorted(os.listdir(BASE)))
        return f"No .html file found next to app.py. Files here: {files}", 404
    return send_file(page)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
