import os
import pymysql
import pickle
import pandas as pd
from sqlalchemy import create_engine

# Database Credentials — env vars on cloud, defaults for local dev
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'YugraJ@007')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'ecommerce_db')

def setup_database():
    try:
        # Step 1: Connect to MySQL server and create the database
        print("Connecting to MySQL to drop and re-create database...")
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        connection.commit()
        connection.close()
        print(f"Database '{DB_NAME}' created or already exists.")

        # Step 2: Load products data
        print("Loading products from recommendation_model.pkl...")
        with open('recommendation_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        products_df = model_data['products_df']
        
        # Step 3: Insert products into MySQL using SQLAlchemy
        from urllib.parse import quote_plus
        encoded_pass = quote_plus(DB_PASS)
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # Initialize the actual schema from models so types match exactly
        from app import app, db
        with app.app_context():
            db.create_all()
            
        print("Writing products to the generic 'product' table... This may take a moment.")
        # Now append data to the strict schema table
        products_df.to_sql('product', con=engine, if_exists='append', index=False)
        
        print(f"Successfully loaded {len(products_df)} products into MySQL!")
        
    except Exception as e:
        import traceback
        with open('setup_db_err.txt', 'w') as f:
            traceback.print_exc(file=f)
        print(f"An error occurred, check setup_db_err.txt: {e}")

if __name__ == "__main__":
    setup_database()
