# sci_dashboard.py
"""
SCI KPI Dashboard Module
This file contains all dashboard functionality as reusable functions.
Import and call sci_kpi_dashboard() from your login page.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from cleaner import load_cleaned_data
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# ==============================================
# CONSTANTS AND CONFIGURATION
# ==============================================

# Load environment variables
load_dotenv()

# Database configuration (using environment variables)
DB_CONFIG = {
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Stcs@9978"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "3306"),
    "name": os.getenv("DB_NAME", "sci_db")
}

# KPI columns
KPI_COLS = ["Total_Income", "DOE", "IOE", "PBT", "GOP"]
KPI_COLORS = {
    "Total_Income": "#1f77b4",
    "DOE": "#ff7f0e",
    "IOE": "#2ca02c",
    "PBT": "#d62728",
    "GOP": "#9467bd"
}

# Month names and ordering
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
MONTH_ORDER = {month: idx for idx, month in enumerate(MONTHS, start=1)}

# Quarter mapping
QUARTER_MAP = {
    "January": "Q1", "February": "Q1", "March": "Q1",
    "April": "Q2", "May": "Q2", "June": "Q2",
    "July": "Q3", "August": "Q3", "September": "Q3",
    "October": "Q4", "November": "Q4", "December": "Q4"
}

# ==============================================
# HELPER FUNCTIONS
# ==============================================

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        /* Main page styling */
        .main {
            background-color: #0e1117;
        }
        
        /* Header styling */
        .header {
            padding: 1rem 0;
            background: linear-gradient(90deg, #1a2a6c, #2a52be);
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: white;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .header h2 {
            color: #f0f0f0;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 300;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #1e2130;
            padding: 1rem;
            border-radius: 10px;
        }
        
        /* Card styling */
        .card {
            background-color: #1e2130;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #2a52be;
        }
        
        .card h3 {
            color: #ffffff;
            border-bottom: 1px solid #2a52be;
            padding-bottom: 0.5rem;
            margin-top: 0;
        }
        
        /* KPI summary styling */
        .kpi-card {
            background-color: #1e2130;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .kpi-title {
            font-size: 1rem;
            color: #a0a0a0;
            margin-bottom: 0.5rem;
        }
        
        .kpi-value {
            font-size: 1.4rem;
            font-weight: bold;
            color: #ffffff;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(90deg, #1a2a6c, #2a52be);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #1e2130 !important;
            border-radius: 5px 5px 0 0 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #2a52be !important;
            color: white !important;
        }
        
        /* Metric styling */
        .metric-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .metric-box {
            flex: 1;
            min-width: 200px;
            background: linear-gradient(135deg, #1e2130, #2a3a6c);
            border-radius: 10px;
            padding: 1.2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .metric-label {
            font-size: 1rem;
            color: #a0a0a0;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #ffffff;
        }
        
        /* Filter styling */
        .filter-box {
            background-color: #1e2130;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .filter-box h3 {
            color: #ffffff;
            margin-top: 0;
            border-bottom: 1px solid #2a52be;
            padding-bottom: 0.5rem;
        }
        
        /* Table styling */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
        
        .dataframe th {
            background-color: #2a52be !important;
            color: white !important;
        }
        
        .dataframe tr:nth-child(even) {
            background-color: #1e2130;
        }
        
        .dataframe tr:nth-child(odd) {
            background-color: #252a40;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def create_db_engine():
    """Create and cache database engine"""
    escaped_password = quote_plus(DB_CONFIG['password'])
    return create_engine(
        f"mysql+pymysql://{DB_CONFIG['user']}:{escaped_password}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}"
    )

@st.cache_data(ttl=3600)
def load_and_clean_data(_engine):
    """Load and clean data from database with caching"""
    try:
        df = pd.read_sql("SELECT * FROM kpi_data", con=_engine)
        
        # Data cleaning
        df['year'] = df['year'].astype(int)
        df['sector'] = df['sector'].astype(str).str.strip()
        df['vessel'] = df['vessel'].astype(str).str.strip()
        df = df.dropna(subset=['year', 'sector', 'vessel'])
        
        # Add month index and month-year columns
        df['month_index'] = df['month'].map(MONTH_ORDER)
        df["month_year"] = (
            df["year"].astype(str) + "-" + df["month_index"].astype(str).str.zfill(2)
        )
        df["month_year"] = pd.to_datetime(
            df["month_year"], format="%Y-%m"
        ).dt.strftime('%b %Y')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def display_kpi_summary(df, kpi_cols):
    """Display KPI summary cards"""
    totals = {col: df[col].sum() for col in kpi_cols}
    
    cols = st.columns(len(kpi_cols))
    for i, kpi in enumerate(kpi_cols):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">{kpi}</div>
                <div class="kpi-value">₹{-1*(totals[kpi]):,.2f} Lacs</div>
            </div>
            """, unsafe_allow_html=True)

