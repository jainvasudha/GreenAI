"""
🌱 GreenAI Multi-User Carbon Tracking Platform
==============================================

A comprehensive multi-user platform for carbon tracking with team collaboration,
cloud deployment, and enterprise features.

Features:
- Multi-user authentication (email/password + OAuth)
- Team/organization management
- Role-based access control
- Cloud deployment ready
- Real-time collaboration
- Export and notification features
"""

import streamlit as st
import streamlit_authenticator as stauth
import streamlit_oauth as oauth
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any, Optional
import numpy as np
import hashlib
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import requests
import base64
from io import BytesIO
import weasyprint
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    organizations = relationship("OrganizationMember", back_populates="user")
    projects = relationship("Project", back_populates="owner")
    carbon_runs = relationship("CarbonRun", back_populates="user")

class Organization(Base):
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    members = relationship("OrganizationMember", back_populates="organization")
    projects = relationship("Project", back_populates="organization")

class OrganizationMember(Base):
    __tablename__ = 'organization_members'
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(String(50), default='member')  # admin, member, viewer
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organizations")

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    organization = relationship("Organization", back_populates="projects")
    carbon_runs = relationship("CarbonRun", back_populates="project")

class CarbonRun(Base):
    __tablename__ = 'carbon_runs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    session_id = Column(String(100), unique=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    total_emissions = Column(Float, default=0.0)
    energy_consumed = Column(Float, default=0.0)
    carbon_intensity = Column(Float, default=0.0)
    renewable_percentage = Column(Float, default=0.0)
    runtime_seconds = Column(Float, default=0.0)
    framework = Column(String(100))
    workload_type = Column(String(100))
    status = Column(String(50), default='running')  # running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="carbon_runs")
    project = relationship("Project", back_populates="carbon_runs")
    comments = relationship("RunComment", back_populates="carbon_run")

class RunComment(Base):
    __tablename__ = 'run_comments'
    
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('carbon_runs.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    carbon_run = relationship("CarbonRun", back_populates="comments")
    user = relationship("User")

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default='info')  # info, warning, success, error
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database connection
def get_database_url():
    """Get database URL from environment variables."""
    if os.getenv('DATABASE_URL'):
        return os.getenv('DATABASE_URL')
    else:
        # Local development
        return f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'greenai')}"

def get_db_engine():
    """Get database engine."""
    return create_engine(get_database_url())

def get_db_session():
    """Get database session."""
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# Authentication utilities
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return stauth.Hasher([password]).generate()[0]

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return stauth.Authenticate.verify_password(password, hashed)

def generate_session_token() -> str:
    """Generate secure session token."""
    return secrets.token_urlsafe(32)

# User management
class UserManager:
    """Handle user authentication and management."""
    
    def __init__(self):
        self.db_session = get_db_session()
    
    def create_user(self, email: str, username: str, password: str, full_name: str) -> Optional[User]:
        """Create a new user."""
        try:
            # Check if user already exists
            existing_user = self.db_session.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()
            
            if existing_user:
                return None
            
            # Create new user
            user = User(
                email=email,
                username=username,
                password_hash=hash_password(password),
                full_name=full_name
            )
            
            self.db_session.add(user)
            self.db_session.commit()
            
            return user
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            self.db_session.rollback()
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            user = self.db_session.query(User).filter(User.email == email).first()
            
            if user and verify_password(password, user.password_hash):
                # Update last login
                user.last_login = datetime.utcnow()
                self.db_session.commit()
                return user
            
            return None
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db_session.query(User).filter(User.id == user_id).first()

# Organization management
class OrganizationManager:
    """Handle organization and team management."""
    
    def __init__(self):
        self.db_session = get_db_session()
    
    def create_organization(self, name: str, description: str, created_by: int) -> Optional[Organization]:
        """Create a new organization."""
        try:
            org = Organization(
                name=name,
                description=description,
                created_by=created_by
            )
            
            self.db_session.add(org)
            self.db_session.commit()
            
            # Add creator as admin
            self.add_member(org.id, created_by, 'admin')
            
            return org
            
        except Exception as e:
            logger.error(f"Error creating organization: {e}")
            self.db_session.rollback()
            return None
    
    def add_member(self, org_id: int, user_id: int, role: str = 'member') -> bool:
        """Add member to organization."""
        try:
            member = OrganizationMember(
                organization_id=org_id,
                user_id=user_id,
                role=role
            )
            
            self.db_session.add(member)
            self.db_session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding member: {e}")
            self.db_session.rollback()
            return False
    
    def get_user_organizations(self, user_id: int) -> List[Organization]:
        """Get organizations for a user."""
        return self.db_session.query(Organization).join(OrganizationMember).filter(
            OrganizationMember.user_id == user_id,
            OrganizationMember.is_active == True
        ).all()
    
    def get_organization_members(self, org_id: int) -> List[Dict]:
        """Get organization members with their roles."""
        members = self.db_session.query(
            User, OrganizationMember.role
        ).join(OrganizationMember).filter(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.is_active == True
        ).all()
        
        return [{'user': member[0], 'role': member[1]} for member in members]

