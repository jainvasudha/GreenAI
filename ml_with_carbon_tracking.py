#!/usr/bin/env python3
"""
Machine Learning with Carbon Emission Tracking
==============================================

This example shows how to integrate carbon emission tracking into a real ML training script.
It demonstrates tracking emissions during model training, evaluation, and inference.

Features:
- Real-time carbon emission tracking
- Per-epoch emission monitoring
- Visualization of emissions over time
- Environmental impact reporting
"""

import sys
import time
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MLCarbonTracker:
    """
    Carbon emission tracker specifically designed for ML experiments.
    """
    
    def __init__(self, project_name: str = "MLExperiment"):
        self.project_name = project_name
        self.tracker = None
        self.start_time = None
        self.epoch_emissions = []
        self.checkpoints = []
        
    def _install_dependencies(self):
        """Install required dependencies."""
        try:
            import codecarbon
            import plotly
            return True
        except ImportError:
            logger.info("Installing required dependencies...")
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "codecarbon", "plotly"])
                return True
            except subprocess.CalledProcessError:
                logger.error("Failed to install dependencies")
                return False
    
    def start_tracking(self):
        """Start carbon emission tracking."""
        if not self._install_dependencies():
            return False
        
        try:
            from codecarbon import EmissionsTracker
            
            self.tracker = EmissionsTracker(
                project_name=self.project_name,
                log_level="WARNING",
                tracking_mode="process"
            )
            
            self.tracker.start()
            self.start_time = datetime.now()
            
            logger.info(f"🌱 Started carbon tracking for: {self.project_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start carbon tracking: {e}")
            return False
    
    def log_epoch(self, epoch: int, loss: float, additional_info: str = ""):
        """Log emissions at the end of each epoch."""
        if self.tracker:
            current_time = datetime.now()
            elapsed = (current_time - self.start_time).total_seconds()
            
            self.epoch_emissions.append({
                'epoch': epoch,
                'timestamp': current_time,
                'elapsed_seconds': elapsed,
                'loss': loss,
                'info': additional_info
            })
            
            logger.info(f"📊 Epoch {epoch}: Loss={loss:.4f}, Time={elapsed:.1f}s")
    
    def log_checkpoint(self, checkpoint_name: str, metrics: Dict = None):
        """Log emissions at specific checkpoints."""
        if self.tracker:
            current_time = datetime.now()
            elapsed = (current_time - self.start_time).total_seconds()
            
            self.checkpoints.append({
                'name': checkpoint_name,
                'timestamp': current_time,
                'elapsed_seconds': elapsed,
                'metrics': metrics or {}
            })
            
            logger.info(f"📍 Checkpoint '{checkpoint_name}': {elapsed:.1f}s elapsed")
    
    def stop_tracking(self) -> Dict:
        """Stop tracking and return comprehensive results."""
        if not self.tracker:
            return {"error": "No active tracker"}
        
        try:
            # Stop tracker
            emissions_data = self.tracker.stop()
            end_time = datetime.now()
            total_time = (end_time - self.start_time).total_seconds()
            
            # Extract emissions
            if hasattr(emissions_data, 'emissions'):
                total_emissions = emissions_data.emissions
                carbon_intensity = getattr(emissions_data, 'carbon_intensity', 0.0)
                renewable_percentage = getattr(emissions_data, 'renewable_percentage', 0.0)
            else:
                total_emissions = float(emissions_data) if emissions_data else 0.0
                carbon_intensity = 0.0
                renewable_percentage = 0.0
            
            results = {
                'project_name': self.project_name,
                'total_emissions_kg': total_emissions,
                'total_time_seconds': total_time,
                'carbon_intensity': carbon_intensity,
                'renewable_percentage': renewable_percentage,
                'start_time': self.start_time,
                'end_time': end_time,
                'epoch_emissions': self.epoch_emissions,
                'checkpoints': self.checkpoints,
                'emissions_per_second': total_emissions / total_time if total_time > 0 else 0
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error stopping tracker: {e}")
            return {"error": str(e)}
    
    def create_emission_visualization(self, results: Dict):
        """Create visualization of emission data."""
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            if "error" in results:
                logger.warning("Cannot create visualization due to error")
                return
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Emissions Over Time', 'Loss vs Emissions', 
                              'Emission Rate', 'Checkpoint Timeline'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Prepare data
            epochs = [e['epoch'] for e in self.epoch_emissions]
            elapsed_times = [e['elapsed_seconds'] for e in self.epoch_emissions]
            losses = [e['loss'] for e in self.epoch_emissions]
            
            # Simulate cumulative emissions (CodeCarbon doesn't provide real-time data)
            cumulative_emissions = np.linspace(0, results['total_emissions_kg'], len(epochs))
            
            # 1. Emissions over time
            fig.add_trace(
                go.Scatter(x=elapsed_times, y=cumulative_emissions, 
                          mode='lines+markers', name='Cumulative CO₂',
                          line=dict(color='red', width=2)),
                row=1, col=1
            )
            
            # 2. Loss vs Emissions
            fig.add_trace(
                go.Scatter(x=losses, y=cumulative_emissions, 
                          mode='markers', name='Loss vs Emissions',
                          marker=dict(color='blue', size=8)),
                row=1, col=2
            )
            
            # 3. Emission rate
            emission_rate = [results['emissions_per_second']] * len(elapsed_times)
            fig.add_trace(
                go.Scatter(x=elapsed_times, y=emission_rate, 
                          mode='lines', name='Emission Rate (kg/s)',
                          line=dict(color='green', width=2)),
                row=2, col=1
            )
            
            # 4. Checkpoint timeline
            checkpoint_times = [c['elapsed_seconds'] for c in self.checkpoints]
            checkpoint_names = [c['name'] for c in self.checkpoints]
            fig.add_trace(
                go.Scatter(x=checkpoint_times, y=checkpoint_names, 
                          mode='markers', name='Checkpoints',
                          marker=dict(color='orange', size=10)),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title=f"🌍 Carbon Emission Analysis - {results['project_name']}",
                showlegend=True,
                height=800,
                template="plotly_white"
            )
            
            # Update axes
            fig.update_xaxes(title_text="Time (seconds)", row=1, col=1)
            fig.update_yaxes(title_text="CO₂ (kg)", row=1, col=1)
            fig.update_xaxes(title_text="Loss", row=1, col=2)
            fig.update_yaxes(title_text="CO₂ (kg)", row=1, col=2)
            fig.update_xaxes(title_text="Time (seconds)", row=2, col=1)
            fig.update_yaxes(title_text="Emission Rate (kg/s)", row=2, col=2)
            fig.update_xaxes(title_text="Time (seconds)", row=2, col=2)
            fig.update_yaxes(title_text="Checkpoints", row=2, col=2)
            
            # Save and show
            filename = f"carbon_analysis_{self.project_name.replace(' ', '_')}.html"
            fig.write_html(filename)
            fig.show()
            
            logger.info(f"📊 Visualization saved as '{filename}'")
            
        except ImportError:
            logger.warning("Plotly not available. Skipping visualization.")
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
    
    def print_detailed_report(self, results: Dict):
        """Print a detailed emission report."""
        if "error" in results:
            print(f"❌ Error: {results['error']}")
            return
        
        print("\n" + "="*70)
        print("🌍 DETAILED CARBON EMISSION REPORT")
        print("="*70)
        print(f"📋 Project: {results['project_name']}")
        print(f"⏰ Start Time: {results['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏰ End Time: {results['end_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  Total Runtime: {results['total_time_seconds']:.2f} seconds")
        print(f"🌱 Total CO₂ Emissions: {results['total_emissions_kg']:.6f} kg")
        print(f"⚡ Average Emission Rate: {results['emissions_per_second']:.8f} kg/s")
        
        if results['carbon_intensity'] > 0:
            print(f"🔋 Carbon Intensity: {results['carbon_intensity']:.2f} gCO₂/kWh")
        if results['renewable_percentage'] > 0:
            print(f"🌿 Renewable Energy: {results['renewable_percentage']:.1f}%")
        
        # Epoch analysis
        if self.epoch_emissions:
            print(f"\n📊 Training Analysis:")
            print(f"   • Total Epochs: {len(self.epoch_emissions)}")
            print(f"   • Average Time per Epoch: {results['total_time_seconds']/len(self.epoch_emissions):.2f}s")
            print(f"   • Final Loss: {self.epoch_emissions[-1]['loss']:.4f}")
        
        # Checkpoint analysis
        if self.checkpoints:
            print(f"\n📍 Checkpoints ({len(self.checkpoints)}):")
            for checkpoint in self.checkpoints:
                print(f"   • {checkpoint['name']}: {checkpoint['elapsed_seconds']:.1f}s")
        
        # Environmental impact
        co2_kg = results['total_emissions_kg']
        if co2_kg > 0:
            trees_needed = co2_kg * 0.06
            car_miles = co2_kg * 2.2
            print(f"\n🌳 Environmental Impact:")
            print(f"   • Trees needed to offset: {trees_needed:.2f}")
            print(f"   • Equivalent car miles: {car_miles:.1f} miles")
            print(f"   • Equivalent to {car_miles/100:.1f}% of a cross-country drive")
        
        print("="*70)

def simulate_ml_training():
    """
    Simulate a realistic ML training process with carbon tracking.
    """
    print("🤖 Starting ML Training with Carbon Tracking...")
    
    # Initialize carbon tracker
    tracker = MLCarbonTracker("NeuralNetworkTraining")
    
    # Start tracking
    if not tracker.start_tracking():
        print("❌ Failed to start carbon tracking")
        return
    
    try:
        # Simulate data loading
        print("📊 Loading dataset...")
        tracker.log_checkpoint("Data Loading")
        time.sleep(1)
        
        # Simulate data preprocessing
        print("🔧 Preprocessing data...")
        tracker.log_checkpoint("Data Preprocessing")
        time.sleep(2)
        
        # Simulate model training with epochs
        print("🏋️ Training model...")
        tracker.log_checkpoint("Training Start")
        
        # Simulate training epochs
        initial_loss = 1.0
        for epoch in range(10):
            # Simulate training step
            time.sleep(0.5)
            
            # Simulate loss reduction
            loss = initial_loss * (0.8 ** epoch) + np.random.normal(0, 0.01)
            
            # Log epoch with emissions
            tracker.log_epoch(epoch + 1, loss, f"Epoch {epoch + 1} completed")
            
            print(f"   Epoch {epoch + 1}/10: Loss = {loss:.4f}")
        
        # Simulate model evaluation
        print("📈 Evaluating model...")
        tracker.log_checkpoint("Model Evaluation")
        time.sleep(1)
        
        # Simulate hyperparameter tuning
        print("⚙️ Hyperparameter tuning...")
        tracker.log_checkpoint("Hyperparameter Tuning")
        time.sleep(2)
        
        # Simulate model saving
        print("💾 Saving model...")
        tracker.log_checkpoint("Model Saving")
        time.sleep(1)
        
        print("✅ Training completed!")
        
    except KeyboardInterrupt:
        print("⏹️  Training interrupted by user")
    except Exception as e:
        print(f"❌ Error during training: {e}")
    
    finally:
        # Stop tracking and get results
        print("🛑 Stopping carbon tracking...")
        results = tracker.stop_tracking()
        
        # Print detailed report
        tracker.print_detailed_report(results)
        
        # Create visualization
        print("📊 Creating emission visualization...")
        tracker.create_emission_visualization(results)
        
        print("\n🎉 Carbon emission tracking completed!")
        print("📁 Check the generated HTML file for detailed visualizations")

if __name__ == "__main__":
    simulate_ml_training()
