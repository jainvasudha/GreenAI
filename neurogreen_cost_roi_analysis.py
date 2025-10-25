#!/usr/bin/env python3
"""
🧠 NeuroGreen - Cost & ROI Analysis Platform
============================================

Enhanced NeuroGreen with automated cost and ROI analysis:
- Real-time cost calculations for carbon, energy, and water
- ROI analysis with value projections
- Interactive cost dashboard
- Export capabilities for reports
- Regional pricing configuration
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import json

# Page configuration
st.set_page_config(
    page_title="NeuroGreen",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class CostMetrics:
    """Cost metrics for environmental impact."""
    carbon_cost: float
    energy_cost: float
    water_cost: float
    total_cost: float
    carbon_price: float
    energy_price: float
    water_price: float

@dataclass
class ROIMetrics:
    """ROI analysis metrics."""
    project_value: float
    total_cost: float
    roi_ratio: float
    roi_percentage: float
    payback_period: float
    sustainability_score: float

@dataclass
class EnhancedCarbonMetrics:
    """Enhanced carbon metrics with cost analysis."""
    timestamp: datetime
    carbon_emissions: float
    energy_consumed: float
    water_usage: float
    carbon_intensity: float
    water_intensity: float
    renewable_percentage: float
    workload_type: str
    framework: str
    gpu_utilization: float
    cpu_utilization: float
    memory_usage: float
    region: str
    cloud_provider: str
    hardware_type: str
    runtime_seconds: float
    cost_metrics: CostMetrics
    roi_metrics: Optional[ROIMetrics] = None

class CostCalculator:
    """Calculate costs for environmental impact."""
    
    def __init__(self):
        # Default regional pricing (USD)
        self.regional_pricing = {
            "us-west-2": {
                "electricity": 0.12,  # $/kWh
                "water": 0.003,       # $/L
                "carbon": 0.05        # $/kg CO2
            },
            "us-east-1": {
                "electricity": 0.15,
                "water": 0.004,
                "carbon": 0.08
            },
            "eu-west-1": {
                "electricity": 0.18,
                "water": 0.005,
                "carbon": 0.12
            },
            "ap-southeast-1": {
                "electricity": 0.14,
                "water": 0.002,
                "carbon": 0.06
            }
        }
    
    def calculate_costs(self, metrics: EnhancedCarbonMetrics, custom_pricing: Dict = None) -> CostMetrics:
        """Calculate costs for environmental metrics."""
        region = metrics.region
        pricing = custom_pricing or self.regional_pricing.get(region, self.regional_pricing["us-west-2"])
        
        # Calculate individual costs
        carbon_cost = metrics.carbon_emissions * pricing["carbon"]
        energy_cost = metrics.energy_consumed * pricing["electricity"]
        water_cost = metrics.water_usage * pricing["water"]
        total_cost = carbon_cost + energy_cost + water_cost
        
        return CostMetrics(
            carbon_cost=carbon_cost,
            energy_cost=energy_cost,
            water_cost=water_cost,
            total_cost=total_cost,
            carbon_price=pricing["carbon"],
            energy_price=pricing["electricity"],
            water_price=pricing["water"]
        )

class ROIAnalyzer:
    """Analyze ROI for AI projects."""
    
    def __init__(self):
        self.value_estimates = {
            "training": {"base_value": 1000, "multiplier": 1.5},
            "inference": {"base_value": 100, "multiplier": 1.0},
            "data_processing": {"base_value": 500, "multiplier": 1.2},
            "evaluation": {"base_value": 300, "multiplier": 1.1},
            "fine_tuning": {"base_value": 800, "multiplier": 1.3}
        }
    
    def calculate_roi(self, metrics: EnhancedCarbonMetrics, custom_value: float = None) -> ROIMetrics:
        """Calculate ROI metrics."""
        # Estimate project value
        if custom_value:
            project_value = custom_value
        else:
            workload = metrics.workload_type
            base_value = self.value_estimates.get(workload, {"base_value": 500, "multiplier": 1.0})["base_value"]
            multiplier = self.value_estimates.get(workload, {"base_value": 500, "multiplier": 1.0})["multiplier"]
            project_value = base_value * multiplier * (metrics.runtime_seconds / 3600)  # Scale by runtime hours
        
        total_cost = metrics.cost_metrics.total_cost
        roi_ratio = project_value / total_cost if total_cost > 0 else float('inf')
        roi_percentage = ((project_value - total_cost) / total_cost * 100) if total_cost > 0 else float('inf')
        
        # Calculate payback period (in hours)
        payback_period = total_cost / (project_value / (metrics.runtime_seconds / 3600)) if project_value > 0 else float('inf')
        
        # Calculate sustainability score (0-100)
        sustainability_score = min(100, max(0, 100 - (metrics.carbon_emissions * 1000) - (metrics.energy_consumed * 10)))
        
        return ROIMetrics(
            project_value=project_value,
            total_cost=total_cost,
            roi_ratio=roi_ratio,
            roi_percentage=roi_percentage,
            payback_period=payback_period,
            sustainability_score=sustainability_score
        )

def create_sample_data_with_costs():
    """Create sample data with cost analysis."""
    sample_metrics = []
    cost_calculator = CostCalculator()
    roi_analyzer = ROIAnalyzer()
    
    # Sample workloads
    workloads = [
        ("training", "pytorch", "us-west-2", "aws", "apple_m2 + rtx_4090"),
        ("training", "tensorflow", "us-east-1", "aws", "intel_i9 + rtx_4090"),
        ("inference", "huggingface", "eu-west-1", "aws", "apple_m3 + rtx_4080"),
        ("data_processing", "scikit-learn", "ap-southeast-1", "aws", "amd_ryzen7 + none"),
        ("evaluation", "transformers", "us-west-2", "gcp", "intel_i7 + rtx_3080"),
        ("fine_tuning", "pytorch", "us-west-2", "aws", "apple_m2 + rtx_4090"),
        ("training", "tensorflow", "us-east-1", "aws", "intel_i9 + rtx_4090"),
        ("inference", "huggingface", "eu-west-1", "aws", "apple_m3 + rtx_4080"),
        ("data_processing", "scikit-learn", "us-west-2", "gcp", "amd_ryzen7 + none"),
        ("evaluation", "transformers", "ap-southeast-1", "aws", "intel_i7 + rtx_3080"),
    ]
    
    base_time = datetime.now() - timedelta(days=14)
    
    for i, (workload, framework, region, cloud, hardware) in enumerate(workloads):
        # Generate environmental metrics
        runtime = np.random.uniform(300, 7200)
        energy = np.random.uniform(0.5, 3.0)
        carbon_emissions = energy * np.random.uniform(200, 500) / 1000
        water_usage = energy * np.random.uniform(1.0, 2.0)
        
        # Create base metrics
        base_metrics = EnhancedCarbonMetrics(
            timestamp=base_time + timedelta(hours=i*12),
            carbon_emissions=carbon_emissions,
            energy_consumed=energy,
            water_usage=water_usage,
            carbon_intensity=np.random.uniform(200, 500),
            water_intensity=np.random.uniform(1.0, 2.0),
            renewable_percentage=np.random.uniform(20, 80),
            workload_type=workload,
            framework=framework,
            gpu_utilization=np.random.uniform(0.0, 0.9),
            cpu_utilization=np.random.uniform(0.3, 0.8),
            memory_usage=np.random.uniform(0.4, 0.7),
            region=region,
            cloud_provider=cloud,
            hardware_type=hardware,
            runtime_seconds=runtime,
            cost_metrics=None,  # Will be calculated
            roi_metrics=None
        )
        
        # Calculate costs
        cost_metrics = cost_calculator.calculate_costs(base_metrics)
        base_metrics.cost_metrics = cost_metrics
        
        # Calculate ROI
        roi_metrics = roi_analyzer.calculate_roi(base_metrics)
        base_metrics.roi_metrics = roi_metrics
        
        sample_metrics.append(base_metrics)
    
    return sample_metrics

def show_cost_analysis_tab(metrics_list: List[EnhancedCarbonMetrics]):
    """Display cost analysis tab."""
    st.markdown("### 💰 Cost Analysis")
    
    # Summary metrics
    total_carbon_cost = sum(m.cost_metrics.carbon_cost for m in metrics_list)
    total_energy_cost = sum(m.cost_metrics.energy_cost for m in metrics_list)
    total_water_cost = sum(m.cost_metrics.water_cost for m in metrics_list)
    total_cost = sum(m.cost_metrics.total_cost for m in metrics_list)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Carbon Cost", f"${total_carbon_cost:.2f}")
    with col2:
        st.metric("Energy Cost", f"${total_energy_cost:.2f}")
    with col3:
        st.metric("Water Cost", f"${total_water_cost:.2f}")
    with col4:
        st.metric("Total Cost", f"${total_cost:.2f}")
    
    # Cost breakdown chart
    cost_data = []
    for metrics in metrics_list:
        cost_data.append({
            'Timestamp': metrics.timestamp,
            'Carbon Cost': metrics.cost_metrics.carbon_cost,
            'Energy Cost': metrics.cost_metrics.energy_cost,
            'Water Cost': metrics.cost_metrics.water_cost,
            'Total Cost': metrics.cost_metrics.total_cost,
            'Workload': metrics.workload_type,
            'Region': metrics.region
        })
    
    df = pd.DataFrame(cost_data)
    
    # Cost over time
    fig_cost_time = px.line(
        df, 
        x='Timestamp', 
        y='Total Cost',
        title='Total Cost Over Time',
        markers=True
    )
    st.plotly_chart(fig_cost_time, use_container_width=True)
    
    # Cost breakdown by category
    col1, col2 = st.columns(2)
    
    with col1:
        cost_breakdown = df[['Carbon Cost', 'Energy Cost', 'Water Cost']].sum()
        fig_breakdown = px.pie(
            values=cost_breakdown.values,
            names=cost_breakdown.index,
            title='Cost Breakdown by Category'
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    with col2:
        regional_costs = df.groupby('Region')['Total Cost'].sum().reset_index()
        fig_regional = px.bar(
            regional_costs,
            x='Region',
            y='Total Cost',
            title='Total Cost by Region',
            color='Total Cost',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_regional, use_container_width=True)

def show_roi_analysis_tab(metrics_list: List[EnhancedCarbonMetrics]):
    """Display ROI analysis tab."""
    st.markdown("### 📈 ROI Analysis")
    
    # Summary ROI metrics
    total_value = sum(m.roi_metrics.project_value for m in metrics_list)
    total_cost = sum(m.roi_metrics.total_cost for m in metrics_list)
    avg_roi = np.mean([m.roi_metrics.roi_percentage for m in metrics_list])
    avg_sustainability = np.mean([m.roi_metrics.sustainability_score for m in metrics_list])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Value", f"${total_value:.2f}")
    with col2:
        st.metric("Total Cost", f"${total_cost:.2f}")
    with col3:
        st.metric("Avg ROI", f"{avg_roi:.1f}%")
    with col4:
        st.metric("Sustainability Score", f"{avg_sustainability:.1f}/100")
    
    # ROI data
    roi_data = []
    for metrics in metrics_list:
        roi_data.append({
            'Timestamp': metrics.timestamp,
            'Project Value': metrics.roi_metrics.project_value,
            'Total Cost': metrics.roi_metrics.total_cost,
            'ROI %': metrics.roi_metrics.roi_percentage,
            'ROI Ratio': metrics.roi_metrics.roi_ratio,
            'Payback Period (h)': metrics.roi_metrics.payback_period,
            'Sustainability Score': metrics.roi_metrics.sustainability_score,
            'Workload': metrics.workload_type,
            'Region': metrics.region
        })
    
    df = pd.DataFrame(roi_data)
    
    # ROI over time
    fig_roi_time = px.line(
        df, 
        x='Timestamp', 
        y='ROI %',
        title='ROI Percentage Over Time',
        markers=True
    )
    st.plotly_chart(fig_roi_time, use_container_width=True)
    
    # ROI vs Sustainability scatter
    col1, col2 = st.columns(2)
    
    with col1:
        fig_roi_sustainability = px.scatter(
            df,
            x='Sustainability Score',
            y='ROI %',
            color='Workload',
            size='Project Value',
            title='ROI vs Sustainability Score',
            hover_data=['Region', 'Workload']
        )
        st.plotly_chart(fig_roi_sustainability, use_container_width=True)
    
    with col2:
        workload_roi = df.groupby('Workload')['ROI %'].mean().reset_index()
        fig_workload_roi = px.bar(
            workload_roi,
            x='Workload',
            y='ROI %',
            title='Average ROI by Workload Type',
            color='ROI %',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_workload_roi, use_container_width=True)

def show_pricing_configuration():
    """Display pricing configuration panel."""
    st.markdown("### ⚙️ Pricing Configuration")
    
    # Regional pricing configuration
    st.markdown("#### Regional Pricing (USD)")
    
    regions = ["us-west-2", "us-east-1", "eu-west-1", "ap-southeast-1"]
    region_names = ["US West (Oregon)", "US East (Virginia)", "EU West (Ireland)", "Asia Pacific (Singapore)"]
    
    pricing_config = {}
    
    for i, (region, name) in enumerate(zip(regions, region_names)):
        st.markdown(f"**{name}**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            electricity = st.number_input(
                f"Electricity ($/kWh) - {name}",
                value=0.12 + i * 0.01,
                min_value=0.01,
                max_value=1.0,
                step=0.01,
                key=f"elec_{region}"
            )
        
        with col2:
            water = st.number_input(
                f"Water ($/L) - {name}",
                value=0.003 + i * 0.001,
                min_value=0.001,
                max_value=0.1,
                step=0.001,
                key=f"water_{region}"
            )
        
        with col3:
            carbon = st.number_input(
                f"Carbon ($/kg CO₂) - {name}",
                value=0.05 + i * 0.02,
                min_value=0.01,
                max_value=1.0,
                step=0.01,
                key=f"carbon_{region}"
            )
        
        pricing_config[region] = {
            "electricity": electricity,
            "water": water,
            "carbon": carbon
        }
    
    return pricing_config

def export_cost_roi_report(metrics_list: List[EnhancedCarbonMetrics], format: str = "csv"):
    """Export cost and ROI report."""
    export_data = []
    
    for metrics in metrics_list:
        export_data.append({
            'Timestamp': metrics.timestamp,
            'Workload Type': metrics.workload_type,
            'Framework': metrics.framework,
            'Region': metrics.region,
            'Hardware': metrics.hardware_type,
            'Runtime (s)': metrics.runtime_seconds,
            'Carbon Emissions (kg)': metrics.carbon_emissions,
            'Energy Consumed (kWh)': metrics.energy_consumed,
            'Water Usage (L)': metrics.water_usage,
            'Carbon Cost ($)': metrics.cost_metrics.carbon_cost,
            'Energy Cost ($)': metrics.cost_metrics.energy_cost,
            'Water Cost ($)': metrics.cost_metrics.water_cost,
            'Total Cost ($)': metrics.cost_metrics.total_cost,
            'Project Value ($)': metrics.roi_metrics.project_value,
            'ROI %': metrics.roi_metrics.roi_percentage,
            'ROI Ratio': metrics.roi_metrics.roi_ratio,
            'Payback Period (h)': metrics.roi_metrics.payback_period,
            'Sustainability Score': metrics.roi_metrics.sustainability_score
        })
    
    df = pd.DataFrame(export_data)
    
    if format == "csv":
        csv = df.to_csv(index=False)
        return csv
    elif format == "json":
        return df.to_json(orient='records', date_format='iso')
    else:
        return df

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
            AI-Powered Environmental Intelligence with Cost & ROI Analysis
        </p>
        <p style="margin: 10px 0 0 0; font-size: 1em; opacity: 0.8;">
            💰 Cost Analysis • 📈 ROI Tracking • 🌍 Environmental Impact • 📊 Interactive Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'sample_data' not in st.session_state:
        st.session_state.sample_data = create_sample_data_with_costs()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Cost Analysis",
        "📈 ROI Analysis", 
        "⚙️ Configuration",
        "📊 Dashboard",
        "📤 Export"
    ])
    
    with tab1:
        show_cost_analysis_tab(st.session_state.sample_data)
    
    with tab2:
        show_roi_analysis_tab(st.session_state.sample_data)
    
    with tab3:
        pricing_config = show_pricing_configuration()
        
        if st.button("🔄 Recalculate with New Pricing", type="primary"):
            # Recalculate costs with new pricing
            cost_calculator = CostCalculator()
            cost_calculator.regional_pricing = pricing_config
            
            for metrics in st.session_state.sample_data:
                metrics.cost_metrics = cost_calculator.calculate_costs(metrics, pricing_config.get(metrics.region))
            
            st.success("Costs recalculated with new pricing!")
            st.rerun()
    
    with tab4:
        st.markdown("### 📊 Comprehensive Dashboard")
        
        # Summary statistics
        total_cost = sum(m.cost_metrics.total_cost for m in st.session_state.sample_data)
        total_value = sum(m.roi_metrics.project_value for m in st.session_state.sample_data)
        avg_roi = np.mean([m.roi_metrics.roi_percentage for m in st.session_state.sample_data])
        avg_sustainability = np.mean([m.roi_metrics.sustainability_score for m in st.session_state.sample_data])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Cost", f"${total_cost:.2f}")
        with col2:
            st.metric("Total Value", f"${total_value:.2f}")
        with col3:
            st.metric("Average ROI", f"{avg_roi:.1f}%")
        with col4:
            st.metric("Sustainability Score", f"{avg_sustainability:.1f}/100")
        
        # Detailed data table
        st.markdown("#### 📋 Detailed Metrics Table")
        
        table_data = []
        for metrics in st.session_state.sample_data:
            table_data.append({
                'Timestamp': metrics.timestamp.strftime('%Y-%m-%d %H:%M'),
                'Workload': metrics.workload_type,
                'Region': metrics.region,
                'Cost ($)': f"${metrics.cost_metrics.total_cost:.2f}",
                'Value ($)': f"${metrics.roi_metrics.project_value:.2f}",
                'ROI %': f"{metrics.roi_metrics.roi_percentage:.1f}%",
                'Sustainability': f"{metrics.roi_metrics.sustainability_score:.1f}/100"
            })
        
        df_table = pd.DataFrame(table_data)
        st.dataframe(df_table, use_container_width=True)
    
    with tab5:
        st.markdown("### 📤 Export Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export CSV Report", type="primary"):
                csv_data = export_cost_roi_report(st.session_state.sample_data, "csv")
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"neurogreen_cost_roi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📋 Export JSON Report", type="primary"):
                json_data = export_cost_roi_report(st.session_state.sample_data, "json")
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"neurogreen_cost_roi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        # Show preview of export data
        st.markdown("#### 📋 Export Preview")
        export_df = export_cost_roi_report(st.session_state.sample_data, "dataframe")
        st.dataframe(export_df.head(10), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🧠 <strong>NeuroGreen</strong> - AI-Powered Environmental Intelligence with Cost & ROI Analysis</p>
        <p>Complete platform with cost tracking, ROI analysis, and sustainability metrics!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
