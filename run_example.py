"""
Example usage of Green AI Carbon Tracker
Demonstrates key features and capabilities
"""
import time
import logging
from datetime import datetime
import numpy as np

# Import our modules
from src.monitoring.carbon_tracker import CarbonTracker, CarbonMetrics
from src.api.carbon_intensity import CarbonIntensityAPI
from src.recommendations.engine import RecommendationEngine
from src.analytics.baseline_comparison import BaselineComparison
from src.cloud.integration import CloudCarbonTracker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def demo_carbon_tracking():
    """Demonstrate carbon tracking functionality"""
    print("\n🌱 Carbon Tracking Demo")
    print("=" * 50)
    
    # Initialize tracker
    tracker = CarbonTracker("DemoProject")
    
    # Start tracking
    session_id = tracker.start_tracking("training", "pytorch")
    print(f"Started tracking session: {session_id}")
    
    # Simulate some AI workload
    print("Simulating AI training workload...")
    time.sleep(3)  # Simulate training time
    
    # Stop tracking and get metrics
    metrics = tracker.stop_tracking(session_id)
    
    print(f"\n📊 Carbon Metrics:")
    print(f"  Carbon Emissions: {metrics.carbon_emissions:.4f} kg CO2")
    print(f"  Energy Consumed: {metrics.energy_consumed:.4f} kWh")
    print(f"  Carbon Intensity: {metrics.carbon_intensity:.0f} g CO2/kWh")
    print(f"  Renewable Energy: {metrics.renewable_percentage:.0f}%")
    print(f"  CPU Utilization: {metrics.cpu_utilization:.0f}%")
    print(f"  GPU Utilization: {metrics.gpu_utilization:.0f}%")
    
    return metrics

def demo_carbon_intensity_api():
    """Demonstrate carbon intensity API functionality"""
    print("\n🌍 Carbon Intensity API Demo")
    print("=" * 50)
    
    # Initialize API
    api = CarbonIntensityAPI()
    
    # Get current carbon intensity
    try:
        current = api.get_current_intensity("US", "US-CA")
        print(f"Current Carbon Intensity: {current.carbon_intensity:.0f} g CO2/kWh")
        print(f"Renewable Energy: {current.renewable_percentage:.0f}%")
        print(f"Region: {current.region}")
        print(f"Timestamp: {current.timestamp}")
    except Exception as e:
        print(f"API Error (using fallback): {e}")
        current = api.get_current_intensity("US", "US-CA")  # Will use fallback
        print(f"Estimated Carbon Intensity: {current.carbon_intensity:.0f} g CO2/kWh")
    
    # Get optimal scheduling windows
    try:
        optimal_windows = api.get_optimal_scheduling_windows("US-CA", 24)
        if optimal_windows:
            print(f"\n⏰ Optimal Scheduling Windows (next 3):")
            for i, (time, intensity) in enumerate(optimal_windows[:3]):
                print(f"  {i+1}. {time.strftime('%H:%M')} - {intensity:.0f} g CO2/kWh")
        else:
            print("No optimal windows available (API not configured)")
    except Exception as e:
        print(f"Scheduling API Error: {e}")
    
    return current

def demo_recommendations(metrics):
    """Demonstrate recommendation engine"""
    print("\n💡 Recommendation Engine Demo")
    print("=" * 50)
    
    # Initialize recommendation engine
    engine = RecommendationEngine()
    
    # Generate recommendations
    workload_characteristics = {
        'framework': 'pytorch',
        'duration_hours': 4,
        'gpu_required': True,
        'batch_size': 32
    }
    
    recommendations = engine.generate_recommendations(metrics, workload_characteristics)
    
    print(f"Generated {len(recommendations)} recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.title}")
        print(f"   Description: {rec.description}")
        print(f"   Carbon Savings: {rec.carbon_savings_kg:.3f} kg CO2")
        print(f"   Energy Savings: {rec.energy_savings_kwh:.3f} kWh")
        print(f"   Confidence: {rec.confidence_score:.0%}")
        print(f"   Effort: {rec.implementation_effort.title()}")
        print(f"   Timeframe: {rec.timeframe.replace('_', ' ').title()}")
    
    # Create optimization plan
    plan = engine.create_optimization_plan(recommendations)
    print(f"\n📋 Optimization Plan:")
    print(f"  Total Carbon Savings: {plan.total_carbon_savings:.3f} kg CO2")
    print(f"  Total Energy Savings: {plan.total_energy_savings:.3f} kWh")
    print(f"  Estimated Timeline: {plan.estimated_timeline}")
    print(f"  Success Probability: {plan.success_probability:.0%}")
    
    return recommendations

