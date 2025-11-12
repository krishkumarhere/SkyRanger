import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import numpy as np
from streamlit_extras import let_it_rain
import requests 



# Page Configuration
st.set_page_config(
    page_title="SkyRanger Control Center",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    h1, h2, h3 {
        color: ;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        font-weight: 700;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(0, 255, 136, 0.2);
        box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 255, 136, 0.3);
        border-color: rgba(0, 255, 136, 0.5);
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(0, 255, 136, 0.2);
    }
    
    .stMetric label {
        color: #00ff88 !important;
        font-weight: 600;
    }
    
    .stMetric div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2em !important;
    }
    
    .creator-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 200, 255, 0.1) 100%);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid rgba(0, 255, 136, 0.3);
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.2);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .creator-card:hover {
        transform: scale(1.05);
        border-color: rgba(0, 255, 136, 0.8);
        box-shadow: 0 15px 60px rgba(0, 255, 136, 0.4);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00ff88 0%, #00c8ff 100%);
        color: #0a0e27;
        border: none;
        border-radius: 15px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 255, 136, 0.5);
    }
    
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9em;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid #10b981;
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid #f59e0b;
    }
    
    .status-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    
    .sidebar .sidebar-content {
        background: rgba(10, 14, 39, 0.95);
    }
    
    div[data-testid="stSidebarNav"] {
        background: rgba(10, 14, 39, 0.95);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #00ff88;
        border: 1px solid rgba(0, 255, 136, 0.2);
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.3) 0%, rgba(0, 200, 255, 0.3) 100%);
        border-color: #00ff88;
    }
    
    .alert-box {
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .glow-text {
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
        50% { text-shadow: 0 0 40px rgba(0, 255, 136, 0.8); }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🚁 SkyRanger</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["DASHBOARD", "LIVE STREAM", "AI INSIGHTS",
         "MISSION MAPS", "DATA LOGS", "CONTRIBUTORS", "SETTINGS"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### System Status")
    st.markdown('<span class="status-badge status-active">● ONLINE</span>', unsafe_allow_html=True)
    st.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
    st.markdown(f"**Mission:** Field Survey #42")

# Generate mock data
def generate_flight_data():
    return {
        'altitude': np.random.uniform(00, 00),
        'speed': np.random.uniform(00, 00),
        'battery': max(00, 000 - time.time() % 50),
        'gps_lock': True,
        'temperature': np.random.uniform(00, 00),
        'humidity': np.random.uniform(00, 00),
        'air_quality': np.random.uniform(80, 95),
        'disease_count': np.random.randint(0, 5),
        'plant_health': np.random.uniform(00, 00)
    }

# Dashboard Page
if page == "DASHBOARD":
    st.markdown("<h1 class='glow-text'>🌾 SkyRanger Control Center</h1>", unsafe_allow_html=True)
    st.markdown("**Real-time agricultural drone monitoring and AI-powered analytics**")
    
    # Live data
    data = generate_flight_data()
    
    # Status Cards Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Altitude", f"{data['altitude']:.1f} m", f"+{np.random.uniform(0.1, 0.5):.1f}")
    
    with col2:
        st.metric("Speed", f"{data['speed']:.1f} m/s", f"{np.random.uniform(-0.5, 0.5):.1f}")
    
    with col3:
        battery_delta = -0.5 if data['battery'] < 70 else 0
        st.metric("Battery", f"{data['battery']:.0f}%", f"{battery_delta:.1f}%")
    
    with col4:
        gps_status = "LOCKED ✓" if data['gps_lock'] else "SEARCHING"
        st.metric("GPS", gps_status, "8 sats")
    
    st.markdown("---")
    
    # Status Cards Row 2
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperature", f"{data['temperature']:.1f}°C", f"+{np.random.uniform(0, 0.5):.1f}")
    
    with col2:
        st.metric("Humidity", f"{data['humidity']:.0f}%", f"{np.random.uniform(-1, 1):.0f}")
    
    with col3:
        st.metric("Air Quality", f"{data['air_quality']:.0f}%", "Good")
    
    with col4:
        st.metric("AI Detections", f"{data['disease_count']}", "Active")
    
    st.markdown("---")
    
    # Real-time Graphs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Altitude & Battery Tracking")
        
        # Generate time series data
        times = pd.date_range(end=datetime.now(), periods=20, freq='30S')
        altitude_data = 45 + np.cumsum(np.random.randn(20) * 0.5)
        battery_data = np.linspace(100, data['battery'], 20)
        
        df_flight = pd.DataFrame({
            'Time': times,
            'Altitude (m)': altitude_data,
            'Battery (%)': battery_data
        })
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df_flight['Time'], 
            y=df_flight['Altitude (m)'],
            name='Altitude',
            line=dict(color='#00ff88', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 136, 0.2)'
        ))
        fig1.add_trace(go.Scatter(
            x=df_flight['Time'], 
            y=df_flight['Battery (%)'],
            name='Battery',
            line=dict(color='#00c8ff', width=3),
            yaxis='y2'
        ))
        
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            yaxis=dict(title='Altitude (m)', gridcolor='rgba(255,255,255,0.1)'),
            yaxis2=dict(title='Battery (%)', overlaying='y', side='right', gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(bgcolor='rgba(0,0,0,0.5)'),
            height=350
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### Environmental Conditions")
        
        temp_data = 28 + np.cumsum(np.random.randn(20) * 0.2)
        humidity_data = 65 + np.cumsum(np.random.randn(20) * 0.5)
        
        df_env = pd.DataFrame({
            'Time': times,
            'Temperature (°C)': temp_data,
            'Humidity (%)': humidity_data
        })
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_env['Time'], 
            y=df_env['Temperature (°C)'],
            name='Temperature',
            line=dict(color='#ff6b6b', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ))
        fig2.add_trace(go.Scatter(
            x=df_env['Time'], 
            y=df_env['Humidity (%)'],
            name='Humidity',
            line=dict(color='#4ecdc4', width=3),
            yaxis='y2'
        ))
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            yaxis=dict(title='Temperature (°C)', gridcolor='rgba(255,255,255,0.1)'),
            yaxis2=dict(title='Humidity (%)', overlaying='y', side='right', gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(bgcolor='rgba(0,0,0,0.5)'),
            height=350
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
  
# Live Stream Page
elif page == "LIVE STREAM":

    st.markdown("<h1 class='glow-text'>📹 Live Camera Stream</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        stream_quality = st.selectbox("Quality", ["HD (1080p)", "SD (720p)", "Low (480p)"])
    with col2:
        stream_fps = st.selectbox("FPS", ["30", "15", "10"])
    with col3:
        if st.button("Start Live Detection"):
            st.success("AI Detection Active")

    pi_ip = "http://10.240.133.80:5000"  # <-- your Pi's IP

    st.markdown(f"""
    <div style='background: rgba(0,0,0,0.5); border: 2px solid rgba(0,255,136,0.3); 
                border-radius: 20px; padding: 10px; text-align: center; margin: 20px 0;'>
        <h2 style='color: #00ff88;'>🎥 Live Feed from Pi Camera</h2>
        <iframe src="{pi_ip}" width="100%" height="480" style="border:none; border-radius:10px;"></iframe>
        <p style='color: #00ff88; margin-top: 10px;'>Connected to {pi_ip}</p>
    </div>
    """, unsafe_allow_html=True)

    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Stream Statistics")
        st.metric("Latency", "45 ms", "-5 ms")
        st.metric("Frame Rate", "29.8 FPS", "+0.3")
        st.metric("Bitrate", "2.4 Mbps", "+0.1")
    
    with col2:
        st.markdown("### Detection Overlay")
        st.checkbox("Show AI Bounding Boxes", value=True)
        st.checkbox("Show Plant Health Overlay", value=True)
        st.checkbox("Show GPS Coordinates", value=False)

# AI Insights Page
elif page == "AI INSIGHTS":
    st.markdown("<h1 class='glow-text'>🧠 AI Plant Disease Detection</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📸 Upload Image or Use Live Feed")
        uploaded_file = st.file_uploader("Upload plant image", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is None:
            st.markdown("""
            <div style='background: rgba(0,0,0,0.3); border: 2px dashed rgba(0,255,136,0.3); 
                        border-radius: 15px; padding: 80px; text-align: center;'>
                <h3>📷 Upload Image or Start Live Detection</h3>
                <p>Supported formats: JPG, PNG</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎥 Start Live Detection"):
                st.info("Analyzing frames from live feed...")
        with col_b:
            if st.button("🔄 Analyze Current Frame"):
                st.success("Analysis complete")
    
    with col2:
        st.markdown("### 🎯 Detection Results")
        
        confidence = np.random.uniform(85, 98)
        disease_detected = np.random.choice([True, False], p=[0.3, 0.7])
        
        if disease_detected:
            disease_type = np.random.choice(["Leaf Blight", "Powdery Mildew", "Rust", "Bacterial Spot"])
            st.markdown(f"""
            <div class='alert-box' style='background: rgba(239, 68, 68, 0.2); border-color: #ef4444;'>
                <strong>⚠️ DISEASE DETECTED</strong><br>
                <strong>Type:</strong> {disease_type}<br>
                <strong>Confidence:</strong> {confidence:.1f}%<br>
                <strong>Severity:</strong> Moderate
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-box' style='background: rgba(16, 185, 129, 0.2); border-color: #10b981;'>
                <strong>✓ HEALTHY PLANT</strong><br>
                <strong>Confidence:</strong> {confidence:.1f}%<br>
                <strong>Plant Health:</strong> Excellent
            </div>
            """, unsafe_allow_html=True)
        
        st.metric("🌱 Plant Health Score", f"{np.random.uniform(85, 98):.0f}%")
        st.metric("🔬 Total Scans Today", f"{np.random.randint(45, 120)}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Health Distribution")
        
        health_data = pd.DataFrame({
            'Status': ['Healthy', 'Diseased', 'Uncertain'],
            'Count': [87, 13, 5],
            'Color': ['#10b981', '#ef4444', '#f59e0b']
        })
        
        fig = px.pie(health_data, values='Count', names='Status', 
                     color='Status',
                     color_discrete_map={'Healthy': '#10b981', 'Diseased': '#ef4444', 'Uncertain': '#f59e0b'})
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            showlegend=True,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Detection Timeline (Last Hour)")
        
        timeline_times = pd.date_range(end=datetime.now(), periods=12, freq='5T')
        detections = np.random.randint(0, 8, 12)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=timeline_times,
            y=detections,
            marker=dict(color='#00ff88', line=dict(color='#00ff88', width=2)),
            name='Detections'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            yaxis=dict(title='Detections', gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent detections table
    st.markdown("### 📋 Recent Disease Detections")
    
    recent_detections = pd.DataFrame({
        'Time': [datetime.now() - timedelta(minutes=i*5) for i in range(8)],
        'Disease': np.random.choice(['Leaf Blight', 'Powdery Mildew', 'Rust', 'Healthy', 'Bacterial Spot'], 8),
        'Confidence': np.random.uniform(80, 99, 8),
        'Location': [f"GPS: {np.random.uniform(25, 26):.4f}, {np.random.uniform(85, 86):.4f}" for _ in range(8)]
    })
    
    recent_detections['Time'] = recent_detections['Time'].dt.strftime('%H:%M:%S')
    recent_detections['Confidence'] = recent_detections['Confidence'].round(1).astype(str) + '%'
    
    st.dataframe(recent_detections, use_container_width=True, hide_index=True)

# Mission Map Page
elif page == "MISSION MAPS":
    st.markdown("<h1 class='glow-text'>🗺️ Mission Map & GPS Tracking</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📍 Current Position", "25.5941°N, 85.1376°E")
    with col2:
        st.metric("🛤️ Distance Traveled", "2.4 km")
    with col3:
        st.metric("⏱️ Mission Time", "18:32")
    
    st.markdown("---")
    
    # Map placeholder
    st.markdown("### 🗺️ Live GPS Tracking with Leaflet.js")
    st.info("💡 Integration: Use Streamlit-Folium for interactive maps with drone path, waypoints, and LiDAR overlay")
    
    st.markdown("""
    <div style='background: rgba(0,0,0,0.3); border: 2px solid rgba(0,255,136,0.3); 
                border-radius: 15px; padding: 100px; text-align: center;'>
        <h3>🗺️ Interactive Map Placeholder</h3>
        <p>Live drone position • Flight path • Waypoints • Field boundaries</p>
        <p style='color: #00ff88;'>Install: pip install streamlit-folium</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Flight Statistics")
        st.metric("Waypoints Completed", "8 / 12")
        st.metric("Area Covered", "3.2 hectares")
        st.metric("Avg Speed", "12.3 m/s")
    
    with col2:
        st.markdown("### 🎯 Mission Parameters")
        st.metric("Flight Mode", "AUTO")
        st.metric("Altitude Setting", "45m AGL")
        st.metric("Return Home", "Enabled ✓")

# Data Logs Page
elif page == "DATA LOGS":
    st.markdown("<h1 class='glow-text'>📊 Mission Data & Analytics</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        date_range = st.date_input("Select Date Range", 
                                   value=(datetime.now() - timedelta(days=7), datetime.now()))
    with col2:
        if st.button("⬇️ Download CSV"):
            st.success("Downloading mission data...")
    
    st.markdown("---")
    
    # Historical mission data
    st.markdown("### 📋 Mission History")
    
    mission_data = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(10)],
        'Mission ID': [f"MSN-{1000+i}" for i in range(10)],
        'Duration': [f"{np.random.randint(15, 45)} min" for _ in range(10)],
        'Area Covered': [f"{np.random.uniform(2, 5):.1f} ha" for _ in range(10)],
        'Diseases Detected': np.random.randint(0, 15, 10),
        'Sensor Health': np.random.choice(['Excellent', 'Good', 'Fair'], 10, p=[0.7, 0.2, 0.1]),
        'Status': np.random.choice(['✓ Complete', '⚠ Partial', '✗ Failed'], 10, p=[0.8, 0.15, 0.05])
    })
    
    st.dataframe(mission_data, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Disease Detection Trends")
        
        trend_dates = [(datetime.now() - timedelta(days=i)).strftime('%b %d') for i in range(14, 0, -1)]
        detections = np.random.randint(5, 25, 14)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_dates,
            y=detections,
            mode='lines+markers',
            line=dict(color='#ef4444', width=3),
            marker=dict(size=8, color='#ef4444'),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)',
            name='Detections'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            yaxis=dict(title='Disease Count', gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🔋 Sensor Performance Over Time")
        
        sensor_names = ['DHT11', 'PIR', 'MQ2', 'MQ7', 'Ultrasonic', 'ESP32']
        uptime = np.random.uniform(95, 100, 6)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sensor_names,
            y=uptime,
            marker=dict(
                color=uptime,
                colorscale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']],
                showscale=False
            ),
            text=[f"{val:.1f}%" for val in uptime],
            textposition='outside'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            yaxis=dict(title='Uptime %', gridcolor='rgba(255,255,255,0.1)', range=[0, 105]),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Database connection status
    st.markdown("### 🗄️ Database Connection")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Type:** MongoDB Atlas")
    with col2:
        st.success("**Status:** Connected ✓")
    with col3:
        st.metric("Records", "1,247")

# Creators Page
elif page == "CONTRIBUTORS":
    st.markdown("<h1 class='glow-text'>👥 Meet the SkyRanger Team</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Creator profiles
    creators = [
        {
            'name': 'Krish Kumar',
            'role': 'Lead Developer',
            'github': 'https://github.com/krishkumar',
            'linkedin': 'https://linkedin.com/in/krishkumar'
        },
        {
            'name': 'Rudra Bishwakarma',
            'role': 'Hardware and IoT engineer',
            'github': 'https://github.com/Swastika2401',
            'linkedin': 'https://www.linkedin.com/in/rudra-bishwakarma'  # Corrected key
        },
        {
            'name': 'Swastika kumari',
            'role': 'AI/ML Engineer',
            'github': 'https://github.com/Swastika2401',
            'linkedin': 'https://www.linkedin.com/in/swastika-kumari-423288290/'
        }
    ]
    
    # Display creators in grid (fixed, safe access to keys)
    for i in range(0, len(creators), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(creators):
                creator = creators[idx]
                name = creator.get('name', 'Unknown')
                role = creator.get('role', '')
                emoji = creator.get('emoji', '👤')
                tagline = creator.get('tagline', '')
                github = (creator.get('github') or '').strip()
                linkedin = (creator.get('linkedin') or creator.get('linkdin') or '').strip()

                links = []
                if github:
                    links.append(f"<a href='{github}' target='_blank' style='margin: 0 8px; text-decoration: none; font-size: 1.3em;'>Github</a>")
                if linkedin:
                    links.append(f"<a href='{linkedin}' target='_blank' style='margin: 0 8px; text-decoration: none; font-size: 1.3em;'>Linkedin</a>")

                links_html = " ".join(links)  # may be empty

                with col:
                    # render the visual card (no embedded links_html here)
                    st.markdown(f"""
                    <div class='creator-card'>
                        <div style='font-size: 3.8em; margin-bottom: 10px;'>{emoji}</div>
                        <h2 style='margin: 6px 0; color: #00ff88;'>{name}</h2>
                        <h4 style='color: #00c8ff; margin: 4px 0;'>{role}</h4>
                        {f"<p style='color: #ffffff; margin: 12px 0 0 0; font-size: 0.95em;'>{tagline}</p>" if tagline else ""}
                    </div>
                    """, unsafe_allow_html=True)

                    # render links separately so Streamlit doesn't escape them
                    if links_html:
                        st.markdown(f"<div style='margin-top:12px; text-align:center;'>{links_html}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Want to Contribute?")
    st.markdown("""
    SkyRanger is an open-source project! We welcome contributions from developers, 
    researchers, and agricultural enthusiasts worldwide.
    """)
    
    col1 = st.columns(1)[0]
    with col1:
        st.markdown("**GitHub:** github.com/skyranger")

# Settings Page
elif page == "SETTINGS":
    st.markdown("<h1 class='glow-text'>⚙️ System Settings & Configuration</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 General", "🌐 API Config", "🤖 AI Models", "🔄 System"])
    
    with tab1:
        st.markdown("### 🎨 Theme & Display")
        
        col1, col2 = st.columns(2)
        with col1:
            theme_option = st.selectbox("Color Theme", 
                                       ["Dark (Neon Green)", "Dark (Blue)", "Dark (Purple)", "Light"])
            st.selectbox("Font Family", ["Space Grotesk", "Inter", "Poppins", "Roboto"])
        
        with col2:
            st.slider("UI Scale", 80, 120, 100, 5, format="%d%%")
            st.checkbox("Enable Animations", value=True)
        
        st.markdown("---")
        st.markdown("### 🔔 Notifications")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Disease Detection Alerts", value=True)
            st.checkbox("Low Battery Warnings", value=True)
        with col2:
            st.checkbox("Sensor Malfunction Alerts", value=True)
            st.checkbox("Mission Complete Notifications", value=True)
    
    with tab2:
        st.markdown("### 🌐 API Configuration")
        
        st.text_input("FastAPI Backend URL", value="http://raspberrypi.local:8000")
        st.text_input("Camera Stream URL", value="http://raspberrypi.local:8080/stream.mjpg")
        st.text_input("WebSocket URL", value="ws://raspberrypi.local:8000/ws")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Request Timeout (seconds)", min_value=5, max_value=60, value=30)
        with col2:
            st.number_input("Refresh Rate (seconds)", min_value=1, max_value=10, value=2)
        
        if st.button("🧪 Test Connection"):
            with st.spinner("Testing API connection..."):
                time.sleep(1.5)
                st.success("✓ Connection successful!")
    
    with tab3:
        st.markdown("### 🤖 AI Model Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Disease Detection Model", 
                        ["YOLOv8 Custom (v2.1)", "YOLOv8 Custom (v1.9)", "ResNet50 Fine-tuned"])
            st.slider("Detection Confidence Threshold", 0.0, 1.0, 0.75, 0.05)
        
        with col2:
            st.selectbox("Plant Classification Model", 
                        ["EfficientNet-B3", "MobileNetV3", "Custom CNN"])
            st.slider("NMS IoU Threshold", 0.0, 1.0, 0.45, 0.05)
        
        st.markdown("---")
        st.markdown("### 📊 Model Performance")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Accuracy", "94.2%")
        with col2:
            st.metric("Inference Time", "42ms")
        with col3:
            st.metric("F1 Score", "0.91")
        
        if st.button("🔄 Reload Models"):
            with st.spinner("Reloading AI models..."):
                time.sleep(2)
                st.success("✓ Models reloaded successfully!")
    
    with tab4:
        st.markdown("### 🔄 System Control")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Sensor Calibration")
            if st.button("📡 Calibrate All Sensors"):
                with st.spinner("Calibrating sensors..."):
                    time.sleep(2)
                    st.success("✓ Calibration complete!")
            
            if st.button("🔄 Reset Sensor Data"):
                st.warning("This will clear all historical sensor data!")
        
        with col2:
            st.markdown("#### Service Control")
            if st.button("🔄 Restart Backend Services"):
                with st.spinner("Restarting services..."):
                    time.sleep(3)
                    st.success("✓ Services restarted!")
            
            if st.button("🗄️ Backup Database"):
                st.success("✓ Database backup created!")
        
        st.markdown("---")
        st.markdown("### 🧹 Maintenance")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Storage Used", "2.4 GB / 32 GB")
        with col2:
            st.metric("System Uptime", "14d 7h 23m")
        with col3:
            st.metric("Last Backup", "2 hours ago")
        
        if st.button("🗑️ Clear Cache & Logs"):
            with st.spinner("Clearing cache..."):
                time.sleep(1)
                st.success("✓ Cache cleared!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: rgba(255,255,255,0.7);'>
    <p style='font-size: 1.1em;'>© 2025 SkyRanger Project | Developed by Team SkyRanger</p>
    <p>
        <a href='https://github.com/skyranger' target='_blank' style='color: #00ff88; text-decoration: none; margin: 0 10px;'>
            💻 GitHub
        </a> | 
        <a href='mailto:team@skyranger.ai' style='color: #00ff88; text-decoration: none; margin: 0 10px;'>
            📧 Contact
        </a> | 
        <a href='https://skyranger.ai' target='_blank' style='color: #00ff88; text-decoration: none; margin: 0 10px;'>
            🌐 Website
        </a>
    </p>
    <p style='margin-top: 15px; font-size: 2em;'>🚁</p>
</div>
""", unsafe_allow_html=True)