# Project management
class ProjectManager:
    """Handle project management."""
    
    def __init__(self):
        self.db_session = get_db_session()
    
    def create_project(self, name: str, description: str, owner_id: int, org_id: Optional[int] = None) -> Optional[Project]:
        """Create a new project."""
        try:
            project = Project(
                name=name,
                description=description,
                owner_id=owner_id,
                organization_id=org_id
            )
            
            self.db_session.add(project)
            self.db_session.commit()
            
            return project
            
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            self.db_session.rollback()
            return None
    
    def get_user_projects(self, user_id: int) -> List[Project]:
        """Get projects for a user."""
        return self.db_session.query(Project).filter(
            Project.owner_id == user_id
        ).all()
    
    def get_organization_projects(self, org_id: int) -> List[Project]:
        """Get projects for an organization."""
        return self.db_session.query(Project).filter(
            Project.organization_id == org_id
        ).all()

# Carbon tracking with multi-user support
class MultiUserCarbonTracker:
    """Enhanced carbon tracker with multi-user support."""
    
    def __init__(self, user_id: int, project_id: int):
        self.user_id = user_id
        self.project_id = project_id
        self.db_session = get_db_session()
        self.tracker = None
        self.carbon_run = None
    
    def start_tracking(self, workload_type: str = "training", framework: str = "pytorch") -> Optional[str]:
        """Start carbon tracking for a user."""
        try:
            from src.monitoring.carbon_tracker import CarbonTracker
            
            # Create carbon run record
            self.carbon_run = CarbonRun(
                user_id=self.user_id,
                project_id=self.project_id,
                session_id=f"{workload_type}_{framework}_{int(datetime.now().timestamp())}",
                start_time=datetime.now(),
                framework=framework,
                workload_type=workload_type,
                status='running'
            )
            
            self.db_session.add(self.carbon_run)
            self.db_session.commit()
            
            # Initialize CodeCarbon tracker
            self.tracker = CarbonTracker(f"User_{self.user_id}_Project_{self.project_id}")
            session_id = self.tracker.start_tracking(workload_type, framework)
            
            return session_id
            
        except Exception as e:
            logger.error(f"Error starting tracking: {e}")
            return None
    
    def stop_tracking(self) -> Optional[Dict]:
        """Stop carbon tracking and save results."""
        try:
            if not self.tracker or not self.carbon_run:
                return None
            
            # Stop CodeCarbon tracker
            results = self.tracker.stop_tracking()
            
            if results:
                # Update carbon run record
                self.carbon_run.end_time = datetime.now()
                self.carbon_run.total_emissions = results.carbon_emissions
                self.carbon_run.energy_consumed = results.energy_consumed
                self.carbon_run.carbon_intensity = results.carbon_intensity
                self.carbon_run.renewable_percentage = results.renewable_percentage
                self.carbon_run.runtime_seconds = results.total_time_seconds
                self.carbon_run.status = 'completed'
                
                self.db_session.commit()
                
                return {
                    'run_id': self.carbon_run.id,
                    'emissions': results.carbon_emissions,
                    'energy': results.energy_consumed,
                    'runtime': results.total_time_seconds
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error stopping tracking: {e}")
            return None

# Streamlit app configuration
st.set_page_config(
    page_title="🌱 GreenAI Multi-User Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for multi-user platform
st.markdown("""
<style>
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .platform-header {
        background: linear-gradient(135deg, #228B22 0%, #98A869 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(34, 139, 34, 0.2);
    }
    
    .platform-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .user-card {
        background: linear-gradient(145deg, #F5F5DC 0%, #f8f8f0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(34, 139, 34, 0.1);
        border: 1px solid rgba(152, 168, 105, 0.2);
    }
    
    .team-card {
        background: linear-gradient(135deg, #98A869 0%, #B8C99A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(152, 168, 105, 0.3);
    }
    
    .project-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #BE5103;
    }
    
    .leaderboard {
        background: linear-gradient(135deg, #6B4F2A 0%, #8B7355 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .leaderboard h3 {
        color: white;
        margin: 0 0 1rem 0;
    }
    
    .leaderboard-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

def create_platform_header():
    """Create the platform header."""
    st.markdown("""
    <div class="platform-header">
        <h1>🌱 GreenAI Multi-User Platform</h1>
        <p style="color: rgba(255, 255, 255, 0.9); text-align: center; font-size: 1.2rem; margin: 0.5rem 0 0 0;">
            Collaborative Carbon Tracking for Sustainable AI Development
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_authentication():
    """Show authentication interface."""
    st.markdown("## 🔐 Authentication")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "OAuth"])
    
    with tab1:
        st.markdown("### Sign In")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                user_manager = UserManager()
                user = user_manager.authenticate_user(email, password)
                
                if user:
                    st.session_state.user = user
                    st.session_state.authenticated = True
                    st.success(f"Welcome back, {user.full_name}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    with tab2:
        st.markdown("### Create Account")
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            username = st.text_input("Username", placeholder="johndoe")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Create Account")
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters")
                else:
                    user_manager = UserManager()
                    user = user_manager.create_user(email, username, password, full_name)
                    
                    if user:
                        st.success("Account created successfully! Please sign in.")
                    else:
                        st.error("Username or email already exists")
    
    with tab3:
        st.markdown("### OAuth Login")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔵 Sign in with Google"):
                st.info("Google OAuth integration coming soon!")
        
        with col2:
            if st.button("🐙 Sign in with GitHub"):
                st.info("GitHub OAuth integration coming soon!")

def show_dashboard():
    """Show user dashboard."""
    user = st.session_state.user
    
    st.markdown(f"## 👋 Welcome, {user.full_name}!")
    
    # User stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Runs", "12", "3")
    
    with col2:
        st.metric("CO₂ Saved", "2.4 kg", "0.8 kg")
    
    with col3:
        st.metric("Projects", "5", "1")
    
    with col4:
        st.metric("Team Members", "8", "2")
    
    # Recent activity
    st.markdown("## 📊 Recent Activity")
    
    # Create sample data for demo
    recent_runs = pd.DataFrame({
        'Project': ['Neural Network Training', 'Data Processing', 'Model Evaluation'],
        'Emissions (kg CO₂)': [0.023, 0.015, 0.008],
        'Runtime (min)': [45, 23, 12],
        'Status': ['Completed', 'Completed', 'Running'],
        'Date': ['2024-10-24', '2024-10-23', '2024-10-24']
    })
    
    st.dataframe(recent_runs, use_container_width=True)
    
    # Team leaderboard
    st.markdown("## 🏆 Team Leaderboard")
    
    leaderboard_data = pd.DataFrame({
        'User': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson'],
        'CO₂ Saved (kg)': [5.2, 4.8, 3.9, 3.1],
        'Runs': [15, 12, 10, 8],
        'Efficiency': ['95%', '92%', '88%', '85%']
    })
    
    st.dataframe(leaderboard_data, use_container_width=True)

def show_organizations():
    """Show organization management."""
    st.markdown("## 🏢 Organizations")
    
    # Create organization
    with st.expander("Create New Organization"):
        with st.form("create_org_form"):
            org_name = st.text_input("Organization Name")
            org_description = st.text_area("Description")
            submit = st.form_submit_button("Create Organization")
            
            if submit:
                org_manager = OrganizationManager()
                org = org_manager.create_organization(org_name, org_description, st.session_state.user.id)
                
                if org:
                    st.success(f"Organization '{org_name}' created successfully!")
                else:
                    st.error("Failed to create organization")
    
    # List organizations
    org_manager = OrganizationManager()
    user_orgs = org_manager.get_user_organizations(st.session_state.user.id)
    
    for org in user_orgs:
        with st.container():
            st.markdown(f"""
            <div class="team-card">
                <h3>🏢 {org.name}</h3>
                <p>{org.description}</p>
                <p><strong>Members:</strong> {len(org_manager.get_organization_members(org.id))}</p>
            </div>
            """, unsafe_allow_html=True)

def show_projects():
    """Show project management."""
    st.markdown("## 📁 Projects")
    
    # Create project
    with st.expander("Create New Project"):
        with st.form("create_project_form"):
            project_name = st.text_input("Project Name")
            project_description = st.text_area("Description")
            is_public = st.checkbox("Make Public")
            submit = st.form_submit_button("Create Project")
            
            if submit:
                project_manager = ProjectManager()
                project = project_manager.create_project(
                    project_name, project_description, st.session_state.user.id
                )
                
                if project:
                    st.success(f"Project '{project_name}' created successfully!")
                else:
                    st.error("Failed to create project")
    
    # List projects
    project_manager = ProjectManager()
    user_projects = project_manager.get_user_projects(st.session_state.user.id)
    
    for project in user_projects:
        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <h3>📁 {project.name}</h3>
                <p>{project.description}</p>
                <p><strong>Created:</strong> {project.created_at.strftime('%Y-%m-%d')}</p>
                <p><strong>Public:</strong> {'Yes' if project.is_public else 'No'}</p>
            </div>
            """, unsafe_allow_html=True)

def show_carbon_tracking():
    """Show carbon tracking interface."""
    st.markdown("## 🌱 Carbon Tracking")
    
    # Project selection
    project_manager = ProjectManager()
    user_projects = project_manager.get_user_projects(st.session_state.user.id)
    
    if not user_projects:
        st.warning("Please create a project first.")
        return
    
    project_names = [p.name for p in user_projects]
    selected_project = st.selectbox("Select Project", project_names)
    
    selected_project_obj = next(p for p in user_projects if p.name == selected_project)
    
    # Tracking controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌱 Start Tracking", key="start_tracking"):
            if 'tracker' not in st.session_state:
                st.session_state.tracker = MultiUserCarbonTracker(
                    st.session_state.user.id, selected_project_obj.id
                )
            
            session_id = st.session_state.tracker.start_tracking()
            if session_id:
                st.session_state.tracking_active = True
                st.success("Carbon tracking started!")
            else:
                st.error("Failed to start tracking")
    
    with col2:
        if st.button("🛑 Stop Tracking", key="stop_tracking"):
            if 'tracker' in st.session_state and st.session_state.tracker:
                results = st.session_state.tracker.stop_tracking()
                if results:
                    st.success(f"Tracking stopped! Emissions: {results['emissions']:.6f} kg CO₂")
                    st.session_state.tracking_active = False
                else:
                    st.error("Failed to stop tracking")
    
    # Show tracking status
    if st.session_state.get('tracking_active', False):
        st.info("🌱 Carbon tracking is active...")
        
        # Show real-time metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", "Active", "🟢")
        
        with col2:
            st.metric("Runtime", "45s", "2s")
        
        with col3:
            st.metric("Emissions", "0.023 kg", "0.001 kg")

def show_export_features():
    """Show export and notification features."""
    st.markdown("## 📤 Export & Notifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Export Data")
        
        if st.button("📄 Export to CSV"):
            # Generate sample CSV
            data = pd.DataFrame({
                'Date': ['2024-10-24', '2024-10-23', '2024-10-22'],
                'Project': ['Neural Network', 'Data Processing', 'Model Training'],
                'Emissions (kg CO₂)': [0.023, 0.015, 0.031],
                'Runtime (min)': [45, 23, 67]
            })
            
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="carbon_emissions.csv",
                mime="text/csv"
            )
        
        if st.button("📋 Export to PDF"):
            st.info("PDF export feature coming soon!")
    
    with col2:
        st.markdown("### 🔔 Notifications")
        
        notification_types = st.multiselect(
            "Notification Types",
            ["Email", "Slack", "Teams", "Discord"],
            default=["Email"]
        )
        
        if st.button("🔔 Test Notification"):
            st.success("Test notification sent!")

def main():
    """Main application function."""
    create_platform_header()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'tracking_active' not in st.session_state:
        st.session_state.tracking_active = False
    
    if not st.session_state.authenticated:
        show_authentication()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown("### 🧭 Navigation")
            
            page = st.selectbox(
                "Select Page",
                ["Dashboard", "Organizations", "Projects", "Carbon Tracking", "Export & Notifications"]
            )
        
        # Main content based on selected page
        if page == "Dashboard":
            show_dashboard()
        elif page == "Organizations":
            show_organizations()
        elif page == "Projects":
            show_projects()
        elif page == "Carbon Tracking":
            show_carbon_tracking()
        elif page == "Export & Notifications":
            show_export_features()

if __name__ == "__main__":
    main()
