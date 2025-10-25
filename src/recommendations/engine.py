"""
AI-powered recommendation engine for optimal carbon-aware scheduling
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
import pandas as pd

from src.monitoring.carbon_tracker import CarbonMetrics
from src.api.carbon_intensity import CarbonIntensityData, CarbonIntensityAPI
from config.settings import metrics

logger = logging.getLogger(__name__)

class RecommendationType(Enum):
    """Types of recommendations"""
    SCHEDULE_OPTIMIZATION = "schedule_optimization"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    FRAMEWORK_SWITCH = "framework_switch"
    HARDWARE_OPTIMIZATION = "hardware_optimization"
    BATCH_PROCESSING = "batch_processing"

@dataclass
class Recommendation:
    """Individual recommendation with impact assessment"""
    type: RecommendationType
    title: str
    description: str
    carbon_savings_kg: float
    energy_savings_kwh: float
    confidence_score: float  # 0-1
    implementation_effort: str  # "low", "medium", "high"
    timeframe: str  # "immediate", "short_term", "long_term"
    prerequisites: List[str]
    code_example: Optional[str] = None

@dataclass
class OptimizationPlan:
    """Complete optimization plan with multiple recommendations"""
    plan_id: str
    total_carbon_savings: float
    total_energy_savings: float
    implementation_priority: List[Recommendation]
    estimated_timeline: str
    success_probability: float

class RecommendationEngine:
    """AI-powered recommendation engine for carbon optimization"""
    
    def __init__(self):
        """Initialize recommendation engine"""
        self.carbon_api = CarbonIntensityAPI()
        self.recommendation_history = []
        self.optimization_baselines = {}
        
    def generate_recommendations(self, 
                               current_metrics: CarbonMetrics,
                               workload_characteristics: Dict[str, Any],
                               user_preferences: Dict[str, Any] = None) -> List[Recommendation]:
        """
        Generate carbon optimization recommendations
        
        Args:
            current_metrics: Current carbon metrics
            workload_characteristics: Workload details (framework, duration, etc.)
            user_preferences: User preferences and constraints
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Schedule optimization recommendations
        schedule_recs = self._generate_schedule_recommendations(
            current_metrics, workload_characteristics
        )
        recommendations.extend(schedule_recs)
        
        # Resource efficiency recommendations
        resource_recs = self._generate_resource_recommendations(
            current_metrics, workload_characteristics
        )
        recommendations.extend(resource_recs)
        
        # Framework optimization recommendations
        framework_recs = self._generate_framework_recommendations(
            current_metrics, workload_characteristics
        )
        recommendations.extend(framework_recs)
        
        # Hardware optimization recommendations
        hardware_recs = self._generate_hardware_recommendations(
            current_metrics, workload_characteristics
        )
        recommendations.extend(hardware_recs)
        
        # Sort by carbon savings potential
        recommendations.sort(key=lambda x: x.carbon_savings_kg, reverse=True)
        
        return recommendations
    
    def _generate_schedule_recommendations(self, 
                                        current_metrics: CarbonMetrics,
                                        workload_characteristics: Dict) -> List[Recommendation]:
        """Generate scheduling optimization recommendations"""
        recommendations = []
        
        try:
            # Get current carbon intensity
            current_intensity = self.carbon_api.get_current_intensity()
            
            # Get optimal scheduling windows
            optimal_windows = self.carbon_api.get_optimal_scheduling_windows(
                current_intensity.region, 24
            )
            
            if optimal_windows:
                best_time, best_intensity = optimal_windows[0]
                carbon_savings = (current_metrics.carbon_intensity - best_intensity) * current_metrics.energy_consumed / 1000
                
                if carbon_savings > 0:
                    recommendations.append(Recommendation(
                        type=RecommendationType.SCHEDULE_OPTIMIZATION,
                        title="Schedule for Low Carbon Hours",
                        description=f"Reschedule workload to {best_time.strftime('%H:%M')} when carbon intensity is {best_intensity:.0f} g CO2/kWh",
                        carbon_savings_kg=carbon_savings,
                        energy_savings_kwh=0,
                        confidence_score=0.8,
                        implementation_effort="low",
                        timeframe="immediate",
                        prerequisites=["Flexible scheduling", "Workload can be delayed"],
                        code_example=self._get_scheduling_code_example(best_time)
                    ))
        
        except Exception as e:
            logger.error(f"Failed to generate schedule recommendations: {e}")
        
        return recommendations
    
    def _generate_resource_recommendations(self, 
                                         current_metrics: CarbonMetrics,
                                         workload_characteristics: Dict) -> List[Recommendation]:
        """Generate resource efficiency recommendations"""
        recommendations = []
        
        # CPU utilization optimization
        if current_metrics.cpu_utilization < 70:
            recommendations.append(Recommendation(
                type=RecommendationType.RESOURCE_EFFICIENCY,
                title="Optimize CPU Utilization",
                description="Increase CPU utilization to improve energy efficiency per computation",
                carbon_savings_kg=current_metrics.carbon_emissions * 0.15,
                energy_savings_kwh=current_metrics.energy_consumed * 0.15,
                confidence_score=0.7,
                implementation_effort="medium",
                timeframe="short_term",
                prerequisites=["Multi-threading capability", "Parallel processing support"],
                code_example=self._get_cpu_optimization_code()
            ))
        
        # Memory optimization
        if current_metrics.memory_usage > 80:
            recommendations.append(Recommendation(
                type=RecommendationType.RESOURCE_EFFICIENCY,
                title="Optimize Memory Usage",
                description="Reduce memory usage to lower energy consumption",
                carbon_savings_kg=current_metrics.carbon_emissions * 0.1,
                energy_savings_kwh=current_metrics.energy_consumed * 0.1,
                confidence_score=0.6,
                implementation_effort="medium",
                timeframe="short_term",
                prerequisites=["Memory profiling tools", "Code refactoring capability"],
                code_example=self._get_memory_optimization_code()
            ))
        
        return recommendations
    
    def _generate_framework_recommendations(self, 
                                         current_metrics: CarbonMetrics,
                                         workload_characteristics: Dict) -> List[Recommendation]:
        """Generate framework optimization recommendations"""
        recommendations = []
        
        framework = workload_characteristics.get('framework', 'unknown')
        
        # Framework-specific optimizations
        if framework.lower() == 'pytorch':
            recommendations.append(Recommendation(
                type=RecommendationType.FRAMEWORK_SWITCH,
                title="Enable PyTorch Optimizations",
                description="Use PyTorch's built-in optimizations for better energy efficiency",
                carbon_savings_kg=current_metrics.carbon_emissions * 0.2,
                energy_savings_kwh=current_metrics.energy_consumed * 0.2,
                confidence_score=0.8,
                implementation_effort="low",
                timeframe="immediate",
                prerequisites=["PyTorch 1.8+", "CUDA support"],
                code_example=self._get_pytorch_optimization_code()
            ))
        
        elif framework.lower() == 'tensorflow':
            recommendations.append(Recommendation(
                type=RecommendationType.FRAMEWORK_SWITCH,
                title="Enable TensorFlow Optimizations",
                description="Use TensorFlow's XLA compiler and mixed precision training",
                carbon_savings_kg=current_metrics.carbon_emissions * 0.25,
                energy_savings_kwh=current_metrics.energy_consumed * 0.25,
                confidence_score=0.8,
                implementation_effort="medium",
                timeframe="short_term",
                prerequisites=["TensorFlow 2.4+", "GPU support"],
                code_example=self._get_tensorflow_optimization_code()
            ))
        
        return recommendations
    
    def _generate_hardware_recommendations(self, 
                                        current_metrics: CarbonMetrics,
                                        workload_characteristics: Dict) -> List[Recommendation]:
        """Generate hardware optimization recommendations"""
        recommendations = []
        
        # GPU utilization optimization
        if current_metrics.gpu_utilization < 50:
            recommendations.append(Recommendation(
                type=RecommendationType.HARDWARE_OPTIMIZATION,
                title="Optimize GPU Utilization",
                description="Increase GPU utilization or consider CPU-only processing for small workloads",
                carbon_savings_kg=current_metrics.carbon_emissions * 0.3,
                energy_savings_kwh=current_metrics.energy_consumed * 0.3,
                confidence_score=0.6,
                implementation_effort="high",
                timeframe="long_term",
                prerequisites=["Hardware analysis", "Workload profiling"],
                code_example=self._get_gpu_optimization_code()
            ))
        
        return recommendations
    
    def create_optimization_plan(self, 
                               recommendations: List[Recommendation],
                               user_constraints: Dict[str, Any] = None) -> OptimizationPlan:
        """
        Create a comprehensive optimization plan
        
        Args:
            recommendations: List of recommendations
            user_constraints: User constraints and preferences
            
        Returns:
            OptimizationPlan with prioritized recommendations
        """
        # Filter recommendations based on constraints
        if user_constraints:
            max_effort = user_constraints.get('max_effort', 'high')
            max_timeframe = user_constraints.get('max_timeframe', 'long_term')
            
            effort_levels = {'low': 1, 'medium': 2, 'high': 3}
            timeframe_levels = {'immediate': 1, 'short_term': 2, 'long_term': 3}
            
            filtered_recs = [
                rec for rec in recommendations
                if (effort_levels.get(rec.implementation_effort, 3) <= effort_levels.get(max_effort, 3) and
                    timeframe_levels.get(rec.timeframe, 3) <= timeframe_levels.get(max_timeframe, 3))
            ]
        else:
            filtered_recs = recommendations
        
        # Sort by carbon savings and confidence
        prioritized_recs = sorted(
            filtered_recs,
            key=lambda x: (x.carbon_savings_kg * x.confidence_score),
            reverse=True
        )
        
        # Calculate total savings
        total_carbon_savings = sum(rec.carbon_savings_kg for rec in prioritized_recs)
        total_energy_savings = sum(rec.energy_savings_kwh for rec in prioritized_recs)
        
        # Estimate timeline
        timeframes = [rec.timeframe for rec in prioritized_recs]
        if 'immediate' in timeframes:
            timeline = "1-7 days"
        elif 'short_term' in timeframes:
            timeline = "1-4 weeks"
        else:
            timeline = "1-3 months"
        
        # Calculate success probability
        avg_confidence = np.mean([rec.confidence_score for rec in prioritized_recs])
        success_probability = min(0.95, avg_confidence * 0.8)
        
        plan_id = f"optimization_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return OptimizationPlan(
            plan_id=plan_id,
            total_carbon_savings=total_carbon_savings,
            total_energy_savings=total_energy_savings,
            implementation_priority=prioritized_recs,
            estimated_timeline=timeline,
            success_probability=success_probability
        )
    
    def _get_scheduling_code_example(self, optimal_time: datetime) -> str:
        """Get code example for scheduling optimization"""
        return f"""
# Schedule workload for optimal carbon intensity
import schedule
from datetime import datetime

def run_workload():
    # Your ML training/inference code here
    pass

# Schedule for optimal time: {optimal_time.strftime('%H:%M')}
schedule.every().day.at("{optimal_time.strftime('%H:%M')}").do(run_workload)

# Alternative: Use cron-like scheduling
# 0 {optimal_time.hour} * * * python your_script.py
"""
    
    def _get_cpu_optimization_code(self) -> str:
        """Get code example for CPU optimization"""
        return """
# CPU optimization for better energy efficiency
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

# Use all available CPU cores
num_cores = mp.cpu_count()

# Parallel processing example
with ThreadPoolExecutor(max_workers=num_cores) as executor:
    results = executor.map(your_function, data_chunks)

# For PyTorch: Enable CPU optimizations
torch.set_num_threads(num_cores)
"""
    
    def _get_memory_optimization_code(self) -> str:
        """Get code example for memory optimization"""
        return """
# Memory optimization techniques
import gc
import psutil

# Monitor memory usage
def monitor_memory():
    memory = psutil.virtual_memory()
    print(f"Memory usage: {memory.percent}%")
    return memory.percent < 80  # Alert if > 80%

# Clear unused variables
del large_variable
gc.collect()

# Use memory-efficient data types
import numpy as np
# Use float32 instead of float64 when possible
data = np.array(your_data, dtype=np.float32)
"""
    
    def _get_pytorch_optimization_code(self) -> str:
        """Get code example for PyTorch optimization"""
        return """
# PyTorch energy optimization
import torch
import torch.nn as nn

# Enable optimizations
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = False

# Use mixed precision training
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()

# Compile model for better performance (PyTorch 2.0+)
model = torch.compile(model)

# Use efficient data loaders
dataloader = torch.utils.data.DataLoader(
    dataset, batch_size=batch_size, 
    num_workers=4, pin_memory=True
)
"""
    
    def _get_tensorflow_optimization_code(self) -> str:
        """Get code example for TensorFlow optimization"""
        return """
# TensorFlow energy optimization
import tensorflow as tf

# Enable XLA compilation
tf.config.optimizer.set_jit(True)

# Use mixed precision
policy = tf.keras.mixed_precision.Policy('mixed_float16')
tf.keras.mixed_precision.set_global_policy(policy)

# Optimize for inference
model = tf.function(model, experimental_compile=True)

# Use efficient data pipeline
dataset = dataset.prefetch(tf.data.AUTOTUNE)
dataset = dataset.cache()
"""
    
    def _get_gpu_optimization_code(self) -> str:
        """Get code example for GPU optimization"""
        return """
# GPU optimization for energy efficiency
import torch

# Check if GPU is available and efficient for workload
if torch.cuda.is_available():
    gpu_memory = torch.cuda.get_device_properties(0).total_memory
    if workload_size < gpu_memory * 0.1:  # Small workload
        print("Consider CPU processing for small workloads")
    else:
        # Use GPU efficiently
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        
        # Enable GPU optimizations
        torch.backends.cudnn.benchmark = True
"""
    
    def track_recommendation_impact(self, 
                                 recommendation: Recommendation,
                                 before_metrics: CarbonMetrics,
                                 after_metrics: CarbonMetrics) -> Dict[str, float]:
        """
        Track the impact of implementing a recommendation
        
        Args:
            recommendation: The recommendation that was implemented
            before_metrics: Metrics before implementation
            after_metrics: Metrics after implementation
            
        Returns:
            Dictionary with impact metrics
        """
        carbon_reduction = before_metrics.carbon_emissions - after_metrics.carbon_emissions
        energy_reduction = before_metrics.energy_consumed - after_metrics.energy_consumed
        
        actual_vs_predicted = {
            'predicted_carbon_savings': recommendation.carbon_savings_kg,
            'actual_carbon_savings': carbon_reduction,
            'predicted_energy_savings': recommendation.energy_savings_kwh,
            'actual_energy_savings': energy_reduction,
            'accuracy_score': min(1.0, carbon_reduction / max(recommendation.carbon_savings_kg, 0.001))
        }
        
        # Store for learning
        self.recommendation_history.append({
            'recommendation': recommendation,
            'before_metrics': before_metrics,
            'after_metrics': after_metrics,
            'impact': actual_vs_predicted
        })
        
        return actual_vs_predicted

# Example usage
if __name__ == "__main__":
    engine = RecommendationEngine()
    
    # Example workload characteristics
    workload_chars = {
        'framework': 'pytorch',
        'duration_hours': 4,
        'gpu_required': True,
        'batch_size': 32
    }
    
    # Example current metrics
    from src.monitoring.carbon_tracker import CarbonMetrics
    current_metrics = CarbonMetrics(
        timestamp=datetime.now(),
        energy_consumed=2.5,
        carbon_emissions=1.2,
        carbon_intensity=480,
        renewable_percentage=25,
        workload_type='training',
        framework='pytorch',
        gpu_utilization=60,
        cpu_utilization=45,
        memory_usage=70
    )
    
    # Generate recommendations
    recommendations = engine.generate_recommendations(current_metrics, workload_chars)
    
    print(f"Generated {len(recommendations)} recommendations:")
    for rec in recommendations:
        print(f"- {rec.title}: {rec.carbon_savings_kg:.2f} kg CO2 savings")
    
    # Create optimization plan
    plan = engine.create_optimization_plan(recommendations)
    print(f"\nOptimization Plan: {plan.total_carbon_savings:.2f} kg CO2 total savings")