def create_bar_chart(df, x, y, color=None, facet_col=None, 
                     barmode="group", text_auto=True, width=1000, facet_col_wrap=None):
    """Create standardized bar chart"""
    # Format bar text
    df["formatted_text"] = df[y].apply(lambda val: f"{-val:,.2f}")
    
    fig = px.bar(
        df,
        x=x,
        y=df[y]* -1,
        color=color,
        facet_col=facet_col,
        facet_col_wrap=facet_col_wrap,
        barmode=barmode,
        text="formatted_text",
        width=width,
        color_discrete_map=KPI_COLORS
    )
    
    fig.update_traces(textposition="inside", texttemplate="%{text}")
    fig.update_layout(
        bargap=0.15, 
        bargroupgap=0.05,
        xaxis_title=x.replace("_", " ").title(),
        yaxis_title="₹ (Lacs)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=False)    
    fig.update_yaxes(showgrid=True, gridcolor='#2a3a6c')
    return fig


def create_date_filters(df):
    """Create standardized date filters"""
    years = sorted(df['year'].unique().tolist())
    with st.sidebar.expander("📆 Date Range", expanded=True):
        from_year = st.selectbox("From Year", years, key="from_year")
        to_year = st.selectbox("To Year", [y for y in years if y >= from_year], key="to_year")
        from_month = st.selectbox("From Month", MONTHS, key="from_month")
        to_month = st.selectbox("To Month", 
                                [m for m in MONTHS if MONTH_ORDER[m] >= MONTH_ORDER[from_month]],
                                key="to_month")
    return from_year, to_year, from_month, to_month

def create_sector_vessel_filters(df):
    """Create sector and vessel filters"""
    sectors = sorted(df['sector'].unique().tolist())
    vessels = sorted(df['vessel'].unique().tolist())
    
    with st.sidebar.expander("🔍 Additional Filters", expanded=True):
        selected_sector = st.selectbox("Select Sector", ["All"] + sectors, key="sector")
        selected_vessel = st.selectbox("Select Vessel", ["All"] + vessels, key="vessel")
    
    return selected_sector, selected_vessel

def create_data_preview(df, title):
    """Create styled data preview"""
    with st.expander(f"📋 {title}", expanded=False):
        st.dataframe(df.style.format({col: "₹{:,.2f}" for col in KPI_COLS}))

def filter_data(df, year_range, month_range, sector, vessel):
    """Apply common filters to dataframe"""
    # Year filter
    filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Month filter (apply only if 'month' column is present)
    if 'month' in df.columns:
        from_idx = MONTH_ORDER[month_range[0]]
        to_idx = MONTH_ORDER[month_range[1]]
        months_in_range = [m for m in MONTHS if MONTH_ORDER[m] >= from_idx and MONTH_ORDER[m] <= to_idx]
        filtered = filtered[filtered['month'].isin(months_in_range)]

    # Sector filter
    if sector != "All":
        filtered = filtered[filtered['sector'] == sector]
    
    # Vessel filter
    if vessel != "All":
        filtered = filtered[filtered['vessel'] == vessel]
    
    return filtered

# ==============================================
# ANALYSIS FUNCTIONS
# ==============================================

def yearly_analysis(df):
    """Optimized yearly analysis"""
    # Create filters
    with st.sidebar.expander("🔍 Analysis Filters", expanded=True):
        years = sorted(df['year'].unique().tolist())
        from_year = st.selectbox("From Year", years, key="y_from_year")
        to_year = st.selectbox("To Year", [y for y in years if y >= from_year], key="y_to_year")
        selected_sector, selected_vessel = create_sector_vessel_filters(df)

    # Data processing
    grouped_df = df.groupby(['year', 'sector', 'vessel'])[KPI_COLS].sum().reset_index()
    
    # Filter data
    filtered_df = filter_data(
        grouped_df, 
        (from_year, to_year),
        ("January", "December"),  # Full year
        selected_sector,
        selected_vessel
    )
    
    # Display results
    render_analysis_results(filtered_df, "year", "Show Filtered Data")

def monthly_analysis(df):
    """Optimized monthly analysis"""
    # Create filters
    # Custom monthly filter logic:
    from_year, to_year = sorted(df['year'].unique().tolist())[0], sorted(df['year'].unique().tolist())[-1]
    with st.sidebar.expander("📆 Date Range", expanded=True):
        from_year = st.selectbox("From Year", sorted(df['year'].unique().tolist()), key="m_from_year")
        to_year = st.selectbox("To Year", [y for y in sorted(df['year'].unique().tolist()) if y >= from_year], key="m_to_year")
        if from_year == to_year:
            from_month = st.selectbox("From Month", MONTHS, key="m_from_month")
            to_month = st.selectbox("To Month", 
                                    [m for m in MONTHS if MONTH_ORDER[m] >= MONTH_ORDER[from_month]],
                                    key="m_to_month")
        else:
            selected_month = st.selectbox("Select One Month", MONTHS, key="m_only_month")
            from_month = to_month = selected_month
    selected_sector, selected_vessel = create_sector_vessel_filters(df)
    
    # Data processing
    grouped_df = df.groupby(['year', 'month', 'sector', 'vessel'])[KPI_COLS].sum().reset_index()
    grouped_df["month_index"] = grouped_df["month"].map(MONTH_ORDER)
    grouped_df["month_year"] = (
        grouped_df["year"].astype(str) + "-" +
        grouped_df["month_index"].astype(str).str.zfill(2)
    )
    grouped_df["month_year"] = pd.to_datetime(
        grouped_df["month_year"], format="%Y-%m"
    ).dt.strftime('%b %Y')
    
    # Filter data
    filtered_df = filter_data(
        grouped_df,
        (from_year, to_year),
        (from_month, to_month),
        selected_sector,
        selected_vessel
    )
    
    # Display results
    x_axis = "month_year" if from_year == to_year else "year"
    render_analysis_results(filtered_df, x_axis, "Show Filtered Monthly Data",barmode="stack")

def quarterly_analysis(df):
    """Optimized quarterly analysis"""
    # Define quarter options
    quarter_options = ["Q1", "Q2", "Q3", "Q4"]
    
    # Create filters
    with st.sidebar.expander("🔍 Analysis Filters", expanded=True):
        years = sorted(df['year'].unique().tolist())
        from_year = st.selectbox("From Year", years, key="q_from_year")
        to_year = st.selectbox("To Year", [y for y in years if y >= from_year], key="q_to_year")
        
        # Quarter selection
        if from_year == to_year:
            selected_quarters = st.multiselect("Select Quarter(s)", quarter_options, default=quarter_options)
        else:
            selected_quarter = st.selectbox("Select Quarter", quarter_options)
            selected_quarters = [selected_quarter]
        
        selected_sector, selected_vessel = create_sector_vessel_filters(df)
    
    # Data processing
    df["quarter"] = df["month"].map(QUARTER_MAP)
    grouped_df = df.groupby(["year", "quarter", "sector", "vessel"])[KPI_COLS].sum().reset_index()
    grouped_df["quarter_year"] = grouped_df["quarter"] + " " + grouped_df["year"].astype(str)

    # Filter data
    filtered_df = grouped_df[
        (grouped_df["year"] >= from_year) &
        (grouped_df["year"] <= to_year) &
        (grouped_df["quarter"].isin(selected_quarters))
    ]
    
    if selected_sector != "All":
        filtered_df = filtered_df[filtered_df["sector"] == selected_sector]
    if selected_vessel != "All":
        filtered_df = filtered_df[filtered_df["vessel"] == selected_vessel]

    # Display results
    x_axis = "quarter" if from_year == to_year else "year"
    render_analysis_results(filtered_df, x_axis, "Show Filtered Quarterly Data")

def sector_wise_analysis(df):
    """Optimized sector-wise analysis"""
    from_year, to_year, from_month, to_month = create_date_filters(df)
    sectors = sorted(df['sector'].unique().tolist())
    with st.sidebar.expander("🔍 Additional Filters", expanded=True):
        if from_year == to_year:
            selected_sectors = st.multiselect("Select Sector(s)", sectors, default=sectors, key="sector_only_multi")
        else:
            selected_sector = st.selectbox("Select One Sector", sectors, key="sector_only_single")
            selected_sectors = [selected_sector]
    # Data processing
    grouped_df = df.groupby(['year', 'sector', 'month'])[KPI_COLS].sum().reset_index()
    # Filter data
    filtered_df = filter_data(
        grouped_df,
        (from_year, to_year),
        (from_month, to_month),
        "All",  # Sector will be filtered below
        "All"   # All vessels
    )
    if selected_sectors != ["All"]:
        filtered_df = filtered_df[filtered_df["sector"].isin(selected_sectors)]
    # Display results
    x_axis = "sector" if from_year == to_year else "year"
    render_analysis_results(filtered_df,x_axis,"Show Filtered Sector-wise Data",barmode="stack")

def vessel_wise_analysis(df):
    """Optimized vessel-wise analysis"""
    from_year, to_year, from_month, to_month = create_date_filters(df)
    vessels = sorted(df['vessel'].unique().tolist())
    with st.sidebar.expander("🔍 Additional Filters", expanded=True):
        if from_year == to_year:
            selected_vessels = st.multiselect("Select Vessel(s)", vessels, default=vessels, key="vessel_only")
        else:
            selected_vessel = st.selectbox("Select One Vessel", vessels, key="vessel_only_single")
            selected_vessels = [selected_vessel]
    # Data processing
    grouped_df = df.groupby(['year', 'vessel', 'month'])[KPI_COLS].sum().reset_index()
    # Filter data
    filtered_df = filter_data(
        grouped_df,
        (from_year, to_year),
        (from_month, to_month),
        "All",  # All sectors
        "All"  # We'll filter vessel(s) below
    )
    if selected_vessels != ["All"]:
        filtered_df = filtered_df[filtered_df["vessel"].isin(selected_vessels)]
    # Display results
    x_axis = "vessel" if from_year == to_year else "year"
    render_analysis_results(filtered_df, x_axis, "Show Filtered Vessel-wise Data",barmode="stack")

def render_analysis_results(df, x_axis, preview_title,barmode="group"):
    """Render common analysis results (replaces repeated code)"""
    if df.empty:
        st.warning("⚠️ No data matches your filter criteria.")
        return
    display_kpi_summary(df, KPI_COLS)
    
    # KPI Trends
    st.markdown("### 📈 KPI Trends")
    viz_type = st.radio("Chart Type", ["Multi-KPI Bar Chart", "Table"], horizontal=True, index=0, key=f"viz_{x_axis}")
    
    if viz_type == "Multi-KPI Bar Chart":
        aggregated_df = df.groupby(x_axis)[KPI_COLS].sum().reset_index()
        long_df = pd.melt(aggregated_df, id_vars=[x_axis], value_vars=KPI_COLS,
                          var_name="KPI", value_name="Value")
        fig = create_bar_chart(long_df, x=x_axis, y="Value", color="KPI",barmode=barmode)
        if x_axis == "year":
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(df.style.format({col: "₹{:,.2f}" for col in KPI_COLS}))
    
    # Individual KPI analysis
    st.markdown("### 📊 Individual KPI Analysis")
    for kpi in KPI_COLS:
        st.markdown(f"#### {kpi} Trend")
        tab1, tab2 = st.tabs(["📊 Chart", "📋 Data"])
        
        kpi_df = df[[x_axis, kpi]].groupby(x_axis).sum().reset_index()
        kpi_df["value"] = kpi_df[kpi].apply(lambda val: f"{-val:,.2f}")
        
        with tab1:
            fig = px.bar(
                kpi_df, 
                x=x_axis, 
                y=kpi_df[kpi]* -1,
                text="value",
                color_discrete_sequence=[KPI_COLORS[kpi]]
            )
            if x_axis == "year":
                fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
            fig.update_traces(width=0.7)
            fig.update_layout(
                title=f"{kpi} Trend",
                xaxis_title=x_axis.replace("_", " ").title(),
                yaxis_title="₹ (Lacs)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            st.dataframe(kpi_df.style.format({kpi: "₹{:,.2f}"}))

def handle_csv_upload(engine):
    """Handle CSV upload functionality"""
    st.markdown("## 📤 Upload Weekly KPI CSV File")
    uploaded_file = st.file_uploader("Upload your KPI CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df_uploaded = load_cleaned_data(uploaded_file)
            df_uploaded.to_sql("kpi_data", con=engine, if_exists='append', index=False)
            st.success(f"✅ Uploaded and saved {len(df_uploaded)} rows to the database.")
            
            # Clear cache to show updated data
            st.cache_data.clear()
            
            # Display uploaded data
            with st.expander("View Uploaded Data", expanded=True):
                st.dataframe(df_uploaded.style.format({col: "₹{:,.2f}" for col in KPI_COLS}))
        except Exception as e:
            st.error(f"❌ Failed to process: {e}")

# ==============================================
# MAIN DASHBOARD FUNCTION - CALL THIS FROM LOGIN PAGE
# ==============================================

def sci_kpi_dashboard():
    """
    Main SCI KPI Dashboard function.
    Call this function from your login page after successful authentication.
    
    Usage:
        from sci_dashboard import sci_kpi_dashboard
        
        # After login success:
        sci_kpi_dashboard()
    """
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize database engine
    engine = create_db_engine()
    
    # Main header
    st.markdown("""
    <div class="header">
        <h1>SCI Analysis Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h2>⛴️ Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio("Choose Action", ["📤 Upload CSV", "📊 KPI Dashboard"])
    
    if page == "📤 Upload CSV":
        handle_csv_upload(engine)
        return
    
    # Main dashboard - Load data
    df_cleaned = load_and_clean_data(engine)
    
    # Report type selection
    st.markdown("### 📁 Select Report Type to Continue")
    report_type = st.selectbox("Choose analysis type:", [
        "Select...", 
        "📅 Yearly Analysis", 
        "📆 Monthly Analysis", 
        "🔄 Quarterly Analysis",
        "🌐 Sector-wise Analysis", 
        "🚢 Vessel-wise Analysis"
    ])
    
    # Route to analysis
    analysis_functions = {
        "📅 Yearly Analysis": yearly_analysis,
        "📆 Monthly Analysis": monthly_analysis,
        "🔄 Quarterly Analysis": quarterly_analysis,
        "🌐 Sector-wise Analysis": sector_wise_analysis,
        "🚢 Vessel-wise Analysis": vessel_wise_analysis
    }
    
    if report_type in analysis_functions:
        analysis_functions[report_type](df_cleaned)