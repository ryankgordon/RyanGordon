from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("visitors.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            count INTEGER
        )
    """)
    cur = conn.execute("SELECT count FROM counter WHERE id = 1")
    if cur.fetchone() is None:
        conn.execute("INSERT INTO counter (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.execute("SELECT count FROM counter WHERE id = 1")
    count = cur.fetchone()["count"] + 1
    conn.execute("UPDATE counter SET count = ? WHERE id = 1", (count,))
    conn.commit()
    conn.close()
    return render_template("index.html", visitors=count)

# NEW ROUTE FOR RESUME
@app.route("/resume")
def resume():
    return render_template("resume.html")
    
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

