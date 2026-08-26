import pandas as pd
import numpy as np
import urllib.parse
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global Budget Analytics Core",
    page_icon="🏛️",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. CACHED DATABASE ENGINE & DATA LOADERS
# -----------------------------------------------------------------------------
@st.cache_resource
def get_engine():
    """
    Creates and caches the SQLAlchemy database engine connection pool.
    """
    password_quoted = urllib.parse.quote_plus("root23")
    return create_engine(
        f"mysql+mysqlconnector://root:{password_quoted}@localhost/global_budget_db",
        pool_pre_ping=True
    )

@st.cache_data(ttl=3600)
def get_countries():
    """
    Fetches available country names with 1-hour cache.
    """
    engine = get_engine()
    query = "SELECT country_name FROM countries ORDER BY country_name"
    return pd.read_sql_query(query, engine)

# -----------------------------------------------------------------------------
# 3. HEADER & SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.title("🏛️ Global Government Budget Analytics Core")
st.markdown(
    "An interactive platform exploring public finance shifts, sector dominance, and predictive trajectories."
)

try:
    countries_df = get_countries()
    country_list = countries_df["country_name"].tolist()
    
    selected_country = st.sidebar.selectbox(
        "Select a Country to Filter", 
        country_list
    )
except Exception as e:
    st.sidebar.error("Database connection error.")
    st.error(f"**Failed to load country list from database:** {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 4. NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_macro, tab_sectors, tab_anomalies, tab_research_lab = st.tabs([
    "📈 Macro Historical Trends",
    "🍕 Sector Structural Spreads",
    "🔍 Statistical Anomalies",
    "🔬 Macro Economic Research Lab",
])

# --- TAB 1: MACRO HISTORICAL TRENDS ---
with tab_macro:
    st.header("Global Spending Growth Pathways")
    engine = get_engine()
    q_macro = """
        SELECT b.year, b.total_budget_billions_usd
        FROM budgets b 
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s 
        ORDER BY b.year
    """
    df_macro = pd.read_sql_query(q_macro, engine, params=(selected_country,))

    if not df_macro.empty:
        fig_macro = px.line(
            df_macro,
            x="year",
            y="total_budget_billions_usd",
            title=f"Historical Expenditure Strategy: {selected_country}",
            template="plotly_dark",
            labels={
                "total_budget_billions_usd": "Total Budget (Billions USD)"
            },
        )
        st.plotly_chart(fig_macro, use_container_width=True)
    else:
        st.info("No macro expenditure records found for the selected country.")

