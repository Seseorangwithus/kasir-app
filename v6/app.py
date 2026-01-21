from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("kasir_v6.db")

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            harga INTEGER,
            qty INTEGER
        )
    """)

    if request.method == "POST":
        nama = request.form["nama"]
        harga = int(request.form["harga"])
        qty = int(request.form["qty"])

        cur.execute(
            "INSERT INTO items (nama, harga, qty) VALUES (?, ?, ?)",
            (nama, harga, qty)
        )
        db.commit()
        return redirect("/")

    cur.execute("SELECT nama, harga, qty FROM items")
    items = cur.fetchall()

    total = sum(i[1] * i[2] for i in items)
    ppn = total * 0.11
    grand_total = total + ppn

    return render_template(
        "index.html",
        items=items,
        total=total,
        ppn=ppn,
        grand_total=grand_total
    )

if __name__ == "__main__":
    app.run(debug=True)
