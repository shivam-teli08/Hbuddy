from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from src.services.admin_service import get_all_businesses, register_business
from src.services.auth_service import is_admin_user


@login_required
def dashboard():
    if not is_admin_user():
        return redirect(url_for("auth.login"))
    businesses = get_all_businesses()
    return render_template("admin/dashboard.html", businesses=businesses)


@login_required
def register_business_view():
    if not is_admin_user():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        register_business(
            name=request.form.get("name"),
            username=request.form.get("username"),
            password=request.form.get("password"),
            business_type=request.form.get("business_type"),
        )
        flash("Business registered successfully")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/register_business.html")
