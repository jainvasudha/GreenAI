"""
Green AI Recommendations Bot + Carbon Tracker
Streamlit-based conversational interface
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any

# Import our modules
from src.monitoring.carbon_tracker import CarbonTracker, CarbonMetrics
from src.api.carbon_intensity import CarbonIntensityAPI
from src.recommendations.engine import RecommendationEngine, Recommendation
from config.settings import config, metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Green AI Carbon Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .recommendation-card {
        background-color: #fff8dc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffa500;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #f1f8e9;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'carbon_tracker' not in st.session_state:
    st.session_state.carbon_tracker = CarbonTracker()
if 'recommendation_engine' not in st.session_state:
    st.session_state.recommendation_engine = RecommendationEngine()
if 'carbon_api' not in st.session_state:
    st.session_state.carbon_api = CarbonIntensityAPI()
if 'current_metrics' not in st.session_state:
    st.session_state.current_metrics = None

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🌱 Green AI Carbon Tracker</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI Sustainability Assistant")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Tracking controls
        st.subheader("Carbon Tracking")
        if st.button("🟢 Start Tracking", type="primary"):
            session_id = st.session_state.carbon_tracker.start_tracking()
            st.session_state.current_session = session_id
            st.success(f"Started tracking session: {session_id}")
        
        if st.button("🔴 Stop Tracking"):
            if hasattr(st.session_state, 'current_session'):
                metrics = st.session_state.carbon_tracker.stop_tracking(st.session_state.current_session)
                st.session_state.current_metrics = metrics
                st.success("Stopped tracking and saved metrics")
            else:
                st.warning("No active tracking session")
        
        # Settings
        st.subheader("⚙️ Settings")
        region = st.selectbox("Region", ["US-CA", "US-NY", "GB", "DE", "FR"])
        framework = st.selectbox("ML Framework", ["pytorch", "tensorflow", "scikit-learn", "other"])
        
        # Display current carbon intensity
        try:
            current_intensity = st.session_state.carbon_api.get_current_intensity(region.split('-')[0], region)
            st.metric("Current Carbon Intensity", f"{current_intensity.carbon_intensity:.0f} g CO2/kWh")
            st.metric("Renewable Energy", f"{current_intensity.renewable_percentage:.0f}%")
        except Exception as e:
            st.error(f"Failed to get carbon intensity: {e}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chatbot", "📊 Dashboard", "🎯 Recommendations", "📈 Analytics"])
    
    with tab1:
        chatbot_interface()
    
    with tab2:
        dashboard_interface()
    
    with tab3:
        recommendations_interface()
    
    with tab4:
        analytics_interface()

def chatbot_interface():
    """Chatbot interface for sustainability recommendations"""
    
    st.header("💬 Sustainability Chatbot")
    st.markdown("Ask me about carbon optimization, energy efficiency, or get personalized recommendations!")
    
    # Chat input
    user_input = st.text_input("Ask me anything about green AI:", placeholder="How can I reduce my model's carbon footprint?")
    
    if st.button("Send", type="primary") or user_input:
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "message": user_input,
                "timestamp": datetime.now()
            })
            
            # Generate bot response
            bot_response = generate_chatbot_response(user_input)
            
            # Add bot response to chat history
            st.session_state.chat_history.append({
                "role": "bot",
                "message": bot_response,
                "timestamp": datetime.now()
            })
    
    # Display chat history
    st.subheader("💭 Conversation History")
    for message in reversed(st.session_state.chat_history[-10:]):  # Show last 10 messages
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["message"]}
                <br><small>{message["timestamp"].strftime("%H:%M:%S")}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🌱 Green AI Bot:</strong> {message["message"]}
                <br><small>{message["timestamp"].strftime("%H:%M:%S")}</small>
            </div>
            """, unsafe_allow_html=True)

