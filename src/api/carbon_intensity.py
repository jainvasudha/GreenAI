"""
Real-time carbon intensity API integration
Supports ElectricityMap and WattTime APIs
"""
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json

from config.settings import config

logger = logging.getLogger(__name__)

@dataclass
class CarbonIntensityData:
    """Carbon intensity data from grid APIs"""
    timestamp: datetime
    carbon_intensity: float  # g CO2/kWh
    renewable_percentage: float  # %
    fossil_percentage: float  # %
    country_code: str
    region: str
    forecast_accuracy: float  # 0-1 confidence score

class CarbonIntensityAPI:
    """Real-time carbon intensity data integration"""
    
    def __init__(self):
        """Initialize carbon intensity API client"""
        self.electricity_map_key = config.electricity_map_api_key
        self.watt_time_key = config.watt_time_api_key
        self.current_provider = "electricity_map"  # Default provider
        
    def get_current_intensity(self, country_code: str = "US", 
                           region: str = "US-CA") -> CarbonIntensityData:
        """
        Get current carbon intensity for a region
        
        Args:
            country_code: ISO country code (e.g., "US", "GB", "DE")
            region: Region code (e.g., "US-CA", "GB", "DE")
            
        Returns:
            CarbonIntensityData object with current intensity
        """
        try:
            if self.electricity_map_key:
                return self._get_electricity_map_data(region)
            elif self.watt_time_key:
                return self._get_watt_time_data(region)
            else:
                # Fallback to estimated data
                return self._get_estimated_data(country_code)
                
        except Exception as e:
            logger.error(f"Failed to get carbon intensity data: {e}")
            return self._get_estimated_data(country_code)
    
    def _get_electricity_map_data(self, region: str) -> CarbonIntensityData:
        """Get data from ElectricityMap API"""
        try:
            # ElectricityMap API endpoint
            url = f"https://api.electricitymap.org/v3/carbon-intensity/latest"
            headers = {
                "auth-token": self.electricity_map_key,
                "Content-Type": "application/json"
            }
            params = {"zone": region}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return CarbonIntensityData(
                timestamp=datetime.fromisoformat(data['datetime'].replace('Z', '+00:00')),
                carbon_intensity=data['carbonIntensity'],
                renewable_percentage=data.get('renewablePercentage', 0),
                fossil_percentage=data.get('fossilPercentage', 100),
                country_code=region.split('-')[0],
                region=region,
                forecast_accuracy=data.get('forecastAccuracy', 0.8)
            )
            
        except Exception as e:
            logger.error(f"ElectricityMap API error: {e}")
            raise
    
    def _get_watt_time_data(self, region: str) -> CarbonIntensityData:
        """Get data from WattTime API"""
        try:
            # WattTime API endpoint
            url = "https://api.watttime.org/v3/index"
            headers = {
                "Authorization": f"Bearer {self.watt_time_key}",
                "Content-Type": "application/json"
            }
            params = {"ba": region}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return CarbonIntensityData(
                timestamp=datetime.fromisoformat(data['point_time'].replace('Z', '+00:00')),
                carbon_intensity=data['moer'],  # Marginal Operating Emissions Rate
                renewable_percentage=100 - data['moer'],  # Approximate
                fossil_percentage=data['moer'],
                country_code=region.split('-')[0],
                region=region,
                forecast_accuracy=0.7  # WattTime doesn't provide accuracy
            )
            
        except Exception as e:
            logger.error(f"WattTime API error: {e}")
            raise
    
    def _get_estimated_data(self, country_code: str) -> CarbonIntensityData:
        """Get estimated carbon intensity data when APIs are unavailable"""
        # Fallback estimates based on country averages
        country_estimates = {
            "US": {"intensity": 400, "renewable": 20},
            "GB": {"intensity": 250, "renewable": 40},
            "DE": {"intensity": 350, "renewable": 45},
            "FR": {"intensity": 50, "renewable": 80},
            "CA": {"intensity": 150, "renewable": 60},
            "AU": {"intensity": 800, "renewable": 25}
        }
        
        estimate = country_estimates.get(country_code, {"intensity": 400, "renewable": 30})
        
        return CarbonIntensityData(
            timestamp=datetime.now(),
            carbon_intensity=estimate["intensity"],
            renewable_percentage=estimate["renewable"],
            fossil_percentage=100 - estimate["renewable"],
            country_code=country_code,
            region=f"{country_code}-ESTIMATED",
            forecast_accuracy=0.3  # Low confidence for estimates
        )
    
    def get_forecast(self, region: str, hours_ahead: int = 24) -> List[CarbonIntensityData]:
        """
        Get carbon intensity forecast for the next N hours
        
        Args:
            region: Region code
            hours_ahead: Number of hours to forecast
            
        Returns:
            List of CarbonIntensityData objects
        """
        try:
            if self.electricity_map_key:
                return self._get_electricity_map_forecast(region, hours_ahead)
            else:
                # Generate simple forecast based on current data
                current = self.get_current_intensity(region.split('-')[0], region)
                return self._generate_simple_forecast(current, hours_ahead)
                
        except Exception as e:
            logger.error(f"Failed to get forecast: {e}")
            return []
    
    def _get_electricity_map_forecast(self, region: str, hours_ahead: int) -> List[CarbonIntensityData]:
        """Get forecast from ElectricityMap API"""
        try:
            url = f"https://api.electricitymap.org/v3/carbon-intensity/forecast"
            headers = {"auth-token": self.electricity_map_key}
            params = {"zone": region}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast_data = []
            
            for point in data['forecast'][:hours_ahead]:
                forecast_data.append(CarbonIntensityData(
                    timestamp=datetime.fromisoformat(point['datetime'].replace('Z', '+00:00')),
                    carbon_intensity=point['carbonIntensity'],
                    renewable_percentage=point.get('renewablePercentage', 0),
                    fossil_percentage=point.get('fossilPercentage', 100),
                    country_code=region.split('-')[0],
                    region=region,
                    forecast_accuracy=point.get('forecastAccuracy', 0.7)
                ))
            
            return forecast_data
            
        except Exception as e:
            logger.error(f"ElectricityMap forecast error: {e}")
            return []
    
    def _generate_simple_forecast(self, current: CarbonIntensityData, 
                                hours_ahead: int) -> List[CarbonIntensityData]:
        """Generate simple forecast based on current data"""
        import random
        
        forecast = []
        base_intensity = current.carbon_intensity
        
        for i in range(hours_ahead):
            # Simple variation: ±20% with some randomness
            variation = random.uniform(-0.2, 0.2)
            forecast_intensity = base_intensity * (1 + variation)
            
            forecast.append(CarbonIntensityData(
                timestamp=current.timestamp + timedelta(hours=i+1),
                carbon_intensity=max(0, forecast_intensity),
                renewable_percentage=current.renewable_percentage,
                fossil_percentage=current.fossil_percentage,
                country_code=current.country_code,
                region=current.region,
                forecast_accuracy=0.5  # Lower confidence for simple forecast
            ))
        
        return forecast
    
    def get_optimal_scheduling_windows(self, region: str, 
                                     hours_ahead: int = 24) -> List[Tuple[datetime, float]]:
        """
        Get optimal time windows for scheduling workloads
        
        Args:
            region: Region code
            hours_ahead: Hours to look ahead
            
        Returns:
            List of (datetime, carbon_intensity) tuples sorted by intensity
        """
        forecast = self.get_forecast(region, hours_ahead)
        
        if not forecast:
            return []
        
        # Sort by carbon intensity (lowest first)
        optimal_windows = [
            (point.timestamp, point.carbon_intensity) 
            for point in sorted(forecast, key=lambda x: x.carbon_intensity)
        ]
        
        return optimal_windows
    
    def is_green_energy_available(self, region: str, 
                                threshold: float = 200.0) -> bool:
        """
        Check if green energy is currently available
        
        Args:
            region: Region code
            threshold: Carbon intensity threshold (g CO2/kWh)
            
        Returns:
            True if green energy is available
        """
        current = self.get_current_intensity(region.split('-')[0], region)
        return current.carbon_intensity <= threshold

# Example usage
if __name__ == "__main__":
    api = CarbonIntensityAPI()
    
    # Get current carbon intensity
    current = api.get_current_intensity("US", "US-CA")
    print(f"Current carbon intensity: {current.carbon_intensity} g CO2/kWh")
    print(f"Renewable percentage: {current.renewable_percentage}%")
    
    # Get optimal scheduling windows
    optimal_windows = api.get_optimal_scheduling_windows("US-CA", 24)
    print(f"Optimal scheduling windows: {optimal_windows[:3]}")
    
    # Check if green energy is available
    is_green = api.is_green_energy_available("US-CA")
    print(f"Green energy available: {is_green}")
