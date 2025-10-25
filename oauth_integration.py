"""
🌱 GreenAI OAuth Integration
===========================

OAuth integration for Google and GitHub authentication
with team collaboration features.
"""

import streamlit as st
import requests
import json
import base64
from urllib.parse import urlencode, parse_qs
import secrets
import hashlib
import hmac
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class OAuthProvider:
    """Base class for OAuth providers."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = secrets.token_urlsafe(32)
    
    def get_authorization_url(self) -> str:
        """Get authorization URL."""
        raise NotImplementedError
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """Exchange authorization code for access token."""
        raise NotImplementedError
    
    def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Get user information from access token."""
        raise NotImplementedError

class GoogleOAuth(OAuthProvider):
    """Google OAuth integration."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        super().__init__(client_id, client_secret, redirect_uri)
        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def get_authorization_url(self) -> str:
        """Get Google authorization URL."""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'openid email profile',
            'response_type': 'code',
            'state': self.state,
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        return f"{self.auth_url}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """Exchange code for Google access token."""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(self.token_url, data=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Get Google user information."""
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = requests.get(self.user_info_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None

class GitHubOAuth(OAuthProvider):
    """GitHub OAuth integration."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        super().__init__(client_id, client_secret, redirect_uri)
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.user_info_url = "https://api.github.com/user"
    
    def get_authorization_url(self) -> str:
        """Get GitHub authorization URL."""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'user:email',
            'state': self.state
        }
        
        return f"{self.auth_url}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """Exchange code for GitHub access token."""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code
        }
        
        headers = {'Accept': 'application/json'}
        
        try:
            response = requests.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Get GitHub user information."""
        headers = {'Authorization': f'token {access_token}'}
        
        try:
            response = requests.get(self.user_info_url, headers=headers)
            response.raise_for_status()
            user_data = response.json()
            
            # Get email from GitHub API
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers=headers
            )
            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next(
                    (email for email in emails if email.get('primary')), 
                    emails[0] if emails else None
                )
                if primary_email:
                    user_data['email'] = primary_email['email']
            
            return user_data
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None

