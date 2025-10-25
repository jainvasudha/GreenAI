"""
🌱 Enhanced Environmental Tracker
================================

Extended carbon tracking with energy consumption and water usage calculations
using regional water intensity factors and cloud-specific data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class EnvironmentalMetrics:
    """Enhanced environmental metrics including energy and water usage."""
    timestamp: datetime
    carbon_emissions: float  # kg CO2
    energy_consumed: float    # kWh
    water_usage: float       # liters
    carbon_intensity: float  # g CO2/kWh
    water_intensity: float   # liters/kWh
    renewable_percentage: float  # %
    region: str
    cloud_provider: str
    workload_type: str
    framework: str
    runtime_seconds: float
    hardware_type: str
    gpu_utilization: float
    cpu_utilization: float
    memory_usage: float

class WaterIntensityData:
    """Water intensity data for different regions and cloud providers."""
    
    # Default water intensity factors (liters per kWh)
    # Based on published research and cloud provider data
    WATER_INTENSITY_FACTORS = {
        'aws': {
            'us-east-1': 1.2,      # Virginia
            'us-west-2': 1.5,      # Oregon
            'eu-west-1': 1.1,      # Ireland
            'ap-southeast-1': 1.8,  # Singapore
            'default': 1.3
        },
        'gcp': {
            'us-central1': 1.4,     # Iowa
            'us-west1': 1.6,       # Oregon
            'europe-west1': 1.0,   # Belgium
            'asia-southeast1': 1.9, # Singapore
            'default': 1.4
        },
        'azure': {
            'eastus': 1.3,         # Virginia
            'westus2': 1.7,        # Washington
            'westeurope': 1.1,     # Netherlands
            'southeastasia': 1.8,  # Singapore
            'default': 1.4
        },
        'local': {
            'default': 1.5  # Average for local data centers
        }
    }
    
    @classmethod
    def get_water_intensity(cls, cloud_provider: str, region: str) -> float:
        """Get water intensity factor for a specific cloud provider and region."""
        provider_data = cls.WATER_INTENSITY_FACTORS.get(cloud_provider.lower(), {})
        return provider_data.get(region.lower(), provider_data.get('default', 1.5))

class EnergyCalculator:
    """Calculate energy consumption based on hardware and runtime."""
    
    # Hardware power consumption estimates (Watts)
    HARDWARE_POWER_CONSUMPTION = {
        'cpu': {
            'intel_i7': 65,      # Intel i7
            'intel_i9': 95,      # Intel i9
            'amd_ryzen7': 65,    # AMD Ryzen 7
            'amd_ryzen9': 105,   # AMD Ryzen 9
            'apple_m1': 20,       # Apple M1
            'apple_m2': 25,       # Apple M2
            'apple_m3': 30,       # Apple M3
            'default': 50
        },
        'gpu': {
            'rtx_3080': 320,     # NVIDIA RTX 3080
            'rtx_3090': 350,     # NVIDIA RTX 3090
            'rtx_4080': 320,     # NVIDIA RTX 4080
            'rtx_4090': 450,     # NVIDIA RTX 4090
            'a100': 400,         # NVIDIA A100
            'v100': 300,         # NVIDIA V100
            'tesla_t4': 70,      # NVIDIA Tesla T4
            'default': 200
        },
        'memory': {
            'ddr4_16gb': 5,      # 16GB DDR4
            'ddr4_32gb': 10,     # 32GB DDR4
            'ddr5_16gb': 4,      # 16GB DDR5
            'ddr5_32gb': 8,      # 32GB DDR5
            'default': 8
        }
    }
    
    @classmethod
    def calculate_energy_consumption(cls, runtime_seconds: float, 
                                   hardware_specs: Dict[str, Any]) -> float:
        """Calculate energy consumption in kWh."""
        total_power_watts = 0
        
        # CPU power
        cpu_type = hardware_specs.get('cpu_type', 'default')
        cpu_utilization = hardware_specs.get('cpu_utilization', 0.5)
        cpu_power = cls.HARDWARE_POWER_CONSUMPTION['cpu'].get(cpu_type, 50)
        total_power_watts += cpu_power * cpu_utilization
        
        # GPU power
        gpu_type = hardware_specs.get('gpu_type', 'default')
        gpu_utilization = hardware_specs.get('gpu_utilization', 0.0)
        if gpu_utilization > 0:
            gpu_power = cls.HARDWARE_POWER_CONSUMPTION['gpu'].get(gpu_type, 200)
            total_power_watts += gpu_power * gpu_utilization
        
        # Memory power
        memory_gb = hardware_specs.get('memory_gb', 16)
        memory_power = cls.HARDWARE_POWER_CONSUMPTION['memory'].get(f'ddr4_{memory_gb}gb', 8)
        total_power_watts += memory_power
        
        # Convert to kWh
        energy_kwh = (total_power_watts * runtime_seconds) / 3600000  # Convert to kWh
        return energy_kwh

class EnvironmentalTracker:
    """Enhanced environmental tracker with energy and water calculations."""
    
    def __init__(self, project_name: str = "GreenAI", region: str = "us-east-1", 
                 cloud_provider: str = "aws"):
        self.project_name = project_name
        self.region = region
        self.cloud_provider = cloud_provider
        self.metrics_history: List[EnvironmentalMetrics] = []
        self.current_run = None
        self.start_time = None
        
    def start_tracking(self, workload_type: str = "training", framework: str = "pytorch",
                      hardware_specs: Dict[str, Any] = None) -> str:
        """Start environmental tracking."""
        if hardware_specs is None:
            hardware_specs = self._get_default_hardware_specs()
        
        self.start_time = datetime.now()
        self.current_run = {
            'workload_type': workload_type,
            'framework': framework,
            'hardware_specs': hardware_specs,
            'start_time': self.start_time
        }
        
        session_id = f"{workload_type}_{framework}_{int(self.start_time.timestamp())}"
        logger.info(f"Started environmental tracking: {session_id}")
        return session_id
    
    def stop_tracking(self) -> Optional[EnvironmentalMetrics]:
        """Stop tracking and calculate environmental metrics."""
        if not self.current_run or not self.start_time:
            logger.warning("No active tracking to stop")
            return None
        
        end_time = datetime.now()
        runtime_seconds = (end_time - self.start_time).total_seconds()
        
        # Calculate energy consumption
        energy_kwh = EnergyCalculator.calculate_energy_consumption(
            runtime_seconds, self.current_run['hardware_specs']
        )
        
        # Calculate carbon emissions (simplified calculation)
        # In practice, this would use CodeCarbon or similar
        carbon_intensity = self._get_carbon_intensity()
        carbon_emissions = energy_kwh * carbon_intensity / 1000  # Convert to kg CO2
        
        # Calculate water usage
        water_intensity = WaterIntensityData.get_water_intensity(
            self.cloud_provider, self.region
        )
        water_usage = energy_kwh * water_intensity
        
        # Get renewable percentage
        renewable_percentage = self._get_renewable_percentage()
        
        # Create metrics object
        metrics = EnvironmentalMetrics(
            timestamp=end_time,
            carbon_emissions=carbon_emissions,
            energy_consumed=energy_kwh,
            water_usage=water_usage,
            carbon_intensity=carbon_intensity,
            water_intensity=water_intensity,
            renewable_percentage=renewable_percentage,
            region=self.region,
            cloud_provider=self.cloud_provider,
            workload_type=self.current_run['workload_type'],
            framework=self.current_run['framework'],
            runtime_seconds=runtime_seconds,
            hardware_type=self._get_hardware_type(),
            gpu_utilization=self.current_run['hardware_specs'].get('gpu_utilization', 0.0),
            cpu_utilization=self.current_run['hardware_specs'].get('cpu_utilization', 0.5),
            memory_usage=self.current_run['hardware_specs'].get('memory_usage', 0.5)
        )
        
        self.metrics_history.append(metrics)
        self.current_run = None
        self.start_time = None
        
        logger.info(f"Stopped environmental tracking. Emissions: {carbon_emissions:.6f} kg CO2, "
                   f"Energy: {energy_kwh:.6f} kWh, Water: {water_usage:.6f} L")
        
        return metrics
    
    def _get_default_hardware_specs(self) -> Dict[str, Any]:
        """Get default hardware specifications."""
        return {
            'cpu_type': 'apple_m2',  # Default for Mac
            'gpu_type': 'default',
            'memory_gb': 16,
            'cpu_utilization': 0.5,
            'gpu_utilization': 0.0,
            'memory_usage': 0.5
        }
    
    def _get_carbon_intensity(self) -> float:
        """Get carbon intensity for the region (g CO2/kWh)."""
        # Simplified carbon intensity by region
        carbon_intensity_by_region = {
            'us-east-1': 300,      # Virginia - mixed grid
            'us-west-2': 200,      # Oregon - hydro-heavy
            'eu-west-1': 250,      # Ireland - wind-heavy
            'ap-southeast-1': 500, # Singapore - fossil-heavy
            'default': 350
        }
        return carbon_intensity_by_region.get(self.region.lower(), 350)
    
    def _get_renewable_percentage(self) -> float:
        """Get renewable energy percentage for the region."""
        renewable_by_region = {
            'us-east-1': 30,       # Virginia
            'us-west-2': 80,       # Oregon
            'eu-west-1': 70,       # Ireland
            'ap-southeast-1': 20,  # Singapore
            'default': 40
        }
        return renewable_by_region.get(self.region.lower(), 40)
    
    def _get_hardware_type(self) -> str:
        """Get hardware type description."""
        if self.current_run:
            specs = self.current_run['hardware_specs']
            cpu = specs.get('cpu_type', 'unknown')
            gpu = specs.get('gpu_type', 'none')
            return f"{cpu} + {gpu}" if gpu != 'none' else cpu
        return "unknown"
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for all tracked runs."""
        if not self.metrics_history:
            return {}
        
        total_emissions = sum(m.carbon_emissions for m in self.metrics_history)
        total_energy = sum(m.energy_consumed for m in self.metrics_history)
        total_water = sum(m.water_usage for m in self.metrics_history)
        
        avg_carbon_intensity = np.mean([m.carbon_intensity for m in self.metrics_history])
        avg_water_intensity = np.mean([m.water_intensity for m in self.metrics_history])
        avg_renewable = np.mean([m.renewable_percentage for m in self.metrics_history])
        
        return {
            'total_runs': len(self.metrics_history),
            'total_emissions_kg': total_emissions,
            'total_energy_kwh': total_energy,
            'total_water_liters': total_water,
            'avg_carbon_intensity': avg_carbon_intensity,
            'avg_water_intensity': avg_water_intensity,
            'avg_renewable_percentage': avg_renewable,
            'trees_needed': total_emissions * 0.06,  # 1 kg CO2 ≈ 0.06 trees
            'car_miles': total_emissions * 2.2,      # 1 kg CO2 ≈ 2.2 car miles
            'bottles_equivalent': total_water / 0.5,   # 500ml bottles
            'shower_equivalent': total_water / 65     # Average shower uses 65L
        }

