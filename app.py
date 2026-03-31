import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Product, Interaction
from recommender import Recommender
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'yugra_secret_key_123')

# Database Setup — uses environment variables on cloud, falls back to localhost for local dev
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'YugraJ@007')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'ecommerce_db')

from urllib.parse import quote_plus
encoded_pass = quote_plus(DB_PASS)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
import os
import time
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Product, Interaction
from recommender import Recommender
from api import api_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_overrides=None):
    """Application factory. Returns a Flask app instance."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'yugra_secret_key_123')

    # Database Setup — uses environment variables on cloud, falls back to localhost for local dev
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASS = os.environ.get('DB_PASS', 'YugraJ@007')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'ecommerce_db')

    from urllib.parse import quote_plus
    encoded_pass = quote_plus(DB_PASS)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    bcrypt = Bcrypt(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    # Register API blueprint
    app.register_blueprint(api_bp)

    # Load the ML Model once on startup and attach to app for reuse
    with app.app_context():
        logger.info("Loading Recommendation Model... Please wait...")
        start = time.time()
        app.recommender = Recommender('recommendation_model.pkl')
        logger.info(f"Model loaded in {time.time() - start:.2f} seconds.")

        # Create tables if they do not exist (safe for local/dev only)
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # --- ROUTES (HTML pages) ---
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            customer_id = request.form.get('customer_id') # Optional linking to ML target user id

            if User.query.filter_by(username=username).first():
                flash('Username already exists. Please choose a different one.', 'warning')
                return redirect(url_for('register'))

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, password_hash=hashed_password, customer_id=customer_id)
            db.session.add(user)
            db.session.commit()

            flash('Account created! You can now log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        # If the user linked an original Customer ID, we use it for collaborative filtering logic.
        collab_products = []

        if current_user.customer_id:
            res = app.recommender.recommend_collaborative(current_user.customer_id, 8)
            if "products" in res:
                collab_products = res["products"]

        recent_products = Product.query.limit(10).all() # Just show some items to browse

        return render_template('dashboard.html', user=current_user, collab_products=collab_products, recent_products=recent_products)

    @app.route('/view_product/<string:stock_code>')
    @login_required
    def view_product(stock_code):
        product = db.session.get(Product, stock_code)
        if not product:
            flash("Product not found.", "danger")
            return redirect(url_for('dashboard'))

        # Log interaction
        new_interaction = Interaction(user_id=current_user.id, stock_code=stock_code)
        db.session.add(new_interaction)
        db.session.commit()

        # Get similar content-based recommendations
        res = app.recommender.recommend_content(product.Description or stock_code, 4)
        similar_products = res.get('products', [])

        return render_template('product_view.html', product=product, similar_products=similar_products)

    return app
