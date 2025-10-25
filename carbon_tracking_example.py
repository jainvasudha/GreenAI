#!/usr/bin/env python3
"""
Carbon Tracking Example for GreenAI
===================================

This script demonstrates how to track and visualize carbon emissions
from machine learning experiments using CodeCarbon.

Features:
- Automatic CodeCarbon installation check
- Real-time carbon emission tracking
- Visualization with Plotly
- Detailed emission reporting
- Cross-platform compatibility (Mac, Linux, Windows)

Usage:
    python carbon_tracking_example.py
"""

import sys
import time
import subprocess
import logging
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_and_install_codecarbon():
    """
    Check if CodeCarbon is installed, install if not available.
    This ensures the script works on any machine.
    """
    try:
        import codecarbon
        logger.info(f"✅ CodeCarbon {codecarbon.__version__} is already installed")
        return True
    except ImportError:
        logger.warning("⚠️  CodeCarbon not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "codecarbon"])
            logger.info("✅ CodeCarbon installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install CodeCarbon: {e}")
            return False

def install_visualization_deps():
    """Install visualization dependencies if not available."""
    try:
        import plotly
        import matplotlib
        logger.info("✅ Visualization libraries already available")
        return True
    except ImportError:
        logger.info("📦 Installing visualization dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly", "matplotlib"])
            logger.info("✅ Visualization libraries installed")
            return True
        except subprocess.CalledProcessError:
            logger.warning("⚠️  Could not install visualization libraries. Charts will be skipped.")
            return False