# --- TAB 2: SECTOR STRUCTURAL SPREADS (FIXED) ---
with tab_sectors:
    st.header("Allocation Distribution Analysis")
    engine = get_engine()
    
    # Calculate amount dynamically to avoid missing column errors
    q_sec = """
        SELECT
            b.year,
            sa.sector_name,
            sa.allocated_percentage,
            (sa.allocated_percentage / 100.0) * b.total_budget_billions_usd AS allocated_amount_billions_usd
        FROM sector_allocations sa
        JOIN budgets b ON sa.budget_id = b.budget_id
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s
    """
    df_sec = pd.read_sql_query(q_sec, engine, params=(selected_country,))

    if not df_sec.empty:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fig_pie = px.pie(
                df_sec,
                values="allocated_percentage",
                names="sector_name",
                title=f"Sector Distribution Breakdown: {selected_country}",
                template="plotly_dark",
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_c2:
            fig_bar = px.bar(
                df_sec,
                x="year",
                y="allocated_amount_billions_usd",
                color="sector_name",
                title="Sector Allocation Trajectory Over Time",
                template="plotly_dark",
                labels={"allocated_amount_billions_usd": "Allocated Budget (Billions USD)"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No sector allocation records found for this country.")

# --- TAB 3: STATISTICAL ANOMALIES ---
with tab_anomalies:
    st.header("Descriptive Outlier Detection")
    st.markdown(
        "Identifies fiscal years where spending shifted sharply outside normal historical baselines."
    )

    if not df_macro.empty:
        mean_val = df_macro["total_budget_billions_usd"].mean()
        std_val = df_macro["total_budget_billions_usd"].std()

        if std_val > 0:
            df_macro["z_score"] = (df_macro["total_budget_billions_usd"] - mean_val) / std_val
        else:
            df_macro["z_score"] = 0.0

        anomalies = df_macro[df_macro["z_score"].abs() > 1.96]

        st.write("### Flagged Fiscal Outlier Periods (|Z-Score| > 1.96):")
        if not anomalies.empty:
            st.dataframe(
                anomalies.style.background_gradient(
                    cmap="Reds", subset=["total_budget_billions_usd"]
                ),
                use_container_width=True,
            )
        else:
            st.success(
                "Excellent budget structural stability! No extreme statistical outliers discovered."
            )
    else:
        st.info("Insufficient data available to compute Z-score anomalies.")

# --- TAB 4: MACRO ECONOMIC RESEARCH LAB ---
with tab_research_lab:
    st.header("🔬 Deep Exploratory Research Workspace")
    st.markdown(
        "Advanced analytical modules calculating structural correlation shifts and spending volatility."
    )

    # 1. Cross-Sector Correlation Matrix
    st.subheader("Cross-Sector Allocation Correlation Matrix")
    engine = get_engine()
    q_corr = """
        SELECT b.year, sa.sector_name, sa.allocated_percentage
        FROM sector_allocations sa
        JOIN budgets b ON sa.budget_id = b.budget_id
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s
    """
    df_corr_raw = pd.read_sql_query(q_corr, engine, params=(selected_country,))

    if not df_corr_raw.empty:
        df_corr = (
            df_corr_raw.groupby(["year", "sector_name"], as_index=False)[
                "allocated_percentage"
            ]
            .mean()
            .sort_values(["year", "sector_name"])
        )

        pivot_corr = (
            df_corr.pivot(
                index="year",
                columns="sector_name",
                values="allocated_percentage",
            )
            .dropna(axis=1, how="all")
            .dropna(axis=0, how="all")
        )

        if pivot_corr.shape[1] >= 2 and pivot_corr.shape[0] >= 2:
            matrix_corr = pivot_corr.corr()
            fig_corr = px.imshow(
                matrix_corr, text_auto=True, template="plotly_dark"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info(
                "Not enough distinct sector data points to build a correlation matrix for this country."
            )

    # 2. Volatility Index Calculation
    st.subheader("Rolling 10-Year Volatility Index")
    engine = get_engine()
    q_vol = """
        SELECT b.year, b.total_budget_billions_usd
        FROM budgets b 
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s 
        ORDER BY b.year ASC
    """
    df_vol = pd.read_sql_query(q_vol, engine, params=(selected_country,))

    if not df_vol.empty:
        df_vol = df_vol.sort_values("year")
        df_vol["rolling_mean"] = (
            df_vol["total_budget_billions_usd"].rolling(window=10).mean()
        )
        df_vol["rolling_std"] = (
            df_vol["total_budget_billions_usd"].rolling(window=10).std()
        )
        df_vol["volatility_index"] = (
            df_vol["rolling_std"] / df_vol["rolling_mean"]
        ) * 100

        fig_vol = go.Figure()
        fig_vol.add_trace(
            go.Scatter(
                x=df_vol["year"],
                y=df_vol["volatility_index"],
                mode="lines+markers",
                name="Volatility Index",
                line=dict(color="#FFA500"),
            )
        )
        fig_vol.update_layout(
            template="plotly_dark", yaxis_title="Volatility Index (%)"
        )
        st.plotly_chart(fig_vol, use_container_width=True)

        st.write("Recent Rolling Statistics (Non-null rows):")
        st.dataframe(
            df_vol.dropna().tail(10), use_container_width=True
        )
    else:
        st.info(
            "Not enough historical data to compute rolling volatility metrics."
        )

    # 3. Polynomial Projection (Analytical)
    st.subheader("Polynomial Projection (Analytical)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        proj_degree = st.selectbox("Projection degree", [1, 2, 3], index=1)
        proj_horizon = st.number_input(
            "Forecast horizon year",
            min_value=2025,
            max_value=2050,
            value=2035,
        )
    with col_p2:
        apply_scenario = st.checkbox("Apply scenario shock to projection")
        shock_pct = st.slider("Shock %", -50, 100, 0)

    if not df_vol.empty:
        x = df_vol["year"].astype(int).values
        y = df_vol["total_budget_billions_usd"].astype(float).values
        
        if len(x) > proj_degree:
            coeffs = np.polyfit(x, y, deg=proj_degree)
            poly = np.poly1d(coeffs)
            years_future = np.arange(int(x.max()) + 1, int(proj_horizon) + 1)
            proj_vals = poly(years_future)
            
            if apply_scenario and shock_pct != 0:
                proj_vals = proj_vals * (1 + shock_pct / 100.0)

            fig_proj = go.Figure()
            fig_proj.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="markers+lines",
                    name="Historical Baseline",
                    marker=dict(color="#888888"),
                )
            )
            fig_proj.add_trace(
                go.Scatter(
                    x=years_future,
                    y=proj_vals,
                    mode="lines",
                    name="Projection",
                    line=dict(color="#00FFAA", dash="dash"),
                )
            )
            fig_proj.update_layout(
                title=f"Polynomial Projection (Degree {proj_degree}) for {selected_country}",
                template="plotly_dark",
                xaxis_title="Year",
                yaxis_title="Total Budget (Billions USD)",
            )
            st.plotly_chart(fig_proj, use_container_width=True)

            df_proj_out = pd.DataFrame(
                {"year": years_future, "projected_budget": proj_vals}
            )
            st.dataframe(
                df_proj_out.style.format(
                    {"projected_budget": "${:,.2f}"}
                ),
                use_container_width=True,
            )
        else:
            st.warning(
                "Not enough historical data points for the selected polynomial degree."
            )
