from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from flask import request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle
from flask import send_file
import io
#================================
#database
#=================================
def init_db():
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    
    
app = Flask(__name__)
app.secret_key = "supersecretkey"

# ===============================
# Load dataset
# ===============================
data = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\house_bot_project\housing.csv")

X = data[[
    "Avg. Area Income",
    "Avg. Area House Age",
    "Avg. Area Number of Rooms",
    "Avg. Area Number of Bedrooms",
    "Area Population"
]]

y = data["Price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Temporary user storage
users = {}

# ===============================
# HOME PAGE
# ===============================
@app.route("/")
def home():
    return render_template("home.html")


# ===============================
# REGISTER
# ===============================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users[username] = password
        return redirect(url_for("login"))

    return render_template("register.html")


# ===============================
# LOGIN
# ===============================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ===============================
# DASHBOARD
# ===============================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("reports.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        user=session["user"],
        reports=reports
    )
# ===============================
# ASSISTANT PAGE
# ===============================
@app.route("/assistant")
def assistant():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# ===============================
# CHAT API
# ===============================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_data = request.get_json()

        sqft = float(user_data["square_feet"])
        budget = float(user_data["budget"])

        avg_values = data[X.columns].mean().values.reshape(1, -1)
        predicted_price = model.predict(avg_values)[0]

        matching = data[data["Price"] <= budget]

        matching_houses = []

        for _, row in matching.head(5).iterrows():
            matching_houses.append({
                "city": row["Address"],
                "price": f"${row['Price']:,.2f}",
                "square_feet": round(row["Avg. Area Number of Rooms"] * 300)
            })

        return jsonify({
            "predicted_price": f"${predicted_price:,.2f}",
            "matching_houses": matching_houses
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Server error"}), 500


# ===============================
# LOGOUT
# ===============================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

#=================================
#Property-Trends
#=================================
@app.route('/dashboard/property-trends')
def property_trends():
    return render_template('property_trends.html')

#===================================
#Saved Reports
#===================================
@app.route("/dashboard/saved-reports")
def saved_reports():
    conn = sqlite3.connect("reports.db")
    conn.row_factory = sqlite3.Row   
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()

    conn.close()

    return render_template("saved_reports.html", reports=reports)
#======================================
# view_report
#======================================
@app.route("/dashboard/report/<int:report_id>")
def view_report(report_id):

    conn = sqlite3.connect("reports.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    report = cursor.fetchone()
    conn.close()

    if report is None:
        return "Report not found", 404

    return render_template("view_report.html", report=report)

#======================================
# export_report
#======================================
@app.route("/dashboard/report/<int:report_id>/export")
def export_report(report_id):

    conn = sqlite3.connect("reports.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    report = cursor.fetchone()
    conn.close()

    if report is None:
        return "Report not found", 404

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Real Estate Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Report Name: {report['name']}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {report['date']}", styles["Normal"]))
    elements.append(Paragraph(f"Type: {report['type']}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Description:", styles["Heading2"]))
    elements.append(Paragraph(report["description"], styles["Normal"]))

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{report['name']}.pdf",
        mimetype="application/pdf"
    )
    
#===================================
#account-settings
#====================================
@app.route('/dashboard/account-settings')
def account_settings():
    user = {
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "Administrator",
        "joined": "January 2025"
    }
    return render_template('account_settings.html', user=user)
#=====================================
#update_password
#======================================
@app.route('/update-password', methods=['POST'])
def update_password():
    if 'user_id' not in session:
        return redirect('/login')

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    user = User.query.get(session['user_id'])

    # Check current password
    if not check_password_hash(user.password, current_password):
        flash("Current password is incorrect!", "error")
        return redirect('/dashboard/account-settings')

    # Check if new passwords match
    if new_password != confirm_password:
        flash("New passwords do not match!", "error")
        return redirect('/dashboard/account-settings')

    # Update password
    user.password = generate_password_hash(new_password)
    db.session.commit()

    flash("Password updated successfully!", "success")
    return redirect('/dashboard/account-settings')

#==============================
#delete_account
#=============================
@app.route('/delete-account')
def delete_account():
    # Example logic (replace with your real DB logic)
    
    # 1️⃣ Delete user from database
    # User.query.filter_by(id=session['user_id']).delete()
    # db.session.commit()

    # 2️⃣ Clear session
    session.clear()

    # 3️⃣ Redirect to login page
    flash("Account deleted successfully", "success")
    return redirect("/login")

#=============================
#sample_reports
#==============================

@app.route("/add-sample-reports")
def add_sample_reports():
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    reports = [
        ("January Market Analysis", "2026-01-15", "Price Trend", "Detailed analysis of January property prices."),
        ("Downtown Growth Report", "2026-02-01", "Area Analysis", "Growth trends in downtown area."),
        ("Luxury Villas Report", "2026-02-10", "Property Type", "Luxury villas performance overview.")
    ]

    cursor.executemany("INSERT INTO reports (name, date, type, description) VALUES (?, ?, ?, ?)", reports)

    conn.commit()
    conn.close()

# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    init_db()   
    app.run(debug=True)