#!/usr/bin/env python3
"""
🧠 NeuroGreen - Enhanced Dashboard with Motivation & Savings
==========================================================

Enhanced NeuroGreen dashboard with:
- Clear cost formatting and savings calculations
- AI recommendations with estimated savings
- Motivational tips and user encouragement
- Comparative visualizations
- Actionable insights
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
class EnhancedMetrics:
    """Enhanced metrics with cost and savings calculations."""
    timestamp: datetime
    carbon_emissions: float
    energy_consumed: float
    water_usage: float
    carbon_cost: float
    energy_cost: float
    water_cost: float
    total_cost: float
    workload_type: str
    region: str
    hardware_type: str
    runtime_hours: float
    sustainability_score: float
    # Additional attributes for tracking
    carbon_intensity: float = 200.0
    water_intensity: float = 1.5
    renewable_percentage: float = 50.0
    framework: str = "pytorch"
    gpu_utilization: float = 0.0
    cpu_utilization: float = 75.0
    memory_usage: float = 8.0
    cloud_provider: str = "aws"

@dataclass
class SavingsRecommendation:
    """Savings recommendation with estimated impact."""
    title: str
    description: str
    carbon_savings_kg: float
    energy_savings_kwh: float
    water_savings_l: float
    cost_savings_usd: float
    savings_percentage: float
    priority: str
    action: str

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
    
    def calculate_costs(self, metrics: EnhancedMetrics, region: str = "us-west-2") -> CostMetrics:
        """Calculate costs for environmental metrics."""
        pricing = self.regional_pricing.get(region, self.regional_pricing["us-west-2"])
        
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
    
    def calculate_roi(self, metrics: EnhancedMetrics, project_value: float) -> ROIMetrics:
        """Calculate ROI metrics."""
        cost_metrics = self.calculate_costs(metrics)
        
        roi_ratio = project_value / cost_metrics.total_cost if cost_metrics.total_cost > 0 else 0
        roi_percentage = (roi_ratio - 1) * 100 if roi_ratio > 0 else 0
        payback_period = cost_metrics.total_cost / project_value if project_value > 0 else float('inf')
        
        # Calculate sustainability score (0-100)
        sustainability_score = min(100, max(0, 100 - (metrics.carbon_emissions * 10 + metrics.energy_consumed * 5)))
        
        return ROIMetrics(
            project_value=project_value,
            total_cost=cost_metrics.total_cost,
            roi_ratio=roi_ratio,
            roi_percentage=roi_percentage,
            payback_period=payback_period,
            sustainability_score=sustainability_score
        )

class SavingsCalculator:
    """Calculate potential savings from recommendations."""
    
    def __init__(self):
        # Regional pricing
        self.regional_pricing = {
            "us-west-2": {"electricity": 0.12, "water": 0.003, "carbon": 0.05},
            "us-east-1": {"electricity": 0.15, "water": 0.004, "carbon": 0.08},
            "eu-west-1": {"electricity": 0.18, "water": 0.005, "carbon": 0.12},
            "ap-southeast-1": {"electricity": 0.14, "water": 0.002, "carbon": 0.06}
        }
        
        # Regional carbon intensity
        self.carbon_intensity = {
            "us-west-2": 200,  # Low carbon
            "us-east-1": 300,  # Medium carbon
            "eu-west-1": 250,  # Medium-low carbon
            "ap-southeast-1": 500  # High carbon
        }
    
    def calculate_savings(self, current_metrics: EnhancedMetrics, recommendation_type: str) -> SavingsRecommendation:
        """Calculate potential savings from recommendations."""
        
        if recommendation_type == "regional_optimization":
            return self._calculate_regional_savings(current_metrics)
        elif recommendation_type == "hardware_optimization":
            return self._calculate_hardware_savings(current_metrics)
        elif recommendation_type == "timing_optimization":
            return self._calculate_timing_savings(current_metrics)
        elif recommendation_type == "workload_optimization":
            return self._calculate_workload_savings(current_metrics)
        else:
            return self._calculate_general_savings(current_metrics)
    
    def _calculate_regional_savings(self, current_metrics: EnhancedMetrics) -> SavingsRecommendation:
        """Calculate savings from regional optimization."""
        current_region = current_metrics.region
        best_region = "us-west-2"  # Oregon - lowest carbon
        
        if current_region == best_region:
            return SavingsRecommendation(
                title="🌍 Already in Optimal Region",
                description="You're already using the most efficient region!",
                carbon_savings_kg=0.0,
                energy_savings_kwh=0.0,
                water_savings_l=0.0,
                cost_savings_usd=0.0,
                savings_percentage=0.0,
                priority="low",
                action="Continue using current region"
            )
        
        # Calculate potential savings
        current_carbon_intensity = self.carbon_intensity[current_region]
        best_carbon_intensity = self.carbon_intensity[best_region]
        
        # Estimate potential carbon savings (30-50% reduction)
        carbon_savings_kg = current_metrics.carbon_emissions * 0.4
        
        # Estimate energy savings (10-20% reduction)
        energy_savings_kwh = current_metrics.energy_consumed * 0.15
        
        # Estimate water savings (15-25% reduction)
        water_savings_l = current_metrics.water_usage * 0.2
        
        # Calculate cost savings
        current_pricing = self.regional_pricing[current_region]
        best_pricing = self.regional_pricing[best_region]
        
        cost_savings_usd = (
            carbon_savings_kg * best_pricing["carbon"] +
            energy_savings_kwh * best_pricing["electricity"] +
            water_savings_l * best_pricing["water"]
        )
        
        savings_percentage = (cost_savings_usd / current_metrics.total_cost) * 100
        
        return SavingsRecommendation(
            title="🌍 Switch to Low-Carbon Region",
            description=f"Switch from {current_region} to {best_region} for significant environmental and cost savings",
            carbon_savings_kg=carbon_savings_kg,
            energy_savings_kwh=energy_savings_kwh,
            water_savings_l=water_savings_l,
            cost_savings_usd=cost_savings_usd,
            savings_percentage=savings_percentage,
            priority="high" if savings_percentage > 20 else "medium",
            action=f"Use {best_region} region for future workloads"
        )
    
    def _calculate_hardware_savings(self, current_metrics: EnhancedMetrics) -> SavingsRecommendation:
        """Calculate savings from hardware optimization."""
        current_hardware = current_metrics.hardware_type
        
        # Hardware efficiency mapping
        hardware_efficiency = {
            "apple_m2 + rtx_4090": 0.9,  # Most efficient
            "apple_m3 + rtx_4080": 0.95,  # Most efficient
            "intel_i9 + rtx_4090": 0.7,   # Medium efficiency
            "intel_i7 + rtx_3080": 0.8,   # Good efficiency
            "amd_ryzen7 + none": 0.6      # Lower efficiency
        }
        
        current_efficiency = hardware_efficiency.get(current_hardware, 0.7)
        best_efficiency = 0.95  # Apple M3 + RTX 4080
        
        if current_efficiency >= 0.9:
            return SavingsRecommendation(
                title="🔧 Hardware Already Optimized",
                description="Your current hardware is already quite efficient!",
                carbon_savings_kg=0.0,
                energy_savings_kwh=0.0,
                water_savings_l=0.0,
                cost_savings_usd=0.0,
                savings_percentage=0.0,
                priority="low",
                action="Continue using current hardware"
            )
        
        # Calculate potential savings (20-40% improvement)
        efficiency_improvement = (best_efficiency - current_efficiency) / current_efficiency
        savings_factor = efficiency_improvement * 0.8  # Conservative estimate
        
        carbon_savings_kg = current_metrics.carbon_emissions * savings_factor
        energy_savings_kwh = current_metrics.energy_consumed * savings_factor
        water_savings_l = current_metrics.water_usage * savings_factor
        
        # Calculate cost savings
        current_pricing = self.regional_pricing[current_metrics.region]
        cost_savings_usd = (
            carbon_savings_kg * current_pricing["carbon"] +
            energy_savings_kwh * current_pricing["electricity"] +
            water_savings_l * current_pricing["water"]
        )
        
        savings_percentage = (cost_savings_usd / current_metrics.total_cost) * 100
        
        return SavingsRecommendation(
            title="🔧 Upgrade to More Efficient Hardware",
            description="Consider upgrading to Apple M3 + RTX 4080 for better energy efficiency",
            carbon_savings_kg=carbon_savings_kg,
            energy_savings_kwh=energy_savings_kwh,
            water_savings_l=water_savings_l,
            cost_savings_usd=cost_savings_usd,
            savings_percentage=savings_percentage,
            priority="medium" if savings_percentage > 15 else "low",
            action="Consider hardware upgrade for future workloads"
        )
    
    def _calculate_timing_savings(self, current_metrics: EnhancedMetrics) -> SavingsRecommendation:
        """Calculate savings from timing optimization."""
        # Estimate savings from running during low-carbon hours
        carbon_savings_kg = current_metrics.carbon_emissions * 0.25  # 25% reduction
        energy_savings_kwh = current_metrics.energy_consumed * 0.15  # 15% reduction
        water_savings_l = current_metrics.water_usage * 0.15  # 15% reduction
        
        # Calculate cost savings
        current_pricing = self.regional_pricing[current_metrics.region]
        cost_savings_usd = (
            carbon_savings_kg * current_pricing["carbon"] +
            energy_savings_kwh * current_pricing["electricity"] +
            water_savings_l * current_pricing["water"]
        )
        
        savings_percentage = (cost_savings_usd / current_metrics.total_cost) * 100
        
        return SavingsRecommendation(
            title="⏰ Run During Low-Carbon Hours",
            description="Schedule workloads during peak renewable energy hours (10 AM - 2 PM)",
            carbon_savings_kg=carbon_savings_kg,
            energy_savings_kwh=energy_savings_kwh,
            water_savings_l=water_savings_l,
            cost_savings_usd=cost_savings_usd,
            savings_percentage=savings_percentage,
            priority="medium",
            action="Schedule future workloads during 10 AM - 2 PM"
        )
    
    def _calculate_workload_savings(self, current_metrics: EnhancedMetrics) -> SavingsRecommendation:
        """Calculate savings from workload optimization."""
        # Estimate savings from workload optimization
        carbon_savings_kg = current_metrics.carbon_emissions * 0.2  # 20% reduction
        energy_savings_kwh = current_metrics.energy_consumed * 0.15  # 15% reduction
        water_savings_l = current_metrics.water_usage * 0.15  # 15% reduction
        
        # Calculate cost savings
        current_pricing = self.regional_pricing[current_metrics.region]
        cost_savings_usd = (
            carbon_savings_kg * current_pricing["carbon"] +
            energy_savings_kwh * current_pricing["electricity"] +
            water_savings_l * current_pricing["water"]
        )
        
        savings_percentage = (cost_savings_usd / current_metrics.total_cost) * 100
        
        return SavingsRecommendation(
            title="🚀 Optimize Workload Configuration",
            description="Use model compression, optimize batch sizes, and implement efficient algorithms",
            carbon_savings_kg=carbon_savings_kg,
            energy_savings_kwh=energy_savings_kwh,
            water_savings_l=water_savings_l,
            cost_savings_usd=cost_savings_usd,
            savings_percentage=savings_percentage,
            priority="medium",
            action="Implement workload optimization techniques"
        )
    
    def _calculate_general_savings(self, current_metrics: EnhancedMetrics) -> SavingsRecommendation:
        """Calculate general sustainability savings."""
        # Estimate general savings
        carbon_savings_kg = current_metrics.carbon_emissions * 0.1  # 10% reduction
        energy_savings_kwh = current_metrics.energy_consumed * 0.1  # 10% reduction
        water_savings_l = current_metrics.water_usage * 0.1  # 10% reduction
        
        # Calculate cost savings
        current_pricing = self.regional_pricing[current_metrics.region]
        cost_savings_usd = (
            carbon_savings_kg * current_pricing["carbon"] +
            energy_savings_kwh * current_pricing["electricity"] +
            water_savings_l * current_pricing["water"]
        )
        
        savings_percentage = (cost_savings_usd / current_metrics.total_cost) * 100
        
        return SavingsRecommendation(
            title="🌱 General Sustainability Tips",
            description="Adopt sustainable AI development practices",
            carbon_savings_kg=carbon_savings_kg,
            energy_savings_kwh=energy_savings_kwh,
            water_savings_l=water_savings_l,
            cost_savings_usd=cost_savings_usd,
            savings_percentage=savings_percentage,
            priority="low",
            action="Follow general sustainability best practices"
        )

def create_sample_data_with_savings():
    """Create sample data with savings calculations."""
    sample_metrics = []
    savings_calculator = SavingsCalculator()
    
    # Sample workloads
    workloads = [
        ("training", "us-west-2", "apple_m2 + rtx_4090", 2.0),
        ("training", "us-east-1", "intel_i9 + rtx_4090", 3.0),
        ("inference", "eu-west-1", "apple_m3 + rtx_4080", 1.0),
        ("data_processing", "ap-southeast-1", "amd_ryzen7 + none", 1.5),
        ("evaluation", "us-west-2", "intel_i7 + rtx_3080", 0.5),
    ]
    
    base_time = datetime.now() - timedelta(days=7)
    
    for i, (workload, region, hardware, runtime_hours) in enumerate(workloads):
        # Generate environmental metrics
        carbon_emissions = np.random.uniform(0.1, 1.0)
        energy_consumed = np.random.uniform(0.5, 3.0)
        water_usage = np.random.uniform(1.0, 5.0)
        
        # Calculate costs
        pricing = savings_calculator.regional_pricing[region]
        carbon_cost = carbon_emissions * pricing["carbon"]
        energy_cost = energy_consumed * pricing["electricity"]
        water_cost = water_usage * pricing["water"]
        total_cost = carbon_cost + energy_cost + water_cost
        
        # Calculate sustainability score
        sustainability_score = max(0, 100 - (carbon_emissions * 100) - (energy_consumed * 10))
        
        # Generate additional metrics
        carbon_intensity = np.random.uniform(150, 400)
        water_intensity = np.random.uniform(1.0, 3.0)
        renewable_percentage = np.random.uniform(30, 80)
        cpu_utilization = np.random.uniform(60, 95)
        memory_usage = np.random.uniform(4, 16)
        gpu_utilization = np.random.uniform(0, 100) if "rtx" in hardware else 0
        
        metrics = EnhancedMetrics(
            timestamp=base_time + timedelta(hours=i*12),
            carbon_emissions=carbon_emissions,
            energy_consumed=energy_consumed,
            water_usage=water_usage,
            carbon_cost=carbon_cost,
            energy_cost=energy_cost,
            water_cost=water_cost,
            total_cost=total_cost,
            workload_type=workload,
            region=region,
            hardware_type=hardware,
            runtime_hours=runtime_hours,
            sustainability_score=sustainability_score,
            carbon_intensity=carbon_intensity,
            water_intensity=water_intensity,
            renewable_percentage=renewable_percentage,
            framework="pytorch",
            gpu_utilization=gpu_utilization,
            cpu_utilization=cpu_utilization,
            memory_usage=memory_usage,
            cloud_provider="aws"
        )
        
        sample_metrics.append(metrics)
    
    return sample_metrics

def format_currency(amount: float) -> str:
    """Format currency to 2 decimal places."""
    return f"${amount:.2f}"

def format_number(number: float, unit: str = "") -> str:
    """Format number to 2 decimal places with unit."""
    return f"{number:.2f} {unit}"

def show_cost_summary_card(metrics: EnhancedMetrics):
    """Display formatted cost summary card."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #28a745;
    ">
        <h3 style="margin: 0 0 10px 0; color: #28a745;">💰 This Run Cost You</h3>
        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
            <span><strong>Carbon Cost:</strong></span>
            <span style="color: #dc3545;">{format_currency(round(metrics.carbon_cost, 2))}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
            <span><strong>Energy Cost:</strong></span>
            <span style="color: #dc3545;">{format_currency(round(metrics.energy_cost, 2))}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
            <span><strong>Water Cost:</strong></span>
            <span style="color: #dc3545;">{format_currency(round(metrics.water_cost, 2))}</span>
        </div>
        <hr style="margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; margin: 5px 0; font-size: 1.2em; font-weight: bold;">
            <span><strong>Total Cost:</strong></span>
            <span style="color: #dc3545;">{format_currency(round(metrics.total_cost, 2))}</span>
        </div>
        <p style="margin: 10px 0 0 0; font-size: 0.9em; color: #666;">
            <strong>Formula:</strong> Carbon Cost + Energy Cost + Water Cost = Total Cost
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_savings_recommendation(recommendation: SavingsRecommendation, current_metrics: EnhancedMetrics):
    """Display savings recommendation with cost comparison using Streamlit components."""
    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    
    # Calculate new cost after recommendation
    new_total_cost = current_metrics.total_cost - recommendation.cost_savings_usd
    
    # Create a container for the recommendation
    with st.container():
        # Header with priority
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {priority_icon.get(recommendation.priority, '🟢')} {recommendation.title}")
        with col2:
            st.markdown(f"**{recommendation.priority.upper()}**")
        
        st.markdown(f"*{recommendation.description}*")
        
        # Highlight if savings > 20%
        if recommendation.savings_percentage > 20:
            st.success(f"🎉 **Great Choice!** This recommendation could save you over 20%!")
        
        # Cost Comparison
        st.markdown("#### 💰 Cost Comparison")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Cost",
                f"${current_metrics.total_cost:.2f}",
                "Your current spend"
            )
        
        with col2:
            st.metric(
                "With Recommendation", 
                f"${new_total_cost:.2f}",
                f"-${recommendation.cost_savings_usd:.2f}"
            )
        
        with col3:
            st.metric(
                "You Save",
                f"${recommendation.cost_savings_usd:.2f}",
                f"{recommendation.savings_percentage:.1f}%"
            )
        
        # Environmental Savings
        st.markdown("#### 💡 Environmental Savings")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Carbon Savings",
                f"{recommendation.carbon_savings_kg:.2f} kg",
                "CO₂ reduction"
            )
        
        with col2:
            st.metric(
                "Energy Savings",
                f"{recommendation.energy_savings_kwh:.2f} kWh",
                "Electricity saved"
            )
        
        with col3:
            st.metric(
                "Water Savings",
                f"{recommendation.water_savings_l:.2f} L",
                "Water saved"
            )
        
        with col4:
            st.metric(
                "Cost Savings",
                f"${recommendation.cost_savings_usd:.2f}",
                "Money saved"
            )
        
        # Action Required
        st.info(f"🎯 **Action Required:** {recommendation.action}")
        
        st.markdown("---")

