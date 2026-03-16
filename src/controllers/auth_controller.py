from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from src.services.auth_service import authenticate_admin, authenticate_business_user


def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = authenticate_business_user(username, password)
        if user:
            login_user(user)
            if not user.is_setup_completed:
                return redirect(url_for("business.setup"))
            return redirect(url_for("business.dashboard"))
        flash("Invalid username or password")
    return render_template("login.html")


def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        admin = authenticate_admin(username, password)
        if admin:
            login_user(admin)
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password")
    return render_template("admin/login.html")


@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
