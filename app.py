# ==============================================================================
# NETFLIX ANALYTICS - STREAMLIT DASHBOARD
# ==============================================================================
# Project Title: Netflix Data Analysis Using Python
# Author       : Data Analytics Intern
# Technology   : Python, Streamlit, Pandas, NumPy, Plotly, Matplotlib, Seaborn
# Design Theme : Premium Netflix Red & Black (#141414, #E50914, #222222)
# ==============================================================================

import os
import re
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------------------
# 1. STREAMLIT APP CONFIGURATION & NETFLIX THEME
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="NETFLIX ANALYTICS",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Netflix CSS Styling
st.markdown(
    """
    <style>
    /* Main Background & Text */
    .stApp {
        background-color: #141414;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Fixed Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0B0B0B;
        border-right: 1px solid #222222;
    }

    /* Sidebar Logo */
    .netflix-logo {
        font-size: 30px;
        font-weight: 900;
        color: #E50914;
        letter-spacing: 3px;
        margin-bottom: 0px;
        text-transform: uppercase;
        font-family: 'Impact', 'Bebas Neue', sans-serif;
    }
    .netflix-sub {
        font-size: 11px;
        color: #888888;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 18px;
        font-weight: 600;
    }

    /* Main Page Header */
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 14px;
        border-bottom: 1px solid #333333;
        margin-bottom: 22px;
    }
    .brand-title {
        font-size: 32px;
        font-weight: 900;
        color: #E50914;
        letter-spacing: 2.5px;
        margin: 0;
        text-transform: uppercase;
        font-family: 'Impact', 'Bebas Neue', sans-serif;
    }
    .brand-title span {
        color: #FFFFFF;
    }
    .brand-sub {
        font-size: 13px;
        color: #B3B3B3;
        margin-top: 4px;
        margin-bottom: 0;
    }
    .status-badge {
        background-color: #162415;
        color: #46D369;
        border: 1px solid #224D20;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background-color: #222222;
        border: 1px solid #333333;
        border-top: 3px solid #E50914;
        border-radius: 8px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-top 0.2s ease;
        margin-bottom: 12px;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        border-top: 3px solid #FF1E27;
        box-shadow: 0 6px 16px rgba(229, 9, 20, 0.25);
    }
    .kpi-icon {
        font-size: 22px;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        margin: 4px 0;
    }
    .kpi-label {
        font-size: 11px;
        color: #B3B3B3;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Callout & Observation Boxes */
    .observation-box {
        background: #1C1C1C;
        border-left: 4px solid #E50914;
        border-radius: 6px;
        padding: 14px 18px;
        margin-top: 15px;
        margin-bottom: 15px;
        border-top: 1px solid #2E2E2E;
        border-right: 1px solid #2E2E2E;
        border-bottom: 1px solid #2E2E2E;
    }
    .observation-title {
        font-size: 14px;
        font-weight: 700;
        color: #E50914;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .observation-text {
        font-size: 13.5px;
        color: #CCCCCC;
        line-height: 1.5;
        margin: 0;
    }

    /* Business Insight Card */
    .insight-card {
        background: #222222;
        border: 1px solid #333333;
        border-left: 4px solid #E50914;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    .insight-title {
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    .insight-text {
        font-size: 13.5px;
        color: #CCCCCC;
        line-height: 1.55;
    }

    /* Recommendation Card */
    .rec-card {
        background: #1A212D;
        border: 1px solid #2A3B52;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    .rec-title {
        font-size: 16px;
        font-weight: 700;
        color: #60A5FA;
        margin-bottom: 6px;
    }
    .rec-text {
        font-size: 13.5px;
        color: #E2E8F0;
        line-height: 1.55;
    }

    /* Streamlit Widget Elements */
    .stSelectbox label, .stTextInput label {
        color: #E5E5E5 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    div[data-baseweb="select"] {
        background-color: #222222 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="input"] {
        background-color: #222222 !important;
        border-radius: 6px !important;
    }
    .stRadio label {
        color: #E5E5E5 !important;
    }

    /* Hide standard Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------------------
# 2. DATA LOADING & CACHING FUNCTION
# ------------------------------------------------------------------------------
@st.cache_data
def load_netflix_data():
    """
    Safely loads Netflix dataset.
    Checks results/cleaned_netflix.csv first; falls back to data/Dataset.csv.
    """
    cleaned_file = os.path.join("results", "cleaned_netflix.csv")
    raw_file = os.path.join("data", "Dataset.csv")

    if os.path.exists(cleaned_file):
        df_loaded = pd.read_csv(cleaned_file)
    elif os.path.exists(raw_file):
        df_loaded = pd.read_csv(raw_file)
        # Perform standard cleaning if raw was loaded
        for col in df_loaded.select_dtypes(include="object").columns:
            df_loaded[col] = df_loaded[col].astype(str).str.strip()
        df_loaded["director"] = df_loaded["director"].replace("Not Given", np.nan)
        df_loaded["country"] = df_loaded["country"].replace("Not Given", np.nan)
    else:
        return None

    # Ensure date_added is converted to datetime
    if "date_added" in df_loaded.columns:
        df_loaded["date_added"] = pd.to_datetime(df_loaded["date_added"], errors="coerce")

    return df_loaded


# Standard Plotly Dark Layout Formatter
def format_dark_chart(fig, title=""):
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=14, color="#FFFFFF", family="Helvetica, Arial"),
            x=0.01,
            y=0.96,
        ),
        paper_bgcolor="#222222",
        plot_bgcolor="#222222",
        font=dict(color="#B3B3B3", family="Helvetica, Arial", size=11),
        margin=dict(l=35, r=25, t=45, b=35),
        xaxis=dict(
            gridcolor="#333333",
            showline=True,
            linecolor="#444444",
            tickfont=dict(color="#B3B3B3", size=10),
        ),
        yaxis=dict(
            gridcolor="#333333",
            showline=True,
            linecolor="#444444",
            tickfont=dict(color="#B3B3B3", size=10),
        ),
        hoverlabel=dict(
            bgcolor="#141414", font_size=12, font_family="Helvetica, Arial"
        ),
        legend=dict(
            font=dict(color="#FFFFFF", size=10),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
    )
    return fig


# ------------------------------------------------------------------------------
# 3. LOAD DATA & INITIALIZE
# ------------------------------------------------------------------------------
df = load_netflix_data()

if df is None:
    st.error("⚠️ Dataset not found! Please ensure 'data/Dataset.csv' exists.")
    st.stop()


# ------------------------------------------------------------------------------
# 4. SIDEBAR - BRANDING & NAVIGATION
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="netflix-logo">NETFLIX</div>', unsafe_allow_html=True)
    st.markdown('<div class="netflix-sub">DATA ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

    # 9 Navigation Pages
    pages = [
        "📊 Overview",
        "🎬 Content Analysis",
        "🌍 Country Analysis",
        "📅 Release Year Analysis",
        "🎭 Genre Analysis",
        "🏷️ Rating Analysis",
        "🔍 Dataset Explorer",
        "💡 Business Insights",
        "ℹ️ About Project",
    ]
    selected_page = st.radio("Navigation", pages, label_visibility="collapsed")

    st.markdown("---")
    st.caption("Developed for Data Analytics Internship Evaluation.")


# ------------------------------------------------------------------------------
# 5. UNIVERSAL HEADER SECTION
# ------------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="main-header">
        <div>
            <h1 class="brand-title">NETFLIX <span>ANALYTICS</span></h1>
            <p class="brand-sub">Explore Movies, TV Shows, Countries, Genres and Content Trends.</p>
        </div>
        <div>
            <span class="status-badge">🟢 Dataset Loaded Successfully ({len(df):,} Titles)</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Pre-calculate Common Exploded Series
exploded_countries_df = (
    df["country"].dropna().str.split(",").explode().str.strip()
)
exploded_genres_df = (
    df["listed_in"].dropna().str.split(",").explode().str.strip()
)


# ==============================================================================
# PAGE 1: OVERVIEW DASHBOARD
# ==============================================================================
if selected_page == "📊 Overview":
    # 6 Attractive KPI Cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    total_titles = len(df)
    total_movies = (df["type"] == "Movie").sum()
    total_tvshows = (df["type"] == "TV Show").sum()
    total_countries = exploded_countries_df.nunique()
    top_genre_name = exploded_genres_df.value_counts().index[0]
    peak_release_yr = df["release_year"].value_counts().idxmax()

    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🎬</div><div class="kpi-value">{total_titles:,}</div><div class="kpi-label">Total Titles</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🎥</div><div class="kpi-value">{total_movies:,}</div><div class="kpi-label">Total Movies</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📺</div><div class="kpi-value">{total_tvshows:,}</div><div class="kpi-label">Total TV Shows</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🌍</div><div class="kpi-value">{total_countries:,}</div><div class="kpi-label">Total Countries</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🎭</div><div class="kpi-value" style="font-size:18px;">{top_genre_name}</div><div class="kpi-label">Top Genre</div></div>', unsafe_allow_html=True)
    with col6:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📅</div><div class="kpi-value">{peak_release_yr}</div><div class="kpi-label">Peak Year</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Charts Grid: 2 Columns
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Chart A: Movies vs TV Shows Donut Chart
        type_counts = df["type"].value_counts()
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=type_counts.index,
                    values=type_counts.values,
                    hole=0.6,
                    marker=dict(colors=["#E50914", "#383838"], line=dict(color="#141414", width=2)),
                    textinfo="label+percent",
                    textfont=dict(color="#FFFFFF", size=12),
                    hoverinfo="label+value+percent",
                )
            ]
        )
        format_dark_chart(fig_donut, "A. Content Distribution: Movies vs TV Shows")
        st.plotly_chart(fig_donut, use_container_width=True)

        # Chart C: Content Release Trend (Line Chart)
        yearly_counts = df["release_year"].value_counts().sort_index()
        fig_line = go.Figure()
        fig_line.add_trace(
            go.Scatter(
                x=yearly_counts.index,
                y=yearly_counts.values,
                mode="lines+markers",
                line=dict(color="#E50914", width=3),
                marker=dict(size=6, color="#FFFFFF", line=dict(color="#E50914", width=2)),
                fill="tozeroy",
                fillcolor="rgba(229, 9, 20, 0.15)",
                name="Releases",
            )
        )
        format_dark_chart(fig_line, "C. Content Released by Year")
        fig_line.update_xaxes(title="Release Year")
        fig_line.update_yaxes(title="Titles Released")
        st.plotly_chart(fig_line, use_container_width=True)

    with chart_col2:
        # Chart B: Top 10 Countries (Horizontal Bar)
        top10_c = exploded_countries_df.value_counts().head(10).sort_values(ascending=True)
        fig_country = go.Figure(
            go.Bar(
                x=top10_c.values,
                y=top10_c.index,
                orientation="h",
                marker=dict(color="#E50914", line=dict(color="#333333", width=1)),
                text=top10_c.values,
                textposition="outside",
                textfont=dict(color="#FFFFFF", size=10),
            )
        )
        format_dark_chart(fig_country, "B. Top 10 Content Producing Countries")
        fig_country.update_xaxes(title="Number of Titles")
        st.plotly_chart(fig_country, use_container_width=True)

        # Chart D: Top 10 Genres (Horizontal Bar)
        top10_g = exploded_genres_df.value_counts().head(10).sort_values(ascending=True)
        fig_genre = go.Figure(
            go.Bar(
                x=top10_g.values,
                y=top10_g.index,
                orientation="h",
                marker=dict(color="#B81D24", line=dict(color="#333333", width=1)),
                text=top10_g.values,
                textposition="outside",
                textfont=dict(color="#FFFFFF", size=10),
            )
        )
        format_dark_chart(fig_genre, "D. Top 10 Content Genres")
        fig_genre.update_xaxes(title="Frequency")
        st.plotly_chart(fig_genre, use_container_width=True)

    # Chart E: Content Rating Distribution (Full Width)
    rating_counts = df["rating"].value_counts().head(10)
    fig_ratings = go.Figure(
        go.Bar(
            x=rating_counts.index,
            y=rating_counts.values,
            marker=dict(
                color=rating_counts.values,
                colorscale=[[0, "#444444"], [0.5, "#B81D24"], [1, "#E50914"]],
                line=dict(color="#141414", width=1),
            ),
            text=rating_counts.values,
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=10),
        )
    )
    format_dark_chart(fig_ratings, "E. Content Rating Distribution")
    fig_ratings.update_xaxes(title="Content Rating Category")
    fig_ratings.update_yaxes(title="Number of Titles")
    st.plotly_chart(fig_ratings, use_container_width=True)


# ==============================================================================
# PAGE 2: CONTENT ANALYSIS
# ==============================================================================
elif selected_page == "🎬 Content Analysis":
    st.subheader("🎬 Movies vs TV Shows Deep Dive")

    col1, col2, col3, col4 = st.columns(4)
    total_titles = len(df)
    m_count = (df["type"] == "Movie").sum()
    tv_count = (df["type"] == "TV Show").sum()
    m_pct = (m_count / total_titles * 100)
    tv_pct = (tv_count / total_titles * 100)

    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🎥</div><div class="kpi-value">{m_count:,}</div><div class="kpi-label">Total Movies</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📊</div><div class="kpi-value">{m_pct:.1f}%</div><div class="kpi-label">Movie Share</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📺</div><div class="kpi-value">{tv_count:,}</div><div class="kpi-label">Total TV Shows</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📈</div><div class="kpi-value">{tv_pct:.1f}%</div><div class="kpi-label">TV Show Share</div></div>', unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        # Comparison Bar Chart
        fig_comp = go.Figure(
            go.Bar(
                x=["Movies", "TV Shows"],
                y=[m_count, tv_count],
                marker=dict(color=["#E50914", "#383838"], line=dict(color="#141414", width=2)),
                text=[f"{m_count:,} ({m_pct:.1f}%)", f"{tv_count:,} ({tv_pct:.1f}%)"],
                textposition="outside",
                textfont=dict(color="#FFFFFF", size=12),
            )
        )
        format_dark_chart(fig_comp, "Content Volume Comparison")
        fig_comp.update_yaxes(title="Total Titles")
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_c2:
        # Yearly Comparison by Content Type
        yearly_type = (
            df.groupby(["release_year", "type"])
            .size()
            .reset_index(name="count")
        )
        fig_yr_type = px.line(
            yearly_type,
            x="release_year",
            y="count",
            color="type",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#FFFFFF"},
            markers=True,
        )
        format_dark_chart(fig_yr_type, "Release Trends: Movies vs TV Shows")
        fig_yr_type.update_xaxes(title="Release Year")
        fig_yr_type.update_yaxes(title="Number of Titles Released")
        st.plotly_chart(fig_yr_type, use_container_width=True)

    # Observation callout box
    st.markdown(
        f"""
        <div class="observation-box">
            <div class="observation-title">📌 Key Content Observation</div>
            <p class="observation-text">
                Movies dominate the Netflix catalog, comprising <b>{m_pct:.1f}%</b> ({m_count:,} titles) of all content,
                compared to TV Shows which make up <b>{tv_pct:.1f}%</b> ({tv_count:,} titles).
                Both content formats expanded rapidly between 2014 and 2018, with film licensing and production volumes consistently leading.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# PAGE 3: COUNTRY ANALYSIS
# ==============================================================================
elif selected_page == "🌍 Country Analysis":
    st.subheader("🌍 Country Distribution & Geographic Reach")

    country_counts = exploded_countries_df.value_counts()
    total_distinct_countries = len(country_counts)
    top_c_name = country_counts.index[0]
    top_c_val = country_counts.values[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🌐</div><div class="kpi-value">{total_distinct_countries}</div><div class="kpi-label">Countries Represented</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🏆</div><div class="kpi-value">{top_c_name}</div><div class="kpi-label">Leading Country</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📊</div><div class="kpi-value">{top_c_val:,}</div><div class="kpi-label">Titles in #1 Country</div></div>', unsafe_allow_html=True)

    # Top 15 Countries Horizontal Bar Chart
    top15_countries = country_counts.head(15).sort_values(ascending=True)
    fig_top_c = go.Figure(
        go.Bar(
            x=top15_countries.values,
            y=top15_countries.index,
            orientation="h",
            marker=dict(color="#E50914", line=dict(color="#333333", width=1)),
            text=top15_countries.values,
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=10),
        )
    )
    format_dark_chart(fig_top_c, "Top 15 Content Producing Countries (Split & Exploded)")
    fig_top_c.update_xaxes(title="Individual Country Mentions")
    st.plotly_chart(fig_top_c, use_container_width=True)

    st.markdown("---")
    st.subheader("🔎 Country Content Explorer")

    available_countries = sorted(country_counts.index.tolist())
    chosen_country = st.selectbox(
        "Select a country to inspect titles:",
        options=available_countries,
    )

    if chosen_country:
        country_subset = df[
            df["country"].fillna("").apply(lambda x: chosen_country in [c.strip() for c in str(x).split(",")])
        ]
        sub_total = len(country_subset)
        sub_movies = (country_subset["type"] == "Movie").sum()
        sub_tv = (country_subset["type"] == "TV Show").sum()

        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            st.metric(f"Total Titles for {chosen_country}", f"{sub_total:,}")
        with c_col2:
            st.metric("Movies", f"{sub_movies:,}")
        with c_col3:
            st.metric("TV Shows", f"{sub_tv:,}")

        st.dataframe(
            country_subset[["title", "type", "release_year", "rating", "duration", "listed_in"]].head(50),
            use_container_width=True,
            hide_index=True,
        )


# ==============================================================================
# PAGE 4: RELEASE YEAR ANALYSIS
# ==============================================================================
elif selected_page == "📅 Release Year Analysis":
    st.subheader("📅 Release Year Historical Analysis")

    earliest_year = int(df["release_year"].min())
    latest_year = int(df["release_year"].max())
    yr_counts = df["release_year"].value_counts()
    peak_release_year = yr_counts.idxmax()
    peak_release_count = yr_counts.max()
    unique_years = df["release_year"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">⏳</div><div class="kpi-value">{earliest_year}</div><div class="kpi-label">Earliest Year</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">✨</div><div class="kpi-value">{latest_year}</div><div class="kpi-label">Latest Year</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🔥</div><div class="kpi-value">{peak_release_year}</div><div class="kpi-label">Peak Year</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🔢</div><div class="kpi-value">{unique_years}</div><div class="kpi-label">Unique Years</div></div>', unsafe_allow_html=True)

    # Full Release Year Trend Chart
    full_trend = df["release_year"].value_counts().sort_index()
    fig_full_yr = go.Figure()
    fig_full_yr.add_trace(
        go.Scatter(
            x=full_trend.index,
            y=full_trend.values,
            mode="lines+markers",
            line=dict(color="#E50914", width=3),
            marker=dict(size=5, color="#FFFFFF", line=dict(color="#E50914", width=1.5)),
            fill="tozeroy",
            fillcolor="rgba(229, 9, 20, 0.18)",
            name="Titles Released",
        )
    )
    fig_full_yr.add_annotation(
        x=peak_release_year,
        y=peak_release_count,
        text=f"Peak: {peak_release_year} ({peak_release_count} titles)",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#FFFFFF",
        font=dict(color="#FFFFFF", size=11, family="Helvetica"),
        bgcolor="#E50914",
        borderpad=4,
    )
    format_dark_chart(fig_full_yr, "Complete Content Release Year Trend (1925 - 2021)")
    fig_full_yr.update_xaxes(title="Release Year")
    fig_full_yr.update_yaxes(title="Titles Released")
    st.plotly_chart(fig_full_yr, use_container_width=True)

    # Top 10 Release Years Bar Chart
    top10_years = yr_counts.head(10).sort_values(ascending=True)
    fig_top_yrs = go.Figure(
        go.Bar(
            x=top10_years.values,
            y=[str(y) for y in top10_years.index],
            orientation="h",
            marker=dict(color="#E50914", line=dict(color="#333333", width=1)),
            text=top10_years.values,
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=10),
        )
    )
    format_dark_chart(fig_top_yrs, "Top 10 Release Years by Content Volume")
    fig_top_yrs.update_xaxes(title="Number of Titles Released")
    fig_top_yrs.update_yaxes(title="Release Year")
    st.plotly_chart(fig_top_yrs, use_container_width=True)


# ==============================================================================
# PAGE 5: GENRE ANALYSIS
# ==============================================================================
elif selected_page == "🎭 Genre Analysis":
    st.subheader("🎭 Content Genres & Categorization")

    genre_frequencies = exploded_genres_df.value_counts()
    total_distinct_genres = len(genre_frequencies)
    top_genre = genre_frequencies.index[0]
    top_genre_count = genre_frequencies.values[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📚</div><div class="kpi-value">{total_distinct_genres}</div><div class="kpi-label">Unique Genres</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🌟</div><div class="kpi-value" style="font-size:18px;">{top_genre}</div><div class="kpi-label">Most Common Genre</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🏷️</div><div class="kpi-value">{top_genre_count:,}</div><div class="kpi-label">Top Genre Appearances</div></div>', unsafe_allow_html=True)

    # Top 15 Genres Horizontal Bar Chart
    top15_genres = genre_frequencies.head(15).sort_values(ascending=True)
    fig_genres = go.Figure(
        go.Bar(
            x=top15_genres.values,
            y=top15_genres.index,
            orientation="h",
            marker=dict(color="#B81D24", line=dict(color="#333333", width=1)),
            text=top15_genres.values,
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=10),
        )
    )
    format_dark_chart(fig_genres, "Top 15 Most Common Genres (Split & Exploded)")
    fig_genres.update_xaxes(title="Frequency of Appearance")
    st.plotly_chart(fig_genres, use_container_width=True)

    st.markdown("---")
    st.subheader("🔎 Genre Content Explorer")

    available_genres = sorted(genre_frequencies.index.tolist())
    chosen_genre = st.selectbox("Select a genre to explore titles:", options=available_genres)

    if chosen_genre:
        genre_subset = df[
            df["listed_in"].fillna("").apply(lambda x: chosen_genre in [g.strip() for g in str(x).split(",")])
        ]
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.metric(f"Total Titles in '{chosen_genre}'", f"{len(genre_subset):,}")
        with g_col2:
            st.metric("Movies vs TV Shows", f"{(genre_subset['type'] == 'Movie').sum()} Movies / {(genre_subset['type'] == 'TV Show').sum()} TV Shows")

        st.dataframe(
            genre_subset[["title", "type", "release_year", "country", "rating", "duration"]].head(50),
            use_container_width=True,
            hide_index=True,
        )


# ==============================================================================
# PAGE 6: RATING ANALYSIS
# ==============================================================================
elif selected_page == "🏷️ Rating Analysis":
    st.subheader("🏷️ Content Rating Distribution & Audience Categorization")

    rating_counts = df["rating"].value_counts()
    top_rating_name = rating_counts.index[0]
    top_rating_num = rating_counts.values[0]
    mature_count = rating_counts.get("TV-MA", 0) + rating_counts.get("R", 0)
    mature_pct = (mature_count / len(df) * 100)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🥇</div><div class="kpi-value">{top_rating_name}</div><div class="kpi-label">Top Rating</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📊</div><div class="kpi-value">{top_rating_num:,}</div><div class="kpi-label">Top Rating Titles</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🔞</div><div class="kpi-value">{mature_count:,}</div><div class="kpi-label">Mature (TV-MA + R)</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📈</div><div class="kpi-value">{mature_pct:.1f}%</div><div class="kpi-label">Mature Share</div></div>', unsafe_allow_html=True)

    # Top Ratings Interactive Bar Chart
    top_ratings = rating_counts.head(10)
    fig_ratings_bar = go.Figure(
        go.Bar(
            x=top_ratings.index,
            y=top_ratings.values,
            marker=dict(color="#E50914", line=dict(color="#333333", width=1)),
            text=[f"{v:,} ({v/len(df)*100:.1f}%)" for v in top_ratings.values],
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=10),
        )
    )
    format_dark_chart(fig_ratings_bar, "Top 10 Content Ratings by Count and Percentage")
    fig_ratings_bar.update_xaxes(title="Content Rating")
    fig_ratings_bar.update_yaxes(title="Number of Titles")
    st.plotly_chart(fig_ratings_bar, use_container_width=True)

    # Rating Breakdown by Content Type
    rating_by_type = (
        df[df["rating"].isin(top_ratings.index)]
        .groupby(["rating", "type"])
        .size()
        .reset_index(name="count")
    )
    fig_stacked = px.bar(
        rating_by_type,
        x="rating",
        y="count",
        color="type",
        color_discrete_map={"Movie": "#E50914", "TV Show": "#383838"},
        barmode="group",
    )
    format_dark_chart(fig_stacked, "Rating Distribution Grouped by Content Type")
    fig_stacked.update_xaxes(title="Rating Category")
    fig_stacked.update_yaxes(title="Number of Titles")
    st.plotly_chart(fig_stacked, use_container_width=True)


