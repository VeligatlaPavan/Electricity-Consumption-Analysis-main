# Project Overview

## Introduction

Electricity is one of the most important resources for industries, businesses, and households. 
Every day, a huge amount of electricity consumption data is generated across different states and regions. 
Analyzing this data manually is time-consuming and difficult. 
This project aims to analyze electricity consumption patterns using Oracle SQL, Tableau, and Flask to generate interactive dashboards and meaningful insights.

---

## Problem Statement

Large electricity consumption datasets contain thousands of records, making manual analysis difficult. 
Identifying high-consuming states, regional trends, and yearly consumption patterns becomes challenging without proper visualization tools. 
There is a need for an efficient system that can analyze and present electricity consumption data in an interactive and understandable format.

---

## Objectives

- Analyze electricity consumption across different Indian states.
- Compare electricity usage between different regions.
- Study yearly electricity consumption trends.
- Create interactive dashboards and stories using Tableau.
- Integrate Tableau dashboards into a Flask web application.

---

# Features of the Project

- Database Management
- Data Cleaning & Preparation
- Interactive Visualizations
- Interactive Dashboard
- Dynamic Filters
- Story Creation
- Performance Analysis
- Tableau Public Publishing
- Flask Web Integration
- Business Insights
- User-Friendly Interface
- Oracle SQL Database Integration
- CSV Dataset Analysis
- Time-based Trend Analysis

---

# System Architecture

```text
CSV Dataset
      │
      ▼
Oracle SQL Database
      │
      ▼
SQL Query Analysis
      │
      ▼
Tableau Dashboard & Story
      │
      ▼
Tableau Public Publishing
      │
      ▼
Flask Web Application
      │
      ▼
User
```

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Oracle SQL | Store and manage electricity consumption data |
| SQL | Perform data analysis and queries |
| Tableau | Create dashboards, stories, charts, and maps |
| Tableau Public | Publish dashboards online |
| Python Flask | Integrate Tableau into a web application |
| HTML | Design web pages |
| CSS | Style the web application |

---

# Working of the Project

### Step 1 – Data Collection

Electricity consumption data is collected in CSV format containing information about states, regions, dates, latitude, longitude, and electricity usage.

### Step 2 – Database Storage

The CSV dataset is imported into Oracle SQL Database, where the data is stored in a structured table.

### Step 3 – SQL Operations

Various SQL queries such as **SELECT, SUM, AVG, COUNT, GROUP BY, ORDER BY, HAVING, CASE Statements, Common Table Expressions (CTEs), and Window Functions** are executed to analyze electricity consumption patterns.

### Step 4 – Tableau Visualization

The Oracle database is connected to Tableau. Different visualizations including filled maps, bar charts, and pie charts are created. These visualizations are combined into an interactive dashboard and story.

### Step 5 – Publishing

The dashboard and story are published to Tableau Public.

### Step 6 – Flask Integration

The published Tableau dashboard and story are embedded into a Flask web application using HTML iframes, allowing users to access the visualizations through a simple website.

---

# Result

The project successfully analyzed electricity consumption data using Oracle SQL and Tableau. Interactive dashboards were created to visualize state-wise, region-wise, and year-wise electricity consumption. The dashboard provides filters, maps, pie charts, and bar charts that help users explore the data efficiently. The dashboard and story were successfully published to Tableau Public and integrated into a Flask web application.

---

# ✅ Conclusion

This project demonstrates how Oracle SQL, Tableau, and Flask can be integrated to transform raw electricity consumption data into meaningful visual insights. The developed dashboard makes it easier to compare electricity usage across states and regions and understand yearly trends. The Flask integration provides a simple web interface for accessing the dashboard and story, making the project user-friendly and effective for data analysis.
