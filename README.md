# E-Commerce Product Recommendation Engine

Hi everyone! This is my project for building an E-Commerce Recommendation System. The goal was to build a system that actively suggests products to users based on their personal browsing history and preferences. 

## Problem Statement
The assignment required building a recommendation engine that dynamically suggests products to users. The required tech stack was:
- Python
- Flask / Django (I went with Flask!)
- MySQL
- Scikit-learn
- AWS / GCP

## What I Built
To solve this, I designed a **Hybrid Recommendation Engine** that uses two different machine learning approaches to cover all bases:

1. **Collaborative Filtering (User-Based):** When a user logs in, the system checks their purchase history in the MySQL database and compares it against a matrix of other users. If "User A" is similar to the logged-in user, the system recommends things "User A" bought that the logged-in user hasn't seen yet.
2. **Content-Based Filtering (Item-Based):** When a user clicks on a specific product to view it, the system uses natural language processing (TF-IDF vectorization) on the product's description to find other items in the catalog that are structurally similar (using cosine similarity).

## Key Features
- **Full-Stack Web App:** A clean, modern UI built with HTML/CSS (glassmorphism design) and connected to a Flask Python backend.
- **MySQL Integration:** Real user accounts with hashed passwords (bcrypt), an interaction history tracker, and a live product catalog.
- **Automated Data Pipeline:** A script (`setup_db.py`) that extracts over 3,600 real E-commerce products from my trained Pandas model and automatically populates the MySQL database.
- **Dynamic Dashboard:** A user dashboard that updates its recommendations live based on the user's linked internal ID.

## How to Run the Project Locally

If you want to test the code on your own machine, follow these steps:

1. **Set up the Database:**
   Make sure you have a local MySQL server running (like XAMPP or MySQL Workbench) with the credentials `root` and your password. Check `setup_db.py` to ensure the credentials match yours. Run the setup script to build the tables and load the product data:
   ```bash
   python setup_db.py
   ```

2. **Start the Flask Server:**
   Install the required python libraries and start the server:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

3. **Test It Out!**
   Open your browser and go to `http://localhost:5000`. Create an account, and when asked for an optional Customer ID, type in `17850` to see the collaborative filtering instantly populate your dashboard with historical recommendations!

## Cloud Deployment (AWS)
The project is built to be production-ready. For a live environment, the codebase can be deployed to an AWS EC2 instance running Gunicorn, while the MySQL connection string is simply swapped out for an AWS RDS endpoint. I've prepared a full cloud migration path in my architecture notes.