# ==============================================================================
# PAGE 7: DATASET EXPLORER
# ==============================================================================
elif selected_page == "🔍 Dataset Explorer":
    st.subheader("🔍 Interactive Dataset Explorer")

    # Search Bar
    search_query = st.text_input(
        "🔎 Search by Title, Director, or Country:",
        placeholder="Type a movie title or director name (e.g., Ganglands, India, Kirsten)...",
    )

    display_df = df.copy()
    if search_query:
        query = search_query.strip().lower()
        display_df = display_df[
            display_df["title"].astype(str).str.lower().str.contains(query)
            | display_df["director"].astype(str).str.lower().str.contains(query)
            | display_df["country"].astype(str).str.lower().str.contains(query)
        ]

    if len(display_df) == 0:
        st.warning(f"No titles found matching search '{search_query}'. Try a different keyword.")
    else:
        st.caption(f"Displaying **{len(display_df):,}** matching records out of {len(df):,} total catalog titles.")

        # Interactive Dataframe
        st.dataframe(
            display_df[["show_id", "type", "title", "director", "country", "date_added", "release_year", "rating", "duration", "listed_in"]],
            use_container_width=True,
            hide_index=True,
        )

        # CSV Download Button
        csv_bytes = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Dataset as CSV",
            data=csv_bytes,
            file_name="netflix_catalog_dataset.csv",
            mime="text/csv",
        )

    st.markdown("---")
    # Technical Dataset Summary Expander
    with st.expander("🛠️ View Dataset Structure & Missing Values"):
        meta_col1, meta_col2 = st.columns(2)
        with meta_col1:
            st.markdown("##### Dataset Shape & Types")
            st.write(f"- Total Rows: **{display_df.shape[0]:,}**")
            st.write(f"- Total Columns: **{display_df.shape[1]}**")
            st.write(pd.DataFrame({"Column": display_df.columns, "Data Type": [str(t) for t in display_df.dtypes]}))
        with meta_col2:
            st.markdown("##### Missing Values Count")
            st.write(pd.DataFrame({"Column": display_df.columns, "Missing Values": display_df.isnull().sum().values}))


