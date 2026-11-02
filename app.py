from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
app = Flask(__name__)
app.secret_key = "samarth123"
def db():
    return psycopg2.connect(host="localhost",
                            database="college_db",
                            user="postgres", 
                            password="root", port=5432)
def setup():
    con = db()
    with con:
        with con.cursor() as c:
            c.execute("CREATE TABLE IF NOT EXISTS portal_users (id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE, password VARCHAR(100))")
            c.execute("INSERT INTO portal_users (username,password) VALUES ('admin','admin123') ON CONFLICT (username) DO NOTHING")
    con.close()
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        con = db()
        with con:
            with con.cursor() as c:
                c.execute("SELECT id FROM portal_users WHERE username=%s AND password=%s",
                          (request.form.get("username", "").strip(), request.form.get("password", "")))
                found = c.fetchone()
        con.close()
        if found:
            session["username"] = request.form["username"].strip()
            return redirect(url_for("dashboard"))
        message = "Wrong username or password"
    return render_template("login.html", message=message)
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")
@app.route("/department")
def department():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("department.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
if __name__ == "__main__":
    setup()
    app.run(debug=True)