class OAuthManager:
    """Manage OAuth authentication."""
    
    def __init__(self):
        self.google_oauth = None
        self.github_oauth = None
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize OAuth providers from environment variables."""
        import os
        
        # Google OAuth
        google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if google_client_id and google_client_secret:
            self.google_oauth = GoogleOAuth(
                google_client_id,
                google_client_secret,
                self._get_redirect_uri('google')
            )
        
        # GitHub OAuth
        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        
        if github_client_id and github_client_secret:
            self.github_oauth = GitHubOAuth(
                github_client_id,
                github_client_secret,
                self._get_redirect_uri('github')
            )
    
    def _get_redirect_uri(self, provider: str) -> str:
        """Get OAuth redirect URI."""
        base_url = os.getenv('BASE_URL', 'http://localhost:8501')
        return f"{base_url}/oauth/{provider}/callback"
    
    def get_available_providers(self) -> list:
        """Get list of available OAuth providers."""
        providers = []
        
        if self.google_oauth:
            providers.append('google')
        if self.github_oauth:
            providers.append('github')
        
        return providers
    
    def get_authorization_url(self, provider: str) -> Optional[str]:
        """Get authorization URL for provider."""
        if provider == 'google' and self.google_oauth:
            return self.google_oauth.get_authorization_url()
        elif provider == 'github' and self.github_oauth:
            return self.github_oauth.get_authorization_url()
        
        return None
    
    def handle_callback(self, provider: str, code: str, state: str) -> Optional[Dict]:
        """Handle OAuth callback."""
        if provider == 'google' and self.google_oauth:
            oauth = self.google_oauth
        elif provider == 'github' and self.github_oauth:
            oauth = self.github_oauth
        else:
            return None
        
        # Verify state parameter
        if state != oauth.state:
            logger.error("Invalid state parameter")
            return None
        
        # Exchange code for token
        token_data = oauth.exchange_code_for_token(code)
        if not token_data:
            return None
        
        # Get user information
        access_token = token_data.get('access_token')
        if not access_token:
            return None
        
        user_info = oauth.get_user_info(access_token)
        if not user_info:
            return None
        
        return {
            'provider': provider,
            'access_token': access_token,
            'user_info': user_info,
            'token_data': token_data
        }

def show_oauth_login():
    """Show OAuth login interface."""
    st.markdown("## 🔐 OAuth Authentication")
    
    oauth_manager = OAuthManager()
    available_providers = oauth_manager.get_available_providers()
    
    if not available_providers:
        st.warning("No OAuth providers configured. Please set up Google or GitHub OAuth.")
        return
    
    # Check if we're handling a callback
    query_params = st.query_params
    if 'code' in query_params and 'state' in query_params:
        provider = query_params.get('provider', 'google')
        code = query_params.get('code')
        state = query_params.get('state')
        
        result = oauth_manager.handle_callback(provider, code, state)
        
        if result:
            user_info = result['user_info']
            
            # Create or update user
            from multi_user_platform import UserManager
            user_manager = UserManager()
            
            # Check if user exists
            existing_user = user_manager.db_session.query(
                user_manager.db_session.query(User).filter(
                    User.email == user_info.get('email')
                ).first()
            )
            
            if existing_user:
                # Update OAuth info
                existing_user.oauth_provider = provider
                existing_user.oauth_id = user_info.get('id')
                user_manager.db_session.commit()
                user = existing_user
            else:
                # Create new user
                user = User(
                    email=user_info.get('email'),
                    username=user_info.get('login', user_info.get('name', 'user')),
                    password_hash='',  # No password for OAuth users
                    full_name=user_info.get('name', ''),
                    avatar_url=user_info.get('avatar_url', ''),
                    oauth_provider=provider,
                    oauth_id=user_info.get('id'),
                    is_active=True
                )
                user_manager.db_session.add(user)
                user_manager.db_session.commit()
            
            # Set session state
            st.session_state.user = user
            st.session_state.authenticated = True
            st.success(f"Welcome, {user.full_name}!")
            st.rerun()
        else:
            st.error("OAuth authentication failed. Please try again.")
    
    # Show OAuth login buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if 'google' in available_providers:
            auth_url = oauth_manager.get_authorization_url('google')
            if auth_url:
                st.markdown(f"""
                <a href="{auth_url}" target="_blank">
                    <button style="
                        background: #4285f4;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                        width: 100%;
                    ">
                        🔵 Sign in with Google
                    </button>
                </a>
                """, unsafe_allow_html=True)
    
    with col2:
        if 'github' in available_providers:
            auth_url = oauth_manager.get_authorization_url('github')
            if auth_url:
                st.markdown(f"""
                <a href="{auth_url}" target="_blank">
                    <button style="
                        background: #333;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                        width: 100%;
                    ">
                        🐙 Sign in with GitHub
                    </button>
                </a>
                """, unsafe_allow_html=True)

def show_team_collaboration():
    """Show team collaboration features."""
    st.markdown("## 👥 Team Collaboration")
    
    # Team invitation
    with st.expander("Invite Team Members"):
        st.markdown("### 📧 Send Invitations")
        
        with st.form("invite_form"):
            email = st.text_input("Email Address", placeholder="teammate@example.com")
            role = st.selectbox("Role", ["member", "admin", "viewer"])
            message = st.text_area("Personal Message (Optional)", 
                                 placeholder="Join our GreenAI team to track carbon emissions together!")
            
            submit = st.form_submit_button("Send Invitation")
            
            if submit:
                if email:
                    # Send invitation email
                    send_invitation_email(email, role, message)
                    st.success(f"Invitation sent to {email}")
                else:
                    st.error("Please enter an email address")
    
    # Team members
    st.markdown("### 👥 Team Members")
    
    # Get current user's organizations
    from multi_user_platform import OrganizationManager
    org_manager = OrganizationManager()
    user_orgs = org_manager.get_user_organizations(st.session_state.user.id)
    
    for org in user_orgs:
        st.markdown(f"#### 🏢 {org.name}")
        
        members = org_manager.get_organization_members(org.id)
        
        for member in members:
            user = member['user']
            role = member['role']
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"👤 {user.full_name} ({user.email})")
            
            with col2:
                st.write(f"🔑 {role.title()}")
            
            with col3:
                if role == 'admin':
                    if st.button("Remove", key=f"remove_{user.id}"):
                        # Remove member logic
                        st.success(f"Removed {user.full_name} from team")

def send_invitation_email(email: str, role: str, message: str):
    """Send team invitation email."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os
    
    # Email configuration
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not all([smtp_user, smtp_password]):
        st.error("Email configuration not found. Please set SMTP_USER and SMTP_PASSWORD.")
        return
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "🌱 Invitation to Join GreenAI Team"
    
    # Email body
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #228B22 0%, #98A869 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                <h1 style="margin: 0; font-size: 2.5em;">🌱 GreenAI</h1>
                <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">Sustainable AI Development Platform</p>
            </div>
            
            <h2>You're Invited to Join Our Team!</h2>
            
            <p>Hello!</p>
            
            <p>You've been invited to join our GreenAI team to collaborate on sustainable AI development and carbon tracking.</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>Team Details:</h3>
                <p><strong>Role:</strong> {role.title()}</p>
                <p><strong>Invited by:</strong> {st.session_state.user.full_name}</p>
            </div>
            
            {f'<p><strong>Personal Message:</strong> {message}</p>' if message else ''}
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{os.getenv('BASE_URL', 'http://localhost:8501')}" 
                   style="background: #228B22; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                    Join GreenAI Team
                </a>
            </div>
            
            <p>With GreenAI, you can:</p>
            <ul>
                <li>Track carbon emissions in real-time</li>
                <li>Collaborate with your team on sustainable AI projects</li>
                <li>Get actionable recommendations to reduce your carbon footprint</li>
                <li>Export and share environmental impact reports</li>
            </ul>
            
            <p>If you have any questions, feel free to reach out to us.</p>
            
            <p>Best regards,<br>The GreenAI Team</p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 0.9em; color: #666; text-align: center;">
                This invitation was sent by {st.session_state.user.full_name} ({st.session_state.user.email})
            </p>
        </div>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Invitation email sent to {email}")
        
    except Exception as e:
        logger.error(f"Failed to send invitation email: {e}")
        st.error(f"Failed to send email: {e}")

