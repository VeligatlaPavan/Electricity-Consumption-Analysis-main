import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'electricity.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), 'Consumption.csv')

def init_db():
    print(f"Initializing database from {CSV_PATH} using Pandas...")
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found!")
        return False

    try:
        # Load dataset with Pandas
        df = pd.read_csv(CSV_PATH)
        
        # Clean columns: rename latitude/longitude to match exactly, format dates
        df.rename(columns={'latitude': 'Latitude', 'longitude': 'Longitude'}, inplace=True)
        
        # Convert date to standard ISO format (YYYY-MM-DD)
        # In the CSV it is typically DD-MM-YYYY
        df['Dates'] = pd.to_datetime(df['Dates'], format='mixed', dayfirst=True)
        df['Dates'] = df['Dates'].dt.strftime('%Y-%m-%d')
        
        # Fill missing values
        df['Latitude'] = df['Latitude'].fillna(0.0)
        df['Longitude'] = df['Longitude'].fillna(0.0)
        df['Usage'] = pd.to_numeric(df['Usage'], errors='coerce').fillna(0.0)
        
        # Connect and save
        conn = sqlite3.connect(DB_PATH)
        
        # Save dataframe to SQL table, replacing if it already exists
        df.to_sql('Electricity', conn, if_exists='replace', index=False)
        
        # Verify load
        count = pd.read_sql_query("SELECT COUNT(*) FROM Electricity", conn).iloc[0, 0]
        print(f"Successfully loaded {count} rows into the database table 'Electricity' using Pandas.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == '__main__':
    init_db()
