import mysql.connector
import pandas as pd
import numpy as np


def generate_statistical_forecast(country_name, target_year=2035, degree=2):
    """
    Fits an n-degree polynomial trend line to historical data
    using NumPy and projects it to a future year.
    """

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root23",
        database="global_budget_db"
    )

    query = """
    SELECT
        b.year,
        b.total_budget_billions_usd
    FROM budgets b
    JOIN countries c
        ON b.country_id = c.country_id
    WHERE c.country_name = %s
    ORDER BY b.year ASC;
    """

    df = pd.read_sql(query, conn, params=(country_name,))
    conn.close()

    if df.empty:
        return None, None

    # Extract historical arrays
    x_hist = df["year"].values
    y_hist = df["total_budget_billions_usd"].values

    # Mathematical Curve Fitting Via Least Squares
    # Fits: y = w0 + w1*x + w2*x^2 + ... + wn*x^n

    coefficients = np.polyfit(x_hist, y_hist, deg=degree)

    polynomial_model = np.poly1d(coefficients)

    # Historical fitted trend
    df["trend_fit"] = polynomial_model(x_hist)

    # Forecast future years
    future_years = np.arange(x_hist.max() + 1, target_year + 1)

    future_predictions = polynomial_model(future_years)

    df_forecast = pd.DataFrame({
        "year": future_years,
        "forecasted_budget": future_predictions
    })

    print(
        f"\n---  Pure Analytical Projections for "
        f"{country_name} ({x_hist.max()+1}-{target_year}) ---"
    )

    print(df_forecast.head(10))

    return df, df_forecast


if __name__ == "__main__":
    # Test a quadratic projection
    hist_fit, future_proj = generate_statistical_forecast(
        "India",
        target_year=2035,
        degree=2
    )