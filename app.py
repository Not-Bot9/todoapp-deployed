from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4

app = Flask(__name__)

# In-memory store (resets on container restart or new revision)
NOTES = []  # each note: {"id": "uuid", "text": "..."}

@app.get("/")
def home():
    return render_template("index.html", notes=NOTES)

@app.post("/add")
def add_note():
    text = (request.form.get("text") or "").strip()
    if text:
        NOTES.append({"id": str(uuid4()), "text": text})
    return redirect(url_for("home"))

@app.post("/edit/<note_id>")
def edit_note(note_id):
    text = (request.form.get("text") or "").strip()
    if text:
        for n in NOTES:
            if n["id"] == note_id:
                n["text"] = text
                break
    return redirect(url_for("home"))

@app.post("/delete/<note_id>")
def delete_note(note_id):
    global NOTES
    NOTES = [n for n in NOTES if n["id"] != note_id]
    return redirect(url_for("home"))

# Health check
@app.get("/_ah/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    # Local run: python app.py
    app.run(host="0.0.0.0", port=8080, debug=True)