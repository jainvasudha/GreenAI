"""
🌱 Enhanced Environmental Visualization App
==========================================

Interactive Streamlit app with comprehensive graphs and tabs for
carbon emissions, energy consumption, and water usage tracking.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional
import logging

# Import the enhanced tracker
from enhanced_carbon_tracker import (
    EnhancedCarbonTracker, 
    WaterIntensityCalculator, 
    EnergyCalculator,
    EnhancedCarbonMetrics
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="NeuroGreen",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #228B22;
    }
    
    .metric-header {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .metric-icon {
        font-size: 1.5em;
        margin-right: 10px;
    }
    
    .metric-title {
        font-weight: 600;
        color: #6B4F2A;
        font-size: 1.1em;
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        color: #228B22;
        margin: 5px 0;
    }
    
    .metric-unit {
        color: #666;
        font-size: 0.9em;
    }
    
    .help-text {
        margin-left: auto;
        cursor: help;
        color: #666;
    }
    
    .tab-content {
        padding: 20px 0;
    }
    
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .comparison-card {
        background: linear-gradient(135deg, #98A869 0%, #B8C99A 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        text-align: center;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        gap: 1px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #228B22;
        color: white;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        border-radius: 0 0 8px 8px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

def create_metric_card(title: str, value: str, unit: str, icon: str, 
                      color: str = "#228B22", help_text: str = None) -> str:
    """Create a styled metric card."""
    help_html = f'<div class="help-text" title="{help_text}">ℹ️</div>' if help_text else ''
    
    return f"""
    <div class="metric-card" style="border-left: 4px solid {color};">
        <div class="metric-header">
            <span class="metric-icon">{icon}</span>
            <span class="metric-title">{title}</span>
            {help_html}
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>
    """

def initialize_session_state():
    """Initialize session state variables."""
    if 'enhanced_tracker' not in st.session_state:
        st.session_state.enhanced_tracker = EnhancedCarbonTracker()
    
    if 'tracking_active' not in st.session_state:
        st.session_state.tracking_active = False
    
    if 'metrics_history' not in st.session_state:
        st.session_state.metrics_history = []

def show_control_panel():
    """Show the control panel for tracking."""
    st.markdown("## 🎛️ Environmental Tracking Controls")
    
    with st.expander("⚙️ Tracking Configuration", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            workload_type = st.selectbox(
                "Workload Type",
                ["training", "inference", "data_processing", "evaluation", "fine_tuning"],
                help="Type of AI workload being performed"
            )
        
        with col2:
            framework = st.selectbox(
                "Framework",
                ["pytorch", "tensorflow", "scikit-learn", "huggingface", "transformers"],
                help="ML framework being used"
            )
        
        with col3:
            region = st.selectbox(
                "Region",
                ["us-east-1", "us-west-2", "us-west-1", "eu-west-1", "ap-southeast-1", "local"],
                help="Geographic region for environmental calculations"
            )
        
        # Hardware specifications
        st.markdown("#### 🔧 Hardware Specifications")
        hw_col1, hw_col2, hw_col3, hw_col4 = st.columns(4)
        
        with hw_col1:
            cpu_type = st.selectbox(
                "CPU Type",
                ["apple_m2", "apple_m3", "intel_i7", "intel_i9", "amd_ryzen7", "amd_ryzen9"],
                help="Processor type for energy calculations"
            )
        
        with hw_col2:
            gpu_type = st.selectbox(
                "GPU Type",
                ["none", "rtx_3080", "rtx_3090", "rtx_4080", "rtx_4090", "a100", "v100"],
                help="Graphics card type (none if not using GPU)"
            )
        
        with hw_col3:
            memory_type = st.selectbox(
                "Memory Type",
                ["ddr4_16gb", "ddr4_32gb", "ddr5_16gb", "ddr5_32gb", "ddr5_64gb"],
                help="System memory configuration"
            )
        
        with hw_col4:
            cloud_provider = st.selectbox(
                "Cloud Provider",
                ["aws", "gcp", "azure", "local"],
                help="Cloud provider for regional factors"
            )
        
        # Tracking controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌱 Start Enhanced Tracking", type="primary", use_container_width=True):
                hardware_specs = {
                    'cpu_type': cpu_type,
                    'gpu_type': gpu_type,
                    'memory_type': memory_type,
                    'cpu_utilization': 0.5,
                    'gpu_utilization': 0.0 if gpu_type == 'none' else 0.8,
                    'memory_usage': 0.5
                }
                
                tracker = st.session_state.enhanced_tracker
                tracker.region = region
                tracker.cloud_provider = cloud_provider
                
                session_id = tracker.start_tracking(workload_type, framework, hardware_specs)
                st.session_state.tracking_active = True
                st.success(f"🌱 Enhanced environmental tracking started: {session_id}")
                st.rerun()
        
        with col2:
            if st.button("🛑 Stop Enhanced Tracking", use_container_width=True):
                if st.session_state.tracking_active:
                    tracker = st.session_state.enhanced_tracker
                    metrics = tracker.stop_tracking()
                    if metrics:
                        st.session_state.metrics_history.append(metrics)
                        st.session_state.tracking_active = False
                        st.success("✅ Enhanced environmental tracking stopped!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to stop tracking")
                else:
                    st.warning("⚠️ No active tracking to stop")

def show_real_time_metrics():
    """Show real-time metrics during tracking."""
    if st.session_state.tracking_active:
        st.markdown("## 📊 Real-time Environmental Metrics")
        
        tracker = st.session_state.enhanced_tracker
        if tracker.start_time:
            current_runtime = (datetime.now() - tracker.start_time).total_seconds()
            current_energy = EnergyCalculator.calculate_energy_consumption(
                current_runtime, tracker.current_hardware_specs
            )
            current_water = WaterIntensityCalculator.calculate_water_usage(
                current_energy, tracker.cloud_provider, tracker.region
            )
            current_emissions = current_energy * tracker.get_carbon_intensity() / 1000
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("⏱️ Runtime", f"{current_runtime:.1f}s", "🟢 Active")
            
            with col2:
                st.metric("⚡ Energy", f"{current_energy:.4f} kWh", "📈 Growing")
            
            with col3:
                st.metric("💧 Water", f"{current_water:.2f} L", "💧 Usage")
            
            with col4:
                st.metric("🌍 CO₂", f"{current_emissions:.6f} kg", "📊 Emissions")

def show_carbon_emissions_tab():
    """Show carbon emissions analysis tab."""
    st.markdown("## 🌍 Carbon Emissions Analysis")
    
    if not st.session_state.metrics_history:
        st.info("🌱 Start tracking to see carbon emissions data!")
        return
    
    # Create DataFrame from metrics history
    df_data = []
    for metrics in st.session_state.metrics_history:
        df_data.append({
            'Timestamp': metrics.timestamp,
            'Workload': metrics.workload_type,
            'Framework': metrics.framework,
            'Region': metrics.region,
            'Cloud': metrics.cloud_provider,
            'Hardware': metrics.hardware_type,
            'Runtime (s)': metrics.runtime_seconds,
            'CO₂ (kg)': metrics.carbon_emissions,
            'Carbon Intensity (g/kWh)': metrics.carbon_intensity,
            'Renewable %': metrics.renewable_percentage
        })
    
    df = pd.DataFrame(df_data)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_emissions = df['CO₂ (kg)'].sum()
        st.metric("🌍 Total CO₂", f"{total_emissions:.6f} kg", 
                 help="Total carbon dioxide emissions across all runs")
    
    with col2:
        avg_intensity = df['Carbon Intensity (g/kWh)'].mean()
        st.metric("🔋 Avg Intensity", f"{avg_intensity:.1f} g/kWh",
                 help="Average carbon intensity of the grid")
    
    with col3:
        avg_renewable = df['Renewable %'].mean()
        st.metric("🌱 Avg Renewable", f"{avg_renewable:.1f}%",
                 help="Average renewable energy percentage")
    
    with col4:
        trees_needed = total_emissions * 0.06
        st.metric("🌳 Trees Needed", f"{trees_needed:.2f}",
                 help="Number of trees needed to offset emissions")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 CO₂ Emissions Over Time")
        fig_time = px.line(
            df, 
            x='Timestamp', 
            y='CO₂ (kg)',
            title='Carbon Emissions Over Time',
            color='Workload',
            markers=True
        )
        fig_time.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌍 Regional CO₂ Comparison")
        regional_data = df.groupby('Region').agg({
            'CO₂ (kg)': 'sum',
            'Carbon Intensity (g/kWh)': 'mean',
            'Renewable %': 'mean'
        }).reset_index()
        
        fig_regional = px.bar(
            regional_data,
            x='Region',
            y='CO₂ (kg)',
            title='Total CO₂ Emissions by Region',
            color='CO₂ (kg)',
            color_continuous_scale='Reds'
        )
        fig_regional.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_regional, use_container_width=True)
    
    # Detailed table
    st.markdown("#### 📊 Detailed CO₂ Data")
    st.dataframe(df[['Timestamp', 'Workload', 'Framework', 'Region', 'CO₂ (kg)', 
                     'Carbon Intensity (g/kWh)', 'Renewable %']], use_container_width=True)

def show_energy_consumption_tab():
    """Show energy consumption analysis tab."""
    st.markdown("## ⚡ Energy Consumption Analysis")
    
    if not st.session_state.metrics_history:
        st.info("🌱 Start tracking to see energy consumption data!")
        return
    
    # Create DataFrame from metrics history
    df_data = []
    for metrics in st.session_state.metrics_history:
        df_data.append({
            'Timestamp': metrics.timestamp,
            'Workload': metrics.workload_type,
            'Framework': metrics.framework,
            'Hardware': metrics.hardware_type,
            'Runtime (s)': metrics.runtime_seconds,
            'Energy (kWh)': metrics.energy_consumed,
            'CPU Utilization': metrics.cpu_utilization,
            'GPU Utilization': metrics.gpu_utilization,
            'Memory Usage': metrics.memory_usage
        })
    
    df = pd.DataFrame(df_data)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_energy = df['Energy (kWh)'].sum()
        st.metric("⚡ Total Energy", f"{total_energy:.6f} kWh",
                 help="Total energy consumption across all runs")
    
    with col2:
        avg_energy = df['Energy (kWh)'].mean()
        st.metric("📊 Avg Energy", f"{avg_energy:.6f} kWh",
                 help="Average energy consumption per run")
    
    with col3:
        energy_per_second = total_energy / df['Runtime (s)'].sum() if df['Runtime (s)'].sum() > 0 else 0
        st.metric("⚡ Energy Rate", f"{energy_per_second:.6f} kWh/s",
                 help="Energy consumption rate per second")
    
    with col4:
        car_miles = total_energy * 2.2  # Rough conversion
        st.metric("🚗 Car Miles", f"{car_miles:.2f} miles",
                 help="Equivalent car miles based on energy")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Energy Consumption Over Time")
        fig_time = px.line(
            df, 
            x='Timestamp', 
            y='Energy (kWh)',
            title='Energy Consumption Over Time',
            color='Workload',
            markers=True
        )
        fig_time.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔧 Hardware Energy Efficiency")
        hardware_data = df.groupby('Hardware').agg({
            'Energy (kWh)': 'sum',
            'Runtime (s)': 'sum'
        }).reset_index()
        hardware_data['Energy per Hour'] = hardware_data['Energy (kWh)'] / (hardware_data['Runtime (s)'] / 3600)
        
        fig_hardware = px.bar(
            hardware_data,
            x='Hardware',
            y='Energy per Hour',
            title='Energy Consumption Rate by Hardware',
            color='Energy per Hour',
            color_continuous_scale='Greens'
        )
        fig_hardware.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_hardware, use_container_width=True)
    
    # Utilization analysis
    st.markdown("#### 📊 Hardware Utilization Analysis")
    utilization_data = df[['CPU Utilization', 'GPU Utilization', 'Memory Usage']].mean()
    
    fig_util = px.bar(
        x=['CPU', 'GPU', 'Memory'],
        y=[utilization_data['CPU Utilization'], 
           utilization_data['GPU Utilization'], 
           utilization_data['Memory Usage']],
        title='Average Hardware Utilization',
        color=['CPU', 'GPU', 'Memory'],
        color_discrete_sequence=['#228B22', '#98A869', '#6B4F2A']
    )
    fig_util.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Utilization %',
        xaxis_title='Hardware Component'
    )
    st.plotly_chart(fig_util, use_container_width=True)
    
    # Detailed table
    st.markdown("#### 📊 Detailed Energy Data")
    st.dataframe(df[['Timestamp', 'Workload', 'Hardware', 'Runtime (s)', 'Energy (kWh)',
                     'CPU Utilization', 'GPU Utilization', 'Memory Usage']], use_container_width=True)

def show_water_usage_tab():
    """Show water usage analysis tab."""
    st.markdown("## 💧 Water Usage Analysis")
    
    if not st.session_state.metrics_history:
        st.info("🌱 Start tracking to see water usage data!")
        return
    
    # Create DataFrame from metrics history
    df_data = []
    for metrics in st.session_state.metrics_history:
        df_data.append({
            'Timestamp': metrics.timestamp,
            'Workload': metrics.workload_type,
            'Framework': metrics.framework,
            'Region': metrics.region,
            'Cloud': metrics.cloud_provider,
            'Runtime (s)': metrics.runtime_seconds,
            'Water (L)': metrics.water_usage,
            'Water Intensity (L/kWh)': metrics.water_intensity,
            'Energy (kWh)': metrics.energy_consumed
        })
    
    df = pd.DataFrame(df_data)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_water = df['Water (L)'].sum()
        st.metric("💧 Total Water", f"{total_water:.2f} L",
                 help="Total water usage across all runs")
    
    with col2:
        avg_water = df['Water (L)'].mean()
        st.metric("📊 Avg Water", f"{avg_water:.2f} L",
                 help="Average water usage per run")
    
    with col3:
        bottles = total_water / 0.5
        st.metric("🍼 Bottles", f"{bottles:.0f} bottles",
                 help="Equivalent to 500ml water bottles")
    
    with col4:
        showers = total_water / 65
        st.metric("🚿 Showers", f"{showers:.1f} showers",
                 help="Equivalent to average shower usage")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Water Usage Over Time")
        fig_time = px.line(
            df, 
            x='Timestamp', 
            y='Water (L)',
            title='Water Usage Over Time',
            color='Workload',
            markers=True
        )
        fig_time.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌍 Regional Water Usage Comparison")
        regional_data = df.groupby('Region').agg({
            'Water (L)': 'sum',
            'Water Intensity (L/kWh)': 'mean'
        }).reset_index()
        
        fig_regional = px.bar(
            regional_data,
            x='Region',
            y='Water (L)',
            title='Total Water Usage by Region',
            color='Water (L)',
            color_continuous_scale='Blues'
        )
        fig_regional.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_regional, use_container_width=True)
    
    # Water intensity analysis
    st.markdown("#### 💧 Water Intensity Analysis")
    intensity_data = df.groupby('Region').agg({
        'Water Intensity (L/kWh)': 'mean',
        'Water (L)': 'sum',
        'Energy (kWh)': 'sum'
    }).reset_index()
    
    fig_intensity = px.scatter(
        intensity_data,
        x='Energy (kWh)',
        y='Water (L)',
        size='Water Intensity (L/kWh)',
        color='Region',
        title='Water Usage vs Energy Consumption by Region',
        hover_data=['Water Intensity (L/kWh)']
    )
    fig_intensity.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_intensity, use_container_width=True)
    
    # Detailed table
    st.markdown("#### 📊 Detailed Water Usage Data")
    st.dataframe(df[['Timestamp', 'Workload', 'Region', 'Cloud', 'Runtime (s)', 
                     'Water (L)', 'Water Intensity (L/kWh)', 'Energy (kWh)']], use_container_width=True)

def show_combined_analysis_tab():
    """Show combined environmental analysis tab."""
    st.markdown("## 🌍 Combined Environmental Impact Analysis")
    
    if not st.session_state.metrics_history:
        st.info("🌱 Start tracking to see combined environmental impact data!")
        return
    
    # Create DataFrame from metrics history
    df_data = []
    for metrics in st.session_state.metrics_history:
        df_data.append({
            'Timestamp': metrics.timestamp,
            'Workload': metrics.workload_type,
            'Framework': metrics.framework,
            'Region': metrics.region,
            'Cloud': metrics.cloud_provider,
            'Hardware': metrics.hardware_type,
            'Runtime (s)': metrics.runtime_seconds,
            'CO₂ (kg)': metrics.carbon_emissions,
            'Energy (kWh)': metrics.energy_consumed,
            'Water (L)': metrics.water_usage,
            'Carbon Intensity (g/kWh)': metrics.carbon_intensity,
            'Water Intensity (L/kWh)': metrics.water_intensity,
            'Renewable %': metrics.renewable_percentage
        })
    
    df = pd.DataFrame(df_data)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_emissions = df['CO₂ (kg)'].sum()
        st.metric("🌍 Total CO₂", f"{total_emissions:.6f} kg")
    
    with col2:
        total_energy = df['Energy (kWh)'].sum()
        st.metric("⚡ Total Energy", f"{total_energy:.6f} kWh")
    
    with col3:
        total_water = df['Water (L)'].sum()
        st.metric("💧 Total Water", f"{total_water:.2f} L")
    
    with col4:
        efficiency = total_emissions / total_energy if total_energy > 0 else 0
        st.metric("🔋 Efficiency", f"{efficiency:.3f} kg/kWh")
    
    # Combined time series
    st.markdown("#### 📈 Combined Environmental Impact Over Time")
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('CO₂ Emissions', 'Energy Consumption', 'Water Usage', 'Environmental Efficiency'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # CO₂ emissions
    fig.add_trace(
        go.Scatter(x=df['Timestamp'], y=df['CO₂ (kg)'], name='CO₂ (kg)', 
                  line=dict(color='#FF6B35', width=3)),
        row=1, col=1
    )
    
    # Energy consumption
    fig.add_trace(
        go.Scatter(x=df['Timestamp'], y=df['Energy (kWh)'], name='Energy (kWh)', 
                  line=dict(color='#228B22', width=3)),
        row=1, col=2
    )
    
    # Water usage
    fig.add_trace(
        go.Scatter(x=df['Timestamp'], y=df['Water (L)'], name='Water (L)', 
                  line=dict(color='#1E90FF', width=3)),
        row=2, col=1
    )
    
    # Environmental efficiency (CO₂ per kWh)
    efficiency_data = df['CO₂ (kg)'] / df['Energy (kWh)']
    fig.add_trace(
        go.Scatter(x=df['Timestamp'], y=efficiency_data, name='Efficiency (kg/kWh)', 
                  line=dict(color='#6B4F2A', width=3)),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional comparison
    st.markdown("#### 🌍 Regional Environmental Impact Comparison")
    
    regional_data = df.groupby('Region').agg({
        'CO₂ (kg)': 'sum',
        'Energy (kWh)': 'sum',
        'Water (L)': 'sum'
    }).reset_index()
    
    fig_regional = px.scatter(
        regional_data,
        x='Energy (kWh)',
        y='Water (L)',
        size='CO₂ (kg)',
        color='Region',
        title='Regional Environmental Impact: Energy vs Water vs CO₂',
        hover_data=['CO₂ (kg)']
    )
    fig_regional.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # Environmental context
    st.markdown("#### 🌍 Environmental Context")
    
    context_col1, context_col2, context_col3 = st.columns(3)
    
    with context_col1:
        trees_needed = total_emissions * 0.06
        st.metric("🌳 Trees Needed", f"{trees_needed:.2f}")
    
    with context_col2:
        car_miles = total_emissions * 2.2
        st.metric("🚗 Car Miles", f"{car_miles:.2f} miles")
    
    with context_col3:
        bottles = total_water / 0.5
        st.metric("🍼 Bottles", f"{bottles:.0f} bottles")
    
    # Detailed combined table
    st.markdown("#### 📊 Detailed Combined Environmental Data")
    st.dataframe(df, use_container_width=True)

def show_calculation_explanation_tab():
    """Show calculation explanation tab."""
    st.markdown("## 📚 How Environmental Metrics Are Calculated")
    
    with st.expander("⚡ Energy Consumption Calculation", expanded=True):
        st.markdown("""
        **Energy consumption is calculated based on:**
        
        1. **Hardware Power Consumption**: Each component (CPU, GPU, Memory) has a base power consumption
        2. **Utilization Rates**: Actual usage percentage during the workload
        3. **Runtime Duration**: Total time the workload was running
        
        **Formula**: `Energy (kWh) = (Total Power × Runtime) / 3600`
        
        **Example**: 
        - CPU: Apple M2 (25W) × 50% utilization = 12.5W
        - GPU: RTX 4090 (450W) × 80% utilization = 360W  
        - Memory: 32GB DDR5 (8W) = 8W
        - Total: 380.5W for 3600 seconds = 0.38 kWh
        """)
    
    with st.expander("💧 Water Usage Calculation", expanded=True):
        st.markdown("""
        **Water usage is calculated using regional water intensity factors:**
        
        1. **Energy Consumption**: From the energy calculation above
        2. **Water Intensity Factor**: Liters of water per kWh (varies by region/cloud provider)
        3. **Regional Factors**: Different regions have different water usage patterns
        
        **Formula**: `Water (L) = Energy (kWh) × Water Intensity Factor (L/kWh)`
        
        **Regional Water Intensity Factors**:
        - AWS US-East-1 (Virginia): 1.2 L/kWh
        - AWS US-West-2 (Oregon): 1.5 L/kWh  
        - AWS EU-West-1 (Ireland): 1.1 L/kWh
        - AWS AP-Southeast-1 (Singapore): 1.8 L/kWh
        - Local Data Centers: 1.5 L/kWh (average)
        
        **Example**: 0.38 kWh × 1.2 L/kWh = 0.46 L water
        """)
    
    with st.expander("🌍 Carbon Emissions Calculation", expanded=True):
        st.markdown("""
        **Carbon emissions are calculated using regional carbon intensity:**
        
        1. **Energy Consumption**: From the energy calculation
        2. **Carbon Intensity**: Grams of CO₂ per kWh (varies by region)
        3. **Regional Grid Mix**: Different regions have different energy sources
        
        **Formula**: `CO₂ (kg) = Energy (kWh) × Carbon Intensity (g/kWh) / 1000`
        
        **Regional Carbon Intensity**:
        - US-East-1 (Virginia): 300 g CO₂/kWh
        - US-West-2 (Oregon): 200 g CO₂/kWh (hydro-heavy)
        - EU-West-1 (Ireland): 250 g CO₂/kWh (wind-heavy)
        - AP-Southeast-1 (Singapore): 500 g CO₂/kWh (fossil-heavy)
        
        **Example**: 0.38 kWh × 300 g/kWh / 1000 = 0.114 kg CO₂
        """)
    
    with st.expander("📊 Environmental Context", expanded=True):
        st.markdown("""
        **Environmental equivalents help understand the impact:**
        
        **Carbon Emissions**:
        - 1 kg CO₂ ≈ 0.06 trees needed to offset
        - 1 kg CO₂ ≈ 2.2 miles driven by car
        
        **Water Usage**:
        - 1 liter ≈ 2 standard 500ml water bottles
        - 1 liter ≈ 1/65th of an average shower (65L)
        
        **Energy Consumption**:
        - 1 kWh ≈ 0.4 kg CO₂ (average grid)
        - 1 kWh ≈ 1.5 L water (average data center)
        """)

def main():
    """Main application function."""
    # Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #228B22 0%, #98A869 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    ">
        <h1 style="margin: 0; font-size: 3rem;">🧠 NeuroGreen</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">
            Track Carbon Emissions, Energy Consumption & Water Usage with Interactive Visualizations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Control panel
    show_control_panel()
    
    # Real-time metrics
    show_real_time_metrics()
    
    # Main content with tabs
    if st.session_state.metrics_history:
        st.markdown("## 📊 Environmental Impact Analysis")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌍 Carbon Emissions", 
            "⚡ Energy Consumption", 
            "💧 Water Usage", 
            "🌍 Combined Analysis",
            "📚 Calculations"
        ])
        
        with tab1:
            show_carbon_emissions_tab()
        
        with tab2:
            show_energy_consumption_tab()
        
        with tab3:
            show_water_usage_tab()
        
        with tab4:
            show_combined_analysis_tab()
        
        with tab5:
            show_calculation_explanation_tab()
    
    else:
        st.info("🌱 Start tracking to see environmental impact data and visualizations!")

if __name__ == "__main__":
    main()
