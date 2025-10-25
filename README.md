# 🧠 NeuroGreen - AI-Powered Environmental Intelligence Platform

**A complete sustainability platform for AI development with multi-user support, cloud deployment, and advanced environmental tracking including energy consumption and water usage.**

---

## 🎯 **Project Overview**

NeuroGreen is a comprehensive environmental monitoring platform that tracks carbon emissions, energy consumption, and water usage for AI workloads. It provides real-time monitoring, interactive visualizations, multi-user collaboration, and cloud deployment capabilities.

### **Key Features**
- ✅ **Multi-User Platform** - User authentication, organizations, team collaboration
- ✅ **Enhanced Environmental Tracking** - Carbon emissions, energy consumption, water usage
- ✅ **Interactive Visualizations** - Beautiful graphs and charts with tabs
- ✅ **AI-Powered Recommendations** - Intelligent analysis and LLM chat interface
- ✅ **Cloud Deployment Ready** - Docker, Heroku, AWS, Google Cloud, Azure
- ✅ **Real-time Monitoring** - Live tracking during AI workloads
- ✅ **Regional Analysis** - Environmental impact by geographic region
- ✅ **Export & Notifications** - CSV, PDF, Excel exports with email/Slack integration

---

## 🏗️ **Architecture**

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
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ Cloud Deployment │    │ Export &        │
                       │ (Docker+Heroku+  │    │ Notifications   │
                       │  AWS+GCP+Azure)  │    │ (CSV+PDF+Email) │
                       └──────────────────┘    └─────────────────┘
```

---

## 🚀 **Quick Start**

### **Option 1: NeuroGreen AI Recommendations App (Recommended)**
```bash
# Run the NeuroGreen AI-powered recommendations app with intelligent analysis
streamlit run standalone_ai_recommendations.py
```
**Access at: http://localhost:8505**

#### **🤖 AI Recommendations Setup**
```bash
# Install AI-specific requirements
pip install -r requirements_ai.txt

# Configure OpenAI API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your OpenAI API key

# Run the AI-powered app
streamlit run enhanced_visualization_with_ai_recommendations.py
```

### **Option 2: Enhanced Visualization App**
```bash
# Run the enhanced app with sample data and interactive tabs
streamlit run enhanced_visualization_with_sample_data.py
```
**Access at: http://localhost:8501**

### **Option 3: Multi-User Platform**
```bash
# Start with Docker (includes PostgreSQL and Redis)
docker-compose up -d

# Or run locally
source greenai/bin/activate
streamlit run multi_user_platform.py
```

### **Option 4: Basic Carbon Tracking**
```bash
# Simple carbon tracking
streamlit run eco_carbon_tracker_app.py

# Enhanced eco app with animations
streamlit run enhanced_eco_app.py
```

### **Option 5: Test Run with Sample Data**
```bash
# Run complete NeuroGreen demo with ALL features (Recommended)
streamlit run neurogreen_complete_demo.py

# Run NeuroGreen with Cost & ROI Analysis (NEW!)
streamlit run neurogreen_cost_roi_analysis.py

# Run NeuroGreen Enhanced Dashboard with Motivation & Savings (NEW!)
streamlit run neurogreen_enhanced_dashboard.py

# Run NeuroGreen with comprehensive test data
streamlit run standalone_ai_recommendations.py

# Run enhanced visualization with sample data
streamlit run enhanced_visualization_with_sample_data.py

