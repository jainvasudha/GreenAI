# 🌱 Enhanced Environmental Features Guide

**Complete guide to energy consumption and water usage tracking in GreenAI**

---

## 📋 Overview

The enhanced GreenAI platform now tracks three key environmental metrics:
1. **Carbon Emissions** (kg CO₂) - Climate impact
2. **Energy Consumption** (kWh) - Resource usage
3. **Water Usage** (liters) - Water footprint

---

## ⚡ Energy Consumption Calculation

### How It Works
Energy consumption is calculated based on:
- **Hardware specifications** (CPU, GPU, Memory)
- **Utilization rates** during workload execution
- **Runtime duration** of the workload

### Formula
```
Energy (kWh) = (Total Power Consumption × Runtime) / 3600
```

### Hardware Power Consumption
| Component | Type | Power (Watts) |
|-----------|------|---------------|
| **CPU** | Apple M2 | 25W |
| | Intel i7 | 65W |
| | Intel i9 | 95W |
| | AMD Ryzen 7 | 65W |
| | AMD Ryzen 9 | 105W |
| **GPU** | RTX 3080 | 320W |
| | RTX 3090 | 350W |
| | RTX 4080 | 320W |
| | RTX 4090 | 450W |
| | A100 | 400W |
| **Memory** | 16GB DDR4 | 5W |
| | 32GB DDR4 | 10W |
| | 32GB DDR5 | 8W |

### Example Calculation
```
CPU: Apple M2 (25W) × 50% utilization = 12.5W
GPU: RTX 4090 (450W) × 80% utilization = 360W
Memory: 32GB DDR5 (8W) = 8W
Total: 380.5W for 3600 seconds = 0.38 kWh
```

---

## 💧 Water Usage Calculation

### How It Works
Water usage is calculated using:
- **Energy consumption** from the workload
- **Regional water intensity factors** (liters per kWh)
- **Cloud provider specific** data

### Formula
```
Water (L) = Energy (kWh) × Water Intensity Factor (L/kWh)
```

### Regional Water Intensity Factors

#### AWS Regions
| Region | Location | Water Intensity (L/kWh) |
|--------|----------|------------------------|
| us-east-1 | Virginia | 1.2 |
| us-west-2 | Oregon | 1.5 |
| us-west-1 | California | 1.3 |
| eu-west-1 | Ireland | 1.1 |
| ap-southeast-1 | Singapore | 1.8 |

#### Google Cloud Regions
| Region | Location | Water Intensity (L/kWh) |
|--------|----------|------------------------|
| us-central1 | Iowa | 1.4 |
| us-west1 | Oregon | 1.6 |
| europe-west1 | Belgium | 1.0 |
| asia-southeast1 | Singapore | 1.9 |

#### Azure Regions
| Region | Location | Water Intensity (L/kWh) |
|--------|----------|------------------------|
| eastus | Virginia | 1.3 |
| westus2 | Washington | 1.7 |
| westeurope | Netherlands | 1.1 |
| southeastasia | Singapore | 1.8 |

### Example Calculation
```
Energy: 0.38 kWh
Region: us-west-2 (Oregon)
Water Intensity: 1.5 L/kWh
Water Usage: 0.38 × 1.5 = 0.57 liters
```

---

## 🌍 Carbon Emissions Calculation

### How It Works
Carbon emissions are calculated using:
- **Energy consumption** from the workload
- **Regional carbon intensity** (g CO₂ per kWh)
- **Grid mix** of the region

### Formula
```
CO₂ (kg) = Energy (kWh) × Carbon Intensity (g/kWh) / 1000
```

### Regional Carbon Intensity

| Region | Carbon Intensity (g CO₂/kWh) | Renewable % |
|--------|------------------------------|-------------|
| us-east-1 | 300 | 30% |
| us-west-2 | 200 | 80% |
| us-west-1 | 250 | 60% |
| eu-west-1 | 250 | 70% |
| ap-southeast-1 | 500 | 20% |