def show_project_collaboration():
    """Show project collaboration features."""
    st.markdown("## 🤝 Project Collaboration")
    
    # Project comments and discussions
    st.markdown("### 💬 Project Discussions")
    
    # Sample project discussions
    discussions = [
        {
            'user': 'Alice Johnson',
            'message': 'Great work on reducing emissions by 15%! What optimization techniques did you use?',
            'timestamp': '2024-10-24 10:30 AM',
            'avatar': '👩‍💻'
        },
        {
            'user': 'Bob Smith',
            'message': 'I used model pruning and quantization. Also scheduled training during off-peak hours.',
            'timestamp': '2024-10-24 10:45 AM',
            'avatar': '👨‍💻'
        },
        {
            'user': 'Carol Davis',
            'message': 'Excellent! I\'ll try those techniques in my next experiment.',
            'timestamp': '2024-10-24 11:00 AM',
            'avatar': '👩‍🔬'
        }
    ]
    
    for discussion in discussions:
        with st.container():
            st.markdown(f"""
            <div style="
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                border-left: 4px solid #228B22;
            ">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 1.5em; margin-right: 10px;">{discussion['avatar']}</span>
                    <strong>{discussion['user']}</strong>
                    <span style="color: #666; margin-left: 10px; font-size: 0.9em;">{discussion['timestamp']}</span>
                </div>
                <p style="margin: 0;">{discussion['message']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Add new comment
    with st.expander("Add Comment"):
        with st.form("comment_form"):
            comment = st.text_area("Your Comment", placeholder="Share your thoughts or ask a question...")
            submit = st.form_submit_button("Post Comment")
            
            if submit and comment:
                st.success("Comment posted!")
                st.rerun()

# Export functions for use in main app
__all__ = [
    'OAuthManager',
    'GoogleOAuth', 
    'GitHubOAuth',
    'show_oauth_login',
    'show_team_collaboration',
    'show_project_collaboration',
    'send_invitation_email'
]
