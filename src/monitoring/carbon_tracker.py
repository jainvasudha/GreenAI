"""
Carbon tracking and monitoring module using CodeCarbon
"""
import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import pandas as pd
import numpy as np

from codecarbon import EmissionsTracker
from codecarbon.core.units import Energy, Time

from config.settings import config, metrics

logger = logging.getLogger(__name__)

@dataclass
class CarbonMetrics:
    """Carbon emission metrics for a workload"""
    timestamp: datetime
    energy_consumed: float  # kWh
    carbon_emissions: float  # kg CO2
    carbon_intensity: float  # g CO2/kWh
    renewable_percentage: float  # %
    workload_type: str
    framework: str
    gpu_utilization: float
    cpu_utilization: float
    memory_usage: float

class CarbonTracker:
    """Main carbon tracking class for AI workloads"""
    
    def __init__(self, project_name: str = "GreenAI", 
                 tracking_mode: str = "process"):
        """
        Initialize carbon tracker
        
        Args:
            project_name: Name of the project being tracked
            tracking_mode: Mode of tracking ('process', 'machine', 'cloud')
        """
        self.project_name = project_name
        self.tracking_mode = tracking_mode
        self.tracker = None
        self.metrics_history: List[CarbonMetrics] = []
        self.baseline_metrics: Optional[CarbonMetrics] = None
        self.start_time: Optional[datetime] = None
        self.session_id: Optional[str] = None
        self.is_tracking: bool = False
        
        # Initialize CodeCarbon tracker
        self._setup_tracker()
        
    def _setup_tracker(self):
        """Setup CodeCarbon tracker with configuration"""
        try:
            self.tracker = EmissionsTracker(
                project_name=self.project_name,
                tracking_mode=self.tracking_mode,
                log_level="INFO"
            )
            logger.info(f"Carbon tracker initialized for project: {self.project_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize carbon tracker: {e}")
            raise
    
    def start_tracking(self, workload_type: str = "training", 
                      framework: str = "pytorch") -> str:
        """
        Start tracking carbon emissions for a workload
        
        Args:
            workload_type: Type of workload ('training', 'inference', 'fine-tuning')
            framework: ML framework being used
            
        Returns:
            Tracking session ID
        """
        if not self.tracker:
            self._setup_tracker()
            
        session_id = f"{workload_type}_{framework}_{int(time.time())}"
        
        try:
            self.tracker.start()
            self.start_time = datetime.now()
            self.session_id = session_id
            self.is_tracking = True
            logger.info(f"Started carbon tracking for session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to start carbon tracking: {e}")
            raise
    
    def stop_tracking(self, session_id: str = None) -> CarbonMetrics:
        """
        Stop tracking and return carbon metrics
        
        Args:
            session_id: Session ID to stop tracking (optional)
            
        Returns:
            CarbonMetrics object with emission data
        """
        if not self.is_tracking:
            logger.warning("No active tracking to stop")
            return None
            
        try:
            # Stop CodeCarbon tracker
            emissions_data = self.tracker.stop()
            
            # Get system metrics
            system_metrics = self._get_system_metrics()
            
            # Create CarbonMetrics object
            # Handle the case where emissions_data might be a float or dict
            if hasattr(emissions_data, 'emissions'):
                emissions = emissions_data.emissions
                carbon_intensity = getattr(emissions_data, 'carbon_intensity', 0.0)
                renewable_percentage = getattr(emissions_data, 'renewable_percentage', 0.0)
            else:
                # If emissions_data is just a number
                emissions = float(emissions_data) if emissions_data else 0.0
                carbon_intensity = 0.0
                renewable_percentage = 0.0
            
            # Use current session_id if not provided
            if session_id is None:
                session_id = self.session_id or "unknown"
            
            carbon_metrics = CarbonMetrics(
                timestamp=datetime.now(),
                energy_consumed=emissions,
                carbon_emissions=emissions,
                carbon_intensity=carbon_intensity,
                renewable_percentage=renewable_percentage,
                workload_type=session_id.split('_')[0] if '_' in session_id else "unknown",
                framework=session_id.split('_')[1] if '_' in session_id else "unknown",
                gpu_utilization=system_metrics['gpu_utilization'],
                cpu_utilization=system_metrics['cpu_utilization'],
                memory_usage=system_metrics['memory_usage']
            )
            
            # Store metrics
            self.metrics_history.append(carbon_metrics)
            
            # Reset tracking state
            self.is_tracking = False
            self.start_time = None
            self.session_id = None
            
            logger.info(f"Stopped carbon tracking for session: {session_id}")
            logger.info(f"Total emissions: {carbon_metrics.carbon_emissions:.4f} kg CO2")
            
            return carbon_metrics
            
        except Exception as e:
            logger.error(f"Failed to stop carbon tracking: {e}")
            raise
    
    def _get_system_metrics(self) -> Dict[str, float]:
        """Get current system resource utilization metrics"""
        try:
            # CPU utilization
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # GPU utilization (if available)
            gpu_utilization = self._get_gpu_utilization()
            
            return {
                'cpu_utilization': cpu_percent,
                'memory_usage': memory_percent,
                'gpu_utilization': gpu_utilization
            }
            
        except Exception as e:
            logger.warning(f"Failed to get system metrics: {e}")
            return {
                'cpu_utilization': 0.0,
                'memory_usage': 0.0,
                'gpu_utilization': 0.0
            }
    
    def _get_gpu_utilization(self) -> float:
        """Get GPU utilization percentage"""
        try:
            # This would integrate with nvidia-ml-py or similar
            # For now, return a placeholder
            return 0.0
        except:
            return 0.0
    
    def get_runtime_seconds(self) -> float:
        """Get the current runtime in seconds"""
        if self.start_time and self.is_tracking:
            return (datetime.now() - self.start_time).total_seconds()
        return 0.0
    
    def get_current_status(self) -> Dict:
        """Get current tracking status"""
        return {
            'is_tracking': self.is_tracking,
            'start_time': self.start_time,
            'session_id': self.session_id,
            'runtime_seconds': self.get_runtime_seconds(),
            'project_name': self.project_name
        }
    
    def get_carbon_summary(self, hours: int = 24) -> Dict:
        """
        Get carbon emission summary for the last N hours
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            Dictionary with carbon summary statistics
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return {
                'total_emissions': 0.0,
                'average_intensity': 0.0,
                'total_energy': 0.0,
                'renewable_percentage': 0.0,
                'workload_count': 0
            }
        
        total_emissions = sum(m.carbon_emissions for m in recent_metrics)
        total_energy = sum(m.energy_consumed for m in recent_metrics)
        avg_intensity = np.mean([m.carbon_intensity for m in recent_metrics])
        avg_renewable = np.mean([m.renewable_percentage for m in recent_metrics])
        
        return {
            'total_emissions': total_emissions,
            'average_intensity': avg_intensity,
            'total_energy': total_energy,
            'renewable_percentage': avg_renewable,
            'workload_count': len(recent_metrics),
            'timeframe_hours': hours
        }
    
    def calculate_efficiency_score(self, workload_metrics: CarbonMetrics) -> float:
        """
        Calculate energy efficiency score for a workload
        
        Args:
            workload_metrics: CarbonMetrics object
            
        Returns:
            Efficiency score (0-1, higher is better)
        """
        # Base efficiency on carbon intensity and resource utilization
        carbon_score = max(0, 1 - (workload_metrics.carbon_intensity / 1000))
        utilization_score = (workload_metrics.cpu_utilization + 
                           workload_metrics.gpu_utilization) / 200
        
        # Weighted efficiency score
        efficiency_score = (carbon_score * 0.6 + utilization_score * 0.4)
        return min(1.0, max(0.0, efficiency_score))
    
    def set_baseline(self, baseline_metrics: CarbonMetrics):
        """Set baseline metrics for comparison"""
        self.baseline_metrics = baseline_metrics
        logger.info("Baseline metrics set for carbon efficiency comparison")
    
    def compare_to_baseline(self, current_metrics: CarbonMetrics) -> Dict:
        """
        Compare current metrics to baseline
        
        Args:
            current_metrics: Current workload metrics
            
        Returns:
            Dictionary with comparison results
        """
        if not self.baseline_metrics:
            return {'error': 'No baseline metrics set'}
        
        carbon_improvement = (
            (self.baseline_metrics.carbon_emissions - current_metrics.carbon_emissions) /
            self.baseline_metrics.carbon_emissions * 100
        )
        
        energy_improvement = (
            (self.baseline_metrics.energy_consumed - current_metrics.energy_consumed) /
            self.baseline_metrics.energy_consumed * 100
        )
        
        return {
            'carbon_improvement_percent': carbon_improvement,
            'energy_improvement_percent': energy_improvement,
            'baseline_emissions': self.baseline_metrics.carbon_emissions,
            'current_emissions': current_metrics.carbon_emissions,
            'improvement_achieved': carbon_improvement > 0
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize tracker
    tracker = CarbonTracker("TestProject")
    
    # Start tracking a training session
    session_id = tracker.start_tracking("training", "pytorch")
    
    # Simulate some work
    time.sleep(2)
    
    # Stop tracking and get metrics
    metrics = tracker.stop_tracking(session_id)
    print(f"Carbon emissions: {metrics.carbon_emissions:.4f} kg CO2")
    print(f"Energy consumed: {metrics.energy_consumed:.4f} kWh")
    
    # Get summary
    summary = tracker.get_carbon_summary()
    print(f"24h summary: {summary}")