def demo_baseline_comparison(metrics):
    """Demonstrate baseline comparison functionality"""
    print("\n📈 Baseline Comparison Demo")
    print("=" * 50)
    
    # Initialize comparison system
    comparison = BaselineComparison()
    
    # Set baseline scenario
    baseline = comparison.set_baseline(
        "baseline_001",
        "Original Training Setup",
        "Standard PyTorch training without optimizations",
        metrics,
        {"framework": "pytorch", "batch_size": 32, "epochs": 10}
    )
    print(f"Set baseline scenario: {baseline.name}")
    
    # Create optimized scenario (simulate 20% improvement)
    optimized_metrics = CarbonMetrics(
        timestamp=datetime.now(),
        energy_consumed=metrics.energy_consumed * 0.8,  # 20% reduction
        carbon_emissions=metrics.carbon_emissions * 0.8,  # 20% reduction
        carbon_intensity=metrics.carbon_intensity * 0.9,  # 10% improvement
        renewable_percentage=metrics.renewable_percentage + 10,  # 10% more renewable
        workload_type=metrics.workload_type,
        framework=metrics.framework,
        gpu_utilization=metrics.gpu_utilization + 10,  # Better utilization
        cpu_utilization=metrics.cpu_utilization + 5,
        memory_usage=metrics.memory_usage - 5  # Better memory usage
    )
    
    optimized = comparison.add_optimized_scenario(
        "optimized_001",
        "Optimized Training Setup",
        "PyTorch training with mixed precision and scheduling optimizations",
        optimized_metrics,
        ["mixed_precision", "optimal_scheduling", "batch_optimization"],
        "medium"
    )
    print(f"Added optimized scenario: {optimized.name}")
    
    # Compare scenarios
    result = comparison.compare_scenarios("baseline_001", "optimized_001")
    
    print(f"\n📊 Comparison Results:")
    print(f"  Carbon Reduction: {result.carbon_reduction_kg:.3f} kg CO2 ({result.carbon_reduction_percent:.1f}%)")
    print(f"  Energy Reduction: {result.energy_reduction_kwh:.3f} kWh ({result.energy_reduction_percent:.1f}%)")
    print(f"  Efficiency Improvement: {result.efficiency_improvement:.3f}")
    print(f"  Cost Savings: ${result.cost_savings_estimate:.2f}")
    print(f"  ROI Period: {result.roi_period_months:.1f} months")
    
    # Generate report
    report = comparison.generate_comparison_report(result)
    print(f"\n📋 Report Generated:")
    print(f"  Recommendations: {len(report['recommendations'])}")
    for rec in report['recommendations']:
        print(f"    - {rec}")
    
    return result

def demo_cloud_integration():
    """Demonstrate cloud integration (if available)"""
    print("\n☁️ Cloud Integration Demo")
    print("=" * 50)
    
    # Try AWS integration
    try:
        aws_tracker = CloudCarbonTracker("aws")
        instances = aws_tracker.get_instances()
        print(f"Found {len(instances)} AWS instances")
        
        if instances:
            for instance in instances[:3]:  # Show first 3
                print(f"  Instance: {instance.instance_id} ({instance.instance_type}) - {instance.status}")
        else:
            print("No AWS instances found (credentials not configured)")
            
    except Exception as e:
        print(f"AWS integration not available: {e}")
    
    # Try GCP integration
    try:
        gcp_tracker = CloudCarbonTracker("gcp")
        instances = gcp_tracker.get_instances()
        print(f"Found {len(instances)} GCP instances")
    except Exception as e:
        print(f"GCP integration not available: {e}")
    
    # Try Azure integration
    try:
        azure_tracker = CloudCarbonTracker("azure")
        instances = azure_tracker.get_instances()
        print(f"Found {len(instances)} Azure instances")
    except Exception as e:
        print(f"Azure integration not available: {e}")

def demo_summary():
    """Generate demo summary"""
    print("\n🎯 Demo Summary")
    print("=" * 50)
    print("The Green AI Carbon Tracker provides:")
    print("✅ Real-time carbon tracking for AI workloads")
    print("✅ Carbon intensity data from global electricity grids")
    print("✅ AI-powered optimization recommendations")
    print("✅ Baseline vs optimized scenario comparison")
    print("✅ Cloud provider integration (AWS, GCP, Azure)")
    print("✅ Comprehensive sustainability reporting")
    print("\n🚀 Next Steps:")
    print("1. Configure API keys in .env file")
    print("2. Run: streamlit run app.py")
    print("3. Start tracking your AI workloads!")
    print("4. Get personalized sustainability recommendations")

def main():
    """Run the complete demo"""
    print("🌱 Green AI Carbon Tracker - Demo")
    print("=" * 60)
    
    try:
        # Run all demos
        metrics = demo_carbon_tracking()
        current_intensity = demo_carbon_intensity_api()
        recommendations = demo_recommendations(metrics)
        comparison_result = demo_baseline_comparison(metrics)
        demo_cloud_integration()
        demo_summary()
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")
        print("This is expected if API keys are not configured.")
        print("Please check the documentation for setup instructions.")

if __name__ == "__main__":
    main()
