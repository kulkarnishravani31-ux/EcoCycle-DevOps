import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-in-production")
db_url = os.getenv("DATABASE_URL", "sqlite:///ecocycle.db")
if db_url.startswith("mysql://"):
    db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)

class PickupRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    preferred_date = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, default="")
    status = db.Column(db.String(30), default="Pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="pickup_requests")

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        user = db.session.get(User, session["user_id"])
        if not user or user.role != "admin":
            flash("Administrator access required.", "danger")
            return redirect(url_for("index"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name, email = request.form["name"].strip(), request.form["email"].strip().lower()
        password = request.form["password"]
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("That email is already registered.", "danger")
        else:
            user = User(name=name, email=email, password_hash=generate_password_hash(password))
            db.session.add(user); db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role
            flash("Welcome back!", "success")
            return redirect(url_for("admin" if user.role == "admin" else "dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    requests_list = PickupRequest.query.filter_by(user_id=session["user_id"]).order_by(PickupRequest.created_at.desc()).all()
    return render_template("dashboard.html", requests=requests_list)

@app.route("/pickup", methods=["GET", "POST"])
@login_required
def pickup():
    if request.method == "POST":
        quantity = request.form.get("quantity", type=int)
        if not quantity or quantity < 1:
            flash("Quantity must be at least 1.", "danger")
        else:
            item = PickupRequest(user_id=session["user_id"], item_type=request.form["item_type"],
                quantity=quantity, address=request.form["address"], preferred_date=request.form["preferred_date"],
                notes=request.form.get("notes", ""))
            db.session.add(item); db.session.commit()
            flash("Pickup request submitted successfully.", "success")
            return redirect(url_for("dashboard"))
    return render_template("pickup.html")

@app.route("/admin")
@admin_required
def admin():
    requests_list = PickupRequest.query.order_by(PickupRequest.created_at.desc()).all()
    return render_template("admin.html", requests=requests_list)

@app.route("/admin/request/<int:request_id>", methods=["POST"])
@admin_required
def update_request(request_id):
    item = db.session.get(PickupRequest, request_id)
    if not item:
        flash("Request not found.", "danger")
    else:
        status = request.form.get("status")
        if status in {"Pending", "Approved", "Collected", "Rejected"}:
            item.status = status
            db.session.commit()
            flash("Request status updated.", "success")
    return redirect(url_for("admin"))

@app.cli.command("create-admin")
def create_admin():
    """Create default admin: admin@ecocycle.local / Admin123! (change after first login)."""
    email = os.getenv("ADMIN_EMAIL", "admin@ecocycle.local")
    password = os.getenv("ADMIN_PASSWORD", "Admin123!")
    if not User.query.filter_by(email=email).first():
        db.session.add(User(name="EcoCycle Admin", email=email,
            password_hash=generate_password_hash(password), role="admin"))
        db.session.commit()
        print(f"Admin created: {email}")

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database tables created.")

@app.route("/health")
def health():
    return {"status": "ok"}

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")
