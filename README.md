# Green AI Recommendations Bot + Carbon Tracker

A comprehensive sustainability assistant that monitors AI workload energy usage and carbon emissions, providing actionable recommendations for optimal scheduling and carbon efficiency.

## 🎯 Project Goals

- **Real-time Monitoring**: Track energy consumption and carbon emissions of AI workloads
- **Smart Recommendations**: Provide optimal scheduling suggestions based on grid carbon intensity
- **Visualization**: Interactive dashboards showing efficiency gains and carbon impact
- **Framework Compatibility**: Support for PyTorch, TensorFlow, and other ML frameworks
- **Cloud Integration**: Scalable across AWS, GCP, and Azure
- **Sustainability Reporting**: Quantify and report carbon efficiency improvements

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Workloads  │───▶│  Carbon Monitor  │───▶│  Recommendation │
│  (PyTorch/TF)   │    │   (CodeCarbon)   │    │     Engine      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ Carbon Intensity │    │   Chatbot UI  │
                       │      API         │    │   (Streamlit)  │
                       │ (ElectricityMap) │    └─────────────────┘
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Dashboard &    │
                       │  Visualization   │
                       └──────────────────┘
```

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📊 Key Features

- **Real-time Carbon Tracking**: Monitor energy usage during training/inference
- **Grid-Aware Scheduling**: Optimize job timing based on renewable energy availability
- **Interactive Chatbot**: Get sustainability recommendations via natural language
- **Comprehensive Dashboards**: Visualize carbon impact and efficiency gains
- **Multi-Framework Support**: Works with PyTorch, TensorFlow, and more
- **Cloud Integration**: Deploy on AWS, GCP, or Azure

## 🔧 Configuration

See `config/` directory for detailed configuration options and API setup instructions.

## 📈 Sustainability Metrics

- **Carbon Intensity**: gCO2/kWh of electricity consumed
- **Energy Efficiency**: Workload performance per unit energy
- **Renewable Percentage**: % of energy from renewable sources
- **Carbon Savings**: Quantified reduction in emissions over time

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details.

## 📄 License

MIT License - see LICENSE file for details.
# GreenAI
Green Recommendations Bot + AI Carbon Tracker monitors energy usage and carbon emissions of AI workloads, providing real-time recommendations to optimize job scheduling for environmental efficiency—making AI development greener and more sustainable.