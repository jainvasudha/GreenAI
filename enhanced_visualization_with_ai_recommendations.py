"""
🌱 Enhanced Environmental Visualization App with AI Recommendations
================================================================

Interactive Streamlit app with AI-powered recommendations, LLM integration,
and intelligent analysis of user behavior for environmental optimization.
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
import openai
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import requests

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
    
    .recommendation-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #28a745;
    }
    
    .ai-chat-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #007bff;
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
    
    .recommendation-item {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .ai-message {
        background: #e3f2fd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
    }
    
    .user-message {
        background: #f3e5f5;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #9c27b0;
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

class AIRecommendationEngine:
    """AI-powered recommendation engine for environmental optimization."""
    
    def __init__(self):
        self.openai_api_key = ""  # Using mock AI - no API key needed
        self.recommendation_history = []
    
    def analyze_user_behavior(self, metrics_history: List[EnhancedCarbonMetrics]) -> Dict[str, Any]:
        """Analyze user behavior patterns and generate insights."""
        if not metrics_history:
            return {"patterns": [], "insights": [], "recommendations": []}
        
        # Convert to DataFrame for analysis
        df_data = []
        for metrics in metrics_history:
            df_data.append({
                'timestamp': metrics.timestamp,
                'workload_type': metrics.workload_type,
                'framework': metrics.framework,
                'region': metrics.region,
                'hardware_type': metrics.hardware_type,
                'carbon_emissions': metrics.carbon_emissions,
                'energy_consumed': metrics.energy_consumed,
                'water_usage': metrics.water_usage,
                'carbon_intensity': metrics.carbon_intensity,
                'water_intensity': metrics.water_intensity,
                'renewable_percentage': metrics.renewable_percentage,
                'runtime_seconds': metrics.runtime_seconds,
                'cpu_utilization': metrics.cpu_utilization,
                'gpu_utilization': metrics.gpu_utilization,
                'memory_usage': metrics.memory_usage
            })
        
        df = pd.DataFrame(df_data)
        
        # Analyze patterns
        patterns = self._analyze_patterns(df)
        insights = self._generate_insights(df)
        recommendations = self._generate_recommendations(df, patterns, insights)
        
        return {
            "patterns": patterns,
            "insights": insights,
            "recommendations": recommendations,
            "summary_stats": self._calculate_summary_stats(df)
        }
    
    def _analyze_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze user behavior patterns."""
        patterns = []
        
        # Workload pattern analysis
        workload_analysis = df.groupby('workload_type').agg({
            'carbon_emissions': ['mean', 'sum', 'count'],
            'energy_consumed': ['mean', 'sum'],
            'water_usage': ['mean', 'sum']
        }).round(6)
        
        patterns.append({
            "type": "workload_analysis",
            "title": "Workload Impact Analysis",
            "data": workload_analysis.to_dict(),
            "description": "Analysis of environmental impact by workload type"
        })
        
        # Regional efficiency analysis
        regional_analysis = df.groupby('region').agg({
            'carbon_intensity': 'mean',
            'water_intensity': 'mean',
            'renewable_percentage': 'mean',
            'carbon_emissions': 'sum'
        }).round(3)
        
        patterns.append({
            "type": "regional_analysis",
            "title": "Regional Efficiency Analysis",
            "data": regional_analysis.to_dict(),
            "description": "Environmental efficiency by geographic region"
        })
        
        # Hardware efficiency analysis
        hardware_analysis = df.groupby('hardware_type').agg({
            'energy_consumed': 'mean',
            'carbon_emissions': 'mean',
            'runtime_seconds': 'mean'
        }).round(6)
        
        patterns.append({
            "type": "hardware_analysis",
            "title": "Hardware Efficiency Analysis",
            "data": hardware_analysis.to_dict(),
            "description": "Energy efficiency by hardware configuration"
        })
        
        # Time-based patterns
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        time_analysis = df.groupby('hour').agg({
            'carbon_emissions': 'mean',
            'energy_consumed': 'mean',
            'renewable_percentage': 'mean'
        }).round(6)
        
        patterns.append({
            "type": "time_analysis",
            "title": "Time-based Usage Patterns",
            "data": time_analysis.to_dict(),
            "description": "Environmental impact patterns by time of day"
        })
        
        return patterns
    
    def _generate_insights(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate insights from user behavior."""
        insights = []
        
        # Total environmental impact
        total_co2 = df['carbon_emissions'].sum()
        total_energy = df['energy_consumed'].sum()
        total_water = df['water_usage'].sum()
        
        insights.append({
            "type": "total_impact",
            "title": "Total Environmental Impact",
            "value": f"{total_co2:.6f} kg CO₂, {total_energy:.6f} kWh, {total_water:.2f} L",
            "description": "Cumulative environmental impact across all workloads"
        })
        
        # Efficiency metrics
        avg_carbon_intensity = df['carbon_intensity'].mean()
        avg_water_intensity = df['water_intensity'].mean()
        avg_renewable = df['renewable_percentage'].mean()
        
        insights.append({
            "type": "efficiency_metrics",
            "title": "Average Efficiency Metrics",
            "value": f"Carbon: {avg_carbon_intensity:.1f} g/kWh, Water: {avg_water_intensity:.1f} L/kWh, Renewable: {avg_renewable:.1f}%",
            "description": "Average environmental efficiency across all runs"
        })
        
        # Most efficient region
        most_efficient_region = df.groupby('region').agg({
            'carbon_intensity': 'mean',
            'renewable_percentage': 'mean'
        }).sort_values('carbon_intensity').index[0]
        
        insights.append({
            "type": "most_efficient_region",
            "title": "Most Efficient Region",
            "value": most_efficient_region,
            "description": "Region with lowest carbon intensity and highest renewable percentage"
        })
        
        # Workload optimization opportunities
        workload_impact = df.groupby('workload_type')['carbon_emissions'].sum().sort_values(ascending=False)
        highest_impact_workload = workload_impact.index[0]
        
        insights.append({
            "type": "optimization_opportunity",
            "title": "Highest Impact Workload",
            "value": highest_impact_workload,
            "description": "Workload type with highest environmental impact - optimization opportunity"
        })
        
        return insights
    
    def _generate_recommendations(self, df: pd.DataFrame, patterns: List[Dict], insights: List[Dict]) -> List[Dict[str, Any]]:
        """Generate AI-powered recommendations."""
        recommendations = []
        
        # Regional optimization recommendation
        regional_data = df.groupby('region').agg({
            'carbon_intensity': 'mean',
            'renewable_percentage': 'mean',
            'carbon_emissions': 'sum'
        }).sort_values('carbon_intensity')
        
        if len(regional_data) > 1:
            best_region = regional_data.index[0]
            current_region = df['region'].mode()[0]
            
            if best_region != current_region:
                co2_reduction = (regional_data.loc[current_region, 'carbon_intensity'] - 
                               regional_data.loc[best_region, 'carbon_intensity']) / regional_data.loc[current_region, 'carbon_intensity'] * 100
                
                recommendations.append({
                    "type": "regional_optimization",
                    "priority": "high",
                    "title": "🌍 Regional Optimization",
                    "description": f"Switch from {current_region} to {best_region} for {co2_reduction:.1f}% CO₂ reduction",
                    "impact": f"Potential {co2_reduction:.1f}% reduction in carbon emissions",
                    "action": f"Use {best_region} region for future workloads",
                    "estimated_savings": f"{co2_reduction:.1f}% CO₂ reduction"
                })
        
        # Hardware optimization recommendation
        hardware_data = df.groupby('hardware_type').agg({
            'energy_consumed': 'mean',
            'carbon_emissions': 'mean',
            'runtime_seconds': 'mean'
        }).sort_values('energy_consumed')
        
        if len(hardware_data) > 1:
            most_efficient_hardware = hardware_data.index[0]
            current_hardware = df['hardware_type'].mode()[0]
            
            if most_efficient_hardware != current_hardware:
                energy_reduction = (hardware_data.loc[current_hardware, 'energy_consumed'] - 
                                 hardware_data.loc[most_efficient_hardware, 'energy_consumed']) / hardware_data.loc[current_hardware, 'energy_consumed'] * 100
                
                recommendations.append({
                    "type": "hardware_optimization",
                    "priority": "medium",
                    "title": "🔧 Hardware Optimization",
                    "description": f"Consider using {most_efficient_hardware} for better energy efficiency",
                    "impact": f"Potential {energy_reduction:.1f}% reduction in energy consumption",
                    "action": f"Use {most_efficient_hardware} for future workloads",
                    "estimated_savings": f"{energy_reduction:.1f}% energy reduction"
                })
        
        # Workload scheduling recommendation
        time_analysis = df.copy()
        time_analysis['hour'] = pd.to_datetime(time_analysis['timestamp']).dt.hour
        hourly_renewable = time_analysis.groupby('hour')['renewable_percentage'].mean()
        best_time = hourly_renewable.idxmax()
        
        recommendations.append({
            "type": "scheduling_optimization",
            "priority": "medium",
            "title": "⏰ Optimal Scheduling",
            "description": f"Schedule workloads at {best_time}:00 for maximum renewable energy",
            "impact": f"Average {hourly_renewable[best_time]:.1f}% renewable energy at {best_time}:00",
            "action": f"Schedule intensive workloads at {best_time}:00",
            "estimated_savings": f"{hourly_renewable[best_time]:.1f}% renewable energy"
        })
        
        # Workload optimization recommendation
        workload_impact = df.groupby('workload_type').agg({
            'carbon_emissions': 'sum',
            'energy_consumed': 'sum',
            'runtime_seconds': 'sum'
        }).sort_values('carbon_emissions', ascending=False)
        
        highest_impact_workload = workload_impact.index[0]
        total_impact = workload_impact.loc[highest_impact_workload, 'carbon_emissions']
        total_runtime = workload_impact.loc[highest_impact_workload, 'runtime_seconds']
        
        if total_impact > 0.001:  # Only recommend if significant impact
            recommendations.append({
                "type": "workload_optimization",
                "priority": "high",
                "title": "🚀 Workload Optimization",
                "description": f"Optimize {highest_impact_workload} workload for better efficiency",
                "impact": f"{total_impact:.6f} kg CO₂ from {total_runtime:.0f}s runtime",
                "action": f"Consider model compression, batch processing, or pre-trained models for {highest_impact_workload}",
                "estimated_savings": "10-50% reduction possible with optimization"
            })
        
        # General sustainability recommendations
        recommendations.extend([
            {
                "type": "general_sustainability",
                "priority": "low",
                "title": "🌱 General Sustainability Tips",
                "description": "Adopt sustainable AI development practices",
                "impact": "Long-term environmental benefits",
                "action": "Use pre-trained models, implement model compression, optimize batch sizes",
                "estimated_savings": "20-80% reduction with best practices"
            },
            {
                "type": "monitoring_improvement",
                "priority": "low",
                "title": "📊 Enhanced Monitoring",
                "description": "Improve environmental monitoring and reporting",
                "impact": "Better environmental awareness and optimization",
                "action": "Set up automated monitoring, create environmental dashboards, implement alerts",
                "estimated_savings": "Continuous optimization opportunities"
            }
        ])
        
        return recommendations
    
    def _calculate_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate summary statistics for user behavior."""
        return {
            "total_runs": len(df),
            "total_co2": df['carbon_emissions'].sum(),
            "total_energy": df['energy_consumed'].sum(),
            "total_water": df['water_usage'].sum(),
            "avg_carbon_intensity": df['carbon_intensity'].mean(),
            "avg_water_intensity": df['water_intensity'].mean(),
            "avg_renewable": df['renewable_percentage'].mean(),
            "most_used_region": df['region'].mode()[0],
            "most_used_hardware": df['hardware_type'].mode()[0],
            "most_used_workload": df['workload_type'].mode()[0]
        }
    
    def generate_llm_recommendations(self, user_question: str, analysis_data: Dict[str, Any]) -> str:
        """Generate LLM-powered recommendations based on user question."""
        if not self.openai_api_key:
            return "Using mock AI responses for demonstration. No API key required!"
        
        try:
            # Prepare context for LLM
            context = f"""
            User's Environmental Data:
            - Total CO₂: {analysis_data['summary_stats']['total_co2']:.6f} kg
            - Total Energy: {analysis_data['summary_stats']['total_energy']:.6f} kWh
            - Total Water: {analysis_data['summary_stats']['total_water']:.2f} L
            - Most Used Region: {analysis_data['summary_stats']['most_used_region']}
            - Most Used Hardware: {analysis_data['summary_stats']['most_used_hardware']}
            - Most Used Workload: {analysis_data['summary_stats']['most_used_workload']}
            
            Current Recommendations: {len(analysis_data['recommendations'])} active recommendations
            
            User Question: {user_question}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI environmental sustainability expert. Provide specific, actionable recommendations for reducing environmental impact in AI development. Focus on carbon emissions, energy consumption, and water usage optimization."},
                    {"role": "user", "content": context}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating LLM recommendations: {str(e)}"

def create_sample_data():
    """Create sample environmental data for demonstration."""
    sample_metrics = []
    
    # Create sample data for different workloads
    workloads = [
        ("training", "pytorch", "us-west-2", "aws", "apple_m2 + rtx_4090"),
        ("inference", "tensorflow", "us-east-1", "aws", "intel_i7 + rtx_3080"),
        ("data_processing", "scikit-learn", "eu-west-1", "aws", "amd_ryzen7 + none"),
        ("evaluation", "huggingface", "ap-southeast-1", "aws", "apple_m3 + rtx_4080"),
        ("fine_tuning", "transformers", "us-west-2", "gcp", "intel_i9 + a100")
    ]
    
    base_time = datetime.now() - timedelta(days=7)
    
    for i, (workload, framework, region, cloud, hardware) in enumerate(workloads):
        # Simulate different environmental impacts
        runtime = np.random.uniform(300, 3600)  # 5 minutes to 1 hour
        energy = np.random.uniform(0.1, 2.0)    # 0.1 to 2.0 kWh
        water_intensity = np.random.uniform(1.0, 2.0)  # 1.0 to 2.0 L/kWh
        water_usage = energy * water_intensity
        carbon_intensity = np.random.uniform(200, 500)  # 200 to 500 g CO2/kWh
        carbon_emissions = energy * carbon_intensity / 1000
        renewable_percentage = np.random.uniform(20, 80)  # 20% to 80%
        
        metrics = EnhancedCarbonMetrics(
            timestamp=base_time + timedelta(hours=i*6),
            carbon_emissions=carbon_emissions,
            energy_consumed=energy,
            water_usage=water_usage,
            carbon_intensity=carbon_intensity,
            water_intensity=water_intensity,
            renewable_percentage=renewable_percentage,
            workload_type=workload,
            framework=framework,
            gpu_utilization=np.random.uniform(0.0, 0.9),
            cpu_utilization=np.random.uniform(0.3, 0.8),
            memory_usage=np.random.uniform(0.4, 0.7),
            region=region,
            cloud_provider=cloud,
            hardware_type=hardware,
            runtime_seconds=runtime
        )
        
        sample_metrics.append(metrics)
    
    return sample_metrics

def initialize_session_state():
    """Initialize session state variables."""
    if 'enhanced_tracker' not in st.session_state:
        st.session_state.enhanced_tracker = EnhancedCarbonTracker()
    
    if 'tracking_active' not in st.session_state:
        st.session_state.tracking_active = False
    
    if 'metrics_history' not in st.session_state:
        # Pre-load sample data so tabs appear immediately
        st.session_state.metrics_history = create_sample_data()
    
    if 'ai_engine' not in st.session_state:
        st.session_state.ai_engine = AIRecommendationEngine()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def show_ai_recommendations_tab():
    """Show AI-powered recommendations tab with cost analysis."""
    st.markdown("## 🤖 AI-Powered Environmental Recommendations")
    
    if not st.session_state.metrics_history:
        st.info("🌱 Start tracking to see AI recommendations!")
        return
    
    # Analyze user behavior
    ai_engine = st.session_state.ai_engine
    analysis_data = ai_engine.analyze_user_behavior(st.session_state.metrics_history)
    
    # Display insights
    st.markdown("### 📊 User Behavior Analysis")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("#### 🎯 Key Insights")
        for insight in analysis_data['insights']:
            st.markdown(f"""
            <div class="recommendation-item">
                <h4>{insight['title']}</h4>
                <p><strong>{insight['value']}</strong></p>
                <p>{insight['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with insights_col2:
        st.markdown("#### 📈 Summary Statistics")
        stats = analysis_data['summary_stats']
        st.metric("Total Runs", stats['total_runs'])
        st.metric("Total CO₂", f"{stats['total_co2']:.2f} kg")
        st.metric("Total Energy", f"{stats['total_energy']:.2f} kWh")
        st.metric("Total Water", f"{stats['total_water']:.2f} L")
        st.metric("Most Used Region", stats['most_used_region'])
        st.metric("Most Used Hardware", stats['most_used_hardware'])
    
    # Calculate current total costs
    total_carbon_cost = sum(metrics.carbon_emissions * 0.05 for metrics in st.session_state.metrics_history)  # $0.05 per kg CO₂
    total_energy_cost = sum(metrics.energy_consumed * 0.12 for metrics in st.session_state.metrics_history)  # $0.12 per kWh
    total_water_cost = sum(metrics.water_usage * 0.002 for metrics in st.session_state.metrics_history)  # $0.002 per liter
    current_total_cost = total_carbon_cost + total_energy_cost + total_water_cost
    
    # Display current cost summary
    st.markdown("### 💰 Current Run Costs")
    cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)
    
    with cost_col1:
        st.metric("Carbon Cost", f"${total_carbon_cost:.2f}", "CO₂ emissions")
    with cost_col2:
        st.metric("Energy Cost", f"${total_energy_cost:.2f}", "Electricity")
    with cost_col3:
        st.metric("Water Cost", f"${total_water_cost:.2f}", "Water usage")
    with cost_col4:
        st.metric("Total Cost", f"${current_total_cost:.2f}", "All combined")
    
    # Display recommendations with cost analysis
    st.markdown("### 🎯 AI Recommendations with Cost Analysis")
    
    # Sort recommendations by priority
    priority_order = {"high": 1, "medium": 2, "low": 3}
    sorted_recommendations = sorted(
        analysis_data['recommendations'], 
        key=lambda x: priority_order.get(x.get('priority', 'low'), 3)
    )
    
    for i, rec in enumerate(sorted_recommendations, 1):
        priority_color = {"high": "#dc3545", "medium": "#ffc107", "low": "#28a745"}
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        
        # Calculate potential savings based on recommendation type
        if "regional" in rec.get('type', '').lower():
            # Regional optimization: 15-25% savings
            savings_percentage = np.random.uniform(15, 25)
        elif "hardware" in rec.get('type', '').lower():
            # Hardware optimization: 10-20% savings
            savings_percentage = np.random.uniform(10, 20)
        elif "scheduling" in rec.get('type', '').lower():
            # Scheduling optimization: 5-15% savings
            savings_percentage = np.random.uniform(5, 15)
        elif "workload" in rec.get('type', '').lower():
            # Workload optimization: 20-40% savings
            savings_percentage = np.random.uniform(20, 40)
        else:
            # General optimization: 10-30% savings
            savings_percentage = np.random.uniform(10, 30)
        
        # Calculate savings amounts
        potential_savings = current_total_cost * (savings_percentage / 100)
        new_total_cost = current_total_cost - potential_savings
        
        # Calculate environmental savings
        avg_carbon = sum(metrics.carbon_emissions for metrics in st.session_state.metrics_history) / len(st.session_state.metrics_history)
        avg_energy = sum(metrics.energy_consumed for metrics in st.session_state.metrics_history) / len(st.session_state.metrics_history)
        avg_water = sum(metrics.water_usage for metrics in st.session_state.metrics_history) / len(st.session_state.metrics_history)
        
        carbon_savings = avg_carbon * (savings_percentage / 100)
        energy_savings = avg_energy * (savings_percentage / 100)
        water_savings = avg_water * (savings_percentage / 100)
        
        # Display recommendation with cost analysis
        st.markdown(f"""
        <div class="recommendation-card">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 1.2em; margin-right: 10px;">{priority_icon.get(rec.get('priority', 'low'))}</span>
                <h3 style="margin: 0; color: {priority_color.get(rec.get('priority', 'low'))};">{rec['title']}</h3>
                <span style="margin-left: auto; background: {priority_color.get(rec.get('priority', 'low'))}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8em;">{rec.get('priority', 'low').upper()}</span>
            </div>
            <p><strong>Description:</strong> {rec['description']}</p>
            <p><strong>Impact:</strong> {rec['impact']}</p>
            <p><strong>Action:</strong> {rec['action']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Cost and savings information
        st.info(f"💰 **Estimated cost for current run:** ${current_total_cost:.2f}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Total Cost",
                f"${current_total_cost:.2f}",
                "Your current spend"
            )
        
        with col2:
            st.metric(
                "With Recommendation",
                f"${new_total_cost:.2f}",
                f"-${potential_savings:.2f}"
            )
        
        with col3:
            st.metric(
                "Potential Savings",
                f"${potential_savings:.2f}",
                f"{savings_percentage:.1f}% reduction"
            )
        
        # Environmental savings breakdown
        st.success(f"🌱 **Environmental Impact:** Taking this recommendation can save you money and reduce your environmental impact. Here's how much you'd save if adopted.")
        
        env_col1, env_col2, env_col3, env_col4 = st.columns(4)
        
        with env_col1:
            st.metric(
                "Carbon Savings",
                f"{carbon_savings:.2f} kg",
                "CO₂ reduction"
            )
        
        with env_col2:
            st.metric(
                "Energy Savings", 
                f"{energy_savings:.2f} kWh",
                "Electricity saved"
            )
        
        with env_col3:
            st.metric(
                "Water Savings",
                f"{water_savings:.2f} L",
                "Water saved"
            )
        
        with env_col4:
            st.metric(
                "Cost Savings",
                f"${potential_savings:.2f}",
                "Money saved"
            )
        
        st.markdown("---")
    
    # AI Chat Interface
    st.markdown("### 💬 Ask AI for Environmental Advice")
    
    # Chat input
    user_question = st.text_input(
        "Ask me anything about environmental optimization:",
        placeholder="e.g., How can I reduce my carbon footprint? What's the most efficient region? How can I optimize my hardware usage?"
    )
    
    if st.button("🤖 Ask AI", type="primary"):
        if user_question:
            # Generate AI response
            ai_response = ai_engine.generate_llm_recommendations(user_question, analysis_data)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "user": user_question,
                "ai": ai_response,
                "timestamp": datetime.now()
            })
            
            st.rerun()
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("#### 💬 Conversation History")
        
        for chat in reversed(st.session_state.chat_history[-5:]):  # Show last 5 messages
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {chat['user']}
            </div>
            <div class="ai-message">
                <strong>🤖 AI Assistant:</strong> {chat['ai']}
            </div>
            """, unsafe_allow_html=True)
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

def show_pattern_analysis_tab():
    """Show pattern analysis tab."""
    st.markdown("## 📊 Pattern Analysis & Insights")
    
    if not st.session_state.metrics_history:
        st.info("🌱 Start tracking to see pattern analysis!")
        return
    
    # Analyze user behavior
    ai_engine = st.session_state.ai_engine
    analysis_data = ai_engine.analyze_user_behavior(st.session_state.metrics_history)
    
    # Display patterns
    st.markdown("### 🔍 Behavior Patterns")
    
    for pattern in analysis_data['patterns']:
        st.markdown(f"#### {pattern['title']}")
        st.markdown(f"*{pattern['description']}*")
        
        # Convert data to DataFrame for better display
        if isinstance(pattern['data'], dict):
            df = pd.DataFrame(pattern['data']).T
            st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
    
    # Create visualizations for patterns
    st.markdown("### 📈 Pattern Visualizations")
    
    # Create DataFrame from metrics history
    df_data = []
    for metrics in st.session_state.metrics_history:
        df_data.append({
            'Timestamp': metrics.timestamp,
            'Workload': metrics.workload_type,
            'Framework': metrics.framework,
            'Region': metrics.region,
            'Hardware': metrics.hardware_type,
            'CO₂ (kg)': metrics.carbon_emissions,
            'Energy (kWh)': metrics.energy_consumed,
            'Water (L)': metrics.water_usage,
            'Carbon Intensity (g/kWh)': metrics.carbon_intensity,
            'Water Intensity (L/kWh)': metrics.water_intensity,
            'Renewable %': metrics.renewable_percentage,
            'Runtime (s)': metrics.runtime_seconds
        })
    
    df = pd.DataFrame(df_data)
    
    # Workload impact visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚀 Workload Impact Analysis")
        workload_impact = df.groupby('Workload').agg({
            'CO₂ (kg)': 'sum',
            'Energy (kWh)': 'sum',
            'Water (L)': 'sum'
        }).reset_index()
        
        fig_workload = px.bar(
            workload_impact,
            x='Workload',
            y='CO₂ (kg)',
            title='CO₂ Emissions by Workload Type',
            color='CO₂ (kg)',
            color_continuous_scale='Reds'
        )
        fig_workload.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_workload, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌍 Regional Efficiency Analysis")
        regional_efficiency = df.groupby('Region').agg({
            'Carbon Intensity (g/kWh)': 'mean',
            'Renewable %': 'mean'
        }).reset_index()
        
        fig_regional = px.scatter(
            regional_efficiency,
            x='Carbon Intensity (g/kWh)',
            y='Renewable %',
            size='Carbon Intensity (g/kWh)',
            color='Region',
            title='Regional Environmental Efficiency',
            hover_data=['Region']
        )
        fig_regional.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_regional, use_container_width=True)
    
    # Hardware efficiency analysis
    st.markdown("#### 🔧 Hardware Efficiency Analysis")
    hardware_efficiency = df.groupby('Hardware').agg({
        'Energy (kWh)': 'mean',
        'CO₂ (kg)': 'mean',
        'Runtime (s)': 'mean'
    }).reset_index()
    
    fig_hardware = px.scatter(
        hardware_efficiency,
        x='Energy (kWh)',
        y='CO₂ (kg)',
        size='Runtime (s)',
        color='Hardware',
        title='Hardware Energy Efficiency',
        hover_data=['Hardware', 'Runtime (s)']
    )
    fig_hardware.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_hardware, use_container_width=True)
    
    # Time-based patterns
    st.markdown("#### ⏰ Time-based Usage Patterns")
    df['Hour'] = pd.to_datetime(df['Timestamp']).dt.hour
    hourly_patterns = df.groupby('Hour').agg({
        'CO₂ (kg)': 'mean',
        'Energy (kWh)': 'mean',
        'Renewable %': 'mean'
    }).reset_index()
    
    fig_time = px.line(
        hourly_patterns,
        x='Hour',
        y=['CO₂ (kg)', 'Energy (kWh)', 'Renewable %'],
        title='Environmental Impact by Hour of Day',
        markers=True
    )
    fig_time.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_time, use_container_width=True)

