"""
Cloud provider integration for carbon tracking and monitoring
Supports AWS, GCP, and Azure
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

# Cloud provider imports (conditional)
try:
    import boto3
    from botocore.exceptions import ClientError
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

try:
    from google.cloud import monitoring_v3
    from google.cloud.monitoring_v3 import query
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False

try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    from azure.identity import DefaultAzureCredential
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from config.settings import config

logger = logging.getLogger(__name__)

@dataclass
class CloudMetrics:
    """Cloud provider metrics for carbon tracking"""
    timestamp: datetime
    provider: str
    region: str
    instance_type: str
    cpu_utilization: float
    memory_utilization: float
    network_io: float
    disk_io: float
    energy_consumption: float  # Estimated kWh
    carbon_emissions: float    # Estimated kg CO2

@dataclass
class CloudInstance:
    """Cloud instance information"""
    instance_id: str
    instance_type: str
    region: str
    provider: str
    status: str
    launch_time: datetime
    tags: Dict[str, str]

class CloudCarbonTracker:
    """Carbon tracking for cloud providers"""
    
    def __init__(self, provider: str = "aws"):
        """
        Initialize cloud carbon tracker
        
        Args:
            provider: Cloud provider ("aws", "gcp", "azure")
        """
        self.provider = provider.lower()
        self.instances: List[CloudInstance] = []
        self.metrics_history: List[CloudMetrics] = []
        
        # Initialize provider-specific clients
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize cloud provider clients"""
        if self.provider == "aws" and AWS_AVAILABLE:
            try:
                self.ec2_client = boto3.client('ec2', region_name=config.aws_region)
                self.cloudwatch_client = boto3.client('cloudwatch', region_name=config.aws_region)
                logger.info("AWS clients initialized")
            except Exception as e:
                logger.error(f"Failed to initialize AWS clients: {e}")
                self.ec2_client = None
                self.cloudwatch_client = None
        
        elif self.provider == "gcp" and GCP_AVAILABLE:
            try:
                self.monitoring_client = monitoring_v3.MetricServiceClient()
                logger.info("GCP monitoring client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize GCP client: {e}")
                self.monitoring_client = None
        
        elif self.provider == "azure" and AZURE_AVAILABLE:
            try:
                self.credential = DefaultAzureCredential()
                logger.info("Azure credential initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Azure credential: {e}")
                self.credential = None
    
    def get_instances(self) -> List[CloudInstance]:
        """
        Get list of running instances
        
        Returns:
            List of CloudInstance objects
        """
        if self.provider == "aws":
            return self._get_aws_instances()
        elif self.provider == "gcp":
            return self._get_gcp_instances()
        elif self.provider == "azure":
            return self._get_azure_instances()
        else:
            logger.error(f"Unsupported provider: {self.provider}")
            return []
    
    def _get_aws_instances(self) -> List[CloudInstance]:
        """Get AWS EC2 instances"""
        if not self.ec2_client:
            return []
        
        try:
            response = self.ec2_client.describe_instances()
            instances = []
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] in ['running', 'pending']:
                        instances.append(CloudInstance(
                            instance_id=instance['InstanceId'],
                            instance_type=instance['InstanceType'],
                            region=instance['Placement']['AvailabilityZone'],
                            provider="aws",
                            status=instance['State']['Name'],
                            launch_time=instance['LaunchTime'],
                            tags={tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                        ))
            
            return instances
            
        except ClientError as e:
            logger.error(f"Failed to get AWS instances: {e}")
            return []
    
    def _get_gcp_instances(self) -> List[CloudInstance]:
        """Get GCP Compute Engine instances"""
        # This would require GCP API setup
        # For now, return empty list
        logger.warning("GCP instance retrieval not fully implemented")
        return []
    
    def _get_azure_instances(self) -> List[CloudInstance]:
        """Get Azure VM instances"""
        # This would require Azure API setup
        # For now, return empty list
        logger.warning("Azure instance retrieval not fully implemented")
        return []
    
    def get_instance_metrics(self, instance_id: str, hours: int = 24) -> List[CloudMetrics]:
        """
        Get metrics for a specific instance
        
        Args:
            instance_id: Instance identifier
            hours: Number of hours to retrieve metrics for
            
        Returns:
            List of CloudMetrics objects
        """
        if self.provider == "aws":
            return self._get_aws_metrics(instance_id, hours)
        elif self.provider == "gcp":
            return self._get_gcp_metrics(instance_id, hours)
        elif self.provider == "azure":
            return self._get_azure_metrics(instance_id, hours)
        else:
            return []
    
    def _get_aws_metrics(self, instance_id: str, hours: int) -> List[CloudMetrics]:
        """Get AWS CloudWatch metrics"""
        if not self.cloudwatch_client:
            return []
        
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)
            
            # Get CPU utilization
            cpu_response = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour
                Statistics=['Average']
            )
            
            # Get memory utilization (if available)
            memory_response = self.cloudwatch_client.get_metric_statistics(
                Namespace='CWAgent',
                MetricName='mem_used_percent',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            
            metrics = []
            for datapoint in cpu_response['Datapoints']:
                cpu_util = datapoint['Average']
                memory_util = 0.0  # Default if not available
                
                # Find corresponding memory data
                for mem_datapoint in memory_response['Datapoints']:
                    if mem_datapoint['Timestamp'] == datapoint['Timestamp']:
                        memory_util = mem_datapoint['Average']
                        break
                
                # Estimate energy consumption and carbon emissions
                energy_consumption = self._estimate_energy_consumption(
                    instance_id, cpu_util, memory_util
                )
                carbon_emissions = self._estimate_carbon_emissions(
                    energy_consumption, config.aws_region
                )
                
                metrics.append(CloudMetrics(
                    timestamp=datapoint['Timestamp'],
                    provider="aws",
                    region=config.aws_region,
                    instance_type=self._get_instance_type(instance_id),
                    cpu_utilization=cpu_util,
                    memory_utilization=memory_util,
                    network_io=0.0,  # Would need additional metrics
                    disk_io=0.0,     # Would need additional metrics
                    energy_consumption=energy_consumption,
                    carbon_emissions=carbon_emissions
                ))
            
            return metrics
            
        except ClientError as e:
            logger.error(f"Failed to get AWS metrics: {e}")
            return []
    
    def _get_gcp_metrics(self, instance_id: str, hours: int) -> List[CloudMetrics]:
        """Get GCP monitoring metrics"""
        # Implementation would use GCP Monitoring API
        logger.warning("GCP metrics retrieval not fully implemented")
        return []
    
    def _get_azure_metrics(self, instance_id: str, hours: int) -> List[CloudMetrics]:
        """Get Azure monitoring metrics"""
        # Implementation would use Azure Monitor API
        logger.warning("Azure metrics retrieval not fully implemented")
        return []
    
    def _estimate_energy_consumption(self, 
                                    instance_id: str,
                                    cpu_utilization: float,
                                    memory_utilization: float) -> float:
        """
        Estimate energy consumption based on instance type and utilization
        
        Args:
            instance_id: Instance identifier
            cpu_utilization: CPU utilization percentage
            memory_utilization: Memory utilization percentage
            
        Returns:
            Estimated energy consumption in kWh
        """
        # Get instance type
        instance_type = self._get_instance_type(instance_id)
        
        # Base power consumption by instance type (watts)
        power_consumption = {
            't2.micro': 10,
            't2.small': 20,
            't2.medium': 40,
            't2.large': 80,
            't2.xlarge': 160,
            't3.micro': 8,
            't3.small': 16,
            't3.medium': 32,
            't3.large': 64,
            'm5.large': 100,
            'm5.xlarge': 200,
            'm5.2xlarge': 400,
            'c5.large': 120,
            'c5.xlarge': 240,
            'p3.2xlarge': 800,  # GPU instance
            'p3.8xlarge': 3200, # GPU instance
        }
        
        base_power = power_consumption.get(instance_type, 100)  # Default 100W
        
        # Adjust based on utilization
        utilization_factor = (cpu_utilization + memory_utilization) / 200
        adjusted_power = base_power * (0.3 + 0.7 * utilization_factor)  # 30% base + 70% utilization
        
        # Convert to kWh (assuming 1 hour)
        energy_kwh = adjusted_power / 1000  # Convert watts to kW
        
        return energy_kwh
    
    def _estimate_carbon_emissions(self, energy_kwh: float, region: str) -> float:
        """
        Estimate carbon emissions based on energy consumption and region
        
        Args:
            energy_kwh: Energy consumption in kWh
            region: AWS region
            
        Returns:
            Estimated carbon emissions in kg CO2
        """
        # Carbon intensity by region (g CO2/kWh)
        region_carbon_intensity = {
            'us-east-1': 400,      # Virginia
            'us-west-2': 200,      # Oregon (more renewable)
            'us-west-1': 300,      # California
            'eu-west-1': 250,      # Ireland
            'eu-central-1': 350,   # Frankfurt
            'ap-southeast-1': 600, # Singapore
            'ap-northeast-1': 500, # Tokyo
        }
        
        carbon_intensity = region_carbon_intensity.get(region, 400)  # Default 400 g CO2/kWh
        
        # Convert to kg CO2
        carbon_emissions_kg = (energy_kwh * carbon_intensity) / 1000
        
        return carbon_emissions_kg
    
    def _get_instance_type(self, instance_id: str) -> str:
        """Get instance type for a given instance ID"""
        instances = self.get_instances()
        for instance in instances:
            if instance.instance_id == instance_id:
                return instance.instance_type
        return "unknown"
    
    def get_carbon_summary(self, hours: int = 24) -> Dict[str, float]:
        """
        Get carbon summary for all instances
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            Dictionary with carbon summary
        """
        instances = self.get_instances()
        total_emissions = 0.0
        total_energy = 0.0
        
        for instance in instances:
            metrics = self.get_instance_metrics(instance.instance_id, hours)
            for metric in metrics:
                total_emissions += metric.carbon_emissions
                total_energy += metric.energy_consumption
        
        return {
            "total_emissions_kg": total_emissions,
            "total_energy_kwh": total_energy,
            "instances_tracked": len(instances),
            "timeframe_hours": hours
        }
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get cloud-specific optimization recommendations
        
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        instances = self.get_instances()
        
        for instance in instances:
            metrics = self.get_instance_metrics(instance.instance_id, 24)
            if not metrics:
                continue
            
            avg_cpu = sum(m.cpu_utilization for m in metrics) / len(metrics)
            avg_memory = sum(m.memory_utilization for m in metrics) / len(metrics)
            
            # Low utilization recommendation
            if avg_cpu < 30:
                recommendations.append({
                    "instance_id": instance.instance_id,
                    "type": "right_sizing",
                    "title": "Consider Right-Sizing Instance",
                    "description": f"Instance {instance.instance_id} has low CPU utilization ({avg_cpu:.1f}%)",
                    "potential_savings": "30-50% energy reduction",
                    "action": f"Consider downgrading from {instance.instance_type}"
                })
            
            # High utilization recommendation
            if avg_cpu > 80:
                recommendations.append({
                    "instance_id": instance.instance_id,
                    "type": "scaling",
                    "title": "Consider Scaling Up",
                    "description": f"Instance {instance.instance_id} has high CPU utilization ({avg_cpu:.1f}%)",
                    "potential_savings": "Better performance, potential efficiency gains",
                    "action": f"Consider upgrading {instance.instance_type}"
                })
            
            # Memory optimization
            if avg_memory > 90:
                recommendations.append({
                    "instance_id": instance.instance_id,
                    "type": "memory_optimization",
                    "title": "Memory Usage Optimization",
                    "description": f"Instance {instance.instance_id} has high memory usage ({avg_memory:.1f}%)",
                    "potential_savings": "10-20% energy reduction",
                    "action": "Optimize application memory usage"
                })
        
        return recommendations

# Example usage
if __name__ == "__main__":
    # Initialize AWS tracker
    tracker = CloudCarbonTracker("aws")
    
    # Get instances
    instances = tracker.get_instances()
    print(f"Found {len(instances)} instances")
    
    for instance in instances:
        print(f"Instance: {instance.instance_id} ({instance.instance_type}) - {instance.status}")
    
    # Get carbon summary
    summary = tracker.get_carbon_summary()
    print(f"Carbon summary: {summary}")
    
    # Get recommendations
    recommendations = tracker.get_optimization_recommendations()
    print(f"Found {len(recommendations)} optimization recommendations")
