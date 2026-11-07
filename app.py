from flask import Flask, jsonify, send_from_directory
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EMOTES_DIR = BASE_DIR / "emotes"
IMAGE_EXTENSIONS = {".png", ".webp", ".jpg", ".jpeg"}

app = Flask(__name__, static_folder=None)


def emote_sort_key(filename):
    stem = Path(filename).stem
    # Numeric IDs sort numerically; other filenames sort after them alphabetically.
    return (0, int(stem)) if stem.isdigit() else (1, stem.lower())


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/emotes")
def emotes():
    if not EMOTES_DIR.is_dir():
        return jsonify({"error": "The emotes folder was not found."}), 500

    files = sorted(
        [
            path.name for path in EMOTES_DIR.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        ],
        key=emote_sort_key
    )
    return jsonify([
        {
            "id": Path(filename).stem,
            "filename": filename,
            "url": f"/emotes/{filename}"
        }
        for filename in files
    ])


@app.route("/emotes/<path:filename>")
def emote_file(filename):
    return send_from_directory(EMOTES_DIR, filename)


@app.route("/<path:filename>")
def project_file(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    print("LUCKY EMOTE WEB is running at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
