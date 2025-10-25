"""
Carbon baseline vs optimized scenario comparison and reporting
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import pandas as pd
import numpy as np
import json

from src.monitoring.carbon_tracker import CarbonMetrics
from config.settings import metrics

logger = logging.getLogger(__name__)

@dataclass
class BaselineScenario:
    """Baseline scenario for comparison"""
    scenario_id: str
    name: str
    description: str
    metrics: CarbonMetrics
    timestamp: datetime
    workload_characteristics: Dict[str, Any]

@dataclass
class OptimizationScenario:
    """Optimized scenario for comparison"""
    scenario_id: str
    name: str
    description: str
    metrics: CarbonMetrics
    timestamp: datetime
    optimizations_applied: List[str]
    implementation_effort: str

@dataclass
class ComparisonResult:
    """Result of baseline vs optimized comparison"""
    baseline: BaselineScenario
    optimized: OptimizationScenario
    carbon_reduction_kg: float
    carbon_reduction_percent: float
    energy_reduction_kwh: float
    energy_reduction_percent: float
    efficiency_improvement: float
    cost_savings_estimate: float
    roi_period_months: float
    environmental_impact: Dict[str, float]

class BaselineComparison:
    """Compare baseline vs optimized scenarios"""
    
    def __init__(self):
        """Initialize baseline comparison system"""
        self.baseline_scenarios: List[BaselineScenario] = []
        self.optimized_scenarios: List[OptimizationScenario] = []
        self.comparison_results: List[ComparisonResult] = []
        
    def set_baseline(self, 
                    scenario_id: str,
                    name: str,
                    description: str,
                    metrics: CarbonMetrics,
                    workload_characteristics: Dict[str, Any]) -> BaselineScenario:
        """
        Set a baseline scenario for comparison
        
        Args:
            scenario_id: Unique identifier for the scenario
            name: Human-readable name
            description: Description of the baseline scenario
            metrics: Carbon metrics for the baseline
            workload_characteristics: Characteristics of the workload
            
        Returns:
            BaselineScenario object
        """
        baseline = BaselineScenario(
            scenario_id=scenario_id,
            name=name,
            description=description,
            metrics=metrics,
            timestamp=datetime.now(),
            workload_characteristics=workload_characteristics
        )
        
        self.baseline_scenarios.append(baseline)
        logger.info(f"Set baseline scenario: {scenario_id}")
        
        return baseline
    
    def add_optimized_scenario(self,
                             scenario_id: str,
                             name: str,
                             description: str,
                             metrics: CarbonMetrics,
                             optimizations_applied: List[str],
                             implementation_effort: str = "medium") -> OptimizationScenario:
        """
        Add an optimized scenario for comparison
        
        Args:
            scenario_id: Unique identifier for the scenario
            name: Human-readable name
            description: Description of the optimized scenario
            metrics: Carbon metrics for the optimized scenario
            optimizations_applied: List of optimizations applied
            implementation_effort: Effort required to implement
            
        Returns:
            OptimizationScenario object
        """
        optimized = OptimizationScenario(
            scenario_id=scenario_id,
            name=name,
            description=description,
            metrics=metrics,
            timestamp=datetime.now(),
            optimizations_applied=optimizations_applied,
            implementation_effort=implementation_effort
        )
        
        self.optimized_scenarios.append(optimized)
        logger.info(f"Added optimized scenario: {scenario_id}")
        
        return optimized
    
    def compare_scenarios(self, 
                         baseline_id: str,
                         optimized_id: str,
                         electricity_cost_per_kwh: float = 0.12) -> ComparisonResult:
        """
        Compare baseline vs optimized scenario
        
        Args:
            baseline_id: ID of the baseline scenario
            optimized_id: ID of the optimized scenario
            electricity_cost_per_kwh: Cost of electricity per kWh
            
        Returns:
            ComparisonResult with detailed comparison
        """
        # Find scenarios
        baseline = next((s for s in self.baseline_scenarios if s.scenario_id == baseline_id), None)
        optimized = next((s for s in self.optimized_scenarios if s.scenario_id == optimized_id), None)
        
        if not baseline:
            raise ValueError(f"Baseline scenario {baseline_id} not found")
        if not optimized:
            raise ValueError(f"Optimized scenario {optimized_id} not found")
        
        # Calculate reductions
        carbon_reduction_kg = baseline.metrics.carbon_emissions - optimized.metrics.carbon_emissions
        carbon_reduction_percent = (carbon_reduction_kg / baseline.metrics.carbon_emissions) * 100
        
        energy_reduction_kwh = baseline.metrics.energy_consumed - optimized.metrics.energy_consumed
        energy_reduction_percent = (energy_reduction_kwh / baseline.metrics.energy_consumed) * 100
        
        # Calculate efficiency improvement
        baseline_efficiency = self._calculate_efficiency_score(baseline.metrics)
        optimized_efficiency = self._calculate_efficiency_score(optimized.metrics)
        efficiency_improvement = optimized_efficiency - baseline_efficiency
        
        # Calculate cost savings
        cost_savings_estimate = energy_reduction_kwh * electricity_cost_per_kwh
        
        # Estimate ROI period (simplified)
        implementation_cost = self._estimate_implementation_cost(optimized.implementation_effort)
        roi_period_months = implementation_cost / (cost_savings_estimate * 30) if cost_savings_estimate > 0 else float('inf')
        
        # Calculate environmental impact
        environmental_impact = self._calculate_environmental_impact(
            carbon_reduction_kg, energy_reduction_kwh
        )
        
        result = ComparisonResult(
            baseline=baseline,
            optimized=optimized,
            carbon_reduction_kg=carbon_reduction_kg,
            carbon_reduction_percent=carbon_reduction_percent,
            energy_reduction_kwh=energy_reduction_kwh,
            energy_reduction_percent=energy_reduction_percent,
            efficiency_improvement=efficiency_improvement,
            cost_savings_estimate=cost_savings_estimate,
            roi_period_months=roi_period_months,
            environmental_impact=environmental_impact
        )
        
        self.comparison_results.append(result)
        logger.info(f"Compared scenarios: {baseline_id} vs {optimized_id}")
        
        return result
    
    def _calculate_efficiency_score(self, metrics: CarbonMetrics) -> float:
        """Calculate efficiency score for metrics"""
        # Base efficiency on carbon intensity and resource utilization
        carbon_score = max(0, 1 - (metrics.carbon_intensity / 1000))
        utilization_score = (metrics.cpu_utilization + metrics.gpu_utilization) / 200
        
        return (carbon_score * 0.6 + utilization_score * 0.4)
    
    def _estimate_implementation_cost(self, effort: str) -> float:
        """Estimate implementation cost based on effort level"""
        cost_mapping = {
            "low": 1000,      # $1,000
            "medium": 5000,   # $5,000
            "high": 15000     # $15,000
        }
        return cost_mapping.get(effort, 5000)
    
    def _calculate_environmental_impact(self, 
                                      carbon_reduction_kg: float,
                                      energy_reduction_kwh: float) -> Dict[str, float]:
        """Calculate environmental impact metrics"""
        return {
            "trees_planted_equivalent": carbon_reduction_kg * 0.02,  # Rough estimate
            "car_miles_offset": carbon_reduction_kg * 2.5,          # kg CO2 to miles
            "coal_burned_avoided_kg": energy_reduction_kwh * 0.5,   # kWh to coal
            "renewable_energy_equivalent_kwh": energy_reduction_kwh
        }
    
    def generate_comparison_report(self, result: ComparisonResult) -> Dict[str, Any]:
        """
        Generate detailed comparison report
        
        Args:
            result: ComparisonResult to generate report for
            
        Returns:
            Dictionary with detailed report data
        """
        report = {
            "comparison_summary": {
                "baseline_name": result.baseline.name,
                "optimized_name": result.optimized.name,
                "carbon_reduction_kg": result.carbon_reduction_kg,
                "carbon_reduction_percent": result.carbon_reduction_percent,
                "energy_reduction_kwh": result.energy_reduction_kwh,
                "energy_reduction_percent": result.energy_reduction_percent,
                "efficiency_improvement": result.efficiency_improvement
            },
            "financial_impact": {
                "cost_savings_estimate": result.cost_savings_estimate,
                "roi_period_months": result.roi_period_months,
                "annual_savings_estimate": result.cost_savings_estimate * 365
            },
            "environmental_impact": result.environmental_impact,
            "optimizations_applied": result.optimized.optimizations_applied,
            "implementation_details": {
                "effort_level": result.optimized.implementation_effort,
                "baseline_timestamp": result.baseline.timestamp.isoformat(),
                "optimized_timestamp": result.optimized.timestamp.isoformat()
            },
            "recommendations": self._generate_recommendations(result)
        }
        
        return report
    
    def _generate_recommendations(self, result: ComparisonResult) -> List[str]:
        """Generate recommendations based on comparison results"""
        recommendations = []
        
        if result.carbon_reduction_percent > 20:
            recommendations.append("Excellent carbon reduction! Consider scaling these optimizations to other workloads.")
        elif result.carbon_reduction_percent > 10:
            recommendations.append("Good carbon reduction achieved. Look for additional optimization opportunities.")
        else:
            recommendations.append("Modest carbon reduction. Consider more aggressive optimization strategies.")
        
        if result.efficiency_improvement > 0.2:
            recommendations.append("Significant efficiency improvement achieved. Monitor for sustained performance.")
        
        if result.roi_period_months < 6:
            recommendations.append("Quick ROI achieved. Consider implementing similar optimizations across the organization.")
        elif result.roi_period_months < 12:
            recommendations.append("Reasonable ROI period. Evaluate long-term benefits before scaling.")
        else:
            recommendations.append("Long ROI period. Consider if environmental benefits justify the investment.")
        
        return recommendations
    
    def get_historical_comparisons(self, days: int = 30) -> List[ComparisonResult]:
        """
        Get comparison results from the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of ComparisonResult objects
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        return [
            result for result in self.comparison_results
            if result.baseline.timestamp >= cutoff_date
        ]
    
    def calculate_aggregate_savings(self, days: int = 30) -> Dict[str, float]:
        """
        Calculate aggregate savings across all comparisons
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dictionary with aggregate savings metrics
        """
        recent_results = self.get_historical_comparisons(days)
        
        if not recent_results:
            return {
                "total_carbon_savings_kg": 0.0,
                "total_energy_savings_kwh": 0.0,
                "total_cost_savings": 0.0,
                "average_carbon_reduction_percent": 0.0,
                "comparison_count": 0
            }
        
        total_carbon_savings = sum(result.carbon_reduction_kg for result in recent_results)
        total_energy_savings = sum(result.energy_reduction_kwh for result in recent_results)
        total_cost_savings = sum(result.cost_savings_estimate for result in recent_results)
        avg_carbon_reduction = np.mean([result.carbon_reduction_percent for result in recent_results])
        
        return {
            "total_carbon_savings_kg": total_carbon_savings,
            "total_energy_savings_kwh": total_energy_savings,
            "total_cost_savings": total_cost_savings,
            "average_carbon_reduction_percent": avg_carbon_reduction,
            "comparison_count": len(recent_results)
        }
    
    def export_comparison_data(self, format: str = "json") -> str:
        """
        Export comparison data in specified format
        
        Args:
            format: Export format ("json", "csv")
            
        Returns:
            Exported data as string
        """
        if format == "json":
            data = {
                "baseline_scenarios": [
                    {
                        "scenario_id": s.scenario_id,
                        "name": s.name,
                        "description": s.description,
                        "timestamp": s.timestamp.isoformat(),
                        "metrics": {
                            "carbon_emissions": s.metrics.carbon_emissions,
                            "energy_consumed": s.metrics.energy_consumed,
                            "carbon_intensity": s.metrics.carbon_intensity
                        }
                    } for s in self.baseline_scenarios
                ],
                "optimized_scenarios": [
                    {
                        "scenario_id": s.scenario_id,
                        "name": s.name,
                        "description": s.description,
                        "timestamp": s.timestamp.isoformat(),
                        "optimizations_applied": s.optimizations_applied,
                        "metrics": {
                            "carbon_emissions": s.metrics.carbon_emissions,
                            "energy_consumed": s.metrics.energy_consumed,
                            "carbon_intensity": s.metrics.carbon_intensity
                        }
                    } for s in self.optimized_scenarios
                ],
                "comparison_results": [
                    {
                        "baseline_id": r.baseline.scenario_id,
                        "optimized_id": r.optimized.scenario_id,
                        "carbon_reduction_kg": r.carbon_reduction_kg,
                        "carbon_reduction_percent": r.carbon_reduction_percent,
                        "energy_reduction_kwh": r.energy_reduction_kwh,
                        "cost_savings_estimate": r.cost_savings_estimate
                    } for r in self.comparison_results
                ]
            }
            return json.dumps(data, indent=2)
        
        elif format == "csv":
            # Create CSV data
            rows = []
            for result in self.comparison_results:
                rows.append({
                    "baseline_name": result.baseline.name,
                    "optimized_name": result.optimized.name,
                    "carbon_reduction_kg": result.carbon_reduction_kg,
                    "carbon_reduction_percent": result.carbon_reduction_percent,
                    "energy_reduction_kwh": result.energy_reduction_kwh,
                    "cost_savings_estimate": result.cost_savings_estimate,
                    "roi_period_months": result.roi_period_months
                })
            
            df = pd.DataFrame(rows)
            return df.to_csv(index=False)
        
        else:
            raise ValueError(f"Unsupported format: {format}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize comparison system
    comparison = BaselineComparison()
    
    # Create baseline scenario
    baseline_metrics = CarbonMetrics(
        timestamp=datetime.now(),
        energy_consumed=5.0,
        carbon_emissions=2.5,
        carbon_intensity=500,
        renewable_percentage=30,
        workload_type="training",
        framework="pytorch",
        gpu_utilization=60,
        cpu_utilization=50,
        memory_usage=70
    )
    
    baseline = comparison.set_baseline(
        "baseline_001",
        "Original Training Setup",
        "Standard PyTorch training without optimizations",
        baseline_metrics,
        {"framework": "pytorch", "batch_size": 32, "epochs": 10}
    )
    
    # Create optimized scenario
    optimized_metrics = CarbonMetrics(
        timestamp=datetime.now(),
        energy_consumed=3.5,
        carbon_emissions=1.4,
        carbon_intensity=400,
        renewable_percentage=40,
        workload_type="training",
        framework="pytorch",
        gpu_utilization=80,
        cpu_utilization=70,
        memory_usage=60
    )
    
    optimized = comparison.add_optimized_scenario(
        "optimized_001",
        "Optimized Training Setup",
        "PyTorch training with mixed precision and scheduling optimizations",
        optimized_metrics,
        ["mixed_precision", "optimal_scheduling", "batch_optimization"],
        "medium"
    )
    
    # Compare scenarios
    result = comparison.compare_scenarios("baseline_001", "optimized_001")
    
    print(f"Carbon reduction: {result.carbon_reduction_kg:.2f} kg CO2 ({result.carbon_reduction_percent:.1f}%)")
    print(f"Energy reduction: {result.energy_reduction_kwh:.2f} kWh ({result.energy_reduction_percent:.1f}%)")
    print(f"Cost savings: ${result.cost_savings_estimate:.2f}")
    
    # Generate report
    report = comparison.generate_comparison_report(result)
    print(f"Report generated with {len(report['recommendations'])} recommendations")