def generate_chatbot_response(user_input: str) -> str:
    """Generate chatbot response based on user input"""
    
    # Simple keyword-based responses (in production, use LLM)
    user_input_lower = user_input.lower()
    
    if "carbon" in user_input_lower or "emission" in user_input_lower:
        return """🌱 **Carbon Optimization Tips:**
        
1. **Schedule during low-carbon hours** - Run training when renewable energy is abundant
2. **Use efficient frameworks** - PyTorch with optimizations, TensorFlow with XLA
3. **Optimize batch sizes** - Larger batches often use energy more efficiently
4. **Consider model pruning** - Smaller models = less energy consumption
5. **Use mixed precision training** - Reduces memory and energy usage

Would you like me to analyze your current setup and provide specific recommendations?"""
    
    elif "energy" in user_input_lower or "efficiency" in user_input_lower:
        return """⚡ **Energy Efficiency Strategies:**
        
1. **Monitor resource utilization** - Ensure CPU/GPU are being used efficiently
2. **Use appropriate hardware** - Match workload to hardware capabilities
3. **Implement early stopping** - Stop training when convergence is reached
4. **Use gradient accumulation** - Reduce memory usage for large models
5. **Enable framework optimizations** - Use built-in performance features

I can help you track your current energy usage and suggest improvements!"""
    
    elif "schedule" in user_input_lower or "timing" in user_input_lower:
        try:
            # Get optimal scheduling windows
            optimal_windows = st.session_state.carbon_api.get_optimal_scheduling_windows("US-CA", 24)
            if optimal_windows:
                best_time, best_intensity = optimal_windows[0]
                return f"""⏰ **Optimal Scheduling:**
                
The best time to run your workload is **{best_time.strftime('%H:%M')}** when carbon intensity is only **{best_intensity:.0f} g CO2/kWh**.

**Next 3 optimal windows:**
{chr(10).join([f"• {time.strftime('%H:%M')} - {intensity:.0f} g CO2/kWh" for time, intensity in optimal_windows[:3]])}

Would you like me to help you schedule your next training run?"""
            else:
                return "I'm having trouble getting scheduling data. Please check your API configuration."
        except Exception as e:
            return f"Sorry, I couldn't get scheduling information: {e}"
    
    elif "help" in user_input_lower or "what" in user_input_lower:
        return """🤖 **How I Can Help:**
        
I'm your AI sustainability assistant! I can help you with:

• **Carbon tracking** - Monitor your AI workload emissions
• **Energy optimization** - Improve efficiency and reduce consumption  
• **Smart scheduling** - Find the greenest times to run workloads
• **Framework recommendations** - Choose the most efficient tools
• **Hardware optimization** - Get the most from your resources
• **Sustainability reporting** - Track your environmental impact

Just ask me anything about making your AI more sustainable! 🌱"""
    
    else:
        return """🌱 I'm here to help with your AI sustainability journey! 

Try asking me about:
• "How can I reduce my model's carbon footprint?"
• "When is the best time to run my training?"
• "What's my current energy efficiency?"
• "How can I optimize my PyTorch model?"

Or use the other tabs to explore dashboards, get recommendations, and analyze your data!"""

