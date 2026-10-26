import os
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-dev-key-change-me")

DEFAULT_DB = Path(app.instance_path) / "contacts.db"
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(DEFAULT_DB))


def get_db():
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                address TEXT NOT NULL DEFAULT ''
            )
        """)


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    with get_db() as connection:
        if search:
            pattern = f"%{search}%"
            contacts = connection.execute(
                """SELECT * FROM contacts
                   WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                   ORDER BY name COLLATE NOCASE""",
                (pattern, pattern, pattern),
            ).fetchall()
        else:
            contacts = connection.execute(
                "SELECT * FROM contacts ORDER BY name COLLATE NOCASE"
            ).fetchall()
    return render_template("index.html", contacts=contacts, search=search)


@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        if not name:
            flash("Name is required.", "error")
            return render_template("contact_form.html", contact=None), 400

        with get_db() as connection:
            connection.execute(
                "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                (name, phone, email, address),
            )
        flash("Contact added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("contact_form.html", contact=None)


@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    with get_db() as connection:
        contact = connection.execute(
            "SELECT * FROM contacts WHERE id = ?", (contact_id,)
        ).fetchone()

        if contact is None:
            return "Contact not found", 404

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            phone = request.form.get("phone", "").strip()
            email = request.form.get("email", "").strip()
            address = request.form.get("address", "").strip()

            if not name:
                flash("Name is required.", "error")
                return render_template("contact_form.html", contact=contact), 400

            connection.execute(
                """UPDATE contacts SET name = ?, phone = ?, email = ?, address = ?
                   WHERE id = ?""",
                (name, phone, email, address, contact_id),
            )
            flash("Contact updated successfully.", "success")
            return redirect(url_for("index"))

    return render_template("contact_form.html", contact=contact)


@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    with get_db() as connection:
        connection.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    flash("Contact deleted if it existed.", "success")
    return redirect(url_for("index"))


@app.route("/health")
def health():
    try:
        with get_db() as connection:
            connection.execute("SELECT 1")
        return {"status": "healthy"}, 200
    except sqlite3.Error:
        return {"status": "unhealthy"}, 500


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