### Example Calculation
```
Energy: 0.38 kWh
Region: us-west-2 (Oregon)
Carbon Intensity: 200 g CO₂/kWh
CO₂ Emissions: 0.38 × 200 / 1000 = 0.076 kg CO₂
```

---

## 🎯 Usage Examples

### Basic Usage
```python
from enhanced_carbon_tracker import EnhancedCarbonTracker

# Initialize tracker
tracker = EnhancedCarbonTracker(
    project_name="My ML Project",
    region="us-west-2",
    cloud_provider="aws"
)

# Set hardware specs
hardware_specs = {
    'cpu_type': 'apple_m2',
    'gpu_type': 'rtx_4090',
    'memory_type': 'ddr5_32gb',
    'cpu_utilization': 0.7,
    'gpu_utilization': 0.9,
    'memory_usage': 0.6
}

# Start tracking
session_id = tracker.start_tracking(
    workload_type="training",
    framework="pytorch",
    hardware_specs=hardware_specs
)

# Your ML code here...
# (training, inference, etc.)

# Stop tracking
metrics = tracker.stop_tracking()

# Access results
print(f"Energy: {metrics.energy_consumed:.6f} kWh")
print(f"Water: {metrics.water_usage:.2f} L")
print(f"CO₂: {metrics.carbon_emissions:.6f} kg")
```

### Streamlit Integration
```python
import streamlit as st
from enhanced_carbon_tracker import show_enhanced_dashboard

# Show enhanced dashboard
show_enhanced_dashboard()
```

### Multi-Run Tracking
```python
# Track multiple runs
for i in range(5):
    tracker.start_tracking(f"experiment_{i}", "pytorch")
    # ... your code ...
    metrics = tracker.stop_tracking()
    print(f"Run {i}: {metrics.energy_consumed:.6f} kWh")

# Get summary
summary = tracker.get_enhanced_summary()
print(f"Total energy: {summary['total_energy_kwh']:.6f} kWh")
print(f"Total water: {summary['total_water_liters']:.2f} L")
```

---

## 📊 Environmental Context

### Carbon Emissions Context
- **1 kg CO₂** ≈ **0.06 trees** needed to offset
- **1 kg CO₂** ≈ **2.2 miles** driven by car
- **1 kg CO₂** ≈ **0.5 kg** of coal burned

### Water Usage Context
- **1 liter** ≈ **2 standard 500ml bottles**
- **1 liter** ≈ **1/65th of an average shower** (65L)
- **1 liter** ≈ **0.26 gallons**

### Energy Context
- **1 kWh** ≈ **0.4 kg CO₂** (average grid)
- **1 kWh** ≈ **1.5 L water** (average data center)
- **1 kWh** ≈ **3.6 MJ** of energy

---

## 🎨 UI Components

### Enhanced Metric Cards
```python
from enhanced_carbon_tracker import create_enhanced_metric_card

# Create metric card with help text
card = create_enhanced_metric_card(
    title="Energy Consumption",
    value="0.38",
    unit="kWh",
    icon="⚡",
    color="#228B22",
    help_text="Total energy consumed during the workload"
)
```

### Visualizations
- **Energy vs Water scatter plots** by region
- **Time series analysis** of environmental impact
- **Regional comparison charts**
- **Hardware efficiency analysis**

---

## 🔧 Configuration

### Environment Variables
```bash
# Regional settings
DEFAULT_REGION=us-west-2
DEFAULT_CLOUD_PROVIDER=aws

# Hardware detection
AUTO_DETECT_HARDWARE=true
DEFAULT_CPU_TYPE=apple_m2
DEFAULT_GPU_TYPE=none

# Water intensity overrides
CUSTOM_WATER_INTENSITY=1.5
```

### Custom Water Intensity
```python
# Override water intensity for specific regions
WaterIntensityCalculator.WATER_INTENSITY_FACTORS['custom'] = {
    'my-region': 1.2,
    'default': 1.5
}
```

---

## 📈 Advanced Features

