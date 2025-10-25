# 🌍 Carbon Emission Tracking Guide

This guide shows you how to track and visualize carbon emissions from your machine learning experiments using CodeCarbon. Perfect for Mac users and any contributor wanting to understand their environmental impact.

## 🚀 Quick Start

### Option 1: Simple Integration (Recommended for existing scripts)

Add these lines to your existing ML script:

```python
from simple_carbon_tracker import CarbonTracker

# At the beginning of your script
tracker = CarbonTracker("MyExperiment")
tracker.start()

# Your ML code here...

# At the end of your script
results = tracker.stop()
print(f"🌍 Total CO₂ emissions: {results['emissions_kg']:.6f} kg")
```

### Option 2: Comprehensive Tracking (For new projects)

Use the full-featured tracker with visualizations:

```python
from ml_with_carbon_tracking import MLCarbonTracker

tracker = MLCarbonTracker("MyMLProject")
tracker.start_tracking()

# Your training code with checkpoints
tracker.log_epoch(1, loss_value)
tracker.log_checkpoint("Data Loading")

# Stop and visualize
results = tracker.stop_tracking()
tracker.print_detailed_report(results)
tracker.create_emission_visualization(results)
```

## 📊 Available Examples

### 1. `simple_carbon_tracker.py` - Minimal Integration
- **Best for**: Adding to existing scripts
- **Features**: Basic emission tracking, automatic dependency installation
- **Output**: Simple emission report

### 2. `ml_with_carbon_tracking.py` - Full ML Integration
- **Best for**: New ML projects
- **Features**: Epoch tracking, checkpoints, visualizations, detailed reporting
- **Output**: HTML visualizations, comprehensive reports

### 3. `carbon_tracking_example.py` - Complete Demo
- **Best for**: Learning and testing
- **Features**: Simulated ML experiment, all tracking features
- **Output**: Full demonstration with visualizations

## 🛠️ Installation & Setup

### Automatic Installation (Recommended)
The examples automatically install CodeCarbon if not present:

```bash
# No manual installation needed - just run!
python3 simple_carbon_tracker.py
```

### Manual Installation
If you prefer manual setup:

```bash
# Install in virtual environment
source greenai/bin/activate
pip install codecarbon plotly matplotlib

# Run examples
python3 simple_carbon_tracker.py
```

## 📈 Understanding the Output

### Basic Emission Report
```
🌍 CARBON EMISSION REPORT
==================================================
📋 Project: MyMLExperiment
⏱️  Runtime: 4.61 seconds
🌱 Total CO₂: 0.000012 kg
⚡ Rate: 0.00000259 kg/s

🌳 Environmental Impact:
   • 0.00 trees needed to offset
   • Equivalent to 0.0 miles driven
```

### Detailed Report (ML Integration)
- **Project Information**: Name, start/end times, total runtime
- **Emission Metrics**: Total CO₂, emission rate, carbon intensity
- **Training Analysis**: Epochs, average time per epoch, final loss
- **Checkpoint Timeline**: All logged checkpoints with timestamps
- **Environmental Impact**: Trees needed, car miles equivalent

### Visualizations
- **Emissions Over Time**: Cumulative CO₂ emissions during training
- **Loss vs Emissions**: Relationship between model loss and emissions
- **Emission Rate**: Real-time emission rate throughout experiment
- **Checkpoint Timeline**: Visual timeline of all checkpoints

## 🎯 Integration Examples

### For PyTorch Training
```python
from simple_carbon_tracker import CarbonTracker

tracker = CarbonTracker("PyTorchTraining")
tracker.start()

# Your PyTorch training loop
for epoch in range(num_epochs):
    for batch in dataloader:
        # Training code...
        pass

results = tracker.stop()
print(f"Training emitted {results['emissions_kg']:.6f} kg CO₂")
```

