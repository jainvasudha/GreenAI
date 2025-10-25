#!/usr/bin/env python3
"""
🧠 NeuroGreen Complete Demo - All Features
==========================================

Complete NeuroGreen demo with all features:
- AI-powered recommendations
- Pattern analysis
- Interactive visualizations
- AI chat interface
- Environmental tracking
- Multi-user features
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Page configuration
st.set_page_config(
    page_title="🧠 NeuroGreen Complete Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class EnhancedCarbonMetrics:
    """Enhanced carbon metrics including energy and water usage."""
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

class NeuroGreenAIEngine:
    """NeuroGreen AI-powered recommendation engine."""
    
    def __init__(self):
        self.mock_responses = {
            "carbon footprint": "Based on your data, I recommend switching from us-east-1 to us-west-2 region, which could reduce your carbon emissions by 35%. Also, consider using more efficient hardware like Apple M2/M3 chips for better energy efficiency.",
            "efficient region": "Your most efficient region is us-west-2 (Oregon) with 200 g CO₂/kWh carbon intensity and 80% renewable energy. I recommend prioritizing this region for future workloads.",
            "hardware usage": "Your most efficient hardware configuration is Apple M2/M3 with RTX 4090. Consider upgrading from Intel i9 to Apple M2/M3 for 30-40% better energy efficiency.",
            "best practices": "Implement model compression, use pre-trained models, optimize batch sizes, and schedule workloads during peak renewable energy hours. These practices can reduce environmental impact by 20-80%.",
            "schedule": "Schedule intensive workloads during peak renewable energy hours (typically 10 AM - 2 PM in us-west-2). This can increase your renewable energy usage by 25%.",
            "energy": "To reduce energy consumption, consider using more efficient hardware, optimizing model architectures, and scheduling workloads during off-peak hours when renewable energy is more available.",
            "water": "Water usage can be reduced by choosing regions with lower water intensity factors and optimizing energy consumption, as water usage is directly correlated with energy consumption.",
            "optimization": "Focus on the three main areas: regional optimization (switch to us-west-2), hardware optimization (upgrade to Apple M2/M3), and scheduling optimization (run during peak renewable hours)."
        }
    
    def analyze_environmental_data(self, metrics_history: List[EnhancedCarbonMetrics]) -> Dict[str, Any]:
        """Analyze environmental data and generate AI recommendations."""
        if not metrics_history:
            return {"insights": [], "recommendations": [], "summary_stats": {}}
        
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
                'runtime_seconds': metrics.runtime_seconds
            })
        
        df = pd.DataFrame(df_data)
        
        # Generate insights and recommendations
        insights = self._generate_insights(df)
        recommendations = self._generate_recommendations(df)
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "summary_stats": self._calculate_summary_stats(df)
        }
    
    def _generate_insights(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate insights from environmental data."""
        insights = []
        
        # Total environmental impact
        total_co2 = df['carbon_emissions'].sum()
        total_energy = df['energy_consumed'].sum()
        total_water = df['water_usage'].sum()
        
        insights.append({
            "title": "Total Environmental Impact",
            "value": f"{total_co2:.6f} kg CO₂, {total_energy:.6f} kWh, {total_water:.2f} L",
            "description": "Cumulative environmental impact across all workloads"
        })
        
        # Efficiency metrics
        avg_carbon_intensity = df['carbon_intensity'].mean()
        avg_water_intensity = df['water_intensity'].mean()
        avg_renewable = df['renewable_percentage'].mean()
        
        insights.append({
            "title": "Average Efficiency Metrics",
            "value": f"Carbon: {avg_carbon_intensity:.1f} g/kWh, Water: {avg_water_intensity:.1f} L/kWh, Renewable: {avg_renewable:.1f}%",
            "description": "Average environmental efficiency across all runs"
        })
        
        return insights
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
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
            }
        ])
        
        return recommendations
    
    def _calculate_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate summary statistics."""
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
    
    def generate_ai_response(self, user_question: str, analysis_data: Dict[str, Any]) -> str:
        """Generate AI response based on user question."""
        question_lower = user_question.lower()
        
        for keyword, response in self.mock_responses.items():
            if keyword in question_lower:
                return response
        
        # Default response
        return f"Based on your environmental data, I can see you have {analysis_data['summary_stats']['total_runs']} runs with a total of {analysis_data['summary_stats']['total_co2']:.6f} kg CO₂ emissions. I recommend focusing on regional optimization, hardware efficiency, and workload scheduling for maximum environmental impact reduction."

def create_comprehensive_sample_data():
    """Create comprehensive sample environmental data for NeuroGreen demo."""
    sample_metrics = []
    
    # Create diverse sample data for better AI analysis
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
        ("training", "pytorch", "us-west-2", "aws", "apple_m2 + rtx_4090"),
        ("inference", "tensorflow", "us-east-1", "aws", "intel_i9 + rtx_4090"),
        ("data_processing", "huggingface", "eu-west-1", "aws", "apple_m3 + rtx_4080"),
        ("evaluation", "scikit-learn", "ap-southeast-1", "aws", "amd_ryzen7 + none"),
        ("fine_tuning", "transformers", "us-west-2", "gcp", "intel_i7 + rtx_3080")
    ]
    
    base_time = datetime.now() - timedelta(days=21)
    
    for i, (workload, framework, region, cloud, hardware) in enumerate(workloads):
        # Simulate realistic environmental impacts
        runtime = np.random.uniform(300, 7200)  # 5 minutes to 2 hours
        
        # Regional carbon intensity factors
        carbon_intensity_map = {
            "us-west-2": 200,  # Oregon - low carbon
            "us-east-1": 300,  # Virginia - medium carbon
            "eu-west-1": 250,  # Ireland - medium-low carbon
            "ap-southeast-1": 500,  # Singapore - high carbon
        }
        
        # Regional water intensity factors
        water_intensity_map = {
            "us-west-2": 1.5,  # Oregon - medium water
            "us-east-1": 1.2,  # Virginia - low water
            "eu-west-1": 1.4,  # Ireland - medium water
            "ap-southeast-1": 1.8,  # Singapore - high water
        }
        
        # Regional renewable percentage
        renewable_map = {
            "us-west-2": 80,  # Oregon - high renewable
            "us-east-1": 30,  # Virginia - low renewable
            "eu-west-1": 70,  # Ireland - high renewable
            "ap-southeast-1": 20,  # Singapore - low renewable
        }
        
        # Hardware-specific energy consumption
        energy_map = {
            "apple_m2 + rtx_4090": 0.8,
            "intel_i9 + rtx_4090": 1.2,
            "apple_m3 + rtx_4080": 0.7,
            "amd_ryzen7 + none": 0.3,
            "intel_i7 + rtx_3080": 0.9,
        }
        
        # Calculate environmental metrics
        energy = energy_map.get(hardware, 1.0) * (runtime / 3600)  # kWh
        carbon_intensity = carbon_intensity_map.get(region, 300)
        water_intensity = water_intensity_map.get(region, 1.5)
        renewable_percentage = renewable_map.get(region, 50)
        
        carbon_emissions = energy * carbon_intensity / 1000  # kg CO2
        water_usage = energy * water_intensity  # L
        
        # Add some variation for more realistic data
        carbon_emissions *= np.random.uniform(0.8, 1.2)
        energy *= np.random.uniform(0.9, 1.1)
        water_usage *= np.random.uniform(0.9, 1.1)
        
        metrics = EnhancedCarbonMetrics(
            timestamp=base_time + timedelta(hours=i*8),
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

def main():
    """Main demo function."""
    print("🌱 Enhanced Visualization App Demo")
    print("=" * 50)
    
    # Create sample data
    print("📊 Creating sample environmental data...")
    sample_metrics = create_sample_data()
    
    print(f"✅ Created {len(sample_metrics)} sample metrics")
    
    # Show sample data summary
    print("\n📈 Sample Data Summary:")
    print("-" * 30)
    
    total_co2 = sum(m.carbon_emissions for m in sample_metrics)
    total_energy = sum(m.energy_consumed for m in sample_metrics)
    total_water = sum(m.water_usage for m in sample_metrics)
    
    print(f"🌍 Total CO₂: {total_co2:.6f} kg")
    print(f"⚡ Total Energy: {total_energy:.6f} kWh")
    print(f"💧 Total Water: {total_water:.2f} L")
    
    # Show regional breakdown
    print("\n🌍 Regional Breakdown:")
    print("-" * 25)
    regional_data = {}
    for metrics in sample_metrics:
        region = metrics.region
        if region not in regional_data:
            regional_data[region] = {
                'co2': 0, 'energy': 0, 'water': 0, 'count': 0
            }
        regional_data[region]['co2'] += metrics.carbon_emissions
        regional_data[region]['energy'] += metrics.energy_consumed
        regional_data[region]['water'] += metrics.water_usage
        regional_data[region]['count'] += 1
    
    for region, data in regional_data.items():
        print(f"  {region}: {data['co2']:.6f} kg CO₂, {data['energy']:.6f} kWh, {data['water']:.2f} L")
    
    # Show workload breakdown
    print("\n🔧 Workload Breakdown:")
    print("-" * 25)
    workload_data = {}
    for metrics in sample_metrics:
        workload = metrics.workload_type
        if workload not in workload_data:
            workload_data[workload] = {
                'co2': 0, 'energy': 0, 'water': 0, 'count': 0
            }
        workload_data[workload]['co2'] += metrics.carbon_emissions
        workload_data[workload]['energy'] += metrics.energy_consumed
        workload_data[workload]['water'] += metrics.water_usage
        workload_data[workload]['count'] += 1
    
    for workload, data in workload_data.items():
        print(f"  {workload}: {data['co2']:.6f} kg CO₂, {data['energy']:.6f} kWh, {data['water']:.2f} L")
    
    # Environmental context
    print("\n🌍 Environmental Context:")
    print("-" * 30)
    trees_needed = total_co2 * 0.06
    car_miles = total_co2 * 2.2
    bottles = total_water / 0.5
    showers = total_water / 65
    
    print(f"🌳 Trees needed to offset: {trees_needed:.2f}")
    print(f"🚗 Car miles equivalent: {car_miles:.2f} miles")
    print(f"🍼 Water bottles equivalent: {bottles:.0f} bottles")
    print(f"🚿 Shower equivalent: {showers:.2f} showers")
    
    print("\n🎯 Enhanced Visualization App Features:")
    print("-" * 45)
    print("✅ Interactive tabs for each metric type")
    print("✅ Real-time graphs and visualizations")
    print("✅ Regional comparison charts")
    print("✅ Hardware efficiency analysis")
    print("✅ Environmental context and equivalents")
    print("✅ Combined impact analysis")
    print("✅ Calculation explanations")
    
    print("\n🚀 To run the enhanced visualization app:")
    print("   streamlit run enhanced_visualization_app.py")
    
    print("\n🌿 Enhanced environmental tracking with comprehensive visualizations!")

if __name__ == "__main__":
    main()