class CarbonEmissionTracker:
    """
    Enhanced carbon emission tracker with visualization capabilities.
    """
    
    def __init__(self, project_name: str = "MyMLExperiment"):
        self.project_name = project_name
        self.tracker = None
        self.start_time = None
        self.emissions_data = []
        self.visualization_available = False
        
    def start_tracking(self):
        """Start carbon emission tracking."""
        try:
            from codecarbon import EmissionsTracker
            
            self.tracker = EmissionsTracker(
                project_name=self.project_name,
                log_level="INFO",
                tracking_mode="process"  # Track current process
            )
            
            self.tracker.start()
            self.start_time = datetime.now()
            
            logger.info(f"🌱 Started carbon tracking for project: {self.project_name}")
            logger.info(f"⏰ Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start carbon tracking: {e}")
            return False
    
    def log_emission_checkpoint(self, step_name: str, additional_info: str = ""):
        """Log current emissions at a specific checkpoint."""
        if self.tracker:
            try:
                # Get current emissions (this is approximate since CodeCarbon doesn't provide real-time data)
                current_time = datetime.now()
                elapsed = (current_time - self.start_time).total_seconds()
                
                self.emissions_data.append({
                    'timestamp': current_time,
                    'step': step_name,
                    'elapsed_seconds': elapsed,
                    'info': additional_info
                })
                
                logger.info(f"📊 Checkpoint '{step_name}': {elapsed:.1f}s elapsed")
                
            except Exception as e:
                logger.warning(f"⚠️  Could not log checkpoint: {e}")
    
    def stop_tracking(self) -> Dict:
        """Stop tracking and return comprehensive emission data."""
        if not self.tracker:
            logger.warning("⚠️  No active tracker to stop")
            return {}
        
        try:
            # Stop the tracker and get emissions data
            emissions_data = self.tracker.stop()
            end_time = datetime.now()
            
            # Calculate total time
            total_time = (end_time - self.start_time).total_seconds()
            
            # Extract emission information
            if hasattr(emissions_data, 'emissions'):
                total_emissions = emissions_data.emissions
                carbon_intensity = getattr(emissions_data, 'carbon_intensity', 0.0)
                renewable_percentage = getattr(emissions_data, 'renewable_percentage', 0.0)
            else:
                # Fallback if emissions_data is just a number
                total_emissions = float(emissions_data) if emissions_data else 0.0
                carbon_intensity = 0.0
                renewable_percentage = 0.0
            
            # Create comprehensive results
            results = {
                'project_name': self.project_name,
                'start_time': self.start_time,
                'end_time': end_time,
                'total_time_seconds': total_time,
                'total_emissions_kg': total_emissions,
                'carbon_intensity': carbon_intensity,
                'renewable_percentage': renewable_percentage,
                'checkpoints': self.emissions_data,
                'emissions_per_second': total_emissions / total_time if total_time > 0 else 0
            }
            
            logger.info(f"🏁 Stopped carbon tracking")
            logger.info(f"⏱️  Total runtime: {total_time:.2f} seconds")
            logger.info(f"🌍 Total CO₂ emissions: {total_emissions:.6f} kg")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error stopping tracker: {e}")
            return {}
    
    def print_emission_report(self, results: Dict):
        """Print a detailed emission report."""
        if not results:
            logger.warning("⚠️  No emission data to report")
            return
        
        print("\n" + "="*60)
        print("🌍 CARBON EMISSION REPORT")
        print("="*60)
        print(f"📋 Project: {results['project_name']}")
        print(f"⏰ Duration: {results['total_time_seconds']:.2f} seconds")
        print(f"🌱 Total CO₂ Emissions: {results['total_emissions_kg']:.6f} kg")
        print(f"⚡ Emissions per second: {results['emissions_per_second']:.8f} kg/s")
        
        if results['carbon_intensity'] > 0:
            print(f"🔋 Carbon Intensity: {results['carbon_intensity']:.2f} gCO₂/kWh")
        if results['renewable_percentage'] > 0:
            print(f"🌿 Renewable Energy: {results['renewable_percentage']:.1f}%")
        
        # Environmental impact context
        co2_kg = results['total_emissions_kg']
        if co2_kg > 0:
            # Rough equivalences for context
            trees_equivalent = co2_kg * 0.06  # Rough estimate: 1 tree absorbs ~16.5kg CO2/year
            car_miles = co2_kg * 2.2  # Rough estimate: 1kg CO2 ≈ 2.2 miles driven
            
            print(f"\n🌳 Environmental Impact Context:")
            print(f"   • Equivalent to {trees_equivalent:.2f} trees needed to offset")
            print(f"   • Equivalent to {car_miles:.1f} miles driven by car")
        
        print("="*60)
    
    def create_visualization(self, results: Dict):
        """Create visualization of emission data."""
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            import plotly.express as px
            
            if not results or not self.emissions_data:
                logger.warning("⚠️  No data available for visualization")
                return
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Emission Timeline', 'Cumulative Emissions', 
                              'Time Distribution', 'Emission Rate'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Prepare data
            timestamps = [d['timestamp'] for d in self.emissions_data]
            elapsed_times = [d['elapsed_seconds'] for d in self.emissions_data]
            steps = [d['step'] for d in self.emissions_data]
            
            # 1. Emission Timeline
            fig.add_trace(
                go.Scatter(x=elapsed_times, y=steps, mode='markers+lines',
                          name='Checkpoints', marker=dict(size=10)),
                row=1, col=1
            )
            
            # 2. Cumulative Emissions (simulated)
            cumulative_emissions = np.linspace(0, results['total_emissions_kg'], len(elapsed_times))
            fig.add_trace(
                go.Scatter(x=elapsed_times, y=cumulative_emissions, 
                          mode='lines', name='Cumulative CO₂', line=dict(color='red')),
                row=1, col=2
            )
            
            # 3. Time Distribution
            time_intervals = [elapsed_times[i] - elapsed_times[i-1] if i > 0 else elapsed_times[i] 
                            for i in range(len(elapsed_times))]
            fig.add_trace(
                go.Bar(x=steps, y=time_intervals, name='Time per Step'),
                row=2, col=1
            )
            
            # 4. Emission Rate
            emission_rates = [results['emissions_per_second']] * len(elapsed_times)
            fig.add_trace(
                go.Scatter(x=elapsed_times, y=emission_rates, mode='lines',
                          name='Emission Rate (kg/s)', line=dict(color='green')),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title=f"🌍 Carbon Emission Analysis - {results['project_name']}",
                showlegend=True,
                height=800,
                template="plotly_white"
            )
            
            # Update axes labels
            fig.update_xaxes(title_text="Time (seconds)", row=1, col=1)
            fig.update_yaxes(title_text="Steps", row=1, col=1)
            fig.update_xaxes(title_text="Time (seconds)", row=1, col=2)
            fig.update_yaxes(title_text="CO₂ (kg)", row=1, col=2)
            fig.update_xaxes(title_text="Steps", row=2, col=1)
            fig.update_yaxes(title_text="Time (seconds)", row=2, col=1)
            fig.update_xaxes(title_text="Time (seconds)", row=2, col=2)
            fig.update_yaxes(title_text="Emission Rate (kg/s)", row=2, col=2)
            
            # Save and show
            fig.write_html("carbon_emission_analysis.html")
            fig.show()
            
            logger.info("📊 Visualization created and saved as 'carbon_emission_analysis.html'")
            
        except ImportError:
            logger.warning("⚠️  Plotly not available. Skipping visualization.")
        except Exception as e:
            logger.error(f"❌ Error creating visualization: {e}")

