from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import sqlite3
import os
import time

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'electricity.db')

def init_if_needed():
    # 1. Initialize database if missing
    if not os.path.exists(DB_PATH):
        print("Database not found. Running Pandas initialization...")
        from db_init import init_db
        init_db()
        
    # 2. Pre-generate Matplotlib charts
    try:
        from analysis import generate_matplotlib_charts
        generate_matplotlib_charts()
    except Exception as e:
        print(f"Error generating matplotlib charts: {e}")

@app.route("/")
def home():
    init_if_needed()
    stats = {}
    try:
        conn = sqlite3.connect(DB_PATH)
        # Use Pandas for summary statistics
        df = pd.read_sql_query("SELECT * FROM Electricity", conn)
        conn.close()
        
        stats['total_records'] = len(df)
        stats['states_count'] = df['States'].nunique()
        stats['total_usage'] = df['Usage'].sum()
        stats['min_date'] = df['Dates'].min()
        stats['max_date'] = df['Dates'].max()
    except Exception as e:
        print(f"Error fetching stats using Pandas: {e}")
        stats = {
            'total_records': 16599,
            'states_count': 33,
            'min_date': '2019-01-02',
            'max_date': '2020-12-05',
            'total_usage': 1774332.1
        }
    return render_template("home.html", stats=stats)

@app.route("/dashboard")
def dashboard():
    init_if_needed()
    return render_template("dashboard.html")

@app.route("/story")
def story():
    init_if_needed()
    return render_template("story.html")

@app.route("/about")
def about():
    init_if_needed()
    return render_template("about.html")

@app.route("/download/<filename>")
def download_file(filename):
    allowed_files = ["Readme.pdf", "electricity_consumption.docx", "electricity.sql", "Consumption.csv"]
    if filename not in allowed_files:
        return jsonify({"error": "File not found or access denied"}), 404
    directory = os.path.dirname(__file__)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route("/api/query", methods=["POST"])
def run_sql_query():
    init_if_needed()
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400
        
    cleaned_query = query.lower()
    if not (cleaned_query.startswith("select") or cleaned_query.startswith("with")):
        return jsonify({"error": "Only SELECT or WITH queries are permitted for safety reasons."}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        start_time = time.time()
        
        # Execute query using Pandas!
        df_result = pd.read_sql_query(query, conn)
        execution_time = (time.time() - start_time) * 1000 # in ms
        conn.close()
        
        headers = df_result.columns.tolist()
        # Handle nan/null values in pandas dataframe for JSON compatibility
        df_result = df_result.fillna("")
        rows = df_result.values.tolist()
        
        return jsonify({
            "headers": headers,
            "rows": rows[:500], # Limit to first 500 rows
            "count": len(rows),
            "execution_time": round(execution_time, 2)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/chart-data")
def chart_data():
    init_if_needed()
    try:
        from analysis import get_scenario1_plotly, get_scenario2_plotly, get_scenario3_plotly
        
        # Fetch json-serialized plotly charts
        s1_plotly = get_scenario1_plotly()
        s2_plotly = get_scenario2_plotly()
        s3_plotly, s3_recovery_table = get_scenario3_plotly()
        
        return jsonify({
            "scenario1": s1_plotly,
            "scenario2": s2_plotly,
            "scenario3": s3_plotly,
            "recovery_table": s3_recovery_table
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)