### For TensorFlow Training
```python
from ml_with_carbon_tracking import MLCarbonTracker

tracker = MLCarbonTracker("TensorFlowTraining")
tracker.start_tracking()

# Your TensorFlow training
model.fit(x_train, y_train, epochs=10, 
          callbacks=[tracker.log_epoch_callback])

results = tracker.stop_tracking()
tracker.create_emission_visualization(results)
```

### For Scikit-learn Experiments
```python
from simple_carbon_tracker import CarbonTracker

tracker = CarbonTracker("SklearnExperiment")
tracker.start()

# Your sklearn pipeline
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)

results = tracker.stop()
print(f"Experiment carbon footprint: {results['emissions_kg']:.6f} kg CO₂")
```

## 🔧 Customization

### Custom Project Names
```python
tracker = CarbonTracker("MyCustomProject")
```

### Custom Checkpoints
```python
# Log specific events
tracker.log_checkpoint("Data Loading Complete")
tracker.log_checkpoint("Model Training Started")
tracker.log_checkpoint("Hyperparameter Tuning")
```

### Custom Epoch Logging
```python
# Log each epoch with metrics
for epoch in range(num_epochs):
    loss = train_one_epoch()
    tracker.log_epoch(epoch, loss, f"Epoch {epoch} completed")
```

## 📱 Mac-Specific Notes

### PowerMetrics Integration
On Mac, you may see warnings about PowerMetrics. This is normal and doesn't affect functionality:

```
[codecarbon WARNING] No CPU tracking mode found. Falling back on CPU constant mode.
```

### Apple Silicon (M1/M2) Support
CodeCarbon works on Apple Silicon but may show warnings about unknown processors. This is expected and doesn't impact tracking accuracy.

### Performance Impact
Carbon tracking adds minimal overhead (~1-2% CPU usage) to your experiments.

## 🌱 Environmental Impact Context

The examples provide environmental context to help you understand your emissions:

- **Trees Equivalent**: How many trees would need to be planted to offset emissions
- **Car Miles**: Equivalent distance driven by car
- **Cross-Country Drive**: Percentage of a cross-country drive

## 🚨 Troubleshooting

### Common Issues

1. **ImportError: No module named 'codecarbon'**
   - Solution: The examples auto-install CodeCarbon, but you can manually install with `pip install codecarbon`

2. **Permission errors on Mac**
   - Solution: The warnings are normal and don't affect functionality

3. **Visualization not working**
   - Solution: Install plotly with `pip install plotly`

4. **Low emission readings**
   - This is normal for short experiments. Try longer training runs for more significant readings.

### Getting Help

- Check the CodeCarbon documentation: https://codecarbon.io/
- Review the example files for implementation details
- Check the generated HTML files for visualizations

## 🎉 Best Practices

1. **Start Simple**: Begin with `simple_carbon_tracker.py` for existing projects
2. **Add Checkpoints**: Use `log_checkpoint()` for important milestones
3. **Track Epochs**: Use `log_epoch()` for training monitoring
4. **Visualize Results**: Always generate visualizations for analysis
5. **Compare Experiments**: Track emissions across different model architectures
6. **Share Results**: Include emission data in your research papers

## 📊 Example Output Files

After running the examples, you'll get:

- **Console Output**: Real-time emission reports
- **HTML Files**: Interactive visualizations (e.g., `carbon_analysis_MyMLProject.html`)
- **Detailed Reports**: Comprehensive emission analysis

## 🤝 Contributing

Want to improve carbon tracking? Here's how:

1. **Add New Features**: Extend the tracker classes with new capabilities
2. **Improve Visualizations**: Enhance the Plotly charts
3. **Add Frameworks**: Create specific trackers for different ML frameworks
4. **Optimize Performance**: Reduce tracking overhead
5. **Documentation**: Improve this guide with your findings

## 📄 License

This carbon tracking code is part of the GreenAI project and follows the same MIT license.

---

**🌍 Make your ML experiments greener! Every emission tracked is a step toward sustainable AI.**
