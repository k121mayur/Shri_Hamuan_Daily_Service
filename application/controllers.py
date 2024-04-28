from flask import request, url_for, redirect, session, jsonify
from flask_session import Session
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template
from flask import current_app as app
from werkzeug.utils import secure_filename
from application.database import db
from application.models import Users
from datetime import datetime as dt
from datetime import timedelta
import os
from email_validator import validate_email
from application.models import party, consignee, Orders
from flask_healthcheck import HealthCheck # For GCloud Deployment

health = HealthCheck()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/health')
@health.fisk_check()
def health_check():
  # Add logic to check your app's health (database connection, etc.)
  # If healthy, return a successful response (e.g., HTTP 200)
  # If unhealthy, return an error response (e.g., HTTP 500)
  return jsonify({'status': 'healthy'})

@app.route("/")
def index():
    return render_template("index.html", error=None)

@app.route("/login", methods=["POST"])
def login():
    if request.method != "POST":
        return redirect(url_for("index"))
    
    role = request.form.get("role")
    username = request.form.get("username")
    password = request.form.get("password")

    user_status = Users.query.filter_by(username=username).first()

    if user_status is None or user_status.password != password or user_status.role.strip().lower() != role.strip().lower():
        return render_template("index.html", error="Invalid role, username or password")
    login_user(user_status)
    if user_status.role.strip().lower() == "admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("dashboard"))


@app.route("/admin_dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    print(current_user.role.strip().lower())
    if current_user.role.strip().lower() == "admin":
        return render_template("admin_dashboard.html")
    else:
        logout_user()
        return render_template("index.html", error="You are not authorized to view this page. Please login again")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/order_entry", methods=["GET", "POST"])
def order_entry():
    if request.method == "GET":
        return render_template("order_entry.html", status = None)
    elif request.method == "POST":
        order_date = dt.now().date()
        order_time = dt.now().time()
        from_branch = request.form.get("from_branch")
        to_branch = request.form.get("to_branch")
        party_id = 0
        cosignee_name = request.form.get("consignee_name")
        consinee_address = request.form.get("consignee_address")
        inovice_number = request.form.get("invoice_number")
        description_of_goods = request.form.get("description_of_goods")
        number_of_packges = request.form.get("number_of_packges")
        consignment_value = request.form.get("consignment_value")
        consignment_weight = request.form.get("consignment_weight")
        pod_charges = request.form.get("pod_charges")
        payment_mode = request.form.get("payment_method")
        total_amount = request.form.get("consignment_charges")
        
        order = Orders(
            order_date = order_date,
            order_time = order_time,
            from_branch = from_branch,
            to_branch = to_branch,
            party_id = int(party_id),
            cosignee_name = cosignee_name,
            consinee_address = consinee_address,
            inovice_number = inovice_number,
            description_of_goods = description_of_goods,
            number_of_packges = number_of_packges,
            consignment_value = int(consignment_value),
            consignment_weight = int(consignment_weight),
            pod_charges = int(pod_charges),
            payment_mode = payment_mode,
            total_amount = int(total_amount),
            entry_by = int(current_user.id)

        )
        db.session.add(order)
        db.session.commit()        
        return render_template("order_entry.html", status = "Order added successfully")


@app.route("/search_consigner", methods=["GET", "POST"])
@login_required
def search_consigner():
    search_term = request.get_json()
    consignors = party.query.filter(party.business_name.like(f"%{search_term['names']}%")).all()
    print(consignors)
    matching_names = [consignor.business_name for consignor in consignors]
    return jsonify(matching_names)

@app.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if current_user.role.strip().lower() != "admin":
        logout_user()
        return render_template("index.html", error="You are not authorized to add user. Please login again")
    if request.method == "GET":
        return render_template("add_user.html", error=None)
    elif request.method == "POST":
        name = request.form.get("name")
        mobile_number = request.form.get("mobile_number")
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            return render_template("add_user.html", error="Password and Confirm Password do not match Please do this again")
        else:
            user = Users(name=name, mobile_number=mobile_number, role=role, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return render_template("add_user.html", error="User added successfully")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')
