"""
🤖 Demo Script for AI-Powered Environmental Recommendations
==========================================================

This script demonstrates the AI recommendation features and generates
sample data to showcase the intelligent analysis capabilities.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any

# Import the AI recommendation engine
from enhanced_visualization_with_ai_recommendations import AIRecommendationEngine
from enhanced_carbon_tracker import EnhancedCarbonMetrics

def create_demo_data():
    """Create comprehensive demo data for AI recommendations."""
    demo_metrics = []
    
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
        ("evaluation", "transformers", "ap-southeast-1", "aws", "intel_i7 + rtx_3080")
    ]
    
    base_time = datetime.now() - timedelta(days=14)
    
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
            timestamp=base_time + timedelta(hours=i*12),
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
        
        demo_metrics.append(metrics)
    
    return demo_metrics

def demonstrate_ai_analysis():
    """Demonstrate AI analysis capabilities."""
    st.markdown("## 🤖 AI Analysis Demonstration")
    
    # Create demo data
    demo_data = create_demo_data()
    
    # Initialize AI engine
    ai_engine = AIRecommendationEngine()
    
    # Analyze user behavior
    st.markdown("### 📊 Analyzing User Behavior...")
    with st.spinner("AI is analyzing your environmental patterns..."):
        analysis_data = ai_engine.analyze_user_behavior(demo_data)
    
    # Display insights
    st.markdown("### 🎯 Key Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("#### 📈 Summary Statistics")
        stats = analysis_data['summary_stats']
        
        st.metric("Total Runs", stats['total_runs'])
        st.metric("Total CO₂", f"{stats['total_co2']:.6f} kg")
        st.metric("Total Energy", f"{stats['total_energy']:.6f} kWh")
        st.metric("Total Water", f"{stats['total_water']:.2f} L")
        st.metric("Most Used Region", stats['most_used_region'])
        st.metric("Most Used Hardware", stats['most_used_hardware'])
    
    with insights_col2:
        st.markdown("#### 🔍 Pattern Analysis")
        for insight in analysis_data['insights']:
            st.markdown(f"**{insight['title']}**")
            st.markdown(f"*{insight['value']}*")
            st.markdown(f"{insight['description']}")
            st.markdown("---")
    
    # Display recommendations
    st.markdown("### 🎯 AI Recommendations")
    
    # Sort by priority
    priority_order = {"high": 1, "medium": 2, "low": 3}
    sorted_recommendations = sorted(
        analysis_data['recommendations'], 
        key=lambda x: priority_order.get(x.get('priority', 'low'), 3)
    )
    
    for i, rec in enumerate(sorted_recommendations, 1):
        priority_color = {"high": "#dc3545", "medium": "#ffc107", "low": "#28a745"}
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 4px solid {priority_color.get(rec.get('priority', 'low'))};
        ">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 1.2em; margin-right: 10px;">{priority_icon.get(rec.get('priority', 'low'))}</span>
                <h3 style="margin: 0; color: {priority_color.get(rec.get('priority', 'low'))};">{rec['title']}</h3>
                <span style="margin-left: auto; background: {priority_color.get(rec.get('priority', 'low'))}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8em;">{rec.get('priority', 'low').upper()}</span>
            </div>
            <p><strong>Description:</strong> {rec['description']}</p>
            <p><strong>Impact:</strong> {rec['impact']}</p>
            <p><strong>Action:</strong> {rec['action']}</p>
            <p><strong>Estimated Savings:</strong> {rec['estimated_savings']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display patterns
    st.markdown("### 📊 Pattern Analysis")
    
    # Create DataFrame for visualization
    df_data = []
    for metrics in demo_data:
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
    
    # Display patterns
    for pattern in analysis_data['patterns']:
        st.markdown(f"#### {pattern['title']}")
        st.markdown(f"*{pattern['description']}*")
        
        if isinstance(pattern['data'], dict):
            pattern_df = pd.DataFrame(pattern['data']).T
            st.dataframe(pattern_df, use_container_width=True)
        
        st.markdown("---")
    
    return analysis_data

def demonstrate_llm_integration():
    """Demonstrate LLM integration capabilities."""
    st.markdown("## 💬 LLM Integration Demonstration")
    
    # Sample questions and responses
    sample_questions = [
        "How can I reduce my carbon footprint?",
        "What's the most efficient region for my workloads?",
        "How can I optimize my hardware usage?",
        "What are the best practices for sustainable AI?",
        "How can I schedule my workloads for maximum efficiency?"
    ]
    
    st.markdown("### 🤖 Sample AI Conversations")
    
    for question in sample_questions:
        st.markdown(f"""
        <div style="
            background: #f3e5f5;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #9c27b0;
        ">
            <strong>You:</strong> {question}
        </div>
        """, unsafe_allow_html=True)
        
        # Generate sample response
        if "carbon footprint" in question.lower():
            response = "Based on your data, I recommend switching from us-east-1 to us-west-2 region, which could reduce your carbon emissions by 35%. Also, consider using more efficient hardware like Apple M2/M3 chips for better energy efficiency."
        elif "efficient region" in question.lower():
            response = "Your most efficient region is us-west-2 (Oregon) with 200 g CO₂/kWh carbon intensity and 80% renewable energy. I recommend prioritizing this region for future workloads."
        elif "hardware usage" in question.lower():
            response = "Your most efficient hardware configuration is Apple M2/M3 with RTX 4090. Consider upgrading from Intel i9 to Apple M2/M3 for 30-40% better energy efficiency."
        elif "best practices" in question.lower():
            response = "Implement model compression, use pre-trained models, optimize batch sizes, and schedule workloads during peak renewable energy hours. These practices can reduce environmental impact by 20-80%."
        elif "schedule" in question.lower():
            response = "Schedule intensive workloads during peak renewable energy hours (typically 10 AM - 2 PM in us-west-2). This can increase your renewable energy usage by 25%."
        else:
            response = "I can help you optimize your environmental impact. Please ask me specific questions about carbon emissions, energy consumption, water usage, or regional optimization."
        
        st.markdown(f"""
        <div style="
            background: #e3f2fd;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #2196f3;
        ">
            <strong>🤖 AI Assistant:</strong> {response}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Try It Yourself!")
    st.info("🌱 In the full app, you can ask the AI assistant any question about environmental optimization. The AI will analyze your specific data and provide personalized recommendations!")

