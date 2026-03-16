import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'          # redirect to login page if not authenticated
login_manager.login_message_category = 'info'

# ---------- Database Models ----------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')   # 'admin' or 'client'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- Forms ----------
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('client', 'Client'), ('admin', 'Admin')], default='client')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# ---------- Web Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return "About page (coming soon)"

@app.route('/contact')
def contact():
    return "Contact page (coming soon)"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('client_dashboard'))

@app.route('/client-dashboard')
@login_required
def client_dashboard():
    if current_user.is_admin():
        flash('Admins cannot access client dashboard.', 'warning')
        return redirect(url_for('admin_dashboard'))
    return render_template('client_dash.html', user=current_user)

@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('client_dashboard'))
    users = User.query.all()
    return render_template('admin_dash.html', users=users)

# ---------- API Endpoints (unchanged) ----------
@app.route('/api/estimate', methods=['POST'])
def estimate():
    data = request.get_json()
    return jsonify({
        "total_cost": 15250.75,
        "currency": "USD",
        "breakdown": {
            "materials": 8750.25,
            "labor": 4500.50,
            "equipment": 2000.00
        }
    })

@app.route('/api/measure', methods=['POST'])
def measure():
    data = request.get_json()
    return jsonify({
        "area_sqft": 2450,
        "volume_cuft": 18375,
        "perimeter_ft": 320
    })

# ---------- Database initialization (run once) ----------
@app.cli.command("init-db")
def init_db():
    """Create database tables."""
    db.create_all()
    print("Database created.")

if __name__ == '__main__':
    app.run(debug=True)