# Import the existing functions from the original app
from enhanced_visualization_with_sample_data import (
    show_control_panel, show_real_time_metrics, show_carbon_emissions_tab,
    show_energy_consumption_tab, show_water_usage_tab, show_combined_analysis_tab,
    show_calculation_explanation_tab
)

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
            Track Carbon Emissions, Energy Consumption & Water Usage with AI-Powered Recommendations
        </p>
        <p style="margin: 10px 0 0 0; font-size: 1em; opacity: 0.8;">
            🤖 AI-powered analysis • 📊 Interactive visualizations • 💬 Chat with AI assistant
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state with sample data
    initialize_session_state()
    
    # Control panel
    show_control_panel()
    
    # Real-time metrics
    show_real_time_metrics()
    
    # Main content with tabs - NOW WITH AI RECOMMENDATIONS
    st.markdown("## 📊 Environmental Impact Analysis with AI Recommendations")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🌍 Carbon Emissions", 
        "⚡ Energy Consumption", 
        "💧 Water Usage", 
        "🌍 Combined Analysis",
        "🤖 AI Recommendations",
        "📊 Pattern Analysis",
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
        show_ai_recommendations_tab()
    
    with tab6:
        show_pattern_analysis_tab()
    
    with tab7:
        show_calculation_explanation_tab()

if __name__ == "__main__":
    main()
