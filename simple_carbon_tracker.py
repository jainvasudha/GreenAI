#!/usr/bin/env python3
"""
Simple Carbon Emission Tracker
==============================

A minimal example showing how to track carbon emissions from any Python script.
Perfect for adding to existing ML experiments.

Usage:
    # Add these lines to the beginning of your script:
    from simple_carbon_tracker import CarbonTracker
    tracker = CarbonTracker("MyExperiment")
    tracker.start()
    
    # Your ML code here...
    
    # Add this at the end:
    results = tracker.stop()
    print(f"🌍 Total CO₂ emissions: {results['emissions_kg']:.6f} kg")
"""

import sys
import subprocess
import logging
from datetime import datetime
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CarbonTracker:
    """
    Simple carbon emission tracker for any Python script.
    """
    
    def __init__(self, project_name: str = "MyExperiment"):
        self.project_name = project_name
        self.tracker = None
        self.start_time = None
        
    def _ensure_codecarbon(self):
        """Ensure CodeCarbon is installed."""
        try:
            import codecarbon
            return True
        except ImportError:
            logger.info("Installing CodeCarbon...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "codecarbon"])
                return True
            except subprocess.CalledProcessError:
                logger.error("Failed to install CodeCarbon")
                return False
    
    def start(self) -> bool:
        """Start tracking carbon emissions."""
        if not self._ensure_codecarbon():
            return False
        
        try:
            from codecarbon import EmissionsTracker
            
            self.tracker = EmissionsTracker(
                project_name=self.project_name,
                log_level="WARNING"  # Reduce verbosity
            )
            
            self.tracker.start()
            self.start_time = datetime.now()
            
            print(f"🌱 Started carbon tracking for: {self.project_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start carbon tracking: {e}")
            return False
    
    def stop(self) -> Dict:
        """Stop tracking and return emission data."""
        if not self.tracker:
            return {"emissions_kg": 0.0, "error": "No active tracker"}
        
        try:
            # Stop tracker and get emissions
            emissions_data = self.tracker.stop()
            end_time = datetime.now()
            
            # Extract emissions value
            if hasattr(emissions_data, 'emissions'):
                emissions_kg = emissions_data.emissions
            else:
                emissions_kg = float(emissions_data) if emissions_data else 0.0
            
            # Calculate runtime
            runtime_seconds = (end_time - self.start_time).total_seconds()
            
            results = {
                "project_name": self.project_name,
                "emissions_kg": emissions_kg,
                "runtime_seconds": runtime_seconds,
                "start_time": self.start_time,
                "end_time": end_time,
                "emissions_per_second": emissions_kg / runtime_seconds if runtime_seconds > 0 else 0
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error stopping tracker: {e}")
            return {"emissions_kg": 0.0, "error": str(e)}

# Example usage function
def track_emissions_example():
    """
    Example showing how to use the CarbonTracker in your code.
    """
    print("🚀 Starting carbon emission tracking example...")
    
    # Initialize tracker
    tracker = CarbonTracker("MyMLExperiment")
    
    # Start tracking
    if not tracker.start():
        print("❌ Failed to start carbon tracking")
        return
    
    try:
        # Your ML code goes here
        print("🤖 Running machine learning experiment...")
        
        # Simulate some computational work
        import time
        import numpy as np
        
        # Simulate data processing
        print("📊 Processing data...")
        data = np.random.randn(1000, 100)
        time.sleep(1)
        
        # Simulate model training
        print("🏋️ Training model...")
        for epoch in range(5):
            # Simulate training step
            np.dot(data, data.T)
            time.sleep(0.5)
            print(f"   Epoch {epoch + 1}/5 completed")
        
        # Simulate model evaluation
        print("📈 Evaluating model...")
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("⏹️  Experiment interrupted")
    except Exception as e:
        print(f"❌ Error during experiment: {e}")
    
    finally:
        # Stop tracking and get results
        print("🛑 Stopping carbon tracking...")
        results = tracker.stop()
        
        # Display results
        if "error" in results:
            print(f"❌ Error: {results['error']}")
        else:
            print("\n" + "="*50)
            print("🌍 CARBON EMISSION REPORT")
            print("="*50)
            print(f"📋 Project: {results['project_name']}")
            print(f"⏱️  Runtime: {results['runtime_seconds']:.2f} seconds")
            print(f"🌱 Total CO₂: {results['emissions_kg']:.6f} kg")
            print(f"⚡ Rate: {results['emissions_per_second']:.8f} kg/s")
            
            # Environmental context
            co2_kg = results['emissions_kg']
            if co2_kg > 0:
                trees_needed = co2_kg * 0.06  # Rough estimate
                car_miles = co2_kg * 2.2     # Rough estimate
                print(f"\n🌳 Environmental Impact:")
                print(f"   • {trees_needed:.2f} trees needed to offset")
                print(f"   • Equivalent to {car_miles:.1f} miles driven")
            
            print("="*50)

if __name__ == "__main__":
    track_emissions_example()