def main():
    """Main demonstration function."""
    st.set_page_config(
        page_title="🤖 AI Recommendations Demo",
        page_icon="🤖",
        layout="wide"
    )
    
    # Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #007bff 0%, #28a745 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    ">
        <h1 style="margin: 0; font-size: 3rem;">🤖 AI Recommendations Demo</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">
            Intelligent Environmental Analysis & LLM-Powered Recommendations
        </p>
        <p style="margin: 10px 0 0 0; font-size: 1em; opacity: 0.8;">
            🧠 AI Analysis • 💬 LLM Chat • 📊 Pattern Recognition • 🎯 Smart Recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "🤖 AI Analysis Demo",
        "💬 LLM Integration Demo", 
        "📊 Pattern Recognition Demo"
    ])
    
    with tab1:
        demonstrate_ai_analysis()
    
    with tab2:
        demonstrate_llm_integration()
    
    with tab3:
        st.markdown("## 📊 Pattern Recognition Demo")
        st.info("🌱 The AI system analyzes your environmental data to identify patterns, trends, and optimization opportunities. This helps you make data-driven decisions for sustainable AI development.")
        
        # Show sample patterns
        st.markdown("### 🔍 Identified Patterns")
        
        patterns = [
            {
                "title": "Workload Impact Analysis",
                "description": "Training workloads have 3x higher environmental impact than inference",
                "recommendation": "Consider using pre-trained models or model compression"
            },
            {
                "title": "Regional Efficiency",
                "description": "us-west-2 region is 40% more efficient than us-east-1",
                "recommendation": "Switch to us-west-2 for future workloads"
            },
            {
                "title": "Hardware Optimization",
                "description": "Apple M2/M3 chips are 30% more energy efficient than Intel i9",
                "recommendation": "Upgrade to Apple M2/M3 hardware for better efficiency"
            },
            {
                "title": "Time-based Patterns",
                "description": "Workloads at 10 AM have 25% higher renewable energy usage",
                "recommendation": "Schedule intensive workloads during peak renewable hours"
            }
        ]
        
        for pattern in patterns:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border-left: 4px solid #007bff;
            ">
                <h4 style="color: #007bff; margin-top: 0;">{pattern['title']}</h4>
                <p><strong>Pattern:</strong> {pattern['description']}</p>
                <p><strong>Recommendation:</strong> {pattern['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🌱 <strong>GreenAI with AI Recommendations</strong> - Making AI Development Intelligent and Sustainable</p>
        <p>Ready to revolutionize your environmental tracking with AI-powered insights!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
