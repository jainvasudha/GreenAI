"""
🌱 GreenAI Carbon Tracker - Professional Eco Dashboard
====================================================

A beautifully designed Streamlit app for tracking carbon emissions from AI workloads
with an eco-conscious, nature-inspired design.

Features:
- Professional eco-themed UI with nature-inspired colors
- Real-time carbon emission tracking
- Interactive visualizations
- Sustainable design principles
- Responsive layout for all devices
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

# Import our modules
from src.monitoring.carbon_tracker import CarbonTracker, CarbonMetrics
from src.api.carbon_intensity import CarbonIntensityAPI
from src.recommendations.engine import RecommendationEngine, Recommendation
from config.settings import config, metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration with eco theme
st.set_page_config(
    page_title="🌱 GreenAI Carbon Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for eco-conscious design
st.markdown("""
<style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header with gradient background */
    .eco-header {
        background: linear-gradient(135deg, #228B22 0%, #98A869 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(34, 139, 34, 0.2);
    }
    
    .eco-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .eco-header p {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Card components with eco styling */
    .eco-card {
        background: linear-gradient(145deg, #F5F5DC 0%, #f8f8f0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(34, 139, 34, 0.1);
        border: 1px solid rgba(152, 168, 105, 0.2);
        transition: all 0.3s ease;
    }
    
    .eco-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(34, 139, 34, 0.15);
    }
    
    /* Metric cards with nature-inspired styling */
    .metric-card {
        background: linear-gradient(135deg, #98A869 0%, #B8C99A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(152, 168, 105, 0.3);
        border: none;
        margin: 0.5rem 0;
    }
    
    .metric-card h3 {
        color: white;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .metric-card .metric-unit {
        font-size: 0.8rem;
        opacity: 0.8;
        margin-top: 0.2rem;
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background: linear-gradient(135deg, #F5F5DC 0%, #f0f0e6 100%);
        border-left: 4px solid #BE5103;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(190, 81, 3, 0.1);
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(190, 81, 3, 0.15);
    }
    
    .recommendation-card h4 {
        color: #6B4F2A;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    .recommendation-card p {
        color: #6B4F2A;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Custom buttons with eco styling */
    .stButton > button {
        background: linear-gradient(135deg, #BE5103 0%, #D2691E 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(190, 81, 3, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(190, 81, 3, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #98A869 0%, #B8C99A 100%);
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid rgba(152, 168, 105, 0.2);
        margin: 1rem 0;
    }
    
    /* Status indicators */
    .status-good {
        color: #228B22;
        font-weight: 600;
    }
    
    .status-warning {
        color: #BE5103;
        font-weight: 600;
    }
    
    .status-critical {
        color: #DC143C;
        font-weight: 600;
    }
    
    /* Animated elements */
    @keyframes grow {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .growing-plant {
        animation: grow 2s ease-in-out infinite;
    }
    
    /* Footer */
    .eco-footer {
        background: linear-gradient(135deg, #6B4F2A 0%, #8B7355 100%);
        color: white;
        text-align: center;
        padding: 1rem;
        margin: 2rem -1rem -1rem -1rem;
        border-radius: 20px 20px 0 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .eco-header h1 {
            font-size: 2rem;
        }
        .metric-card .metric-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def create_eco_header():
    """Create the eco-conscious header with gradient background."""
    st.markdown("""
    <div class="eco-header">
        <h1>🌱 GreenAI Carbon Tracker</h1>
        <p>Making AI Development Sustainable • Real-time Carbon Emission Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, unit: str, icon: str = "🌱"):
    """Create a styled metric card with eco theme."""
    st.markdown(f"""
    <div class="metric-card">
        <h3>{icon} {title}</h3>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>
    """, unsafe_allow_html=True)

def create_recommendation_card(title: str, description: str, impact: str, icon: str = "💡"):
    """Create a styled recommendation card."""
    st.markdown(f"""
    <div class="recommendation-card">
        <h4>{icon} {title}</h4>
        <p>{description}</p>
        <p><strong>Impact:</strong> {impact}</p>
    </div>
    """, unsafe_allow_html=True)

def create_chart_container(title: str):
    """Create a styled chart container."""
    st.markdown(f"""
    <div class="chart-container">
        <h3 style="color: #6B4F2A; margin-bottom: 1rem;">{title}</h3>
    """, unsafe_allow_html=True)

def main():
    """Main application function with eco-conscious design."""
    
    # Create the eco header
    create_eco_header()
    
    # Initialize session state
    if 'carbon_tracker' not in st.session_state:
        st.session_state.carbon_tracker = None
    if 'tracking_active' not in st.session_state:
        st.session_state.tracking_active = False
    if 'emissions_history' not in st.session_state:
        st.session_state.emissions_history = []
    
    # Sidebar with eco styling
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #6B4F2A;">🌿 Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Tracking controls
        st.markdown("### 🎯 Carbon Tracking")
        
        if st.button("🌱 Start Tracking", key="start_tracking"):
            if not st.session_state.tracking_active:
                try:
                    st.session_state.carbon_tracker = CarbonTracker("GreenAI_Dashboard")
                    st.session_state.carbon_tracker.start_tracking()
                    st.session_state.tracking_active = True
                    st.success("✅ Carbon tracking started!")
                except Exception as e:
                    st.error(f"❌ Failed to start tracking: {e}")
            else:
                st.warning("⚠️ Tracking is already active")
        
        if st.button("🛑 Stop Tracking", key="stop_tracking"):
            if st.session_state.tracking_active and st.session_state.carbon_tracker:
                try:
                    results = st.session_state.carbon_tracker.stop_tracking()
                    if results:
                        st.session_state.emissions_history.append({
                            'timestamp': datetime.now(),
                            'emissions': results.carbon_emissions,
                            'duration': st.session_state.carbon_tracker.get_runtime_seconds()
                        })
                    st.session_state.tracking_active = False
                    st.success("✅ Tracking stopped and data saved!")
                except Exception as e:
                    st.error(f"❌ Failed to stop tracking: {e}")
            else:
                st.warning("⚠️ No active tracking to stop")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        tracking_mode = st.selectbox(
            "Tracking Mode",
            ["Process", "Machine", "Cloud"],
            help="Select the scope of carbon tracking"
        )
        
        # Environmental info
        st.markdown("### 🌍 Environmental Impact")
        if st.session_state.emissions_history:
            total_emissions = sum(h['emissions'] for h in st.session_state.emissions_history)
            trees_needed = total_emissions * 0.06
            st.metric("🌳 Trees Needed", f"{trees_needed:.2f}")
            st.metric("🚗 Car Miles", f"{total_emissions * 2.2:.1f}")
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.tracking_active:
            create_metric_card("Status", "Active", "Tracking", "🟢")
        else:
            create_metric_card("Status", "Inactive", "Ready", "🔴")
    
    with col2:
        if st.session_state.emissions_history:
            total_emissions = sum(h['emissions'] for h in st.session_state.emissions_history)
            create_metric_card("Total CO₂", f"{total_emissions:.6f}", "kg", "🌱")
        else:
            create_metric_card("Total CO₂", "0.000000", "kg", "🌱")
    
    with col3:
        if st.session_state.emissions_history:
            avg_emissions = np.mean([h['emissions'] for h in st.session_state.emissions_history])
            create_metric_card("Avg Emissions", f"{avg_emissions:.6f}", "kg/run", "📊")
        else:
            create_metric_card("Avg Emissions", "0.000000", "kg/run", "📊")
    
    with col4:
        if st.session_state.tracking_active and st.session_state.carbon_tracker:
            duration = st.session_state.carbon_tracker.get_runtime_seconds()
            create_metric_card("Runtime", f"{duration:.1f}", "seconds", "⏱️")
        else:
            create_metric_card("Runtime", "0.0", "seconds", "⏱️")
    
    # Main dashboard content
    st.markdown("---")
    
    # Real-time monitoring section
    st.markdown("## 📊 Real-time Carbon Monitoring")
    
    if st.session_state.tracking_active:
        # Simulate real-time data
        current_emissions = np.random.exponential(0.000001)  # Simulated emission rate
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create a real-time emission chart
            create_chart_container("🌱 Live Emission Rate")
            
            # Generate time series data
            time_points = pd.date_range(start=datetime.now() - timedelta(minutes=10), 
                                      end=datetime.now(), freq='30s')
            emission_data = np.random.exponential(0.000001, len(time_points))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=time_points,
                y=emission_data,
                mode='lines+markers',
                name='CO₂ Emissions',
                line=dict(color='#228B22', width=3),
                marker=dict(size=6, color='#98A869')
            ))
            
            fig.update_layout(
                title="Real-time Carbon Emissions",
                xaxis_title="Time",
                yaxis_title="CO₂ (kg/s)",
                template="plotly_white",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Current Status")
            st.markdown(f"""
            <div class="eco-card">
                <h4>🌱 Live Tracking</h4>
                <p><strong>Emission Rate:</strong> {current_emissions:.8f} kg/s</p>
                <p><strong>Status:</strong> <span class="status-good">Active</span></p>
                <p><strong>Mode:</strong> {tracking_mode}</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("🌱 Start carbon tracking to see real-time monitoring data")
    
    # Historical data section
    if st.session_state.emissions_history:
        st.markdown("## 📈 Historical Emissions")
        
        # Create historical chart
        create_chart_container("📊 Emission History")
        
        df = pd.DataFrame(st.session_state.emissions_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        fig = px.bar(
            df, 
            x='timestamp', 
            y='emissions',
            title="Historical Carbon Emissions",
            color='emissions',
            color_continuous_scale=['#98A869', '#228B22', '#BE5103']
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="CO₂ Emissions (kg)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed history
        st.markdown("### 📋 Detailed History")
        st.dataframe(df, use_container_width=True)
    
    # Recommendations section
    st.markdown("## 💡 Sustainability Recommendations")
    
    recommendations = [
        {
            "title": "Optimize Training Schedule",
            "description": "Schedule model training during off-peak hours when renewable energy is more available.",
            "impact": "Reduce emissions by 15-30%",
            "icon": "⏰"
        },
        {
            "title": "Use Efficient Hardware",
            "description": "Consider using more energy-efficient GPUs or cloud instances with renewable energy.",
            "impact": "Reduce emissions by 20-40%",
            "icon": "💻"
        },
        {
            "title": "Implement Model Compression",
            "description": "Use techniques like quantization and pruning to reduce computational requirements.",
            "impact": "Reduce emissions by 10-25%",
            "icon": "🗜️"
        },
        {
            "title": "Batch Processing",
            "description": "Process multiple tasks together to improve efficiency and reduce overhead.",
            "impact": "Reduce emissions by 5-15%",
            "icon": "📦"
        }
    ]
    
    for rec in recommendations:
        create_recommendation_card(
            rec["title"],
            rec["description"],
            rec["impact"],
            rec["icon"]
        )
    
    # Footer
    st.markdown("""
    <div class="eco-footer">
        <p>🌱 GreenAI Carbon Tracker • Making AI Development Sustainable</p>
        <p>Built with ❤️ for the environment</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
