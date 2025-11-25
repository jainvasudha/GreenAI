# 🧠 NeuroGreen - AI-Powered Environmental Intelligence Platform

**A comprehensive sustainability platform for AI development with environmental tracking, multi-user support, and cloud deployment capabilities.**

---

## 🎯 Project Overview

NeuroGreen is an environmental monitoring platform that tracks carbon emissions, energy consumption, and water usage for AI workloads. It provides real-time monitoring, interactive visualizations, multi-user collaboration, and cloud deployment capabilities.

### Key Features
- ✅ **Environmental Tracking** - Carbon emissions, energy consumption, water usage
- ✅ **Interactive Visualizations** - Real-time graphs and charts
- ✅ **AI-Powered Recommendations** - Intelligent analysis and optimization suggestions
- ✅ **Multi-User Platform** - User authentication, organizations, team collaboration
- ✅ **Cloud Deployment Ready** - Docker, Heroku, AWS, Google Cloud, Azure
- ✅ **Real-time Monitoring** - Live tracking during AI workloads
- ✅ **Regional Analysis** - Environmental impact by geographic region
- ✅ **Export & Notifications** - CSV, PDF, Excel exports with email/Slack integration

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose (for multi-user platform)
- PostgreSQL (for multi-user platform)
- Redis (for multi-user platform)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GreenAI
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

### Running the Application

#### Option 1: Basic Application (Recommended for Development)
```bash
streamlit run app.py
```
Access at: http://localhost:8501

#### Option 2: Multi-User Platform (Production)
```bash
# Start with Docker Compose
docker-compose up -d

# Or run locally (requires PostgreSQL and Redis)
streamlit run app.py
```
Access at: http://localhost:8501

---

## 📊 Features

### Environmental Tracking
- **Carbon Emissions** - Real-time CO₂ monitoring with regional carbon intensity factors
- **Energy Consumption** - Hardware-specific power models and utilization-based calculations
- **Water Usage** - Regional water intensity factors and cloud provider specific data
- **Interactive Visualizations** - Real-time charts and graphs with tabbed interface

### AI-Powered Recommendations
- **Intelligent Analysis** - Behavior pattern recognition and efficiency optimization
- **LLM Chat Interface** - Natural language queries about environmental optimization
- **Smart Recommendations** - Prioritized suggestions with impact estimation

### Multi-User Platform
- **User Authentication** - Email/password and OAuth (Google, GitHub)
- **Team Collaboration** - Organization management with role-based access control
- **Project Management** - Shared workspaces and project history

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Workloads  │───▶│ Enhanced Monitor │───▶│ Multi-User      │
│  (PyTorch/TF)   │    │ (Carbon+Energy+  │    │ Platform        │
│                 │    │  Water Tracking)  │    │ (Auth+Teams)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ Regional Factors │    │ Interactive     │
                       │ (Water Intensity │    │ Visualizations  │
                       │  Carbon Grid)    │    │ (Tabs+Charts)   │
                       └──────────────────┘    └─────────────────┘
```

---

## 📁 Project Structure

```
GreenAI/
├── app.py                 # Main Streamlit application
├── src/                   # Core source code
│   ├── monitoring/        # Carbon tracking modules
│   ├── api/               # API integrations
│   ├── recommendations/   # AI recommendation engine
│   ├── analytics/         # Analytics and comparison
│   └── cloud/             # Cloud provider integrations
├── config/                # Configuration files
│   └── settings.py        # Application settings
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── init.sql               # Database schema
└── README.md              # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `env.example`:

```bash
# API Keys
ELECTRICITY_MAP_API_KEY=your_key_here
WATT_TIME_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Cloud Providers
AWS_REGION=us-east-1
GOOGLE_CLOUD_PROJECT=your-project-id

# Notifications
SLACK_WEBHOOK_URL=your_webhook_url
EMAIL_NOTIFICATIONS=false
```

---

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
```

### Production
```bash
docker build -t greenai .
docker run -p 8501:8501 greenai
```

---

## 📈 Usage Examples

### Basic Carbon Tracking
```python
from src.monitoring.carbon_tracker import CarbonTracker

tracker = CarbonTracker("My AI Project")
tracker.start_tracking("training", "pytorch")

# Your ML code here...

metrics = tracker.stop_tracking()
print(f"CO₂: {metrics.carbon_emissions:.6f} kg")
```

### Enhanced Tracking with Energy and Water
```python
from src.monitoring.carbon_tracker import CarbonTracker

tracker = CarbonTracker(
    project_name="My Project",
    region="us-west-2",
    cloud_provider="aws"
)

hardware_specs = {
    'cpu_type': 'apple_m2',
    'gpu_type': 'rtx_4090',
    'cpu_utilization': 0.7,
    'gpu_utilization': 0.9
}

session_id = tracker.start_tracking(
    workload_type="training",
    framework="pytorch",
    hardware_specs=hardware_specs
)

# Your ML code here...

metrics = tracker.stop_tracking()
print(f"Energy: {metrics.energy_consumed:.6f} kWh")
print(f"Water: {metrics.water_usage:.2f} L")
print(f"CO₂: {metrics.carbon_emissions:.6f} kg")
```

---

## ☁️ Cloud Deployment

### Heroku
```bash
heroku create greenai-app
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
git push heroku main
```

### AWS (ECS)
```bash
aws ecs create-cluster --cluster-name greenai-cluster
aws ecs create-service --cluster greenai-cluster --service-name greenai-service
```

### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/your-project/greenai
gcloud run deploy greenai --image gcr.io/your-project/greenai
```

---

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src tests/
```

---

## 📚 Documentation

- [Getting Started](docs/getting_started.md)
- [Architecture](docs/architecture.md)
- [Sustainability Verification](docs/sustainability_verification.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌿 Environmental Impact

NeuroGreen enables:
- **Accurate tracking** of carbon, energy, and water footprints
- **Regional optimization** for environmental efficiency
- **Hardware efficiency** analysis and recommendations
- **Comprehensive reporting** for sustainability goals

---

**🌱 Built with ❤️ for the environment • Making AI Development Sustainable**
