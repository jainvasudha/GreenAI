#!/usr/bin/env python3
"""
💰 NeuroGreen Cost & ROI Calculation Examples
===========================================

Example code snippets for cost calculation, ROI logic, dashboard integration, and export functionality.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Any
import json

# ============================================================================
# 1. COST CALCULATION LOGIC
# ============================================================================

@dataclass
class EnvironmentalMetrics:
    """Environmental impact metrics."""
    carbon_emissions: float  # kg CO2
    energy_consumed: float  # kWh
    water_usage: float      # liters
    runtime_hours: float   # hours

class CostCalculator:
    """Calculate costs for environmental impact."""
    
    def __init__(self):
        # Regional pricing data (USD)
        self.regional_pricing = {
            "us-west-2": {
                "electricity": 0.12,    # $/kWh (Oregon - low cost)
                "water": 0.003,         # $/L
                "carbon": 0.05          # $/kg CO2 (carbon tax/offset)
            },
            "us-east-1": {
                "electricity": 0.15,    # $/kWh (Virginia - medium cost)
                "water": 0.004,
                "carbon": 0.08
            },
            "eu-west-1": {
                "electricity": 0.18,    # $/kWh (Ireland - high cost)
                "water": 0.005,
                "carbon": 0.12
            },
            "ap-southeast-1": {
                "electricity": 0.14,    # $/kWh (Singapore)
                "water": 0.002,
                "carbon": 0.06
            }
        }
    
    def calculate_costs(self, metrics: EnvironmentalMetrics, region: str, custom_pricing: Dict = None) -> Dict[str, float]:
        """Calculate costs for environmental metrics."""
        pricing = custom_pricing or self.regional_pricing.get(region, self.regional_pricing["us-west-2"])
        
        # Calculate individual costs
        carbon_cost = metrics.carbon_emissions * pricing["carbon"]
        energy_cost = metrics.energy_consumed * pricing["electricity"]
        water_cost = metrics.water_usage * pricing["water"]
        total_cost = carbon_cost + energy_cost + water_cost
        
        return {
            "carbon_cost": carbon_cost,
            "energy_cost": energy_cost,
            "water_cost": water_cost,
            "total_cost": total_cost,
            "cost_per_hour": total_cost / metrics.runtime_hours if metrics.runtime_hours > 0 else 0
        }

# Example usage:
def example_cost_calculation():
    """Example of cost calculation."""
    print("=== COST CALCULATION EXAMPLE ===")
    
    # Sample environmental metrics
    metrics = EnvironmentalMetrics(
        carbon_emissions=0.5,    # 0.5 kg CO2
        energy_consumed=2.0,    # 2.0 kWh
        water_usage=3.0,         # 3.0 liters
        runtime_hours=1.5        # 1.5 hours
    )
    
    calculator = CostCalculator()
    
    # Calculate costs for different regions
    regions = ["us-west-2", "us-east-1", "eu-west-1", "ap-southeast-1"]
    region_names = ["Oregon", "Virginia", "Ireland", "Singapore"]
    
    print(f"Environmental Impact:")
    print(f"  Carbon: {metrics.carbon_emissions} kg CO2")
    print(f"  Energy: {metrics.energy_consumed} kWh")
    print(f"  Water: {metrics.water_usage} L")
    print(f"  Runtime: {metrics.runtime_hours} hours")
    print()
    
    for region, name in zip(regions, region_names):
        costs = calculator.calculate_costs(metrics, region)
        print(f"{name} ({region}):")
        print(f"  Carbon Cost: ${costs['carbon_cost']:.3f}")
        print(f"  Energy Cost: ${costs['energy_cost']:.3f}")
        print(f"  Water Cost: ${costs['water_cost']:.3f}")
        print(f"  Total Cost: ${costs['total_cost']:.3f}")
        print(f"  Cost/Hour: ${costs['cost_per_hour']:.3f}")
        print()

# ============================================================================
# 2. ROI ANALYSIS LOGIC
# ============================================================================

class ROIAnalyzer:
    """Analyze ROI for AI projects."""
    
    def __init__(self):
        # Value estimates by workload type
        self.workload_values = {
            "training": {
                "base_value_per_hour": 200,    # $/hour
                "complexity_multiplier": 1.5,   # For complex models
                "data_size_factor": 1.2        # For large datasets
            },
            "inference": {
                "base_value_per_hour": 50,
                "complexity_multiplier": 1.0,
                "data_size_factor": 1.0
            },
            "data_processing": {
                "base_value_per_hour": 100,
                "complexity_multiplier": 1.2,
                "data_size_factor": 1.1
            },
            "evaluation": {
                "base_value_per_hour": 80,
                "complexity_multiplier": 1.1,
                "data_size_factor": 1.0
            },
            "fine_tuning": {
                "base_value_per_hour": 150,
                "complexity_multiplier": 1.3,
                "data_size_factor": 1.1
            }
        }
    
    def calculate_project_value(self, workload_type: str, runtime_hours: float, 
                              complexity: str = "medium", data_size: str = "medium") -> float:
        """Calculate estimated project value."""
        if workload_type not in self.workload_values:
            workload_type = "training"  # Default
        
        base_config = self.workload_values[workload_type]
        base_value = base_config["base_value_per_hour"] * runtime_hours
        
        # Apply complexity multiplier
        complexity_multipliers = {"low": 0.8, "medium": 1.0, "high": 1.5}
        complexity_factor = complexity_multipliers.get(complexity, 1.0)
        
        # Apply data size factor
        data_size_factors = {"small": 0.8, "medium": 1.0, "large": 1.3}
        data_size_factor = data_size_factors.get(data_size, 1.0)
        
        total_value = base_value * complexity_factor * data_size_factor
        return total_value
    
    def calculate_roi_metrics(self, project_value: float, total_cost: float, 
                             runtime_hours: float) -> Dict[str, float]:
        """Calculate ROI metrics."""
        if total_cost == 0:
            return {
                "roi_ratio": float('inf'),
                "roi_percentage": float('inf'),
                "payback_period_hours": 0,
                "net_value": project_value
            }
        
        roi_ratio = project_value / total_cost
        roi_percentage = ((project_value - total_cost) / total_cost) * 100
        payback_period_hours = total_cost / (project_value / runtime_hours) if project_value > 0 else float('inf')
        net_value = project_value - total_cost
        
        return {
            "roi_ratio": roi_ratio,
            "roi_percentage": roi_percentage,
            "payback_period_hours": payback_period_hours,
            "net_value": net_value
        }

def example_roi_analysis():
    """Example of ROI analysis."""
    print("=== ROI ANALYSIS EXAMPLE ===")
    
    analyzer = ROIAnalyzer()
    
    # Sample project scenarios
    scenarios = [
        {
            "workload": "training",
            "runtime_hours": 8.0,
            "complexity": "high",
            "data_size": "large",
            "total_cost": 15.0
        },
        {
            "workload": "inference",
            "runtime_hours": 2.0,
            "complexity": "medium",
            "data_size": "medium",
            "total_cost": 3.0
        },
        {
            "workload": "data_processing",
            "runtime_hours": 4.0,
            "complexity": "medium",
            "data_size": "large",
            "total_cost": 8.0
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}: {scenario['workload'].title()}")
        print(f"  Runtime: {scenario['runtime_hours']} hours")
        print(f"  Complexity: {scenario['complexity']}")
        print(f"  Data Size: {scenario['data_size']}")
        print(f"  Total Cost: ${scenario['total_cost']:.2f}")
        
        # Calculate project value
        project_value = analyzer.calculate_project_value(
            scenario['workload'],
            scenario['runtime_hours'],
            scenario['complexity'],
            scenario['data_size']
        )
        
        # Calculate ROI metrics
        roi_metrics = analyzer.calculate_roi_metrics(
            project_value,
            scenario['total_cost'],
            scenario['runtime_hours']
        )
        
        print(f"  Project Value: ${project_value:.2f}")
        print(f"  ROI Ratio: {roi_metrics['roi_ratio']:.2f}")
        print(f"  ROI Percentage: {roi_metrics['roi_percentage']:.1f}%")
        print(f"  Payback Period: {roi_metrics['payback_period_hours']:.1f} hours")
        print(f"  Net Value: ${roi_metrics['net_value']:.2f}")
        print()

# ============================================================================
# 3. DASHBOARD INTEGRATION
# ============================================================================

def create_cost_dashboard_data(metrics_list: List[Dict]) -> Dict[str, Any]:
    """Create data for cost dashboard."""
    df = pd.DataFrame(metrics_list)
    
    # Calculate summary metrics
    total_carbon_cost = df['carbon_cost'].sum()
    total_energy_cost = df['energy_cost'].sum()
    total_water_cost = df['water_cost'].sum()
    total_cost = df['total_cost'].sum()
    
    # Calculate trends
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_costs = df.groupby('date')['total_cost'].sum()
    
    # Calculate efficiency metrics
    avg_cost_per_hour = df['total_cost'].sum() / df['runtime_hours'].sum()
    cost_efficiency = df['total_cost'] / df['runtime_hours']
    
    return {
        "summary": {
            "total_carbon_cost": total_carbon_cost,
            "total_energy_cost": total_energy_cost,
            "total_water_cost": total_water_cost,
            "total_cost": total_cost,
            "avg_cost_per_hour": avg_cost_per_hour
        },
        "trends": {
            "daily_costs": daily_costs.to_dict(),
            "cost_efficiency": cost_efficiency.tolist()
        },
        "breakdown": {
            "by_region": df.groupby('region')['total_cost'].sum().to_dict(),
            "by_workload": df.groupby('workload_type')['total_cost'].sum().to_dict(),
            "by_hardware": df.groupby('hardware_type')['total_cost'].sum().to_dict()
        }
    }

def create_roi_dashboard_data(metrics_list: List[Dict]) -> Dict[str, Any]:
    """Create data for ROI dashboard."""
    df = pd.DataFrame(metrics_list)
    
    # Calculate ROI summary
    total_value = df['project_value'].sum()
    total_cost = df['total_cost'].sum()
    avg_roi = df['roi_percentage'].mean()
    avg_sustainability = df['sustainability_score'].mean()
    
    # Calculate ROI trends
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_roi = df.groupby('date')['roi_percentage'].mean()
    
    # Calculate efficiency metrics
    value_per_hour = df['project_value'] / df['runtime_hours']
    cost_per_hour = df['total_cost'] / df['runtime_hours']
    
    return {
        "summary": {
            "total_value": total_value,
            "total_cost": total_cost,
            "net_value": total_value - total_cost,
            "avg_roi": avg_roi,
            "avg_sustainability": avg_sustainability
        },
        "trends": {
            "daily_roi": daily_roi.to_dict(),
            "value_per_hour": value_per_hour.tolist(),
            "cost_per_hour": cost_per_hour.tolist()
        },
        "breakdown": {
            "roi_by_workload": df.groupby('workload_type')['roi_percentage'].mean().to_dict(),
            "roi_by_region": df.groupby('region')['roi_percentage'].mean().to_dict(),
            "sustainability_by_hardware": df.groupby('hardware_type')['sustainability_score'].mean().to_dict()
        }
    }

# ============================================================================
# 4. EXPORT FUNCTIONALITY
# ============================================================================

def export_cost_roi_report(metrics_list: List[Dict], format: str = "csv") -> str:
    """Export cost and ROI report in various formats."""
    df = pd.DataFrame(metrics_list)
    
    if format == "csv":
        return df.to_csv(index=False)
    elif format == "json":
        return df.to_json(orient='records', date_format='iso')
    elif format == "excel":
        # For Excel export, you would use openpyxl
        return df.to_excel(index=False)
    else:
        return df.to_string(index=False)

def generate_summary_report(metrics_list: List[Dict]) -> Dict[str, Any]:
    """Generate comprehensive summary report."""
    df = pd.DataFrame(metrics_list)
    
    # Financial summary
    total_cost = df['total_cost'].sum()
    total_value = df['project_value'].sum()
    net_value = total_value - total_cost
    avg_roi = df['roi_percentage'].mean()
    
    # Environmental summary
    total_carbon = df['carbon_emissions'].sum()
    total_energy = df['energy_consumed'].sum()
    total_water = df['water_usage'].sum()
    avg_sustainability = df['sustainability_score'].mean()
    
    # Efficiency metrics
    total_runtime = df['runtime_hours'].sum()
    cost_per_hour = total_cost / total_runtime if total_runtime > 0 else 0
    value_per_hour = total_value / total_runtime if total_runtime > 0 else 0
    
    return {
        "financial": {
            "total_cost": total_cost,
            "total_value": total_value,
            "net_value": net_value,
            "avg_roi": avg_roi,
            "cost_per_hour": cost_per_hour,
            "value_per_hour": value_per_hour
        },
        "environmental": {
            "total_carbon": total_carbon,
            "total_energy": total_energy,
            "total_water": total_water,
            "avg_sustainability": avg_sustainability
        },
        "efficiency": {
            "total_runtime": total_runtime,
            "avg_cost_per_hour": cost_per_hour,
            "avg_value_per_hour": value_per_hour,
            "cost_efficiency_ratio": cost_per_hour / value_per_hour if value_per_hour > 0 else 0
        }
    }

# ============================================================================
# 5. EXAMPLE USAGE
# ============================================================================

def main():
    """Run all examples."""
    print("🧠 NeuroGreen Cost & ROI Analysis Examples")
    print("=" * 50)
    
    # Run cost calculation example
    example_cost_calculation()
    
    # Run ROI analysis example
    example_roi_analysis()
    
    # Example dashboard data
    print("=== DASHBOARD DATA EXAMPLE ===")
    
    # Sample metrics data
    sample_metrics = [
        {
            "timestamp": datetime.now() - timedelta(days=1),
            "workload_type": "training",
            "region": "us-west-2",
            "hardware_type": "apple_m2 + rtx_4090",
            "runtime_hours": 2.0,
            "carbon_emissions": 0.3,
            "energy_consumed": 1.5,
            "water_usage": 2.25,
            "carbon_cost": 0.015,
            "energy_cost": 0.18,
            "water_cost": 0.007,
            "total_cost": 0.202,
            "project_value": 400.0,
            "roi_percentage": 1980.2,
            "sustainability_score": 85.0
        },
        {
            "timestamp": datetime.now() - timedelta(hours=12),
            "workload_type": "inference",
            "region": "us-east-1",
            "hardware_type": "intel_i9 + rtx_4090",
            "runtime_hours": 0.5,
            "carbon_emissions": 0.1,
            "energy_consumed": 0.8,
            "water_usage": 1.2,
            "carbon_cost": 0.008,
            "energy_cost": 0.12,
            "water_cost": 0.005,
            "total_cost": 0.133,
            "project_value": 50.0,
            "roi_percentage": 37500.0,
            "sustainability_score": 90.0
        }
    ]
    
    # Create dashboard data
    cost_data = create_cost_dashboard_data(sample_metrics)
    roi_data = create_roi_dashboard_data(sample_metrics)
    
    print("Cost Dashboard Data:")
    print(f"  Total Cost: ${cost_data['summary']['total_cost']:.3f}")
    print(f"  Avg Cost/Hour: ${cost_data['summary']['avg_cost_per_hour']:.3f}")
    print()
    
    print("ROI Dashboard Data:")
    print(f"  Total Value: ${roi_data['summary']['total_value']:.2f}")
    print(f"  Net Value: ${roi_data['summary']['net_value']:.2f}")
    print(f"  Avg ROI: {roi_data['summary']['avg_roi']:.1f}%")
    print()
    
    # Generate summary report
    summary = generate_summary_report(sample_metrics)
    print("Summary Report:")
    print(f"  Financial: ${summary['financial']['net_value']:.2f} net value")
    print(f"  Environmental: {summary['environmental']['total_carbon']:.3f} kg CO2")
    print(f"  Efficiency: ${summary['efficiency']['avg_cost_per_hour']:.3f}/hour cost")
    print()
    
    # Export example
    print("=== EXPORT EXAMPLE ===")
    csv_export = export_cost_roi_report(sample_metrics, "csv")
    print("CSV Export (first 200 chars):")
    print(csv_export[:200] + "...")
    print()
    
    json_export = export_cost_roi_report(sample_metrics, "json")
    print("JSON Export (first 200 chars):")
    print(json_export[:200] + "...")

if __name__ == "__main__":
    main()
