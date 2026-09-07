# 🏛️ Global Government Budget Analytics Core

> **An interactive data analytics platform for analyzing government budgets, sector-wise spending, fiscal anomalies, volatility, correlations, and future budget trends.**

---

## 📌 Project Overview

**Global Government Budget Analytics Core** is a data engineering and business intelligence project designed to analyze historical government expenditure across countries and sectors.

The project combines:

- 🐍 **Python**
- 🗄️ **MySQL**
- 📊 **Streamlit**
- 📈 **Plotly**
- 🐼 **Pandas**
- 🔢 **NumPy**
- 🧮 **SQL Window Functions**

The system follows an:

**ETL → Database → Analytics → Dashboard**

architecture.

Raw government budget data is loaded from a CSV file, transformed and stored in a normalized MySQL database, and then analyzed through Python-based analytical modules and an interactive Streamlit dashboard.

---

# 🎯 Objectives

The main objectives of this project are:

- 📊 Analyze historical government budget trends
- 🌍 Compare spending across countries
- 🏛️ Understand sector-wise budget allocation
- 🔍 Identify unusual fiscal spending patterns
- 📉 Measure budget volatility over time
- 🔗 Analyze relationships between government sectors
- 🛡️ Compare civilian and defense expenditure
- 🔮 Forecast future budget trends

---

# ✨ Key Features

## 📊 Interactive Dashboard

The Streamlit dashboard provides multiple analytical sections for exploring government budget data.

### 📈 Macro Historical Trends

Visualizes total government expenditure over time and allows users to compare budget trends across different countries.

### 🥧 Sector Structural Analysis

Analyzes how government budgets are distributed among major sectors:

- 🛡️ Defense
- 🎓 Education
- 🏥 Health
- 🏗️ Infrastructure
- 🌾 Agriculture
- 🤝 Social Welfare
- 🏛️ State Transfers
- 💰 Interest Payments
- 🏢 Administration & Others

### 🔍 Fiscal Anomaly Detection

Uses **Z-score analysis** to identify years where government spending significantly differs from historical spending patterns.

### 🔬 Economic Research Lab

Provides advanced analytical capabilities including:

- Sector correlation analysis
- Budget volatility analysis
- Rolling statistics
- Trend analysis
- Polynomial forecasting
- Scenario-based projections

---

# 🧠 Analytical Modules

| Module | Purpose |
|---|---|
| `main_dashboard.py` | Main Streamlit dashboard |
| `advance_query.py` | Advanced SQL analytics and rolling trends |
| `budget_volatility.py` | Calculates 10-year budget volatility |
| `correlations.py` | Calculates Pearson sector correlations |
| `defense_social.py` | Compares civilian and defense spending |
| `forecasting_engine.py` | Forecasts future budgets using polynomial regression |
| `outlier_det.py` | Detects fiscal anomalies using Z-score |
| `python_sql.py` | ETL pipeline for CSV → MySQL |

---

# 🗂️ Project Structure

```text
global-budget-analytics/
│
├── 📄 main_dashboard.py
├── 📄 advance_query.py
├── 📄 budget_volatility.py
├── 📄 correlations.py
├── 📄 defense_social.py
├── 📄 forecasting_engine.py
├── 📄 outlier_det.py
├── 📄 python_sql.py
│
├── 📊 Master_Global_Budgets_Historical.csv
├── 📦 requirements.txt
├── 📘 README.md
│
└── 📸 screenshots/
    ├── dashboard.png
    ├── trends.png
    ├── sector_analysis.png
    ├── anomaly_detection.png
    └── analytics.png

```

---

# 📸 Project Screenshots


## 📈 Historical Budget Trends

![Macro Historical Trends](Screenshots/Macro_Historical_Trends.png)

---

## 🥧 Sector Analysis

![Allocation distribution Analysis](Screenshots/sector_analysis.png)

---

## 🔍 Fiscal Anomaly Detection

![Statistical Anomaly Detection](Screenshots/anomaly_detection.png)