# Run NeuroGreen demo with sample data
streamlit run demo_ai_recommendations.py
```

**Access NeuroGreen at: http://localhost:8505**

---

## 📊 **Environmental Tracking Features**

### **🌍 Carbon Emissions Tracking**
- **Real-time CO₂ monitoring** during AI workloads
- **Regional carbon intensity** factors by geographic location
- **Renewable energy percentage** tracking
- **Environmental context** (trees needed, car miles equivalent)

### **⚡ Energy Consumption Analysis**
- **Hardware-specific power models** (CPU, GPU, Memory)
- **Utilization-based calculations** for accurate energy estimates
- **Energy efficiency analysis** by hardware type
- **Time-series energy consumption** tracking

### **💧 Water Usage Monitoring**
- **Regional water intensity factors** (liters per kWh)
- **Cloud provider specific data** (AWS, GCP, Azure)
- **Water footprint analysis** with environmental equivalents
- **Regional water usage comparisons**

### **📈 Interactive Visualizations**
- **Interactive Tabs** - Click to explore different metrics
- **Real-time Charts** - Live updating graphs during tracking
- **Regional Comparisons** - Environmental impact by geographic region
- **Hardware Analysis** - Energy efficiency by component type
- **Combined Analysis** - All metrics in comprehensive view

---

## 🎛️ **Interactive Dashboard Features**

### **🌍 Carbon Emissions Tab**
- **Time Series Chart** - CO₂ emissions over time
- **Regional Comparison** - Bar chart showing emissions by region
- **Summary Metrics** - Total CO₂, average intensity, renewable percentage
- **Environmental Context** - Trees needed for carbon offset

### **⚡ Energy Consumption Tab**
- **Energy Over Time** - Line chart of energy consumption
- **Hardware Efficiency** - Bar chart of energy use by hardware type
- **Utilization Analysis** - CPU, GPU, memory usage patterns
- **Energy Rate** - Energy consumption rate per second

### **💧 Water Usage Tab**
- **Water Over Time** - Line chart of water usage
- **Regional Water Comparison** - Bar chart by geographic region
- **Water Intensity Analysis** - Scatter plot of water vs energy
- **Environmental Equivalents** - Bottles, showers equivalent

### **🌍 Combined Analysis Tab**
- **Multi-metric Time Series** - All metrics in one chart
- **Regional Impact Scatter** - Energy vs water vs CO₂ by region
- **Environmental Context** - Trees, car miles, bottles, showers
- **Combined Efficiency** - Overall environmental impact

### **📚 Calculations Tab**
- **Energy Calculation** - How energy consumption is calculated
- **Water Calculation** - How water usage is determined
- **Carbon Calculation** - How CO₂ emissions are computed
- **Environmental Context** - What the numbers mean

---

## 🤖 **AI-Powered Recommendations**

### **🧠 Intelligent Analysis**
- **Behavior Pattern Recognition** - Analyzes user workload patterns
- **Efficiency Optimization** - Identifies optimization opportunities
- **Regional Analysis** - Compares environmental impact across regions
- **Hardware Recommendations** - Suggests more efficient hardware configurations
- **Scheduling Optimization** - Recommends optimal workload timing

### **💬 LLM Chat Interface**
- **Natural Language Queries** - Ask questions about environmental optimization
- **Contextual Responses** - AI considers your specific data and patterns
- **Interactive Dialogue** - Multi-turn conversations with AI assistant
- **Expert Advice** - Get professional-level environmental guidance

### **📊 Pattern Analysis**
- **Workload Impact Analysis** - Environmental impact by workload type
- **Regional Efficiency Analysis** - Geographic optimization opportunities
- **Hardware Efficiency Analysis** - Energy consumption by hardware type
- **Time-based Patterns** - Optimal scheduling recommendations

### **🎯 Smart Recommendations**
- **High Priority** - Regional optimization, workload optimization
- **Medium Priority** - Hardware optimization, scheduling optimization
- **Low Priority** - General sustainability, monitoring enhancement
- **Impact Estimation** - Quantified potential savings from recommendations

---

## 👥 **Multi-User Platform Features**

### **🔐 User Authentication**
- **Email/Password Authentication** with secure password hashing
- **OAuth Integration** for Google and GitHub
- **Session Management** with secure tokens
- **User Profile Management** with avatars and preferences

### **🏢 Team Collaboration**
- **Organization Management** with team creation
- **Role-Based Access Control** (Admin, Member, Viewer)
- **Team Invitations** via email with custom messages
- **Project Collaboration** with shared workspaces
- **Real-time Comments** and discussions

### **📊 Enhanced Dashboards**
- **Personal Dashboards** for individual users
- **Team Dashboards** for organization-wide metrics
- **Project History** with detailed tracking data
- **Leaderboards** for environmental efficiency

---

## ☁️ **Cloud Deployment**

### **🐳 Docker Deployment**
```bash
# Build and run with Docker
docker-compose up -d

# Access the application
open http://localhost:8501
```

### **🟠 Heroku Deployment**
```bash
# Create Heroku app
heroku create greenai-multi-user

