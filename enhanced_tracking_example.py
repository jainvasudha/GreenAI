#!/usr/bin/env python3
"""
🌱 Enhanced Environmental Tracking Example
=========================================

Example script showing how to use the enhanced carbon tracker
with energy consumption and water usage calculations.
"""

import time
import numpy as np
from datetime import datetime
from enhanced_carbon_tracker import EnhancedCarbonTracker, WaterIntensityCalculator, EnergyCalculator

def simulate_ml_training():
    """Simulate a machine learning training workload."""
    print("🧠 Simulating ML training workload...")
    
    # Simulate some computational work
    for epoch in range(5):
        print(f"  Epoch {epoch + 1}/5...")
        # Simulate training computation
        data = np.random.randn(1000, 100)
        result = np.dot(data, data.T)
        time.sleep(0.5)  # Simulate processing time
    
    print("✅ Training completed!")

def main():
    """Main example function."""
    print("🌱 Enhanced Environmental Tracking Example")
    print("=" * 50)
    
    # Initialize enhanced tracker
    tracker = EnhancedCarbonTracker(
        project_name="Enhanced ML Training",
        region="us-west-2",  # Oregon - hydro-heavy region
        cloud_provider="aws"
    )
    
    # Set hardware specifications
    hardware_specs = {
        'cpu_type': 'apple_m2',
        'gpu_type': 'rtx_4090',
        'memory_type': 'ddr5_32gb',
        'cpu_utilization': 0.7,
        'gpu_utilization': 0.9,
        'memory_usage': 0.6
    }
    
    print(f"🔧 Hardware: {hardware_specs['cpu_type']} + {hardware_specs['gpu_type']}")
    print(f"🌍 Region: {tracker.region} ({tracker.cloud_provider})")
    print()
    
    # Start tracking
    print("🌱 Starting enhanced environmental tracking...")
    session_id = tracker.start_tracking(
        workload_type="training",
        framework="pytorch",
        hardware_specs=hardware_specs
    )
    print(f"📊 Session ID: {session_id}")
    print()
    
    # Simulate workload
    simulate_ml_training()
    
    # Stop tracking
    print("🛑 Stopping environmental tracking...")
    metrics = tracker.stop_tracking()
    
    if metrics:
        print("\n📊 Environmental Impact Results:")
        print("=" * 40)
        print(f"⏱️  Runtime: {metrics.runtime_seconds:.2f} seconds")
        print(f"⚡ Energy: {metrics.energy_consumed:.6f} kWh")
        print(f"💧 Water: {metrics.water_usage:.2f} liters")
        print(f"🌍 CO₂: {metrics.carbon_emissions:.6f} kg")
        print(f"🔋 Carbon Intensity: {metrics.carbon_intensity:.1f} g CO₂/kWh")
        print(f"💧 Water Intensity: {metrics.water_intensity:.1f} L/kWh")
        print(f"🌱 Renewable Energy: {metrics.renewable_percentage:.1f}%")
        print(f"🏗️  Hardware: {metrics.hardware_type}")
        print(f"🌍 Region: {metrics.region} ({metrics.cloud_provider})")
        
        # Environmental context
        print("\n🌍 Environmental Context:")
        print("=" * 30)
        trees_needed = metrics.carbon_emissions * 0.06
        car_miles = metrics.carbon_emissions * 2.2
        bottles = metrics.water_usage / 0.5
        showers = metrics.water_usage / 65
        
        print(f"🌳 Trees needed to offset: {trees_needed:.2f}")
        print(f"🚗 Car miles equivalent: {car_miles:.2f} miles")
        print(f"🍼 Water bottles equivalent: {bottles:.1f} bottles")
        print(f"🚿 Shower equivalent: {showers:.2f} showers")
        
        # Regional comparison
        print("\n🌍 Regional Impact Comparison:")
        print("=" * 35)
        
        regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
        for region in regions:
            water_intensity = WaterIntensityCalculator.get_water_intensity("aws", region)
            water_usage = metrics.energy_consumed * water_intensity
            print(f"  {region}: {water_usage:.2f} L water")
        
        # Get enhanced summary
        summary = tracker.get_enhanced_summary()
        if summary:
            print(f"\n📈 Enhanced Summary:")
            print("=" * 25)
            print(f"Total runs: {summary['total_runs']}")
            print(f"Total energy: {summary['total_energy_kwh']:.6f} kWh")
            print(f"Total water: {summary['total_water_liters']:.2f} L")
            print(f"Total CO₂: {summary['total_emissions_kg']:.6f} kg")
            print(f"Energy efficiency: {summary['energy_efficiency']:.3f} kg CO₂/kWh")
    
    else:
        print("❌ Failed to get environmental metrics")
    
    print("\n🌿 Enhanced environmental tracking completed!")

if __name__ == "__main__":
    main()