def dashboard_interface():
    """Dashboard interface showing metrics and visualizations"""
    
    st.header("📊 Carbon Impact Dashboard")
    
    # Current metrics display
    if st.session_state.current_metrics:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Carbon Emissions",
                f"{st.session_state.current_metrics.carbon_emissions:.3f} kg CO2",
                delta=None
            )
        
        with col2:
            st.metric(
                "Energy Consumed",
                f"{st.session_state.current_metrics.energy_consumed:.3f} kWh",
                delta=None
            )
        
        with col3:
            st.metric(
                "Carbon Intensity",
                f"{st.session_state.current_metrics.carbon_intensity:.0f} g CO2/kWh",
                delta=None
            )
        
        with col4:
            st.metric(
                "Renewable Energy",
                f"{st.session_state.current_metrics.renewable_percentage:.0f}%",
                delta=None
            )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Carbon Intensity Over Time")
        try:
            # Get forecast data
            forecast = st.session_state.carbon_api.get_forecast("US-CA", 24)
            if forecast:
                df = pd.DataFrame([{
                    'time': point.timestamp,
                    'carbon_intensity': point.carbon_intensity,
                    'renewable_percentage': point.renewable_percentage
                } for point in forecast])
                
                fig = px.line(df, x='time', y='carbon_intensity', 
                            title='24-Hour Carbon Intensity Forecast')
                fig.update_layout(xaxis_title="Time", yaxis_title="Carbon Intensity (g CO2/kWh)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No forecast data available. Check your API configuration.")
        except Exception as e:
            st.error(f"Failed to load forecast data: {e}")
    
    with col2:
        st.subheader("🌱 Renewable Energy Forecast")
        try:
            forecast = st.session_state.carbon_api.get_forecast("US-CA", 24)
            if forecast:
                df = pd.DataFrame([{
                    'time': point.timestamp,
                    'renewable_percentage': point.renewable_percentage
                } for point in forecast])
                
                fig = px.area(df, x='time', y='renewable_percentage',
                            title='24-Hour Renewable Energy Forecast')
                fig.update_layout(xaxis_title="Time", yaxis_title="Renewable Energy (%)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No forecast data available.")
        except Exception as e:
            st.error(f"Failed to load renewable data: {e}")
    
    # Historical data
    if st.session_state.carbon_tracker.metrics_history:
        st.subheader("📊 Historical Performance")
        
        # Create historical dataframe
        history_data = []
        for metrics in st.session_state.carbon_tracker.metrics_history:
            history_data.append({
                'timestamp': metrics.timestamp,
                'carbon_emissions': metrics.carbon_emissions,
                'energy_consumed': metrics.energy_consumed,
                'carbon_intensity': metrics.carbon_intensity,
                'workload_type': metrics.workload_type,
                'framework': metrics.framework
            })
        
        df_history = pd.DataFrame(history_data)
        
        # Emissions over time
        fig = px.line(df_history, x='timestamp', y='carbon_emissions',
                     color='workload_type', title='Carbon Emissions Over Time')
        st.plotly_chart(fig, use_container_width=True)
        
        # Framework comparison
        framework_emissions = df_history.groupby('framework')['carbon_emissions'].mean()
        fig = px.bar(x=framework_emissions.index, y=framework_emissions.values,
                    title='Average Emissions by Framework')
        fig.update_layout(xaxis_title="Framework", yaxis_title="Average Emissions (kg CO2)")
        st.plotly_chart(fig, use_container_width=True)