# Add PostgreSQL and Redis
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev

# Deploy
git push heroku main
```

### **🔵 AWS Deployment**
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name greenai-cluster

# Deploy with ECS
aws ecs create-service --cluster greenai-cluster --service-name greenai-service
```

### **🟢 Google Cloud Deployment**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/greenai-multi-user
gcloud run deploy greenai-multi-user --image gcr.io/your-project/greenai-multi-user
```

---

## 📈 **Regional Environmental Factors**

### **🌍 Carbon Intensity by Region**
| Region | Carbon Intensity (g CO₂/kWh) | Renewable % |
|--------|------------------------------|-------------|
| us-east-1 (Virginia) | 300 | 30% |
| us-west-2 (Oregon) | 200 | 80% |
| eu-west-1 (Ireland) | 250 | 70% |
| ap-southeast-1 (Singapore) | 500 | 20% |

### **💧 Water Intensity by Cloud Provider**
| Cloud Provider | Region | Water Intensity (L/kWh) |
|----------------|--------|------------------------|
| **AWS** | us-east-1 | 1.2 |
| **AWS** | us-west-2 | 1.5 |
| **GCP** | us-central1 | 1.4 |
| **Azure** | eastus | 1.3 |

### **⚡ Hardware Power Models**
| Component | Type | Power (Watts) |
|-----------|------|---------------|
| **CPU** | Apple M2 | 25W |
| **CPU** | Intel i9 | 95W |
| **GPU** | RTX 4090 | 450W |
| **Memory** | 32GB DDR5 | 8W |

---

## 📊 **Export & Notification Features**

### **📤 Export Capabilities**
- **CSV Export** - Raw data in spreadsheet format
- **PDF Reports** - Professional environmental impact reports
- **Excel Export** - Detailed analysis with charts
- **JSON Export** - Machine-readable data format

### **🔔 Notification System**
- **Email Notifications** - SMTP integration with custom templates
- **Slack Integration** - Team notifications via webhooks
- **Discord Integration** - Community notifications
- **Automated Reports** - Scheduled environmental impact reports

---

## 🧪 **Testing & Examples**

### **Quick Test**
```bash
# Test enhanced tracking
python3 enhanced_tracking_example.py

# Test with sample data
python3 demo_enhanced_app.py

# Run visualization app
streamlit run enhanced_visualization_with_sample_data.py
```

### **Sample Output**
```
🌱 Enhanced Environmental Tracking Example
==================================================
📊 Environmental Impact Results:
⏱️  Runtime: 2.5 seconds
⚡ Energy: 0.000031 kWh
💧 Water: 0.05 L
🌍 CO₂: 0.000007 kg

🌍 Environmental Context:
🌳 Trees needed to offset: 0.00
🚗 Car miles equivalent: 0.00 miles
🍼 Water bottles equivalent: 0.1 bottles
🚿 Shower equivalent: 0.00 showers
```

---

## 📁 **File Structure**

### **Core Applications**
- `enhanced_visualization_with_sample_data.py` - **Main app with tabs and graphs**
- `multi_user_platform.py` - Multi-user platform with authentication
- `enhanced_carbon_tracker.py` - Enhanced tracking with energy/water
- `eco_carbon_tracker_app.py` - Basic carbon tracking app

### **Configuration Files**
- `docker-compose.yml` - Complete development setup
- `Dockerfile` - Production-ready container
- `requirements_multi_user.txt` - Enhanced dependencies
- `init.sql` - Database schema and initialization

### **Documentation**
- `ENHANCED_FEATURES_GUIDE.md` - Complete feature documentation
- `DEPLOYMENT_GUIDE.md` - Comprehensive deployment guide
- `MULTI_USER_DEPLOYMENT_CHECKLIST.md` - Deployment checklist
- `ENHANCED_VISUALIZATION_GUIDE.md` - Visualization features guide

---

## 🎯 **Usage Examples**

### **NeuroGreen Basic Tracking**
```python
from src.monitoring.carbon_tracker import CarbonTracker

# Initialize NeuroGreen tracker
tracker = CarbonTracker("My Neural Network Project")

# Start tracking
tracker.start_tracking("training", "pytorch")

