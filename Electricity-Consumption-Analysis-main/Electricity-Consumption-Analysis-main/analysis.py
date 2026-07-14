import pandas as pd
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'electricity.db')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')

def load_data():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database {DB_PATH} not initialized.")
    conn = sqlite3.connect(DB_PATH)
    # Load into Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM Electricity", conn)
    # Ensure Dates are datetime objects in Pandas
    df['Dates'] = pd.to_datetime(df['Dates'])
    conn.close()
    return df

def generate_matplotlib_charts():
    df = load_data()
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # 1. Overall Trend Static Chart (Scenario 1)
    df_monthly = df.groupby(df['Dates'].dt.to_period('M'))['Usage'].sum().reset_index()
    df_monthly['Dates'] = df_monthly['Dates'].astype(str)
    
    plt.figure(figsize=(10, 5), facecolor='#0b0f19')
    ax = plt.axes()
    ax.set_facecolor('#111827')
    
    # Line Plot
    plt.plot(df_monthly['Dates'], df_monthly['Usage'], color='#3b82f6', marker='o', linewidth=2)
    
    # Highlight lockdown
    lockdown_indices = [i for i, x in enumerate(df_monthly['Dates']) if x in ['2020-03', '2020-04', '2020-05', '2020-06']]
    if lockdown_indices:
        plt.axvspan(lockdown_indices[0], lockdown_indices[-1], color='#ef4444', alpha=0.15, label='Lockdown Span')
        
    plt.title("National Monthly Power Consumption (Matplotlib)", color='#f3f4f6', fontsize=14, pad=15)
    plt.xlabel("Month", color='#9ca3af', fontsize=12)
    plt.ylabel("Electricity Consumed (MU)", color='#9ca3af', fontsize=12)
    plt.xticks(rotation=45, color='#9ca3af')
    plt.yticks(color='#9ca3af')
    
    # Grid & borders
    plt.grid(True, color='#ffffff0d', linestyle='--')
    for spine in ax.spines.values():
        spine.set_color('#ffffff1a')
        
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'matplotlib_trend.png'), dpi=150, facecolor='#0b0f19')
    plt.close()
    
    # 2. Regional Share Static Pie Chart (Scenario 2)
    df_regional = df.groupby('Regions')['Usage'].sum().reset_index()
    
    plt.figure(figsize=(6, 6), facecolor='#0b0f19')
    ax = plt.axes()
    ax.set_facecolor('#111827')
    
    colors = ['#3b82f6', '#8b5cf6', '#0d9488', '#f59e0b', '#ef4444']
    plt.pie(df_regional['Usage'], labels=df_regional['Regions'], colors=colors, autopct='%1.1f%%', 
            textprops={'color': '#f3f4f6', 'fontsize': 11}, startangle=140, 
            wedgeprops={'edgecolor': '#0b0f19', 'linewidth': 2})
            
    plt.title("Grid Region Electricity Distribution Share", color='#f3f4f6', fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'matplotlib_regions.png'), dpi=150, facecolor='#0b0f19')
    plt.close()
    print("Matplotlib static charts generated successfully.")

def get_scenario1_plotly():
    df = load_data()
    # Scenario 1: Timeline
    df_monthly = df.groupby(df['Dates'].dt.strftime('%Y-%m'))['Usage'].sum().reset_index()
    df_monthly.rename(columns={'Dates': 'Month'}, inplace=True)
    
    fig = px.line(df_monthly, x='Month', y='Usage', markers=True,
                  title="National Monthly Electricity Consumption (Interactive Plotly)")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Poppins',
        font_color='#f3f4f6',
        title_font_size=16,
        xaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)', color='#9ca3af'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)', color='#9ca3af'),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    fig.update_traces(line_color='#3b82f6', line_width=3, marker=dict(size=7, color='#3b82f6'))
    
    # Highlight lockdown span using shapes
    fig.add_vrect(
        x0="2020-03", x1="2020-06",
        fillcolor="rgba(239, 68, 68, 0.15)", opacity=0.8,
        layer="below", line_width=0,
        annotation_text="COVID Lockdown", annotation_position="top left",
        annotation_font=dict(color="#ef4444", size=10, family="Poppins")
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def get_scenario2_plotly():
    df = load_data()
    # Scenario 2: Regional variations
    df['Year'] = df['Dates'].dt.strftime('%Y')
    df_regional = df.groupby(['Regions', 'Year'])['Usage'].sum().reset_index()
    
    fig = px.bar(df_regional, x='Regions', y='Usage', color='Year', barmode='group',
                 color_discrete_map={'2019': '#3b82f6', '2020': '#8b5cf6'},
                 title="Regional YoY Usage Comparison")
                 
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Poppins',
        font_color='#f3f4f6',
        xaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)', color='#9ca3af'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)', color='#9ca3af'),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def get_scenario3_plotly():
    df = load_data()
    # Scenario 3: Recovery post-lockdown using NumPy vector operations
    # Define phases
    dates_np = df['Dates'].values
    usage_np = df['Usage'].values
    states_np = df['States'].values
    
    # Vectorized indexing
    pre_mask = dates_np < np.datetime64('2020-03-01')
    lock_mask = (dates_np >= np.datetime64('2020-03-01')) & (dates_np <= np.datetime64('2020-06-30'))
    post_mask = dates_np > np.datetime64('2020-06-30')
    
    # Top 5 states by total usage
    top_5_states = df.groupby('States')['Usage'].sum().nlargest(5).index.tolist()
    
    s3_data = []
    for state in top_5_states:
        state_mask = states_np == state
        
        pre_avg = np.mean(usage_np[state_mask & pre_mask])
        lock_avg = np.mean(usage_np[state_mask & lock_mask])
        post_avg = np.mean(usage_np[state_mask & post_mask])
        
        # Calculate recovery rate using numpy: (Post - Lockdown) / Pre
        recovery_pct = ((post_avg - lock_avg) / pre_avg) * 100
        
        s3_data.append({
            "State": state,
            "Pre-Lockdown Avg": round(pre_avg, 2),
            "Lockdown Avg": round(lock_avg, 2),
            "Post-Lockdown Avg": round(post_avg, 2),
            "Recovery Rate (%)": round(recovery_pct, 1)
        })
        
    df_s3 = pd.DataFrame(s3_data)
    
    # Generate interactive multi-bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Pre-Lockdown Avg', x=df_s3['State'], y=df_s3['Pre-Lockdown Avg'], marker_color='#0d9488'))
    fig.add_trace(go.Bar(name='Lockdown Avg', x=df_s3['State'], y=df_s3['Lockdown Avg'], marker_color='#ef4444'))
    fig.add_trace(go.Bar(name='Post-Lockdown Avg', x=df_s3['State'], y=df_s3['Post-Lockdown Avg'], marker_color='#3b82f6'))
    
    fig.update_layout(
        barmode='group',
        title="Post-Lockdown Recovery Averages for Top States",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Poppins',
        font_color='#f3f4f6',
        xaxis=dict(color='#9ca3af'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)', color='#9ca3af'),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder), df_s3.to_dict(orient='records')

# Import plotly inside methods to avoid namespace clash
import plotly