def create_environmental_metric_card(title: str, value: str, unit: str, 
                                   icon: str, color: str = "#228B22", 
                                   help_text: str = None) -> str:
    """Create a styled metric card for environmental data."""
    help_html = f'<div class="help-text" title="{help_text}">ℹ️</div>' if help_text else ''
    
    return f"""
    <div class="metric-card" style="background: linear-gradient(135deg, {color}15 0%, {color}25 100%); border-left: 4px solid {color};">
        <div class="metric-header">
            <span class="metric-icon">{icon}</span>
            <span class="metric-title">{title}</span>
            {help_html}
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>
    """

def show_enhanced_dashboard():
    """Show enhanced dashboard with energy and water metrics."""
    st.markdown("## 🌱 Enhanced Environmental Dashboard")
    
    # Initialize tracker if not in session state
    if 'env_tracker' not in st.session_state:
        st.session_state.env_tracker = EnvironmentalTracker()
    
    tracker = st.session_state.env_tracker
    
    # Control panel
    with st.expander("🎛️ Tracking Controls", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            workload_type = st.selectbox(
                "Workload Type",
                ["training", "inference", "data_processing", "evaluation"],
                help="Type of AI workload being performed"
            )
        
        with col2:
            framework = st.selectbox(
                "Framework",
                ["pytorch", "tensorflow", "scikit-learn", "huggingface", "custom"],
                help="ML framework being used"
            )
        
        with col3:
            region = st.selectbox(
                "Region",
                ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "local"],
                help="Geographic region for carbon/water intensity calculations"
            )
        
        # Hardware specifications
        st.markdown("#### 🔧 Hardware Specifications")
        hw_col1, hw_col2, hw_col3 = st.columns(3)
        
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
            memory_gb = st.selectbox(
                "Memory (GB)",
                [8, 16, 32, 64, 128],
                help="Total system memory"
            )
        
        # Tracking controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌱 Start Environmental Tracking", type="primary"):
                hardware_specs = {
                    'cpu_type': cpu_type,
                    'gpu_type': gpu_type,
                    'memory_gb': memory_gb,
                    'cpu_utilization': 0.5,
                    'gpu_utilization': 0.0 if gpu_type == 'none' else 0.8,
                    'memory_usage': 0.5
                }
                
                tracker.region = region
                tracker.cloud_provider = "aws" if region != "local" else "local"
                
                session_id = tracker.start_tracking(workload_type, framework, hardware_specs)
                st.session_state.tracking_active = True
                st.success(f"🌱 Environmental tracking started: {session_id}")
        
        with col2:
            if st.button("🛑 Stop Tracking"):
                if st.session_state.get('tracking_active', False):
                    metrics = tracker.stop_tracking()
                    if metrics:
                        st.session_state.tracking_active = False
                        st.success("✅ Environmental tracking stopped!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to stop tracking")
                else:
                    st.warning("⚠️ No active tracking to stop")
    
    # Real-time metrics
    if st.session_state.get('tracking_active', False):
        st.markdown("### 📊 Real-time Environmental Metrics")
        
        # Calculate current metrics
        if tracker.start_time:
            current_runtime = (datetime.now() - tracker.start_time).total_seconds()
            current_energy = EnergyCalculator.calculate_energy_consumption(
                current_runtime, tracker.current_run['hardware_specs']
            )
            current_water = current_energy * WaterIntensityData.get_water_intensity(
                tracker.cloud_provider, tracker.region
            )
            current_emissions = current_energy * tracker._get_carbon_intensity() / 1000
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("⏱️ Runtime", f"{current_runtime:.1f}s", "🟢 Active")
            
            with col2:
                st.metric("⚡ Energy", f"{current_energy:.4f} kWh", "📈 Growing")
            
            with col3:
                st.metric("💧 Water", f"{current_water:.2f} L", "💧 Usage")
            
            with col4:
                st.metric("🌍 CO₂", f"{current_emissions:.6f} kg", "📊 Emissions")
    
    # Historical data
    if tracker.metrics_history:
        st.markdown("### 📈 Environmental Impact Summary")
        
        # Get summary statistics
        stats = tracker.get_summary_stats()
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🌍 Total CO₂",
                f"{stats['total_emissions_kg']:.6f} kg",
                help="Total carbon dioxide emissions across all runs"
            )
        
        with col2:
            st.metric(
                "⚡ Total Energy",
                f"{stats['total_energy_kwh']:.4f} kWh",
                help="Total energy consumption across all runs"
            )
        
        with col3:
            st.metric(
                "💧 Total Water",
                f"{stats['total_water_liters']:.2f} L",
                help="Total water usage across all runs"
            )
        
        with col4:
            st.metric(
                "🌱 Trees Needed",
                f"{stats['trees_needed']:.2f}",
                help="Number of trees needed to offset emissions"
            )
        
        # Environmental context
        st.markdown("#### 🌍 Environmental Context")
        
        context_col1, context_col2, context_col3 = st.columns(3)
        
        with context_col1:
            st.metric(
                "🚗 Car Miles",
                f"{stats['car_miles']:.2f} miles",
                help="Equivalent distance driven by car"
            )
        
        with context_col2:
            st.metric(
                "🍼 Bottles",
                f"{stats['bottles_equivalent']:.0f} bottles",
                help="Equivalent to 500ml water bottles"
            )
        
        with context_col3:
            st.metric(
                "🚿 Showers",
                f"{stats['shower_equivalent']:.1f} showers",
                help="Equivalent to average shower usage"
            )
        
        # Detailed metrics table
        st.markdown("#### 📊 Detailed Metrics")
        
        # Create DataFrame from metrics history
        df_data = []
        for metrics in tracker.metrics_history:
            df_data.append({
                'Timestamp': metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Workload': metrics.workload_type,
                'Framework': metrics.framework,
                'Runtime (s)': f"{metrics.runtime_seconds:.1f}",
                'Energy (kWh)': f"{metrics.energy_consumed:.6f}",
                'Water (L)': f"{metrics.water_usage:.2f}",
                'CO₂ (kg)': f"{metrics.carbon_emissions:.6f}",
                'Carbon Intensity (g/kWh)': f"{metrics.carbon_intensity:.1f}",
                'Water Intensity (L/kWh)': f"{metrics.water_intensity:.1f}",
                'Renewable %': f"{metrics.renewable_percentage:.1f}%",
                'Region': metrics.region
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Visualizations
        st.markdown("#### 📈 Environmental Impact Visualizations")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Energy consumption over time
            fig_energy = px.bar(
                df, 
                x='Timestamp', 
                y='Energy (kWh)',
                title='⚡ Energy Consumption Over Time',
                color='Energy (kWh)',
                color_continuous_scale='Greens'
            )
            fig_energy.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_energy, use_container_width=True)
        
        with viz_col2:
            # Water usage over time
            fig_water = px.bar(
                df, 
                x='Timestamp', 
                y='Water (L)',
                title='💧 Water Usage Over Time',
                color='Water (L)',
                color_continuous_scale='Blues'
            )
            fig_water.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_water, use_container_width=True)
        
        # Combined environmental impact
        st.markdown("#### 🌍 Combined Environmental Impact")
        
        # Create a combined chart
        fig_combined = go.Figure()
        
        # Add energy consumption
        fig_combined.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Energy (kWh)'].astype(float),
            mode='lines+markers',
            name='Energy (kWh)',
            line=dict(color='#228B22', width=3),
            yaxis='y'
        ))
        
        # Add water usage (scaled)
        fig_combined.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Water (L)'].astype(float) * 10,  # Scale for visibility
            mode='lines+markers',
            name='Water (L × 10)',
            line=dict(color='#1E90FF', width=3),
            yaxis='y2'
        ))
        
        # Add CO2 emissions (scaled)
        fig_combined.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['CO₂ (kg)'].astype(float) * 1000,  # Scale for visibility
            mode='lines+markers',
            name='CO₂ (kg × 1000)',
            line=dict(color='#FF6B35', width=3),
            yaxis='y3'
        ))
        
        fig_combined.update_layout(
            title='🌍 Combined Environmental Impact Over Time',
            xaxis=dict(title='Timestamp'),
            yaxis=dict(title='Energy (kWh)', side='left'),
            yaxis2=dict(title='Water (L)', side='right', overlaying='y'),
            yaxis3=dict(title='CO₂ (kg)', side='right', overlaying='y', position=0.85),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_combined, use_container_width=True)
        
        # Regional comparison
        st.markdown("#### 🌍 Regional Impact Comparison")
        
        regional_data = df.groupby('Region').agg({
            'Energy (kWh)': lambda x: sum(float(val) for val in x),
            'Water (L)': lambda x: sum(float(val) for val in x),
            'CO₂ (kg)': lambda x: sum(float(val) for val in x)
        }).reset_index()
        
        fig_regional = px.scatter(
            regional_data,
            x='Energy (kWh)',
            y='Water (L)',
            size='CO₂ (kg)',
            color='Region',
            title='🌍 Regional Environmental Impact',
            hover_data=['CO₂ (kg)']
        )
        
        fig_regional.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_regional, use_container_width=True)
    
    else:
        st.info("🌱 Start tracking to see environmental impact data!")