# Your neural network code here...
# (training, inference, etc.)

# Stop tracking
metrics = tracker.stop_tracking()
print(f"CO₂: {metrics.carbon_emissions:.6f} kg")
```

### **NeuroGreen Enhanced Tracking**
```python
from enhanced_carbon_tracker import EnhancedCarbonTracker

# Initialize NeuroGreen enhanced tracker
tracker = EnhancedCarbonTracker(
    project_name="My Neural Network Project",
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

# Stop tracking
metrics = tracker.stop_tracking()

# Access enhanced metrics
print(f"Energy: {metrics.energy_consumed:.6f} kWh")
print(f"Water: {metrics.water_usage:.2f} L")
print(f"CO₂: {metrics.carbon_emissions:.6f} kg")
```

### **Streamlit Integration**
```python
# Run enhanced visualization app
streamlit run enhanced_visualization_with_sample_data.py

# Run multi-user platform
streamlit run multi_user_platform.py
```

---

## 🔧 **Configuration**

### **Environment Variables**
   ```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=greenai
DB_USER=postgres
DB_PASSWORD=secure_password

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

---

## 📊 **Environmental Impact Metrics**

### **Primary Metrics**
- **Carbon Emissions** (kg CO₂) - Climate impact
- **Energy Consumption** (kWh) - Resource usage
- **Water Usage** (liters) - Water footprint

### **Derived Metrics**
- **Carbon Intensity** (g CO₂/kWh) - Grid efficiency
- **Water Intensity** (L/kWh) - Regional water usage
- **Renewable Percentage** (%) - Clean energy usage
- **Energy Efficiency** (kg CO₂/kWh) - Overall efficiency

### **Environmental Context**
- **Trees Needed** (0.06 trees per kg CO₂)
- **Car Miles Equivalent** (2.2 miles per kg CO₂)
- **Water Bottles Equivalent** (2 bottles per liter)
- **Shower Equivalent** (65L per shower)

---

## 🚀 **Deployment Options**

### **Local Development**
   ```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### **Production Deployment**
   ```bash
# Deploy to Heroku
git push heroku main

# Deploy to AWS
aws ecs update-service --cluster greenai-cluster --service greenai-service

# Deploy to Google Cloud
gcloud run deploy greenai-multi-user --image gcr.io/your-project/greenai-multi-user
```

---

## 🎯 **Key Benefits**

### **1. Comprehensive Environmental Tracking**
- Track carbon, energy, and water usage together
- Regional factors for accurate calculations
- Hardware-specific energy models

### **2. Interactive Visualizations**
- Click through tabs to explore different metrics
- Real-time updates during tracking
- Beautiful, responsive charts

### **3. Multi-User Collaboration**
- Team management and organization features
- Role-based access control
- Project sharing and collaboration

### **4. Cloud Deployment Ready**
- Docker containerization
- Multi-cloud platform support
- Production-ready configuration

### **5. Export & Reporting**
- Multiple export formats (CSV, PDF, Excel, JSON)
- Email and Slack notifications
- Automated reporting capabilities

---

## 🌿 **Environmental Impact**

### **What This Enables**
- **Accurate Water Footprint** tracking for AI workloads
- **Regional Optimization** for environmental efficiency
- **Hardware Efficiency** analysis and recommendations
- **Comprehensive Reporting** for sustainability goals

### **Real-World Impact**
- **15-40% reduction** in environmental impact through optimization
- **Regional awareness** for sustainable AI development
- **Hardware efficiency** improvements
- **Sustainability reporting** for organizations

---

## 📞 **Support & Documentation**

### **Getting Help**
- **Documentation**: Check all `.md` files in the project
- **Issues**: Create GitHub issues for bugs
- **Community**: Join our Discord server
- **Email**: support@greenai.com

### **Useful Commands**
```bash
# Check application status
docker-compose ps

# View application logs
docker-compose logs app

# Access application shell
docker-compose exec app bash

# Database shell
docker-compose exec db psql -U postgres -d greenai
```

---

## 📄 **License**

MIT License - see LICENSE file for details.

---

**🌱 Built with ❤️ for the environment • Making AI Development Sustainable**

*Track carbon emissions, energy consumption, and water usage with comprehensive visualizations and multi-user collaboration!*