def simulate_ml_experiment():
    """
    Simulate a machine learning experiment with various computational tasks.
    This represents typical ML workloads that consume energy.
    """
    logger.info("🤖 Starting simulated ML experiment...")
    
    # Simulate data loading
    logger.info("📊 Loading dataset...")
    time.sleep(1)  # Simulate I/O operations
    
    # Simulate data preprocessing
    logger.info("🔧 Preprocessing data...")
    time.sleep(2)  # Simulate CPU-intensive preprocessing
    
    # Simulate model training
    logger.info("🏋️ Training model...")
    time.sleep(3)  # Simulate GPU/CPU intensive training
    
    # Simulate model evaluation
    logger.info("📈 Evaluating model...")
    time.sleep(1)  # Simulate inference
    
    # Simulate hyperparameter tuning
    logger.info("⚙️ Hyperparameter tuning...")
    time.sleep(2)  # Simulate multiple training runs
    
    logger.info("✅ ML experiment completed!")

def main():
    """
    Main function demonstrating carbon emission tracking.
    """
    print("🌱 GreenAI Carbon Emission Tracking Demo")
    print("="*50)
    
    # Step 1: Check and install CodeCarbon
    logger.info("🔍 Checking CodeCarbon installation...")
    if not check_and_install_codecarbon():
        logger.error("❌ Cannot proceed without CodeCarbon")
        return
    
    # Step 2: Install visualization dependencies
    install_visualization_deps()
    
    # Step 3: Initialize carbon tracker
    logger.info("🚀 Initializing carbon emission tracker...")
    tracker = CarbonEmissionTracker("MyMLExperiment")
    
    # Step 4: Start tracking
    if not tracker.start_tracking():
        logger.error("❌ Failed to start carbon tracking")
        return
    
    try:
        # Step 5: Run the ML experiment with checkpoints
        logger.info("🎯 Running ML experiment with emission tracking...")
        
        # Simulate various ML tasks with emission checkpoints
        tracker.log_emission_checkpoint("Data Loading", "Loading training dataset")
        simulate_ml_experiment()
        
        tracker.log_emission_checkpoint("Data Preprocessing", "Feature engineering and cleaning")
        time.sleep(1)
        
        tracker.log_emission_checkpoint("Model Training", "Training neural network")
        time.sleep(2)
        
        tracker.log_emission_checkpoint("Model Evaluation", "Testing model performance")
        time.sleep(1)
        
        tracker.log_emission_checkpoint("Hyperparameter Tuning", "Grid search optimization")
        time.sleep(1)
        
        tracker.log_emission_checkpoint("Final Results", "Generating reports and visualizations")
        time.sleep(1)
        
    except KeyboardInterrupt:
        logger.info("⏹️  Experiment interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error during experiment: {e}")
    
    finally:
        # Step 6: Stop tracking and get results
        logger.info("🛑 Stopping carbon emission tracking...")
        results = tracker.stop_tracking()
        
        # Step 7: Print detailed report
        tracker.print_emission_report(results)
        
        # Step 8: Create visualization
        logger.info("📊 Creating emission visualization...")
        tracker.create_visualization(results)
        
        print("\n🎉 Carbon emission tracking completed!")
        print("📁 Check 'carbon_emission_analysis.html' for detailed visualizations")

if __name__ == "__main__":
    main()