def show_motivational_tips(metrics_list: List[EnhancedMetrics]):
    """Display motivational tips and user encouragement."""
    # Calculate user's total savings
    total_cost = sum(m.total_cost for m in metrics_list)
    total_carbon = sum(m.carbon_emissions for m in metrics_list)
    total_energy = sum(m.energy_consumed for m in metrics_list)
    total_water = sum(m.water_usage for m in metrics_list)
    
    # Calculate potential savings
    potential_savings = total_cost * 0.3  # Assume 30% potential savings
    potential_carbon_savings = total_carbon * 0.3
    potential_energy_savings = total_energy * 0.3
    potential_water_savings = total_water * 0.3
    
    st.markdown("### 🌟 Your Sustainability Journey")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border-left: 4px solid #28a745;
        ">
            <h4 style="margin: 0 0 15px 0; color: #155724;">📊 Your Impact This Week</h4>
            <div style="margin: 10px 0;">
                <strong>Total Cost:</strong> {format_currency(total_cost)}
            </div>
            <div style="margin: 10px 0;">
                <strong>Carbon Footprint:</strong> {format_number(total_carbon, 'kg CO₂')}
            </div>
            <div style="margin: 10px 0;">
                <strong>Energy Used:</strong> {format_number(total_energy, 'kWh')}
            </div>
            <div style="margin: 10px 0;">
                <strong>Water Used:</strong> {format_number(total_water, 'L')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border-left: 4px solid #ffc107;
        ">
            <h4 style="margin: 0 0 15px 0; color: #856404;">💡 Potential Savings</h4>
            <div style="margin: 10px 0;">
                <strong>Cost Savings:</strong> {format_currency(potential_savings)}
            </div>
            <div style="margin: 10px 0;">
                <strong>Carbon Reduction:</strong> {format_number(potential_carbon_savings, 'kg CO₂')}
            </div>
            <div style="margin: 10px 0;">
                <strong>Energy Reduction:</strong> {format_number(potential_energy_savings, 'kWh')}
            </div>
            <div style="margin: 10px 0;">
                <strong>Water Reduction:</strong> {format_number(potential_water_savings, 'L')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Motivational tips
    st.markdown("### 💚 Why Sustainable Choices Matter")
    
    tips = [
        {
            "title": "🌍 Environmental Impact",
            "description": "Every kg of CO₂ you save is equivalent to planting a tree. Your sustainable choices directly contribute to a healthier planet!",
            "impact": f"By optimizing your workloads, you could save {format_number(potential_carbon_savings, 'kg CO₂')} - that's like planting {int(potential_carbon_savings)} trees!"
        },
        {
            "title": "💰 Cost Savings",
            "description": "Sustainable choices aren't just good for the planet - they save you money too!",
            "impact": f"You could save {format_currency(potential_savings)} this week by following our recommendations."
        },
        {
            "title": "⚡ Energy Efficiency",
            "description": "Running during low-carbon hours helps the planet and saves you money!",
            "impact": f"Schedule your workloads during 10 AM - 2 PM to maximize renewable energy usage."
        },
        {
            "title": "🔧 Hardware Optimization",
            "description": "Efficient hardware means lower costs and better performance.",
            "impact": "Consider upgrading to more efficient hardware for long-term savings."
        }
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <h4 style="margin: 0 0 10px 0; color: #495057;">{tip['title']}</h4>
            <p style="margin: 0 0 10px 0; color: #666;">{tip['description']}</p>
            <p style="margin: 0; color: #28a745; font-weight: bold;">{tip['impact']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_comparative_visualization(metrics: EnhancedMetrics, recommendation: SavingsRecommendation):
    """Show comparative visualization of current vs recommended."""
    if recommendation.savings_percentage == 0:
        return
    
    # Current vs recommended data
    current_data = {
        "Carbon (kg CO₂)": metrics.carbon_emissions,
        "Energy (kWh)": metrics.energy_consumed,
        "Water (L)": metrics.water_usage,
        "Cost ($)": metrics.total_cost
    }
    
    recommended_data = {
        "Carbon (kg CO₂)": metrics.carbon_emissions - recommendation.carbon_savings_kg,
        "Energy (kWh)": metrics.energy_consumed - recommendation.energy_savings_kwh,
        "Water (L)": metrics.water_usage - recommendation.water_savings_l,
        "Cost ($)": metrics.total_cost - recommendation.cost_savings_usd
    }
    
    # Create comparison chart
    categories = list(current_data.keys())
    current_values = list(current_data.values())
    recommended_values = list(recommended_data.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current Run',
        x=categories,
        y=current_values,
        marker_color='#dc3545'
    ))
    
    fig.add_trace(go.Bar(
        name='With Recommendation',
        x=categories,
        y=recommended_values,
        marker_color='#28a745'
    ))
    
    fig.update_layout(
        title='Current Run vs. With Recommendation: You Save!',
        xaxis_title='Metrics',
        yaxis_title='Values',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show savings summary
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        border: 2px solid #28a745;
    ">
        <h3 style="margin: 0 0 15px 0; color: #155724;">🎉 You Save!</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div>
                <strong>Carbon:</strong> {format_number(recommendation.carbon_savings_kg, 'kg CO₂')}
            </div>
            <div>
                <strong>Energy:</strong> {format_number(recommendation.energy_savings_kwh, 'kWh')}
            </div>
            <div>
                <strong>Water:</strong> {format_number(recommendation.water_savings_l, 'L')}
            </div>
            <div>
                <strong>Cost:</strong> {format_currency(recommendation.cost_savings_usd)}
            </div>
        </div>
        <div style="margin-top: 15px; font-size: 1.2em; font-weight: bold; color: #155724;">
            Total Savings: {recommendation.savings_percentage:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

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
            Enhanced Dashboard with Motivation & Savings Analysis
        </p>
        <p style="margin: 10px 0 0 0; font-size: 1em; opacity: 0.8;">
            💰 Clear Cost Display • 💡 Actionable Savings • 🌟 Motivational Tips • 📊 Comparative Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'sample_data' not in st.session_state:
        st.session_state.sample_data = create_sample_data_with_savings()
    
    if 'savings_calculator' not in st.session_state:
        st.session_state.savings_calculator = SavingsCalculator()
    
    if 'cost_calculator' not in st.session_state:
        st.session_state.cost_calculator = CostCalculator()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Cost & Savings Analysis",
        "🌱 Carbon Tracking",
        "⚡ Energy Tracking", 
        "💧 Water Tracking",
        "🤖 AI Recommendations",
        "📊 Visualizations"
    ])
    
    with tab1:
        st.markdown("### 💰 Cost & Savings Analysis")
        st.markdown("Understand the financial impact of your AI workloads and discover how much you could save with optimization.")
        
        # Pricing Configuration
        st.markdown("#### 🔧 Formula & Prices Used")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            carbon_price = st.number_input(
                "Carbon Price ($/kg CO₂):",
                min_value=0.001,
                value=0.05,
                step=0.001,
                format="%.3f",
                help="Cost per kilogram of CO₂ emissions"
            )
        
        with col2:
            energy_price = st.number_input(
                "Energy Price ($/kWh):",
                min_value=0.001,
                value=0.12,
                step=0.001,
                format="%.3f",
                help="Cost per kilowatt-hour of electricity"
            )
        
        with col3:
            water_price = st.number_input(
                "Water Price ($/L):",
                min_value=0.0001,
                value=0.003,
                step=0.0001,
                format="%.4f",
                help="Cost per liter of water"
            )
        
        st.markdown("---")
        
        # Show cost analysis for each run
        for i, metrics in enumerate(st.session_state.sample_data):
            st.markdown(f"#### Run {i+1}: {metrics.workload_type.title()}")
            
            # Calculate costs with user-defined pricing
            carbon_cost = round(metrics.carbon_emissions * carbon_price, 2)
            energy_cost = round(metrics.energy_consumed * energy_price, 2)
            water_cost = round(metrics.water_usage * water_price, 2)
            total_cost = round(carbon_cost + energy_cost + water_cost, 2)
            
            # Your Total Footprint Cost
            st.markdown("##### 💸 Your Total Footprint Cost")
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
                border-radius: 15px;
                padding: 25px;
                margin: 15px 0;
                text-align: center;
                border: 2px solid #c62828;
            ">
                <h3 style="margin: 0 0 15px 0; color: #c62828;">This run cost you ${total_cost:.2f} in total.</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px;">
                    <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 8px;">
                        <strong>Carbon:</strong> ${carbon_cost:.2f}<br>
                        <small>{metrics.carbon_emissions:.2f} kg × ${carbon_price:.3f}</small>
                    </div>
                    <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 8px;">
                        <strong>Energy:</strong> ${energy_cost:.2f}<br>
                        <small>{metrics.energy_consumed:.2f} kWh × ${energy_price:.3f}</small>
                    </div>
                    <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 8px;">
                        <strong>Water:</strong> ${water_cost:.2f}<br>
                        <small>{metrics.water_usage:.2f} L × ${water_price:.4f}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Possible Savings from AI Recommendations
            st.markdown("##### 💡 Possible Savings")
            
            # Generate savings recommendations
            recommendation_types = ["regional_optimization", "hardware_optimization", "timing_optimization"]
            total_savings = 0
            total_carbon_savings = 0
            total_water_savings = 0
            best_recommendation = None
            max_savings = 0
            
            for rec_type in recommendation_types:
                recommendation = st.session_state.savings_calculator.calculate_savings(metrics, rec_type)
                if recommendation.savings_percentage > max_savings:
                    max_savings = recommendation.savings_percentage
                    best_recommendation = recommendation
                    total_savings = recommendation.cost_savings_usd
                    total_carbon_savings = recommendation.carbon_savings_kg
                    total_water_savings = recommendation.water_savings_l
            
            if best_recommendation and total_savings > 0:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
                    border-radius: 15px;
                    padding: 25px;
                    margin: 15px 0;
                    text-align: center;
                    border: 2px solid #2e7d32;
                ">
                    <h3 style="margin: 0 0 15px 0; color: #2e7d32;">If you'd optimized, you would save ${total_savings:.2f}, {max_savings:.1f}% emissions, and {total_water_savings:.2f} liters</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px;">
                        <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 8px;">
                            <strong>Cost Savings:</strong> ${total_savings:.2f}
                        </div>
                        <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 8px;">
                            <strong>Carbon Savings:</strong> {total_carbon_savings:.2f} kg
                        </div>
                        <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 8px;">
                            <strong>Water Savings:</strong> {total_water_savings:.2f} L
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show the best recommendation
                st.info(f"💡 **Best Optimization:** {best_recommendation.title} - {best_recommendation.description}")
            else:
                st.warning("No significant savings opportunities found for this run.")
            
            # Why This Matters
            st.markdown("##### 🌟 Why This Matters")
            
            # Calculate potential annual savings
            annual_savings = total_savings * 365 if total_savings > 0 else 0
            annual_carbon_savings = total_carbon_savings * 365 if total_carbon_savings > 0 else 0
            
            if annual_savings > 0:
                st.success(f"""
                **🎯 Quick Impact:** If you run this workload daily, you could save **${annual_savings:.2f} per year** and reduce your carbon footprint by **{annual_carbon_savings:.2f} kg CO₂ annually**.
                
                **💡 Pro Tip:** {best_recommendation.action if best_recommendation else "Consider running during off-peak hours to reduce energy costs."}
                """)
            else:
                st.info("💡 **Pro Tip:** Your current setup is already quite efficient! Consider monitoring your usage patterns to identify further optimization opportunities.")
            
            st.markdown("---")
    
    with tab2:
        st.markdown("### 🌱 Carbon Tracking")
        st.markdown("Monitor your carbon emissions and environmental impact across all AI workloads.")
        
        # Show carbon data for each run
        for i, metrics in enumerate(st.session_state.sample_data):
            st.markdown(f"#### Run {i+1}: {metrics.workload_type.title()}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Carbon Emissions",
                    f"{round(metrics.carbon_emissions, 2)} kg CO₂",
                    f"Intensity: {metrics.carbon_intensity:.0f} g/kWh"
                )
            
            with col2:
                st.metric(
                    "Renewable Energy",
                    f"{round(metrics.renewable_percentage, 1)}%",
                    "Clean Energy Usage"
                )
            
            with col3:
                st.metric(
                    "Runtime",
                    f"{round(metrics.runtime_hours, 2)} hours",
                    f"Region: {metrics.region}"
                )
            
            # Show cost summary card
            show_cost_summary_card(metrics)
            
            st.markdown("---")
    
    with tab3:
        st.markdown("### ⚡ Energy Tracking")
        st.markdown("Track energy consumption and efficiency across your AI workloads.")
        
        # Show energy data for each run
        for i, metrics in enumerate(st.session_state.sample_data):
            st.markdown(f"#### Run {i+1}: {metrics.workload_type.title()}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Energy Consumed",
                    f"{round(metrics.energy_consumed, 2)} kWh",
                    f"Hardware: {metrics.hardware_type}"
                )
            
            with col2:
                st.metric(
                    "CPU Utilization",
                    f"{round(metrics.cpu_utilization, 1)}%",
                    "Processing Efficiency"
                )
            
            with col3:
                st.metric(
                    "Memory Usage",
                    f"{round(metrics.memory_usage, 1)} GB",
                    "RAM Consumption"
                )
            
            # Energy efficiency insights
            efficiency_score = min(100, max(0, 100 - (metrics.energy_consumed * 10)))
            st.info(f"🔋 **Energy Efficiency Score:** {efficiency_score:.1f}/100 - {'Excellent' if efficiency_score > 80 else 'Good' if efficiency_score > 60 else 'Needs Improvement'}")
            
            st.markdown("---")
    
    with tab4:
        st.markdown("### 💧 Water Tracking")
        st.markdown("Monitor water usage and efficiency in your AI workloads.")
        
        # Show water data for each run
        for i, metrics in enumerate(st.session_state.sample_data):
            st.markdown(f"#### Run {i+1}: {metrics.workload_type.title()}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Water Usage",
                    f"{round(metrics.water_usage, 2)} L",
                    f"Intensity: {metrics.water_intensity:.2f} L/kWh"
                )
            
            with col2:
                st.metric(
                    "Energy to Water Ratio",
                    f"{round(metrics.water_usage / metrics.energy_consumed, 2)} L/kWh",
                    "Water Efficiency"
                )
            
            with col3:
                st.metric(
                    "Cloud Provider",
                    metrics.cloud_provider,
                    f"Region: {metrics.region}"
                )
            
            # Water efficiency insights
            water_efficiency = min(100, max(0, 100 - (metrics.water_usage * 5)))
            st.info(f"💧 **Water Efficiency Score:** {water_efficiency:.1f}/100 - {'Excellent' if water_efficiency > 80 else 'Good' if water_efficiency > 60 else 'Needs Improvement'}")
            
            st.markdown("---")
    
    with tab5:
        st.markdown("### 🤖 AI Recommendations")
        st.markdown("Get intelligent recommendations to optimize your AI workloads for cost and environmental impact.")
        
        # Generate recommendations for each run
        for i, metrics in enumerate(st.session_state.sample_data):
            st.markdown(f"#### Recommendations for Run {i+1}: {metrics.workload_type.title()}")
            
            # Generate different types of recommendations
            recommendation_types = ["regional_optimization", "hardware_optimization", "timing_optimization", "workload_optimization"]
            
            for rec_type in recommendation_types:
                recommendation = st.session_state.savings_calculator.calculate_savings(metrics, rec_type)
                if recommendation.savings_percentage > 0:  # Only show if there are actual savings
                    show_savings_recommendation(recommendation, metrics)
    
    with tab6:
        st.markdown("### 📊 Visualizations")
        st.markdown("Interactive charts and graphs showing your environmental impact trends.")
        
        # Create DataFrame for visualizations
        df_data = []
        for metrics in st.session_state.sample_data:
            df_data.append({
                'timestamp': metrics.timestamp,
                'workload_type': metrics.workload_type,
                'region': metrics.region,
                'carbon_emissions': metrics.carbon_emissions,
                'energy_consumed': metrics.energy_consumed,
                'water_usage': metrics.water_usage,
                'total_cost': metrics.total_cost,
                'carbon_intensity': metrics.carbon_intensity,
                'renewable_percentage': metrics.renewable_percentage,
                'runtime_hours': metrics.runtime_hours
            })
        
        df = pd.DataFrame(df_data)
        
        # Time series charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Carbon Emissions Over Time")
            fig_carbon = px.line(df, x='timestamp', y='carbon_emissions', 
                               color='workload_type', title='Carbon Emissions by Workload Type',
                               labels={'carbon_emissions': 'CO₂ (kg)', 'timestamp': 'Time'})
            fig_carbon.update_layout(height=400)
            st.plotly_chart(fig_carbon, use_container_width=True)
        
        with col2:
            st.markdown("#### ⚡ Energy Consumption Over Time")
            fig_energy = px.line(df, x='timestamp', y='energy_consumed',
                                color='workload_type', title='Energy Consumption by Workload Type',
                                labels={'energy_consumed': 'Energy (kWh)', 'timestamp': 'Time'})
            fig_energy.update_layout(height=400)
            st.plotly_chart(fig_energy, use_container_width=True)
        
        # Cost analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Total Cost by Region")
            fig_cost = px.bar(df, x='region', y='total_cost', color='workload_type',
                            title='Cost Breakdown by Region and Workload',
                            labels={'total_cost': 'Total Cost ($)', 'region': 'Region'})
            fig_cost.update_layout(height=400)
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with col2:
            st.markdown("#### 🌱 Carbon Intensity by Region")
            fig_intensity = px.scatter(df, x='carbon_intensity', y='renewable_percentage',
                                     color='region', size='total_cost',
                                     title='Carbon Intensity vs Renewable Energy',
                                     labels={'carbon_intensity': 'Carbon Intensity (g/kWh)',
                                            'renewable_percentage': 'Renewable Energy (%)'})
            fig_intensity.update_layout(height=400)
            st.plotly_chart(fig_intensity, use_container_width=True)
        
        # Water usage analysis
        st.markdown("#### 💧 Water Usage Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_water = px.bar(df, x='workload_type', y='water_usage', color='region',
                             title='Water Usage by Workload Type and Region',
                             labels={'water_usage': 'Water Usage (L)', 'workload_type': 'Workload Type'})
            fig_water.update_layout(height=400)
            st.plotly_chart(fig_water, use_container_width=True)
        
        with col2:
            # Efficiency scatter plot
            fig_efficiency = px.scatter(df, x='energy_consumed', y='carbon_emissions',
                                     color='workload_type', size='water_usage',
                                     title='Energy vs Carbon Efficiency',
                                     labels={'energy_consumed': 'Energy (kWh)',
                                            'carbon_emissions': 'Carbon (kg CO₂)'})
            fig_efficiency.update_layout(height=400)
            st.plotly_chart(fig_efficiency, use_container_width=True)
        
        # Summary statistics
        st.markdown("#### 📊 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Carbon",
                f"{df['carbon_emissions'].sum():.2f} kg",
                f"Avg: {df['carbon_emissions'].mean():.2f} kg/run"
            )
        
        with col2:
            st.metric(
                "Total Energy",
                f"{df['energy_consumed'].sum():.2f} kWh",
                f"Avg: {df['energy_consumed'].mean():.2f} kWh/run"
            )
        
        with col3:
            st.metric(
                "Total Water",
                f"{df['water_usage'].sum():.2f} L",
                f"Avg: {df['water_usage'].mean():.2f} L/run"
            )
        
        with col4:
            st.metric(
                "Total Cost",
                f"${df['total_cost'].sum():.2f}",
                f"Avg: ${df['total_cost'].mean():.2f}/run"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🧠 <strong>NeuroGreen</strong> - Enhanced Dashboard with Motivation & Savings Analysis</p>
        <p>Clear cost display, actionable savings, and motivational tips for sustainable AI development!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
