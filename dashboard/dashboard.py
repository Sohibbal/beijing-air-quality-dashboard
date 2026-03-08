import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp {
        background-color: #0e1117;
    }
    
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #fafafa;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #b0b0b0;
        margin-bottom: 1rem;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #b0b0b0;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('../data/cleaned_air_quality.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please run the notebook first.")
        st.stop()

df = load_data()

# Streamlit sidebar
with st.sidebar:
    st.markdown("## 🌫️ Air Quality Dashboard")
    st.markdown("---")
    st.markdown("### 📅 Date Range")
    min_date = df['datetime'].min().date()
    max_date = df['datetime'].max().date()
    date_range = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Station filter
    st.markdown("### 📍 Stations")
    all_stations = df['station'].unique().tolist()
    selected_stations = st.multiselect(
        "Select stations",
        options=all_stations,
        default=all_stations,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Pollutant filter
    st.markdown("### 🔬 Pollutant")
    pollutant = st.selectbox(
        "Select pollutant",
        options=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.info("Dashboard ini menampilkan analisis kualitas udara Beijing dari 12 stasiun monitoring (2013-2017).")

# Apply filters
if len(date_range) == 2:
    mask = (
        (df['datetime'].dt.date >= date_range[0]) &
        (df['datetime'].dt.date <= date_range[1]) &
        (df['station'].isin(selected_stations))
    )
else:
    mask = df['station'].isin(selected_stations)

filtered_df = df[mask].copy()
if filtered_df.empty:
    st.error("⚠️ No data available for the selected filters. Please adjust your selection.")
    st.stop()

# Header
st.markdown('<p class="main-header">Analisis Kualitas Udara Beijing (2013-2017)</p>', unsafe_allow_html=True)

# WHO Air Quality Guidelines for reference
guidelines = {
    'PM2.5': 15, 'PM10': 45, 'SO2': 20, 
    'NO2': 40, 'CO': 4000, 'O3': 100
}

# Calculate metrics
avg_value = filtered_df[pollutant].mean()
guideline = guidelines.get(pollutant, 50)
pct_vs_who = ((avg_value - guideline) / guideline) * 100

# Get worst and best stations
station_means = filtered_df.groupby('station')[pollutant].mean()
worst_station = station_means.idxmax()
worst_value = station_means.max()
best_station = station_means.idxmin()
best_value = station_means.min()

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=f"Average {pollutant}",
        value=f"{avg_value:.1f} µg/m³",
        delta=f"↑ {pct_vs_who:.0f}% vs WHO" if pct_vs_who > 0 else f"↓ {abs(pct_vs_who):.0f}% vs WHO",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="Worst Station",
        value=worst_station,
        delta=f"↑ {worst_value:.1f} µg/m³",
        delta_color="off"
    )

with col3:
    st.metric(
        label="Best Station",
        value=best_station,
        delta=f"↑ {best_value:.1f} µg/m³",
        delta_color="off"
    )

with col4:
    st.metric(
        label="Total Records",
        value=f"{len(filtered_df):,}",
        delta=f"↑ {len(selected_stations)} stations",
        delta_color="off"
    )

st.markdown("---")

# Tabs for different analyses
tab1, tab2 = st.tabs(["📊 Overview", "🗺️ Geospatial"])

# Tab 1: Overview
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📊 {pollutant} by Station")
        station_data = filtered_df.groupby('station')[pollutant].mean().sort_values()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=station_data.values,
            y=station_data.index,
            orientation='h',
            marker_color=px.colors.sequential.Reds_r,
            text=[f"{v:.1f}" for v in station_data.values],
            textposition='outside'
        ))
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title=f"{pollutant} (µg/m³)",
            yaxis_title="",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Station Statistics")
        station_stats = filtered_df.groupby('station')[pollutant].agg(['mean', 'median', 'std']).round(2)
        station_stats.columns = ['Mean', 'Median', 'Std Dev']
        station_stats = station_stats.sort_values('Mean', ascending=False)
        st.dataframe(station_stats, use_container_width=True, height=400)
    
    # Yearly trend
    st.subheader(f"📅 {pollutant} Yearly Trend (2013-2017)")
    
    # Yearly average
    yearly_avg = filtered_df.groupby(filtered_df['datetime'].dt.year)[pollutant].mean()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        yearly_sorted = yearly_avg.sort_index(ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=[str(year) for year in yearly_sorted.index],
            x=yearly_sorted.values,
            orientation='h',
            name=f'Yearly Avg {pollutant}',
            marker_color='#2ca02c',
            text=[f'{v:.2f}' for v in yearly_sorted.values],
            textposition='outside'
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title=f'{pollutant} (µg/m³)',
            yaxis_title='Year',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                range=[0, yearly_sorted.values.max() * 1.15]  # Add 15% padding for text
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Yearly Statistics**")
        summary_stats = pd.DataFrame({
            'Year': yearly_avg.index,
            'Mean': yearly_avg.values
        })
        summary_stats['Mean'] = summary_stats['Mean'].round(2)
        st.dataframe(summary_stats.set_index('Year'), use_container_width=True, height=350)
    
    # Seasonal analysis
    st.subheader(f"🌸 {pollutant} by Season")
    col1, col2 = st.columns(2)
    
    with col1:
        season_data = filtered_df.groupby('season')[pollutant].mean()
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_data = season_data.reindex(season_order)
        
        colors = ['#90EE90', '#FFD700', '#FFA500', '#87CEEB']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=season_data.values,
            y=season_data.index,
            orientation='h',
            marker_color=colors,
            text=[f"{v:.1f}" for v in season_data.values],
            textposition='outside'
        ))
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title=f"{pollutant} (µg/m³)",
            yaxis_title="Season",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Seasonal Statistics")
        season_stats = filtered_df.groupby('season')[pollutant].agg(['mean', 'median', 'std']).round(2)
        season_stats.columns = ['Mean', 'Median', 'Std Dev']
        season_stats = season_stats.reindex(season_order)
        st.dataframe(season_stats, use_container_width=True, height=350)
    
    # Weather correlation heatmap
    st.subheader(f"🌤️ {pollutant} vs Weather Variables")
    weather_cols = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    col1, col2 = st.columns([2, 1])
    
    with col1:
        weather_corr_matrix = filtered_df[[pollutant] + weather_cols].corr()
        corr_values = [[weather_corr_matrix.loc[var, pollutant]] for var in weather_cols]
        corr_text = [[f"{weather_corr_matrix.loc[var, pollutant]:.3f}"] for var in weather_cols]
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_values,
            x=[pollutant],
            y=weather_cols,
            colorscale='RdBu_r',
            zmid=0,
            zmin=-1,
            zmax=1,
            text=corr_text,
            texttemplate='%{text}',
            textfont={'size': 16, 'color': 'black'},
            colorbar=dict(title='Correlation'),
            hovertemplate='%{y}<br>Correlation: %{z:.3f}<extra></extra>'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title='',
            yaxis_title='Weather Variable',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Correlation Values**")
        weather_corr = filtered_df[[pollutant] + weather_cols].corr()[pollutant].drop(pollutant)
        corr_df = pd.DataFrame({
            'Variable': weather_corr.index,
            'Correlation': weather_corr.values
        }).sort_values('Correlation', ascending=False)
        corr_df['Correlation'] = corr_df['Correlation'].round(3)
        st.dataframe(corr_df.set_index('Variable'), use_container_width=True)

