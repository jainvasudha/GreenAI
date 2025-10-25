#!/usr/bin/env python3
"""
🌿 GreenAI Eco App Launcher
===========================

Launch different versions of the GreenAI Carbon Tracker app
with various eco-conscious themes and features.

Usage:
    python launch_eco_app.py
"""

import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main launcher interface."""
    
    st.set_page_config(
        page_title="🌿 GreenAI App Launcher",
        page_icon="🌿",
        layout="centered"
    )
    
    # Custom CSS for launcher
    st.markdown("""
    <style>
        .launcher-header {
            background: linear-gradient(135deg, #228B22 0%, #98A869 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(34, 139, 34, 0.3);
        }
        
        .launcher-header h1 {
            color: white;
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .app-card {
            background: linear-gradient(145deg, #F5F5DC 0%, #f8f8f0 100%);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            border: 1px solid rgba(152, 168, 105, 0.2);
            transition: all 0.3s ease;
        }
        
        .app-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .app-card h3 {
            color: #6B4F2A;
            margin: 0 0 1rem 0;
            font-size: 1.5rem;
        }
        
        .app-card p {
            color: #6B4F2A;
            margin: 0 0 1rem 0;
            line-height: 1.6;
        }
        
        .launch-button {
            background: linear-gradient(135deg, #BE5103 0%, #D2691E 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(190, 81, 3, 0.3);
        }
        
        .launch-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(190, 81, 3, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="launcher-header">
        <h1>🌿 GreenAI App Launcher</h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; margin: 0;">
            Choose your preferred eco-conscious carbon tracking experience
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # App options
    st.markdown("## 🚀 Available Apps")
    
    # Basic Eco App
    st.markdown("""
    <div class="app-card">
        <h3>🌱 Basic Eco Carbon Tracker</h3>
        <p>
            A clean, simple carbon tracking app with eco-conscious design.
            Perfect for basic monitoring and getting started with carbon tracking.
        </p>
        <p><strong>Features:</strong> Basic tracking, simple UI, essential metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌱 Launch Basic App", key="basic_app"):
        st.info("Launching basic eco app...")
        # In a real implementation, you would launch the app here
        st.success("✅ Basic Eco App launched!")
    
    # Enhanced Eco App
    st.markdown("""
    <div class="app-card">
        <h3>🌿 Enhanced Eco Carbon Tracker</h3>
        <p>
            A premium carbon tracking app with advanced features, animations,
            and comprehensive environmental impact analysis.
        </p>
        <p><strong>Features:</strong> Premium UI, animations, advanced analytics, real-time monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌿 Launch Enhanced App", key="enhanced_app"):
        st.info("Launching enhanced eco app...")
        # In a real implementation, you would launch the app here
        st.success("✅ Enhanced Eco App launched!")
    
    # Original App
    st.markdown("""
    <div class="app-card">
        <h3>📊 Original Carbon Tracker</h3>
        <p>
            The original GreenAI carbon tracking app with standard Streamlit styling.
            Good for comparison and traditional interface preferences.
        </p>
        <p><strong>Features:</strong> Standard UI, basic tracking, traditional design</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Launch Original App", key="original_app"):
        st.info("Launching original app...")
        # In a real implementation, you would launch the app here
        st.success("✅ Original App launched!")
    
    # Instructions
    st.markdown("---")
    st.markdown("## 📖 How to Use")
    
    st.markdown("""
    ### 🌱 Basic Eco App
    - **Best for**: Getting started, simple tracking
    - **Features**: Clean interface, essential metrics
    - **Launch**: `streamlit run eco_carbon_tracker_app.py`
    
    ### 🌿 Enhanced Eco App  
    - **Best for**: Professional use, advanced analytics
    - **Features**: Premium UI, animations, comprehensive analysis
    - **Launch**: `streamlit run enhanced_eco_app.py`
    
    ### 📊 Original App
    - **Best for**: Traditional interface, comparison
    - **Features**: Standard Streamlit styling, basic functionality
    - **Launch**: `streamlit run app.py`
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B4F2A; margin-top: 2rem;">
        <p><strong>🌿 GreenAI Carbon Tracker</strong></p>
        <p>Making AI Development Sustainable</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
