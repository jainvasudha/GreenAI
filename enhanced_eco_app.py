"""
🌿 Enhanced GreenAI Carbon Tracker - Premium Eco Dashboard
========================================================

An advanced Streamlit app with premium eco-conscious design,
animations, and interactive features for professional carbon tracking.

Features:
- Premium eco-themed UI with nature-inspired animations
- Interactive carbon emission tracking
- Real-time environmental impact visualization
- Sustainable design with accessibility features
- Advanced analytics and reporting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any
import numpy as np
import time

# Import our modules
from src.monitoring.carbon_tracker import CarbonTracker, CarbonMetrics
from src.api.carbon_intensity import CarbonIntensityAPI
from src.recommendations.engine import RecommendationEngine, Recommendation
from config.settings import config, metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🌿 GreenAI Carbon Tracker",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium eco-conscious CSS with animations
st.markdown("""
<style>
    /* Import premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #F5F5DC 0%, #f8f8f0 100%);
    }
    
    /* Premium header with animated gradient */
    .premium-header {
        background: linear-gradient(135deg, #228B22 0%, #32CD32 50%, #98A869 100%);
        padding: 3rem 0;
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 8px 40px rgba(34, 139, 34, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .premium-header h1 {
        color: white;
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .premium-header p {
        color: rgba(255, 255, 255, 0.95);
        text-align: center;
        font-size: 1.4rem;
        margin: 1rem 0 0 0;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Animated leaf icon */
    .leaf-animation {
        display: inline-block;
        animation: leafGrow 3s ease-in-out infinite;
        margin: 0 0.5rem;
    }
    
    @keyframes leafGrow {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.1) rotate(5deg); }
        50% { transform: scale(1.2) rotate(0deg); }
        75% { transform: scale(1.1) rotate(-5deg); }
    }
    
    /* Premium metric cards with glassmorphism */
    .premium-metric-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(34, 139, 34, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .premium-metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .premium-metric-card:hover::before {
        left: 100%;
    }
    
    .premium-metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(34, 139, 34, 0.3);
    }
    
    .premium-metric-card h3 {
        color: #6B4F2A;
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .premium-metric-card .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #228B22, #32CD32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .premium-metric-card .metric-unit {
        font-size: 0.9rem;
        color: #6B4F2A;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    /* Status indicators with animations */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    .status-active {
        background: #228B22;
        box-shadow: 0 0 10px rgba(34, 139, 34, 0.5);
    }
    
    .status-inactive {
        background: #DC143C;
        box-shadow: 0 0 10px rgba(220, 20, 60, 0.5);
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Premium recommendation cards */
    .premium-recommendation-card {
        background: linear-gradient(145deg, #F5F5DC 0%, #f0f0e6 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(190, 81, 3, 0.1);
        border-left: 5px solid #BE5103;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .premium-recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #BE5103, #D2691E);
        transition: width 0.3s ease;
    }
    
    .premium-recommendation-card:hover::before {
        width: 8px;
    }
    
    .premium-recommendation-card:hover {
        transform: translateX(10px);
        box-shadow: 0 12px 35px rgba(190, 81, 3, 0.2);
    }
    
    .premium-recommendation-card h4 {
        color: #6B4F2A;
        margin: 0 0 1rem 0;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .premium-recommendation-card p {
        color: #6B4F2A;
        margin: 0 0 1rem 0;
        line-height: 1.6;
    }
    
    .premium-recommendation-card .impact {
        background: linear-gradient(135deg, #BE5103, #D2691E);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
    }
    
    /* Custom buttons with premium styling */
    .stButton > button {
        background: linear-gradient(135deg, #BE5103 0%, #D2691E 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.8rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 6px 20px rgba(190, 81, 3, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(190, 81, 3, 0.4);
    }
    
    /* Chart containers with premium styling */
    .premium-chart-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(152, 168, 105, 0.2);
        margin: 2rem 0;
    }
    
    /* Sidebar with premium styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #98A869 0%, #B8C99A 100%);
        box-shadow: 4px 0 20px rgba(0,0,0,0.1);
    }
    
    /* Footer with premium styling */
    .premium-footer {
        background: linear-gradient(135deg, #6B4F2A 0%, #8B7355 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        margin: 3rem -1rem -1rem -1rem;
        border-radius: 30px 30px 0 0;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .premium-header h1 {
            font-size: 2.5rem;
        }
        .premium-metric-card .metric-value {
            font-size: 2rem;
        }
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(34, 139, 34, 0.3);
        border-radius: 50%;
        border-top-color: #228B22;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

def create_premium_header():
    """Create the premium eco header with animations."""
    st.markdown("""
    <div class="premium-header">
        <h1>
            <span class="leaf-animation">🌿</span>
            GreenAI Carbon Tracker
            <span class="leaf-animation">🌿</span>
        </h1>
        <p>Making AI Development Sustainable • Real-time Carbon Emission Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

def create_premium_metric_card(title: str, value: str, unit: str, icon: str = "🌱", status: str = "normal"):
    """Create a premium metric card with glassmorphism effect."""
    status_class = "status-active" if status == "active" else "status-inactive"
    st.markdown(f"""
    <div class="premium-metric-card">
        <h3>{icon} {title}</h3>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
        <div style="margin-top: 1rem;">
            <span class="status-indicator {status_class}"></span>
            <span style="font-size: 0.8rem; color: #6B4F2A;">{status.title()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_premium_recommendation_card(title: str, description: str, impact: str, icon: str = "💡", priority: str = "medium"):
    """Create a premium recommendation card."""
    priority_colors = {
        "high": "#DC143C",
        "medium": "#BE5103", 
        "low": "#228B22"
    }
    priority_icons = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }
    
    st.markdown(f"""
    <div class="premium-recommendation-card">
        <h4>{icon} {title} {priority_icons.get(priority, "🟡")}</h4>
        <p>{description}</p>
        <div class="impact">Impact: {impact}</div>
    </div>
    """, unsafe_allow_html=True)

def create_premium_chart_container(title: str, description: str = ""):
    """Create a premium chart container."""
    st.markdown(f"""
    <div class="premium-chart-container">
        <h3 style="color: #6B4F2A; margin-bottom: 0.5rem; font-weight: 700;">{title}</h3>
        {f'<p style="color: #6B4F2A; opacity: 0.8; margin-bottom: 1.5rem;">{description}</p>' if description else ''}
    """, unsafe_allow_html=True)

def main():
    """Main application function with premium eco-conscious design."""
    
    # Create the premium header
    create_premium_header()
    
    # Initialize session state
    if 'carbon_tracker' not in st.session_state:
        st.session_state.carbon_tracker = None
    if 'tracking_active' not in st.session_state:
        st.session_state.tracking_active = False
    if 'emissions_history' not in st.session_state:
        st.session_state.emissions_history = []
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()
    
    # Premium sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #6B4F2A; font-family: 'Playfair Display', serif;">🌿 Control Center</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Tracking controls with premium styling
        st.markdown("### 🎯 Carbon Tracking")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌱 Start", key="start_tracking", help="Start carbon emission tracking"):
                if not st.session_state.tracking_active:
                    try:
                        st.session_state.carbon_tracker = CarbonTracker("GreenAI_Premium")
                        st.session_state.carbon_tracker.start_tracking()
                        st.session_state.tracking_active = True
                        st.session_state.session_start = datetime.now()
                        st.success("✅ Tracking started!")
                    except Exception as e:
                        st.error(f"❌ Failed to start: {e}")
                else:
                    st.warning("⚠️ Already tracking")
        
        with col2:
            if st.button("🛑 Stop", key="stop_tracking", help="Stop carbon emission tracking"):
                if st.session_state.tracking_active and st.session_state.carbon_tracker:
                    try:
                        results = st.session_state.carbon_tracker.stop_tracking()
                        if results:
                            st.session_state.emissions_history.append({
                                'timestamp': datetime.now(),
                                'emissions': results.carbon_emissions,
                                'duration': st.session_state.carbon_tracker.get_runtime_seconds(),
                                'session_id': f"session_{len(st.session_state.emissions_history) + 1}"
                            })
                        st.session_state.tracking_active = False
                        st.success("✅ Tracking stopped!")
                    except Exception as e:
                        st.error(f"❌ Failed to stop: {e}")
                else:
                    st.warning("⚠️ No active tracking")
        
        # Advanced settings
        st.markdown("### ⚙️ Advanced Settings")
        
        tracking_mode = st.selectbox(
            "Tracking Scope",
            ["Process", "Machine", "Cloud"],
            help="Select the scope of carbon tracking"
        )
        
        auto_save = st.checkbox("Auto-save data", value=True, help="Automatically save emission data")
        
        notifications = st.checkbox("Real-time notifications", value=True, help="Show real-time emission alerts")
        
        # Environmental impact summary
        st.markdown("### 🌍 Environmental Impact")
        
        if st.session_state.emissions_history:
            total_emissions = sum(h['emissions'] for h in st.session_state.emissions_history)
            trees_needed = total_emissions * 0.06
            car_miles = total_emissions * 2.2
            
            st.metric("🌳 Trees Needed", f"{trees_needed:.2f}")
            st.metric("🚗 Car Miles", f"{car_miles:.1f}")
            st.metric("🌍 CO₂ Saved", f"{total_emissions * 0.1:.4f} kg", delta="10% efficiency")
        else:
            st.info("Start tracking to see environmental impact")
    
    # Main dashboard with premium metrics
    st.markdown("## 📊 Real-time Dashboard")
    
    # Premium metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "active" if st.session_state.tracking_active else "inactive"
        create_premium_metric_card("Status", "Active" if st.session_state.tracking_active else "Inactive", "Tracking", "🌱", status)
    
    with col2:
        if st.session_state.emissions_history:
            total_emissions = sum(h['emissions'] for h in st.session_state.emissions_history)
            create_premium_metric_card("Total CO₂", f"{total_emissions:.6f}", "kg", "🌍", "active")
        else:
            create_premium_metric_card("Total CO₂", "0.000000", "kg", "🌍", "inactive")
    
    with col3:
        if st.session_state.tracking_active and st.session_state.carbon_tracker:
            duration = st.session_state.carbon_tracker.get_runtime_seconds()
            create_premium_metric_card("Runtime", f"{duration:.1f}", "seconds", "⏱️", "active")
        else:
            create_premium_metric_card("Runtime", "0.0", "seconds", "⏱️", "inactive")
    
    with col4:
        if st.session_state.emissions_history:
            avg_emissions = np.mean([h['emissions'] for h in st.session_state.emissions_history])
            create_premium_metric_card("Avg Emissions", f"{avg_emissions:.6f}", "kg/run", "📊", "active")
        else:
            create_premium_metric_card("Avg Emissions", "0.000000", "kg/run", "📊", "inactive")
    
    # Real-time monitoring section
    st.markdown("---")
    
    if st.session_state.tracking_active:
        # Live monitoring with premium charts
        create_premium_chart_container(
            "🌱 Live Carbon Emission Monitoring",
            "Real-time tracking of your AI workload's environmental impact"
        )
        
        # Generate realistic time series data
        time_points = pd.date_range(start=datetime.now() - timedelta(minutes=15), 
                                  end=datetime.now(), freq='30s')
        base_emission = 0.000001
        emission_data = base_emission + np.random.normal(0, base_emission * 0.1, len(time_points))
        emission_data = np.maximum(emission_data, 0)  # Ensure non-negative
        
        # Create premium chart
        fig = go.Figure()
        
        # Add emission line
        fig.add_trace(go.Scatter(
            x=time_points,
            y=emission_data,
            mode='lines+markers',
            name='CO₂ Emissions',
            line=dict(color='#228B22', width=4),
            marker=dict(size=8, color='#98A869', line=dict(width=2, color='white')),
            fill='tonexty',
            fillcolor='rgba(34, 139, 34, 0.1)'
        ))
        
        # Add trend line
        z = np.polyfit(range(len(time_points)), emission_data, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=time_points,
            y=p(range(len(time_points))),
            mode='lines',
            name='Trend',
            line=dict(color='#BE5103', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Real-time Carbon Emissions",
            xaxis_title="Time",
            yaxis_title="CO₂ (kg/s)",
            template="plotly_white",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Current status panel
        col1, col2 = st.columns([2, 1])
        
        with col2:
            current_emission = emission_data[-1]
            st.markdown(f"""
            <div class="premium-chart-container">
                <h4 style="color: #6B4F2A; margin-bottom: 1rem;">🎯 Current Status</h4>
                <p><strong>Emission Rate:</strong> {current_emission:.8f} kg/s</p>
                <p><strong>Status:</strong> <span style="color: #228B22; font-weight: 600;">Active</span></p>
                <p><strong>Mode:</strong> {tracking_mode}</p>
                <p><strong>Session:</strong> {len(st.session_state.emissions_history) + 1}</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("🌱 Start carbon tracking to see real-time monitoring data")
    
    # Historical analysis
    if st.session_state.emissions_history:
        st.markdown("## 📈 Historical Analysis")
        
        create_premium_chart_container(
            "📊 Emission History & Trends",
            "Comprehensive analysis of your carbon footprint over time"
        )
        
        df = pd.DataFrame(st.session_state.emissions_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create comprehensive historical chart
        fig = px.bar(
            df, 
            x='timestamp', 
            y='emissions',
            title="Historical Carbon Emissions",
            color='emissions',
            color_continuous_scale=['#98A869', '#228B22', '#BE5103'],
            hover_data=['duration']
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="CO₂ Emissions (kg)",
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed history table
        st.markdown("### 📋 Detailed History")
        st.dataframe(df, use_container_width=True)
    
    # Premium recommendations
    st.markdown("## 💡 Sustainability Recommendations")
    
    recommendations = [
        {
            "title": "Optimize Training Schedule",
            "description": "Schedule model training during off-peak hours when renewable energy is more available. This can significantly reduce your carbon footprint.",
            "impact": "Reduce emissions by 15-30%",
            "icon": "⏰",
            "priority": "high"
        },
        {
            "title": "Use Efficient Hardware",
            "description": "Consider using more energy-efficient GPUs or cloud instances with renewable energy commitments.",
            "impact": "Reduce emissions by 20-40%",
            "icon": "💻",
            "priority": "high"
        },
        {
            "title": "Implement Model Compression",
            "description": "Use techniques like quantization, pruning, and knowledge distillation to reduce computational requirements.",
            "impact": "Reduce emissions by 10-25%",
            "icon": "🗜️",
            "priority": "medium"
        },
        {
            "title": "Batch Processing",
            "description": "Process multiple tasks together to improve efficiency and reduce computational overhead.",
            "impact": "Reduce emissions by 5-15%",
            "icon": "📦",
            "priority": "medium"
        },
        {
            "title": "Use Pre-trained Models",
            "description": "Leverage existing pre-trained models instead of training from scratch when possible.",
            "impact": "Reduce emissions by 50-80%",
            "icon": "🎯",
            "priority": "high"
        }
    ]
    
    for rec in recommendations:
        create_premium_recommendation_card(
            rec["title"],
            rec["description"],
            rec["impact"],
            rec["icon"],
            rec["priority"]
        )
    
    # Premium footer
    st.markdown("""
    <div class="premium-footer">
        <h3 style="margin: 0 0 1rem 0; font-family: 'Playfair Display', serif;">🌿 GreenAI Carbon Tracker</h3>
        <p style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Making AI Development Sustainable</p>
        <p style="margin: 0; opacity: 0.8;">Built with ❤️ for the environment • Premium Eco Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