### Regional Optimization
```python
# Find most efficient region
regions = ["us-east-1", "us-west-2", "eu-west-1"]
best_region = None
lowest_impact = float('inf')

for region in regions:
    water_intensity = WaterIntensityCalculator.get_water_intensity("aws", region)
    carbon_intensity = tracker._get_carbon_intensity()
    
    total_impact = water_intensity + carbon_intensity
    if total_impact < lowest_impact:
        lowest_impact = total_impact
        best_region = region

print(f"Most efficient region: {best_region}")
```

### Hardware Optimization
```python
# Compare hardware configurations
configs = [
    {'cpu_type': 'apple_m2', 'gpu_type': 'none'},
    {'cpu_type': 'intel_i9', 'gpu_type': 'rtx_4090'},
    {'cpu_type': 'amd_ryzen9', 'gpu_type': 'rtx_4080'}
]

for config in configs:
    energy = EnergyCalculator.calculate_energy_consumption(3600, config)
    print(f"{config}: {energy:.6f} kWh")
```

### Export Enhanced Data
```python
# Export enhanced metrics
import pandas as pd

df = pd.DataFrame([asdict(metrics) for metrics in tracker.enhanced_metrics_history])
df.to_csv('enhanced_environmental_data.csv', index=False)
```

---

## 🧪 Testing

### Test Energy Calculation
```python
# Test energy calculation
hardware_specs = {
    'cpu_type': 'apple_m2',
    'gpu_type': 'rtx_4090',
    'memory_type': 'ddr5_32gb',
    'cpu_utilization': 0.5,
    'gpu_utilization': 0.8,
    'memory_usage': 0.6
}

energy = EnergyCalculator.calculate_energy_consumption(3600, hardware_specs)
print(f"Energy for 1 hour: {energy:.6f} kWh")
```

### Test Water Calculation
```python
# Test water calculation
energy = 0.5  # kWh
water = WaterIntensityCalculator.calculate_water_usage(energy, "aws", "us-west-2")
print(f"Water usage: {water:.2f} L")
```

### Test Regional Factors
```python
# Test regional factors
regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
for region in regions:
    intensity = WaterIntensityCalculator.get_water_intensity("aws", region)
    print(f"{region}: {intensity:.1f} L/kWh")
```

---

## 🚀 Deployment

### Streamlit App
```bash
# Run enhanced tracker
streamlit run enhanced_environmental_tracker.py
```

### Integration with Existing Apps
```python
# Add to existing carbon tracker
from enhanced_carbon_tracker import EnhancedCarbonTracker

# Replace existing tracker
tracker = EnhancedCarbonTracker("MyProject")
# ... rest of your code ...
```

### Docker Deployment
```dockerfile
# Add to Dockerfile
COPY enhanced_carbon_tracker.py .
COPY enhanced_environmental_tracker.py .

# Run enhanced app
CMD ["streamlit", "run", "enhanced_environmental_tracker.py"]
```

---

## 📚 References

### Research Sources
- **Water Usage**: "The Water Footprint of Data Centers" (2023)
- **Energy Consumption**: "AI and Climate Change" (MIT, 2023)
- **Carbon Intensity**: "Global Electricity Review" (Ember, 2023)

### Cloud Provider Data
- **AWS**: Sustainability reports and regional data
- **Google Cloud**: Environmental impact assessments
- **Azure**: Carbon and water usage transparency reports

### Standards
- **ISO 14064**: Greenhouse gas accounting
- **GHG Protocol**: Corporate accounting standards
- **PAS 2050**: Carbon footprint of products

---

## 🎯 Best Practices

### 1. Accurate Hardware Specs
- Use actual hardware specifications
- Monitor utilization rates
- Update specs when hardware changes

### 2. Regional Selection
- Choose regions with lower carbon intensity
- Consider renewable energy availability
- Factor in water intensity

### 3. Workload Optimization
- Batch processing to reduce overhead
- Use efficient algorithms
- Optimize for energy efficiency

### 4. Monitoring and Reporting
- Track trends over time
- Set environmental targets
- Report to stakeholders

---

**🌿 Making AI development more sustainable, one calculation at a time!**

*For questions or contributions, please refer to the main project documentation.*
