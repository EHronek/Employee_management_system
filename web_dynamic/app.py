#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from models import storage
from models.user import User
from models import storage
from web_dynamic.blueprints.admin_routes import admin_bp
from web_dynamic.blueprints.employee_routes import employee_bp
# from web_dynamic.auth import auth_bp 
import uuid
from web_dynamic.config import Config


app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
# app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(employee_bp, url_prefix="/employees")



@app.teardown_appcontext
def close_db(error):
    """Remove the current session"""
    storage.close()

@app.before_request
def add_cache_id():
    """ Inject cache_id into all templates """
    cache_id = uuid.uuid4()
    app.jinja_env.globals.update(cache_id=cache_id)

@app.route("/", methods=["GET"], strict_slashes=False)
def landing_page():
    """ Main landing page """
    return render_template("landingPage.html")



@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login_page():
    ''' Handles user login '''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        sess = storage.get_session()
        user = sess.query(User).filter_by(username=username).first()

        if not user:
            flash("Invalid credentials. Please check your username.", "danger")
            return render_template("login.html")
        
        if not user.check_password(password):
            flash("Invalid credentials. Please try again.", "danger")
            return render_template("login.html")
        
        session["user_id"] = user.id
        session["role"] = user.role
        session["employee_id"] = user.employee_id

        return redirect(url_for("admin.admin_dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["GET"], strict_slashes=False)
def logout():
    '''Handles user logout'''
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/sign-up", methods=["GET"], strict_slashes=False)
def sign_up():
    """ Sign Up """
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