def recommendations_interface():
    """Recommendations interface"""
    
    st.header("🎯 Sustainability Recommendations")
    
    if st.session_state.current_metrics:
        st.subheader("📋 Current Workload Analysis")
        
        # Generate recommendations
        workload_characteristics = {
            'framework': 'pytorch',  # This would be dynamic in practice
            'duration_hours': 4,
            'gpu_required': True,
            'batch_size': 32
        }
        
        recommendations = st.session_state.recommendation_engine.generate_recommendations(
            st.session_state.current_metrics,
            workload_characteristics
        )
        
        if recommendations:
            st.success(f"Found {len(recommendations)} optimization opportunities!")
            
            for i, rec in enumerate(recommendations, 1):
                with st.expander(f"💡 {rec.title}"):
                    st.markdown(f"**Description:** {rec.description}")
                    st.markdown(f"**Carbon Savings:** {rec.carbon_savings_kg:.3f} kg CO2")
                    st.markdown(f"**Energy Savings:** {rec.energy_savings_kwh:.3f} kWh")
                    st.markdown(f"**Confidence:** {rec.confidence_score:.0%}")
                    st.markdown(f"**Effort:** {rec.implementation_effort.title()}")
                    st.markdown(f"**Timeframe:** {rec.timeframe.replace('_', ' ').title()}")
                    
                    if rec.prerequisites:
                        st.markdown(f"**Prerequisites:** {', '.join(rec.prerequisites)}")
                    
                    if rec.code_example:
                        st.code(rec.code_example, language='python')
        else:
            st.info("No recommendations available. Please run a workload first.")
    else:
        st.info("No current metrics available. Please start tracking a workload first.")
    
    # Manual recommendation request
    st.subheader("🔍 Get Custom Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        framework = st.selectbox("ML Framework", ["pytorch", "tensorflow", "scikit-learn", "other"])
        workload_type = st.selectbox("Workload Type", ["training", "inference", "fine-tuning", "evaluation"])
    
    with col2:
        duration = st.slider("Expected Duration (hours)", 1, 24, 4)
        gpu_required = st.checkbox("GPU Required", value=True)
    
    if st.button("Generate Recommendations", type="primary"):
        # Create mock metrics for demonstration
        mock_metrics = CarbonMetrics(
            timestamp=datetime.now(),
            energy_consumed=2.0,
            carbon_emissions=1.0,
            carbon_intensity=500,
            renewable_percentage=30,
            workload_type=workload_type,
            framework=framework,
            gpu_utilization=70,
            cpu_utilization=60,
            memory_usage=80
        )
        
        workload_chars = {
            'framework': framework,
            'duration_hours': duration,
            'gpu_required': gpu_required,
            'batch_size': 32
        }
        
        recommendations = st.session_state.recommendation_engine.generate_recommendations(
            mock_metrics, workload_chars
        )
        
        if recommendations:
            st.success(f"Generated {len(recommendations)} recommendations for your setup!")
            
            for rec in recommendations:
                st.markdown(f"""
                <div class="recommendation-card">
                    <h4>{rec.title}</h4>
                    <p>{rec.description}</p>
                    <p><strong>Potential Savings:</strong> {rec.carbon_savings_kg:.2f} kg CO2, {rec.energy_savings_kwh:.2f} kWh</p>
                </div>
                """, unsafe_allow_html=True)

def analytics_interface():
    """Analytics interface for detailed analysis"""
    
    st.header("📈 Sustainability Analytics")
    
    if not st.session_state.carbon_tracker.metrics_history:
        st.info("No historical data available. Run some workloads to see analytics.")
        return
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    
    history_data = []
    for metrics in st.session_state.carbon_tracker.metrics_history:
        history_data.append({
            'timestamp': metrics.timestamp,
            'carbon_emissions': metrics.carbon_emissions,
            'energy_consumed': metrics.energy_consumed,
            'carbon_intensity': metrics.carbon_intensity,
            'renewable_percentage': metrics.renewable_percentage,
            'workload_type': metrics.workload_type,
            'framework': metrics.framework,
            'gpu_utilization': metrics.gpu_utilization,
            'cpu_utilization': metrics.cpu_utilization
        })
    
    df = pd.DataFrame(history_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_emissions = df['carbon_emissions'].sum()
        st.metric("Total Emissions", f"{total_emissions:.3f} kg CO2")
    
    with col2:
        total_energy = df['energy_consumed'].sum()
        st.metric("Total Energy", f"{total_energy:.3f} kWh")
    
    with col3:
        avg_intensity = df['carbon_intensity'].mean()
        st.metric("Avg Carbon Intensity", f"{avg_intensity:.0f} g CO2/kWh")
    
    with col4:
        avg_renewable = df['renewable_percentage'].mean()
        st.metric("Avg Renewable %", f"{avg_renewable:.0f}%")
    
    # Detailed charts
    st.subheader("📈 Performance Trends")
    
    # Emissions trend
    fig = px.line(df, x='timestamp', y='carbon_emissions', 
                  color='workload_type', title='Carbon Emissions Over Time')
    st.plotly_chart(fig, use_container_width=True)
    
    # Framework comparison
    framework_comparison = df.groupby('framework').agg({
        'carbon_emissions': 'mean',
        'energy_consumed': 'mean',
        'carbon_intensity': 'mean'
    }).reset_index()
    
    fig = px.bar(framework_comparison, x='framework', y='carbon_emissions',
                title='Average Emissions by Framework')
    st.plotly_chart(fig, use_container_width=True)
    
    # Resource utilization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(df, x='cpu_utilization', y='carbon_emissions',
                        color='framework', title='CPU Utilization vs Emissions')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(df, x='gpu_utilization', y='carbon_emissions',
                        color='framework', title='GPU Utilization vs Emissions')
        st.plotly_chart(fig, use_container_width=True)
    
    # Efficiency analysis
    st.subheader("⚡ Efficiency Analysis")
    
    # Calculate efficiency scores
    df['efficiency_score'] = df.apply(lambda row: 
        st.session_state.carbon_tracker.calculate_efficiency_score(
            CarbonMetrics(**row.to_dict())
        ), axis=1)
    
    fig = px.line(df, x='timestamp', y='efficiency_score',
                  title='Energy Efficiency Score Over Time')
    fig.update_layout(yaxis_title="Efficiency Score (0-1)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Export data
    st.subheader("📥 Export Data")
    
    if st.button("Download Historical Data"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"carbon_tracking_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