# ==============================================================================
# PAGE 8: BUSINESS INSIGHTS
# ==============================================================================
elif selected_page == "💡 Business Insights":
    st.subheader("💡 Business Insights & Data Observations")

    tot_cnt = len(df)
    m_cnt = (df["type"] == "Movie").sum()
    tv_cnt = (df["type"] == "TV Show").sum()
    peak_yr = df["release_year"].value_counts().idxmax()
    peak_val = df["release_year"].value_counts().max()
    top_c = exploded_countries_df.value_counts()
    top_g = exploded_genres_df.value_counts()
    top_r = df["rating"].value_counts()

    leading_country_name = top_c.index[0]
    leading_country_count = top_c.values[0]
    leading_genre_name = top_g.index[0]
    leading_genre_count = top_g.values[0]

    st.caption(f"Dynamically calculated from all **{tot_cnt:,}** verified titles in Netflix library.")

    st.markdown("### 📊 Factual Dataset Observations")

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">1. Content Catalog Split: Movies vs TV Shows</div>
                <div class="insight-text">
                    Movies represent <b>{m_cnt:,}</b> titles (<b>{m_cnt/tot_cnt*100:.1f}%</b>), while TV Shows represent
                    <b>{tv_cnt:,}</b> titles (<b>{tv_cnt/tot_cnt*100:.1f}%</b>). Standalone films constitute the dominant content volume.
                </div>
            </div>
            <div class="insight-card">
                <div class="insight-title">2. Leading Geographic Content Production</div>
                <div class="insight-text">
                    After splitting co-productions, the leading country is <b>{leading_country_name}</b> with <b>{leading_country_count:,}</b> titles,
                    followed by India with <b>{top_c.get('India', 0):,}</b> titles and the United Kingdom with <b>{top_c.get('United Kingdom', 0):,}</b> titles.
                </div>
            </div>
            <div class="insight-card">
                <div class="insight-title">3. Historical Release Volume Peak</div>
                <div class="insight-text">
                    Across all 74 release years spanning 1925 to 2021, the year <b>{peak_yr}</b> represents the single highest release
                    volume with <b>{peak_val:,}</b> titles, followed by 2017 (1,030 titles) and 2019 (1,030 titles).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_i2:
        top_rating_code = top_r.index[0]
        top_rating_cnt = top_r.values[0]
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">4. Audience Age Rating Demographics</div>
                <div class="insight-text">
                    The top two ratings are TV-MA (<b>{top_r.get('TV-MA', 0):,}</b> titles, 36.5%) and TV-14
                    (<b>{top_r.get('TV-14', 0):,}</b> titles, 24.5%). Together, they make up over <b>61%</b> of all titles,
                    showing an audience target focused on teenagers and mature adults.
                </div>
            </div>
            <div class="insight-card">
                <div class="insight-title">5. Core Content Genres</div>
                <div class="insight-text">
                    The top genre is <b>{leading_genre_name}</b> with <b>{leading_genre_count:,}</b> appearances,
                    followed by Dramas with <b>{top_g.get('Dramas', 0):,}</b> and Comedies with <b>{top_g.get('Comedies', 0):,}</b> appearances.
                </div>
            </div>
            <div class="insight-card">
                <div class="insight-title">6. Metadata Quality & Completeness</div>
                <div class="insight-text">
                    <b>{df['director'].isnull().sum():,}</b> titles (29.4%) omit director details (stored as 'Not Given'), primarily among TV Shows.
                    Content type, title, and release year have 100% complete data.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 🎯 Strategic Business Recommendations (Optional Strategy)")

    rec_col1, rec_col2 = st.columns(2)
    with rec_col1:
        st.markdown(
            """
            <div class="rec-card">
                <div class="rec-title">💡 Strategic Focus 1: Expand Episodic TV Show Programming</div>
                <div class="rec-text">
                    While movies provide volume, multi-episode TV series typically generate recurring weekly engagement.
                    Expanding TV series in key international markets can help balance the current 70/30 catalog ratio.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with rec_col2:
        st.markdown(
            """
            <div class="rec-card">
                <div class="rec-title">💡 Strategic Focus 2: Grow Family and Children Offerings</div>
                <div class="rec-text">
                    Children & Family programming currently represents a modest fraction of the catalog. Investing in family-friendly
                    (TV-PG / TV-Y) content provides strong household appeal and broadens demographic reach.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# PAGE 9: ABOUT PROJECT
# ==============================================================================
elif selected_page == "ℹ️ About Project":
    st.subheader("ℹ️ Project Information & Evaluation Overview")

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("#### 📋 Project Profile")
        st.write("- **Project Name**: Netflix Data Analysis Using Python")
        st.write("- **Dashboard Platform**: NETFLIX ANALYTICS (Streamlit)")
        st.write("- **Role**: Data Analytics Intern")
        st.write("- **Dataset Source**: Netflix Movies and TV Shows (`Dataset.csv`)")
        st.write("- **Total Records**: 8,790 titles across 10 metadata columns")

    with col_a2:
        st.markdown("#### 🛠️ Technologies & Libraries")
        st.write("- **Python**: Scripting, data wrangling, and pipeline execution")
        st.write("- **Streamlit**: Web dashboard framework and interactive controls")
        st.write("- **Pandas & NumPy**: Tabular data manipulation, aggregation, and null handling")
        st.write("- **Plotly Express & Graph Objects**: Interactive dark-themed visualizations")
        st.write("- **Matplotlib & Seaborn**: Static high-resolution analytical charting")

    st.markdown("---")
    st.markdown("#### 🔄 Project Workflow Pipeline")
    st.markdown(
        """
        ```text
        [1. Raw CSV Ingestion] ➔ [2. Data Cleaning & Normalization] ➔ [3. Exploratory Data Analysis] ➔ [4. Interactive Dashboard & Visuals] ➔ [5. Data-Grounded Insights]
        ```
        """
    )

    st.markdown("---")
    st.markdown("#### 🎓 Student Explanation Summary for Internship Review")
    st.markdown(
        """
        - **Data Handling**: Missing director and country values recorded as `"Not Given"` were safely converted to `np.nan` without dropping rows.
        - **Handling Multiple Values**: Both the `country` and `listed_in` (genres) columns contain comma-separated entries. We used `.str.split(',').explode()` to calculate genuine, unmerged frequencies.
        - **Full Dataset Integrity**: The dashboard displays verified analysis across all 8,790 catalog titles smoothly without filter errors.
        """
    )
