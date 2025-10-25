"""
Configuration settings for Green AI Carbon Tracker
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class CarbonTrackerConfig:
    """Configuration for carbon tracking and monitoring"""
    # API Keys
    electricity_map_api_key: Optional[str] = os.getenv('ELECTRICITY_MAP_API_KEY')
    watt_time_api_key: Optional[str] = os.getenv('WATT_TIME_API_KEY')
    openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
    
    # Database
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///green_ai.db')
    
    # Monitoring
    carbon_tracking_enabled: bool = os.getenv('CARBON_TRACKING_ENABLED', 'true').lower() == 'true'
    real_time_monitoring: bool = os.getenv('REAL_TIME_MONITORING', 'true').lower() == 'true'
    dashboard_refresh_interval: int = int(os.getenv('DASHBOARD_REFRESH_INTERVAL', '30'))
    
    # Cloud Providers
    aws_region: str = os.getenv('AWS_REGION', 'us-east-1')
    gcp_project: str = os.getenv('GOOGLE_CLOUD_PROJECT', '')
    azure_tenant: str = os.getenv('AZURE_TENANT_ID', '')
    
    # Notifications
    slack_webhook: Optional[str] = os.getenv('SLACK_WEBHOOK_URL')
    email_notifications: bool = os.getenv('EMAIL_NOTIFICATIONS', 'false').lower() == 'true'

@dataclass
class SustainabilityMetrics:
    """Key Performance Indicators for sustainability tracking"""
    
    # Carbon Metrics
    carbon_intensity_threshold: float = 200.0  # gCO2/kWh
    renewable_energy_target: float = 80.0      # % renewable energy
    
    # Efficiency Metrics
    energy_efficiency_target: float = 0.8     # Workload performance per unit energy
    carbon_savings_target: float = 30.0       # % reduction in carbon emissions
    
    # Reporting
    baseline_period_days: int = 30
    reporting_frequency: str = 'weekly'
    
    # Optimization
    scheduling_horizon_hours: int = 24
    prediction_confidence_threshold: float = 0.7

# Global configuration instance
config = CarbonTrackerConfig()
metrics = SustainabilityMetrics()