# Tab 2: Geospatial
with tab2:
    st.subheader(f"📍 {pollutant} Distribution Map")
    station_coords = {
        'Aotizhongxin': [40.0047, 116.4074],
        'Changping': [40.2171, 116.2310],
        'Dingling': [40.2906, 116.2201],
        'Dongsi': [39.9294, 116.4171],
        'Guanyuan': [39.9295, 116.3611],
        'Gucheng': [39.9142, 116.1847],
        'Huairou': [40.3282, 116.6281],
        'Nongzhanguan': [39.9370, 116.4614],
        'Shunyi': [40.1277, 116.6555],
        'Tiantan': [39.8869, 116.4074],
        'Wanliu': [39.9870, 116.3050],
        'Wanshouxigong': [39.8781, 116.3664]
    }
    
    # pollutant-specific thresholds
    thresholds = {
        'PM2.5': [25, 50, 75],
        'PM10': [40, 80, 120],
        'SO2': [15, 50, 150],
        'NO2': [30, 60, 120],
        'CO': [1500, 3000, 10000],
        'O3': [80, 120, 160]
    }
    
    thresh = thresholds.get(pollutant, [50, 100, 150])
    
    def get_color(value, thresh):
        if value < thresh[0]:
            return 'green'
        elif value < thresh[1]:
            return 'orange'
        elif value < thresh[2]:
            return 'red'
        else:
            return 'darkred'
    
    # initialize folium map
    m = folium.Map(
        location=[39.95, 116.4],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add markers
    for station, mean_val in station_means.items():
        if station in station_coords:
            color = get_color(mean_val, thresh)
            folium.CircleMarker(
                location=station_coords[station],
                radius=15,
                popup=f"<b>{station}</b><br>{pollutant}: {mean_val:.1f} µg/m³",
                tooltip=f"{station}: {mean_val:.1f}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
    
    # Display map and legend
    col1, col2 = st.columns([3, 1])
    
    with col1:
        folium_static(m, width=900, height=500)
    
    with col2:
        st.markdown(f"""
        **Legend ({pollutant}):**
        - 🟢 Good: < {thresh[0]} µg/m³
        - 🟠 Moderate: {thresh[0]}-{thresh[1]} µg/m³
        - 🔴 Unhealthy: {thresh[1]}-{thresh[2]} µg/m³
        - ⚫ Very Unhealthy: > {thresh[2]} µg/m³
        """)
        
        st.markdown("**Station Summary**")
        summary_df = station_means.sort_values(ascending=False).reset_index()
        summary_df.columns = ['Station', f'{pollutant} (µg/m³)']
        summary_df[f'{pollutant} (µg/m³)'] = summary_df[f'{pollutant} (µg/m³)'].round(2)
        st.dataframe(summary_df, use_container_width=True, height=300)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>📊 Beijing Air Quality Dashboard | Data: 2013-2017 | 12 Monitoring Stations</p>
    <p>Dicoding Submission - Belajar Analisis Data dengan Python</p>
</div>
""", unsafe_allow_html=True)