def show_calculation_explanation():
    """Show explanation of how environmental metrics are calculated."""
    st.markdown("## 📚 How Environmental Metrics Are Calculated")
    
    with st.expander("⚡ Energy Consumption Calculation", expanded=True):
        st.markdown("""
        **Energy consumption is calculated based on:**
        
        1. **Hardware Power Consumption**: Each component (CPU, GPU, Memory) has a base power consumption
        2. **Utilization Rates**: Actual usage percentage during the workload
        3. **Runtime Duration**: Total time the workload was running
        
        **Formula**: `Energy (kWh) = (Total Power × Runtime) / 3600`
        
        **Example**: 
        - CPU: 65W × 50% utilization = 32.5W
        - GPU: 200W × 80% utilization = 160W  
        - Memory: 8W
        - Total: 200.5W for 3600 seconds = 0.2 kWh
        """)
    
    with st.expander("💧 Water Usage Calculation", expanded=True):
        st.markdown("""
        **Water usage is calculated using regional water intensity factors:**
        
        1. **Energy Consumption**: From the energy calculation above
        2. **Water Intensity Factor**: Liters of water per kWh (varies by region/cloud provider)
        3. **Regional Factors**: Different regions have different water usage patterns
        
        **Formula**: `Water (L) = Energy (kWh) × Water Intensity Factor`
        
        **Regional Water Intensity Factors**:
        - AWS US-East-1 (Virginia): 1.2 L/kWh
        - AWS US-West-2 (Oregon): 1.5 L/kWh  
        - AWS EU-West-1 (Ireland): 1.1 L/kWh
        - AWS AP-Southeast-1 (Singapore): 1.8 L/kWh
        - Local Data Centers: 1.5 L/kWh (average)
        
        **Example**: 0.2 kWh × 1.2 L/kWh = 0.24 L water
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
        
        **Example**: 0.2 kWh × 300 g/kWh / 1000 = 0.06 kg CO₂
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
    st.set_page_config(
        page_title="🌱 Enhanced Environmental Tracker",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
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
    
    .stButton > button {
        background: linear-gradient(135deg, #228B22 0%, #98A869 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(34, 139, 34, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
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
        <h1 style="margin: 0; font-size: 3rem;">🌱 Enhanced Environmental Tracker</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">
            Track Carbon Emissions, Energy Consumption & Water Usage
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.selectbox(
            "Select Page",
            ["Environmental Dashboard", "Calculation Explanation"]
        )
    
    # Main content
    if page == "Environmental Dashboard":
        show_enhanced_dashboard()
    elif page == "Calculation Explanation":
        show_calculation_explanation()

if __name__ == "__main__":
    main()
