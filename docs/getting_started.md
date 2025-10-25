# Getting Started with Green AI Carbon Tracker

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/greenai/carbon-tracker.git
cd carbon-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your API keys
nano .env
```

Required API keys:
- `ELECTRICITY_MAP_API_KEY`: Get from [ElectricityMap](https://electricitymap.org/)
- `WATT_TIME_API_KEY`: Get from [WattTime](https://www.watttime.org/)
- `OPENAI_API_KEY`: Get from [OpenAI](https://platform.openai.com/) (optional, for advanced chatbot)

### 3. Run the Application

```bash
# Start the Streamlit application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Basic Usage

### Starting Carbon Tracking

1. **Open the application** in your browser
2. **Configure your region** in the sidebar (e.g., "US-CA" for California)
3. **Click "Start Tracking"** to begin monitoring
4. **Run your AI workload** (training, inference, etc.)
5. **Click "Stop Tracking"** when finished

### Getting Recommendations

1. **Use the Chatbot tab** to ask questions like:
   - "How can I reduce my model's carbon footprint?"
   - "When is the best time to run my training?"
   - "What optimizations can I apply?"

2. **Check the Recommendations tab** for specific optimization suggestions

3. **View the Dashboard** for real-time carbon intensity and historical data

## Advanced Usage

### Programmatic Integration

```python
from src.monitoring.carbon_tracker import CarbonTracker
from src.api.carbon_intensity import CarbonIntensityAPI
from src.recommendations.engine import RecommendationEngine

# Initialize components
tracker = CarbonTracker("MyProject")
carbon_api = CarbonIntensityAPI()
recommendation_engine = RecommendationEngine()

# Start tracking
session_id = tracker.start_tracking("training", "pytorch")

# Your AI workload here
# ... training code ...

# Stop tracking and get metrics
metrics = tracker.stop_tracking(session_id)

# Get recommendations
recommendations = recommendation_engine.generate_recommendations(
    metrics, {"framework": "pytorch", "duration_hours": 4}
)

# Get optimal scheduling
optimal_windows = carbon_api.get_optimal_scheduling_windows("US-CA", 24)
```

### Cloud Integration

```python
from src.cloud.integration import CloudCarbonTracker

# Initialize AWS tracker
aws_tracker = CloudCarbonTracker("aws")

# Get instances and metrics
instances = aws_tracker.get_instances()
for instance in instances:
    metrics = aws_tracker.get_instance_metrics(instance.instance_id, 24)
    print(f"Instance {instance.instance_id}: {sum(m.carbon_emissions for m in metrics):.2f} kg CO2")
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ELECTRICITY_MAP_API_KEY` | ElectricityMap API key | None |
| `WATT_TIME_API_KEY` | WattTime API key | None |
| `OPENAI_API_KEY` | OpenAI API key for chatbot | None |
| `DATABASE_URL` | Database connection string | `sqlite:///green_ai.db` |
| `CARBON_TRACKING_ENABLED` | Enable carbon tracking | `true` |
| `REAL_TIME_MONITORING` | Enable real-time monitoring | `true` |
| `DASHBOARD_REFRESH_INTERVAL` | Dashboard refresh interval (seconds) | `30` |

### Sustainability Metrics Configuration

Edit `config/settings.py` to customize:

```python
@dataclass
class SustainabilityMetrics:
    # Carbon thresholds
    carbon_intensity_threshold: float = 200.0  # g CO2/kWh
    renewable_energy_target: float = 80.0      # % renewable
    
    # Efficiency targets
    energy_efficiency_target: float = 0.8     # Performance per unit energy
    carbon_savings_target: float = 30.0       # % reduction target
```

## API Integration

### ElectricityMap API

```python
from src.api.carbon_intensity import CarbonIntensityAPI

api = CarbonIntensityAPI()

# Get current carbon intensity
current = api.get_current_intensity("US", "US-CA")
print(f"Current intensity: {current.carbon_intensity} g CO2/kWh")

# Get 24-hour forecast
forecast = api.get_forecast("US-CA", 24)
for point in forecast:
    print(f"{point.timestamp}: {point.carbon_intensity} g CO2/kWh")
```

### WattTime API

```python
# WattTime provides marginal operating emissions rate (MOER)
# Lower MOER = cleaner energy
current = api.get_current_intensity("US", "US-CA")
if current.carbon_intensity < 200:  # Clean energy available
    print("Good time to run AI workloads!")
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: Failed to get carbon intensity data
   ```
   - Check your API keys in `.env`
   - Verify API key permissions
   - Check API rate limits

2. **CodeCarbon Import Error**
   ```
   ModuleNotFoundError: No module named 'codecarbon'
   ```
   - Install CodeCarbon: `pip install codecarbon`
   - Check Python version (requires 3.8+)

3. **Database Connection Error**
   ```
   Error: Failed to connect to database
   ```
   - Check `DATABASE_URL` in `.env`
   - Ensure database is accessible
   - Check permissions

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

1. **Slow API responses**
   - Check network connectivity
   - Verify API key limits
   - Consider caching responses

2. **High memory usage**
   - Reduce historical data retention
   - Optimize batch processing
   - Use data compression

## Best Practices

### Carbon Optimization

1. **Schedule during low-carbon hours**
   ```python
   # Get optimal scheduling windows
   optimal_windows = carbon_api.get_optimal_scheduling_windows("US-CA", 24)
   best_time, best_intensity = optimal_windows[0]
   ```

2. **Use efficient frameworks**
   ```python
   # PyTorch optimizations
   torch.backends.cudnn.benchmark = True
   torch.backends.cudnn.deterministic = False
   
   # Mixed precision training
   from torch.cuda.amp import autocast, GradScaler
   ```

3. **Monitor resource utilization**
   ```python
   # Check if resources are being used efficiently
   if metrics.cpu_utilization < 70:
       print("Consider increasing batch size or parallel processing")
   ```

### Data Management

1. **Regular data cleanup**
   ```python
   # Archive old data
   cutoff_date = datetime.now() - timedelta(days=90)
   old_metrics = [m for m in metrics_history if m.timestamp < cutoff_date]
   ```

2. **Backup important data**
   ```python
   # Export data for backup
   comparison.export_comparison_data("json")
   ```

### Monitoring

1. **Set up alerts**
   ```python
   # Alert when carbon intensity is high
   if current_intensity.carbon_intensity > 500:
       send_alert("High carbon intensity detected")
   ```

2. **Track efficiency trends**
   ```python
   # Monitor efficiency over time
   efficiency_scores = [tracker.calculate_efficiency_score(m) for m in metrics_history]
   ```

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/greenai/carbon-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/greenai/carbon-tracker/discussions)
- **Email**: support@greenai.com

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