---

## 🔬 Economic Research / Analytics

![Cross Sector Allocation Correlation](Screenshots/sector_allocation_correlation.png)
---
## 🔍 Rolling 10 year Volatility Index

![Rolling 10 year Volatility Index](Screenshots/volatility_index.png)

## 🧪 Ploynomial Project Analysis
---
![Ploynomial Project Analysis](Screenshots/polynomial_analytical.png)

---

# 🗄️ MySQL Database Setup

Open MySQL and create the database:

```sql
CREATE DATABASE global_budget_db;

USE global_budget_db;
```

Create the tables:

```sql
CREATE TABLE countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    year INT NOT NULL,
    total_budget_billions_usd FLOAT NOT NULL,

    FOREIGN KEY (country_id)
    REFERENCES countries(country_id)
);

CREATE TABLE sector_allocations (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    budget_id INT NOT NULL,
    sector_name VARCHAR(100) NOT NULL,
    allocated_percentage FLOAT,
    allocated_amount_billions_usd FLOAT,

    FOREIGN KEY (budget_id)
    REFERENCES budgets(budget_id)
);
```

---

# 🔄 ETL Pipeline

The project includes a Python ETL pipeline that:

```text
CSV Dataset
     ↓
Data Cleaning
     ↓
Transformation
     ↓
Country Dimension
     ↓
Budget Fact Table
     ↓
Sector Allocation Table
     ↓
MySQL Database
     ↓
Analytics
     ↓
Streamlit Dashboard
```

Run the ETL pipeline:

```bash
python python_sql.py
```

---

# 📊 Run the Dashboard

Start the Streamlit application:

```bash
streamlit run main_dashboard.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 📁 Dataset Structure

The CSV dataset should contain fields similar to:

| Column                        | Example |
| ----------------------------- | ------- |
| Country                       | India   |
| Year                          | 2023    |
| Total_Budget_Billions_USD     | 542.3   |
| Defense_Percentage            | 14.2    |
| Defense_Amount_Billions_USD   | 77.0    |
| Education_Percentage          | 12.5    |
| Education_Amount_Billions_USD | 67.8    |

The same percentage and amount pattern is used for the remaining sectors.

---

# 🧪 Run Individual Analytics

### ETL

```bash
python python_sql.py
```

### Advanced SQL Analysis

```bash
python advance_query.py
```

### Budget Volatility

```bash
python budget_volatility.py
```

### Sector Correlations

```bash
python correlations.py
```

### Defense vs Social Spending

```bash
python defense_social.py
```

### Forecasting

```bash
python forecasting_engine.py
```

### Anomaly Detection

```bash
python outlier_det.py
```

### Dashboard

```bash
streamlit run main_dashboard.py
```

---

# 🔐 Database Configuration

Update your MySQL credentials before running the project.

Example:

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="global_budget_db"
)
```

For SQLAlchemy:

```python
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:your_password@localhost/global_budget_db"
)
```

---

# 📦 Requirements

```text
Python 3.10+
MySQL 8.0+
Streamlit
Pandas
NumPy
Plotly
SQLAlchemy
mysql-connector-python
PyMySQL
```

---

# 📊 Example Insights

The platform can be used to answer questions such as:

* Which countries have the highest government expenditure?
* Which sector receives the largest share of the budget?
* How has government spending changed over time?
* Which countries show high budget volatility?
* Which fiscal years contain unusual spending patterns?
* Which sectors have strong positive or negative relationships?
* How does civilian spending compare with defense spending?
* What could future government budgets look like based on historical trends?

---

# 🔮 Future Improvements

Possible future enhancements include:

* [ ] Add authentication
* [ ] Deploy dashboard online
* [ ] Add live government budget data
* [ ] Add more countries and years
* [ ] Add machine-learning forecasting
* [ ] Add automated ETL scheduling
* [ ] Add downloadable reports
* [ ] Add advanced scenario simulation
* [ ] Move database credentials to environment variables

---
