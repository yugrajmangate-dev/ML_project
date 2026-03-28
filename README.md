# E-Commerce AI Recommendation Engine 🚀

This repository contains an end-to-end Machine Learning web application designed to recommend products to users based on an **E-Commerce Collaborative Filtering** and **Content-Based Filtering** model.

## 🛠️ Tech Stack
- **Python**: Core logic programming language.
- **Scikit-learn / Pandas**: For building the similarity matrices and handling dataframes dynamically.
- **Flask**: The backend framework to serve API endpoints cleanly.
- **MySQL (Flask-SQLAlchemy / PyMySQL)**: A fully integrated SQL database that stores real user account details, product histories, and the active catalog.
- **HTML / CSS / JS**: A premium Glassmorphism-themed frontend interface.
- **AWS Deployment Ready**: Scalable cloud production setup guides generated.

## 📦 Features Implemented
1. **Model Dual-Engine Recommendations**:
   * **Collaborative Filtering**: Suggests items based on historical purchase similarities between the logged-in User and other matching neighbors from our dataset.
   * **Content-Based Filtering**: Suggests items that mathematically resemble the *item currently being viewed* based on TF-IDF word vector analysis of product descriptions.
2. **User Authentication & Profile Simulator**: 
   * Fully hashed BCrypt login system mapped to MySQL. Users can log in and browse products to naturally generate historical "views".
3. **Automated DB Population Strategy**: Uses a dynamic `setup_db.py` script that acts as an ETL (Extract, Transform, Load) to automatically suck the 3,665 real product entries directly from the Pandas Pickle object into the MySQL backend.

## 🏃 How to Run Locally

### 1. Database Setup
Ensure you have MySQL installed locally (e.g. via XAMPP or MySQL Workbench). 
Run the population script to dynamically create the schema `ecommerce_db` and insert products:
```bash
python setup_db.py
```

### 2. Start the Server
```bash
pip install -r requirements.txt
python app.py
```

Then navigate to `http://localhost:5000` in your web browser. 
Register a new account (using Customer ID `17850` optionally to test the collaborative engine directly), and begin browsing!
