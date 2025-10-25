"""
🌱 Enhanced Carbon Tracker with Energy & Water Usage
===================================================

Extension of the existing carbon tracker to include energy consumption
and water usage calculations with regional water intensity factors.
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
from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv

# Import the existing carbon tracker
from src.monitoring.carbon_tracker import CarbonTracker, CarbonMetrics

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class EnhancedCarbonMetrics:
    """Enhanced carbon metrics including energy and water usage."""
    timestamp: datetime
    carbon_emissions: float           # kg CO2
    energy_consumed: float = 0.0      # kWh
    water_usage: float = 0.0          # liters
    carbon_intensity: float = 0.0     # g CO2/kWh
    water_intensity: float = 0.0      # liters/kWh
    renewable_percentage: float = 0.0  # % renewable energy
    workload_type: str = "training"   # Type of workload
    framework: str = "pytorch"        # ML framework
    gpu_utilization: float = 0.0      # GPU utilization %
    cpu_utilization: float = 0.0      # CPU utilization %
    memory_usage: float = 0.0         # Memory usage %
    region: str = "us-east-1"         # AWS region or 'local'
    cloud_provider: str = "aws"       # Cloud provider
    hardware_type: str = "unknown"    # Hardware description
    runtime_seconds: float = 0.0      # Runtime in seconds

class WaterIntensityCalculator:
    """Calculate water usage based on energy consumption and regional factors."""
    
    # Water intensity factors by cloud provider and region (liters per kWh)
    WATER_INTENSITY_FACTORS = {
        'aws': {
            'us-east-1': 1.2,      # Virginia - moderate water usage
            'us-west-2': 1.5,      # Oregon - higher due to cooling needs
            'us-west-1': 1.3,      # California
            'eu-west-1': 1.1,      # Ireland - efficient cooling
            'eu-central-1': 1.2,   # Frankfurt
            'ap-southeast-1': 1.8,  # Singapore - high humidity
            'ap-northeast-1': 1.4, # Tokyo
            'ap-south-1': 1.6,     # Mumbai
            'sa-east-1': 1.3,      # São Paulo
            'ca-central-1': 1.2,   # Canada
            'default': 1.3
        },
        'gcp': {
            'us-central1': 1.4,     # Iowa
            'us-west1': 1.6,       # Oregon
            'us-east1': 1.2,       # South Carolina
            'europe-west1': 1.0,   # Belgium - very efficient
            'europe-west4': 1.1,   # Netherlands
            'asia-southeast1': 1.9, # Singapore
            'asia-northeast1': 1.4, # Tokyo
            'asia-south1': 1.6,    # Mumbai
            'australia-southeast1': 1.5, # Sydney
            'default': 1.4
        },
        'azure': {
            'eastus': 1.3,         # Virginia
            'westus2': 1.7,        # Washington
            'centralus': 1.2,      # Iowa
            'westeurope': 1.1,     # Netherlands
            'northeurope': 1.0,    # Ireland
            'southeastasia': 1.8,   # Singapore
            'eastasia': 1.4,       # Hong Kong
            'australiaeast': 1.5,   # Sydney
            'brazilsouth': 1.3,    # São Paulo
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
    
    @classmethod
    def calculate_water_usage(cls, energy_kwh: float, cloud_provider: str, region: str) -> float:
        """Calculate water usage based on energy consumption and regional factors."""
        water_intensity = cls.get_water_intensity(cloud_provider, region)
        return energy_kwh * water_intensity

class EnergyCalculator:
    """Calculate energy consumption based on hardware specifications and runtime."""
    
    # Hardware power consumption estimates (Watts)
    HARDWARE_POWER = {
        'cpu': {
            'intel_i5': 65,         # Intel i5
            'intel_i7': 65,         # Intel i7
            'intel_i9': 95,         # Intel i9
            'intel_xeon': 150,      # Intel Xeon
            'amd_ryzen5': 65,       # AMD Ryzen 5
            'amd_ryzen7': 65,       # AMD Ryzen 7
            'amd_ryzen9': 105,        # AMD Ryzen 9
            'apple_m1': 20,         # Apple M1
            'apple_m2': 25,         # Apple M2
            'apple_m3': 30,         # Apple M3
            'apple_m1_pro': 30,     # Apple M1 Pro
            'apple_m1_max': 40,     # Apple M1 Max
            'apple_m2_pro': 35,     # Apple M2 Pro
            'apple_m2_max': 45,     # Apple M2 Max
            'default': 50
        },
        'gpu': {
            'rtx_3060': 170,        # NVIDIA RTX 3060
            'rtx_3070': 220,        # NVIDIA RTX 3070
            'rtx_3080': 320,        # NVIDIA RTX 3080
            'rtx_3090': 350,        # NVIDIA RTX 3090
            'rtx_4060': 115,        # NVIDIA RTX 4060
            'rtx_4070': 200,        # NVIDIA RTX 4070
            'rtx_4080': 320,        # NVIDIA RTX 4080
            'rtx_4090': 450,        # NVIDIA RTX 4090
            'a100': 400,            # NVIDIA A100
            'v100': 300,            # NVIDIA V100
            'tesla_t4': 70,         # NVIDIA Tesla T4
            'tesla_p100': 300,      # NVIDIA Tesla P100
            'tesla_v100': 300,      # NVIDIA Tesla V100
            'default': 200
        },
        'memory': {
            'ddr4_8gb': 3,          # 8GB DDR4
            'ddr4_16gb': 5,         # 16GB DDR4
            'ddr4_32gb': 10,        # 32GB DDR4
            'ddr4_64gb': 20,        # 64GB DDR4
            'ddr5_16gb': 4,         # 16GB DDR5
            'ddr5_32gb': 8,         # 32GB DDR5
            'ddr5_64gb': 16,        # 64GB DDR5
            'default': 8
        }
    }
    
    @classmethod
    def calculate_energy_consumption(cls, runtime_seconds: float, 
                                   hardware_specs: Dict[str, Any]) -> float:
        """Calculate energy consumption in kWh based on hardware and runtime."""
        total_power_watts = 0
        
        # CPU power consumption
        cpu_type = hardware_specs.get('cpu_type', 'default')
        cpu_utilization = hardware_specs.get('cpu_utilization', 0.5)
        cpu_power = cls.HARDWARE_POWER['cpu'].get(cpu_type, 50)
        total_power_watts += cpu_power * cpu_utilization
        
        # GPU power consumption (if GPU is used)
        gpu_type = hardware_specs.get('gpu_type', 'none')
        gpu_utilization = hardware_specs.get('gpu_utilization', 0.0)
        if gpu_type != 'none' and gpu_utilization > 0:
            gpu_power = cls.HARDWARE_POWER['gpu'].get(gpu_type, 200)
            total_power_watts += gpu_power * gpu_utilization
        
        # Memory power consumption
        memory_type = hardware_specs.get('memory_type', 'default')
        memory_power = cls.HARDWARE_POWER['memory'].get(memory_type, 8)
        total_power_watts += memory_power
        
        # Convert to kWh
        energy_kwh = (total_power_watts * runtime_seconds) / 3600000
        return energy_kwh

class EnhancedCarbonTracker(CarbonTracker):
    """Enhanced carbon tracker with energy and water usage calculations."""
    
    def __init__(self, project_name: str = "GreenAI", tracking_mode: str = "process",
                 region: str = "us-east-1", cloud_provider: str = "aws"):
        super().__init__(project_name, tracking_mode)
        self.region = region
        self.cloud_provider = cloud_provider
        self.enhanced_metrics_history: List[EnhancedCarbonMetrics] = []
        self.current_hardware_specs: Dict[str, Any] = {}
    
    def set_hardware_specs(self, hardware_specs: Dict[str, Any]):
        """Set hardware specifications for energy calculations."""
        self.current_hardware_specs = hardware_specs
    
    def start_tracking(self, workload_type: str = "training", framework: str = "pytorch",
                      hardware_specs: Dict[str, Any] = None) -> str:
        """Start enhanced environmental tracking."""
        if hardware_specs:
            self.set_hardware_specs(hardware_specs)
        
        # Start the base carbon tracking
        session_id = super().start_tracking(workload_type, framework)
        
        # Store additional metadata
        self.current_hardware_specs.update({
            'workload_type': workload_type,
            'framework': framework,
            'region': self.region,
            'cloud_provider': self.cloud_provider
        })
        
        return session_id
    
    def stop_tracking(self, session_id: str = None) -> Optional[EnhancedCarbonMetrics]:
        """Stop tracking and return enhanced environmental metrics."""
        # Stop the base carbon tracking
        base_metrics = super().stop_tracking(session_id)
        
        if not base_metrics:
            return None
        
        # Calculate runtime from start and end times
        if self.start_time:
            runtime_seconds = (datetime.now() - self.start_time).total_seconds()
        else:
            runtime_seconds = 0.0
        
        # Calculate energy consumption
        energy_kwh = EnergyCalculator.calculate_energy_consumption(
            runtime_seconds, self.current_hardware_specs
        )
        
        # Calculate water usage
        water_usage = WaterIntensityCalculator.calculate_water_usage(
            energy_kwh, self.cloud_provider, self.region
        )
        
        # Get water intensity factor
        water_intensity = WaterIntensityCalculator.get_water_intensity(
            self.cloud_provider, self.region
        )
        
        # Get renewable percentage for the region
        renewable_percentage = self._get_renewable_percentage()
        
        # Create enhanced metrics
        enhanced_metrics = EnhancedCarbonMetrics(
            timestamp=base_metrics.timestamp,
            carbon_emissions=base_metrics.carbon_emissions,
            carbon_intensity=base_metrics.carbon_intensity,
            renewable_percentage=renewable_percentage,
            workload_type=base_metrics.workload_type,
            framework=base_metrics.framework,
            gpu_utilization=base_metrics.gpu_utilization,
            cpu_utilization=base_metrics.cpu_utilization,
            memory_usage=base_metrics.memory_usage,
            # Enhanced fields
            energy_consumed=energy_kwh,
            water_usage=water_usage,
            water_intensity=water_intensity,
            region=self.region,
            cloud_provider=self.cloud_provider,
            hardware_type=self._get_hardware_type()
        )
        
        self.enhanced_metrics_history.append(enhanced_metrics)
        
        logger.info(f"Enhanced tracking stopped. Energy: {energy_kwh:.6f} kWh, "
                   f"Water: {water_usage:.6f} L, Emissions: {base_metrics.carbon_emissions:.6f} kg CO2")
        
        return enhanced_metrics
    
    def get_carbon_intensity(self) -> float:
        """Get carbon intensity for the region (g CO2/kWh)."""
        carbon_intensity_by_region = {
            'us-east-1': 300,      # Virginia - mixed grid
            'us-west-2': 200,      # Oregon - hydro-heavy
            'us-west-1': 250,      # California - renewable-heavy
            'eu-west-1': 250,      # Ireland - wind-heavy
            'eu-central-1': 300,   # Germany - mixed
            'ap-southeast-1': 500, # Singapore - fossil-heavy
            'ap-northeast-1': 400, # Japan - mixed
            'ap-south-1': 600,     # India - coal-heavy
            'sa-east-1': 200,     # Brazil - hydro-heavy
            'ca-central-1': 150,   # Canada - hydro-heavy
            'local': 350           # Average for local grids
        }
        return carbon_intensity_by_region.get(self.region.lower(), 350)
    
    def _get_renewable_percentage(self) -> float:
        """Get renewable energy percentage for the region."""
        renewable_by_region = {
            'us-east-1': 30,       # Virginia - mixed grid
            'us-west-2': 80,       # Oregon - hydro-heavy
            'us-west-1': 60,       # California - renewable-heavy
            'eu-west-1': 70,       # Ireland - wind-heavy
            'eu-central-1': 50,    # Germany - mixed
            'ap-southeast-1': 20,  # Singapore - fossil-heavy
            'ap-northeast-1': 30,   # Japan - mixed
            'ap-south-1': 25,      # India - coal-heavy
            'sa-east-1': 60,       # Brazil - hydro-heavy
            'ca-central-1': 80,    # Canada - hydro-heavy
            'local': 40            # Average for local grids
        }
        return renewable_by_region.get(self.region.lower(), 40)
    
    def _get_hardware_type(self) -> str:
        """Get hardware type description."""
        if not self.current_hardware_specs:
            return "unknown"
        
        cpu_type = self.current_hardware_specs.get('cpu_type', 'unknown')
        gpu_type = self.current_hardware_specs.get('gpu_type', 'none')
        
        if gpu_type != 'none':
            return f"{cpu_type} + {gpu_type}"
        else:
            return cpu_type
    
    def get_enhanced_summary(self) -> Dict[str, Any]:
        """Get enhanced summary statistics."""
        if not self.enhanced_metrics_history:
            return {}
        
        total_emissions = sum(m.carbon_emissions for m in self.enhanced_metrics_history)
        total_energy = sum(m.energy_consumed for m in self.enhanced_metrics_history)
        total_water = sum(m.water_usage for m in self.enhanced_metrics_history)
        
        avg_carbon_intensity = np.mean([m.carbon_intensity for m in self.enhanced_metrics_history])
        avg_water_intensity = np.mean([m.water_intensity for m in self.enhanced_metrics_history])
        avg_renewable = np.mean([m.renewable_percentage for m in self.enhanced_metrics_history])
        
        return {
            'total_runs': len(self.enhanced_metrics_history),
            'total_emissions_kg': total_emissions,
            'total_energy_kwh': total_energy,
            'total_water_liters': total_water,
            'avg_carbon_intensity': avg_carbon_intensity,
            'avg_water_intensity': avg_water_intensity,
            'avg_renewable_percentage': avg_renewable,
            'trees_needed': total_emissions * 0.06,
            'car_miles': total_emissions * 2.2,
            'bottles_equivalent': total_water / 0.5,
            'shower_equivalent': total_water / 65,
            'energy_efficiency': total_emissions / total_energy if total_energy > 0 else 0
        }

def create_enhanced_metric_card(title: str, value: str, unit: str, icon: str, 
                               color: str = "#228B22", help_text: str = None) -> str:
    """Create an enhanced metric card with help text."""
    help_html = f'<div class="help-text" title="{help_text}">ℹ️</div>' if help_text else ''
    
    return f"""
    <div class="enhanced-metric-card" style="border-left: 4px solid {color};">
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
    
    # Initialize enhanced tracker if not in session state
    if 'enhanced_tracker' not in st.session_state:
        st.session_state.enhanced_tracker = EnhancedCarbonTracker()
    
    tracker = st.session_state.enhanced_tracker
    
    # Control panel
    with st.expander("🎛️ Enhanced Tracking Controls", expanded=True):
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
                ["pytorch", "tensorflow", "scikit-learn", "huggingface", "transformers", "custom"],
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
            if st.button("🌱 Start Enhanced Tracking", type="primary"):
                hardware_specs = {
                    'cpu_type': cpu_type,
                    'gpu_type': gpu_type,
                    'memory_type': memory_type,
                    'cpu_utilization': 0.5,
                    'gpu_utilization': 0.0 if gpu_type == 'none' else 0.8,
                    'memory_usage': 0.5
                }
                
                tracker.region = region
                tracker.cloud_provider = cloud_provider
                
                session_id = tracker.start_tracking(workload_type, framework, hardware_specs)
                st.session_state.tracking_active = True
                st.success(f"🌱 Enhanced environmental tracking started: {session_id}")
        
        with col2:
            if st.button("🛑 Stop Enhanced Tracking"):
                if st.session_state.get('tracking_active', False):
                    metrics = tracker.stop_tracking()
                    if metrics:
                        st.session_state.tracking_active = False
                        st.success("✅ Enhanced environmental tracking stopped!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to stop tracking")
                else:
                    st.warning("⚠️ No active tracking to stop")
    
    # Real-time metrics
    if st.session_state.get('tracking_active', False):
        st.markdown("### 📊 Real-time Enhanced Metrics")
        
        if tracker.start_time:
            current_runtime = (datetime.now() - tracker.start_time).total_seconds()
            current_energy = EnergyCalculator.calculate_energy_consumption(
                current_runtime, tracker.current_hardware_specs
            )
            current_water = WaterIntensityCalculator.calculate_water_usage(
                current_energy, tracker.cloud_provider, tracker.region
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
    if tracker.enhanced_metrics_history:
        st.markdown("### 📈 Enhanced Environmental Impact Summary")
        
        # Get enhanced summary statistics
        stats = tracker.get_enhanced_summary()
        
        # Display enhanced metrics
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
        
        context_col1, context_col2, context_col3, context_col4 = st.columns(4)
        
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
        
        with context_col4:
            st.metric(
                "⚡ Efficiency",
                f"{stats['energy_efficiency']:.3f} kg/kWh",
                help="Carbon intensity (kg CO₂ per kWh)"
            )
        
        # Detailed metrics table
        st.markdown("#### 📊 Enhanced Metrics Table")
        
        # Create DataFrame from enhanced metrics history
        df_data = []
        for metrics in tracker.enhanced_metrics_history:
            df_data.append({
                'Timestamp': metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Workload': metrics.workload_type,
                'Framework': metrics.framework,
                'Region': metrics.region,
                'Cloud': metrics.cloud_provider,
                'Hardware': metrics.hardware_type,
                'Runtime (s)': f"{metrics.runtime_seconds:.1f}",
                'Energy (kWh)': f"{metrics.energy_consumed:.6f}",
                'Water (L)': f"{metrics.water_usage:.2f}",
                'CO₂ (kg)': f"{metrics.carbon_emissions:.6f}",
                'Carbon Intensity (g/kWh)': f"{metrics.carbon_intensity:.1f}",
                'Water Intensity (L/kWh)': f"{metrics.water_intensity:.1f}",
                'Renewable %': f"{metrics.renewable_percentage:.1f}%"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Enhanced visualizations
        st.markdown("#### 📈 Enhanced Environmental Visualizations")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Energy vs Water scatter plot
            fig_scatter = px.scatter(
                df,
                x='Energy (kWh)',
                y='Water (L)',
                size='CO₂ (kg)',
                color='Region',
                hover_data=['Framework', 'Hardware'],
                title='⚡💧 Energy vs Water Usage by Region',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with viz_col2:
            # Regional comparison
            regional_data = df.groupby('Region').agg({
                'Energy (kWh)': lambda x: sum(float(val) for val in x),
                'Water (L)': lambda x: sum(float(val) for val in x),
                'CO₂ (kg)': lambda x: sum(float(val) for val in x)
            }).reset_index()
            
            fig_regional = px.bar(
                regional_data,
                x='Region',
                y=['Energy (kWh)', 'Water (L)', 'CO₂ (kg)'],
                title='🌍 Regional Environmental Impact Comparison',
                barmode='group'
            )
            fig_regional.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_regional, use_container_width=True)
        
        # Time series analysis
        st.markdown("#### 📊 Time Series Analysis")
        
        # Convert string values back to float for plotting
        df_plot = df.copy()
        df_plot['Energy (kWh)'] = df_plot['Energy (kWh)'].astype(float)
        df_plot['Water (L)'] = df_plot['Water (L)'].astype(float)
        df_plot['CO₂ (kg)'] = df_plot['CO₂ (kg)'].astype(float)
        
        fig_timeseries = go.Figure()
        
        # Add energy consumption
        fig_timeseries.add_trace(go.Scatter(
            x=df_plot['Timestamp'],
            y=df_plot['Energy (kWh)'],
            mode='lines+markers',
            name='Energy (kWh)',
            line=dict(color='#228B22', width=3),
            yaxis='y'
        ))
        
        # Add water usage (scaled)
        fig_timeseries.add_trace(go.Scatter(
            x=df_plot['Timestamp'],
            y=df_plot['Water (L)'] * 10,  # Scale for visibility
            mode='lines+markers',
            name='Water (L × 10)',
            line=dict(color='#1E90FF', width=3),
            yaxis='y2'
        ))
        
        # Add CO2 emissions (scaled)
        fig_timeseries.add_trace(go.Scatter(
            x=df_plot['Timestamp'],
            y=df_plot['CO₂ (kg)'] * 1000,  # Scale for visibility
            mode='lines+markers',
            name='CO₂ (kg × 1000)',
            line=dict(color='#FF6B35', width=3),
            yaxis='y3'
        ))
        
        fig_timeseries.update_layout(
            title='🌍 Environmental Impact Over Time',
            xaxis=dict(title='Timestamp'),
            yaxis=dict(title='Energy (kWh)', side='left'),
            yaxis2=dict(title='Water (L)', side='right', overlaying='y'),
            yaxis3=dict(title='CO₂ (kg)', side='right', overlaying='y', position=0.85),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_timeseries, use_container_width=True)
    
    else:
        st.info("🌱 Start enhanced tracking to see environmental impact data!")

def main():
    """Main application function."""
    st.set_page_config(
        page_title="🌱 Enhanced Environmental Tracker",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for enhanced metrics
    st.markdown("""
    <style>
    .enhanced-metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
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
            Track Carbon Emissions, Energy Consumption & Water Usage with Regional Factors
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main dashboard
    show_enhanced_dashboard()

if __name__ == "__main__":
    main()
