import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import re
from werkzeug.utils import secure_filename
from PIL import Image
from threading import Timer

from method import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def delete_file(filepath):
    try:
        os.remove(filepath)
        print(f"File {filepath} deleted successfully.")
    except Exception as e:
        print(f"Error deleting file {filepath}: {e}")

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    credit = db.Column(db.Float, default=10.0)
    create_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class History(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credits_used = db.Column(db.Float, nullable=False)
    conversion_type = db.Column(db.String(50), nullable=False)  # Add this line
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.errorhandler(404)
def page_not_found(_):
    return render_template('error.html')

@app.route("/")
def index():
    return render_template("index.html")

login = "portal/login.html"
@app.route("/portal/login", methods=["POST", "GET"])
def login_template():
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Must provide username", "danger")
            return render_template(login)

        # Ensure password was submitted
        if not password:
            flash("Must provide password", "danger")
            return render_template(login)

        try:
            # Query database for username
            user = User.query.filter_by(username=username).first()

            # Ensure username exists and password is correct
            if user is None or not check_password_hash(user.hash, password):
                flash("Invalid username and/or password", "danger")
                return render_template(login)

            # Remember which user has logged in
            session["user_id"] = user.id
            session["username"] = user.username
            
            # Redirect user to home page
            flash("Welcome to the system", "success")
            return redirect(url_for("index"))

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return render_template(login)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template(login)

register = "portal/register.html"
@app.route("/portal/register", methods=["GET", "POST"])
def register_template():
    """register user"""

    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")

        if not username:
            flash("Must provide username", "danger")
            return render_template(register)

        # Ensure password was submitted
        elif not password:
            flash("Must provide password", "danger")
            return render_template(register)

        # Ensure confirmation was submitted
        elif not confirmation:
            flash("Must provide password confirmation", "danger")
            return render_template(register)

        # Ensure password and confirmation match
        elif password != confirmation:
            flash("Password and confirmation do not match", "danger")
            return render_template(register)

        # Ensure email was submitted and is valid
        elif not email:
            flash("Must provide email", "danger")
            return render_template(register)

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address", "danger")
            return render_template(register)

        try:
            # Query database for username
            user = User.query.filter_by(username=username).first()

            if user:
                flash("User already exists. Please try again.", "danger")
                return render_template(register)

            # Hash the password
            hashed_password = generate_password_hash(password, method='scrypt', salt_length=16)

            # Insert the new user into the database
            new_user = User(username=username, hash=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()

            # Redirect user to login page after successful registration
            flash("Registration successful. Please log in.", "success")
            return render_template((login))

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return render_template(register)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template(register)

@app.route("/portal/logout")
def logout_template():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("login_template"))

profile = "portal/profile.html"
@app.route("/portal/profile", methods=["GET", "POST"])
@login_required
def profile_template():
    session_id = session["user_id"]

    if request.method == "POST":
        if request.form.get("email"):
            # Handle email update
            email = request.form.get("email")
            if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
                try:
                    user = User.query.filter_by(id=session_id).first()
                    if user and user.email != email:
                        user.email = email
                        db.session.commit()
                        flash("Email updated successfully", "success")
                    elif not user:
                        flash("User not found", "danger")
                except Exception as e:
                    flash(f"An error occurred: {e}", "danger")
            else:
                flash("Invalid email address", "danger")

        elif request.form.get("Old_password"):
            # Handle password update
            old_password = request.form.get("Old_password")
            new_password = request.form.get("New_password")
            confirmation = request.form.get("confirmation")
            if old_password and new_password and confirmation:
                if new_password == confirmation:
                        try:
                            user = User.query.filter_by(id=session_id).first()
                            if user:
                                if check_password_hash(user.hash, old_password):
                                    
                                    user.hash = generate_password_hash(new_password, method='scrypt', salt_length=16)
                                    db.session.commit()
                                    flash("Password updated successfully", "success")
                                    return redirect(url_for("logout_template"))
                                else:
                                    flash("Old password is incorrect", "danger")
                            else:
                                flash("User not found", "danger")
                        except Exception as e:
                            flash(f"An error occurred: {e}", "danger")
                else:
                    flash("Password and confirmation do not match", "danger")
            else:
                flash("Password and confirmation are required", "danger")

        elif request.form.get("delete_account"):
                # Handle account deletion
                try:
                    user = User.query.filter_by(id=session_id).first()
                    if user:
                        if check_password_hash(user.hash, request.form.get("delete_account")):
                            db.session.delete(user)
                            db.session.commit()
                            session.clear()
                            flash("Account deleted successfully", "success")
                            return redirect(url_for("index"))
                        else:
                            flash("Incorrect password", "danger")
                    else:
                        flash("User not found", "danger")
                except Exception as e:
                    flash(f"An error occurred: {e}", "danger")

    # Handle GET request
    try:

        user = User.query.filter_by(id=session_id).first()
        history = History.query.filter_by(user_id=session_id).all()
        return render_template(profile, user=user, history=history)
    

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return render_template(profile, user=None, history=[])
    
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_template():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('dashboard_template'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('dashboard_template'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                # Ensure the uploads directory exists
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                
                print(f"Saving file to {filepath}")
                file.save(filepath)
                print(f"File saved to {filepath}")
                
                output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.', 1)[0] + '.webp')
                print(f"Converting file to {output_filepath}")
                
                # Use Pillow to convert the image
                with Image.open(filepath) as img:
                    img.save(output_filepath, 'WEBP')
                
                print(f"File converted to {output_filepath}")
                flash('File uploaded and converted successfully', 'success')

                # Update user credits and add history
                user = User.query.filter_by(id=session['user_id']).first()
                if user.credit >= 2:
                    user.credit -= 2
                    history = History(user_id=user.id, conversion_type='PNG to WEBP', credits_used=2)
                    db.session.add(history)
                    db.session.commit()
                else:
                    flash('Not enough credits', 'danger')
                    return redirect(url_for('dashboard_template'))

                # Schedule file deletion after 1 minute
                Timer(60, delete_file, args=[filepath]).start()
                Timer(60, delete_file, args=[output_filepath]).start()

                return send_file(output_filepath, as_attachment=False)

            except Exception as e:
                flash(f"An error occurred: {e}", 'danger')
            return redirect(url_for('dashboard_template'))
        else:
            flash('Invalid file type', 'danger')
            return redirect(url_for('dashboard_template'))
    return render_template('dashboard.html')
