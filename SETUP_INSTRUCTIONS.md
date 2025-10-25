# 🌱 GreenAI Multi-User Platform - Setup Instructions

**Step-by-step guide to get your multi-user carbon tracking platform running**

---

## 🚀 Quick Start (5 minutes)

### Option 1: Docker (Recommended)
```bash
# 1. Clone and navigate to project
cd /Users/vasudhajain/Desktop/GreenAI

# 2. Start everything with Docker
docker-compose up -d

# 3. Wait for services to start (30 seconds)
docker-compose logs -f

# 4. Access the application
open http://localhost:8501
```

### Option 2: Local Development
```bash
# 1. Activate virtual environment
source greenai/bin/activate

# 2. Install dependencies
pip install -r requirements_multi_user.txt

# 3. Set up environment
cp env.production .env

# 4. Start PostgreSQL and Redis (if not using Docker)
# Install PostgreSQL and Redis locally, or use Docker for just these services

# 5. Run the application
streamlit run multi_user_platform.py
```

---

## 📋 Detailed Setup Instructions

### Step 1: Prerequisites Check

#### Required Software
```bash
# Check Python version (3.9+ required)
python3 --version

# Check Docker
docker --version
docker-compose --version

# Check if virtual environment exists
ls -la greenai/
```

#### Install Missing Dependencies
```bash
# If Python < 3.9, install Python 3.9+
# If Docker not installed:
# macOS: brew install docker docker-compose
# Ubuntu: sudo apt install docker.io docker-compose
```

### Step 2: Environment Setup

#### Create Environment File
```bash
# Copy the production environment template
cp env.production .env

# Edit the environment file
nano .env
```

#### Essential Environment Variables
```bash
# Database (use defaults for local development)
DATABASE_URL=postgresql://postgres:password@localhost:5432/greenai
DB_HOST=localhost
DB_PORT=5432
DB_NAME=greenai
DB_USER=postgres
DB_PASSWORD=password

# Security (generate your own keys)
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Email (optional for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# OAuth (optional for Google/GitHub login)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

### Step 3: Database Setup

#### Option A: Using Docker (Recommended)
```bash
# Start only database services
docker-compose up -d db redis

# Wait for database to be ready
docker-compose logs -f db

# Initialize database schema
docker-compose exec app python3 -c "
from multi_user_platform import get_db_engine, Base
engine = get_db_engine()
Base.metadata.create_all(engine)
print('Database initialized successfully!')
"
```

#### Option B: Local PostgreSQL
```bash
# Install PostgreSQL locally
# macOS: brew install postgresql
# Ubuntu: sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
# macOS: brew services start postgresql
# Ubuntu: sudo systemctl start postgresql

# Create database
createdb greenai

# Run initialization script
psql -d greenai -f init.sql
```

### Step 4: Install Python Dependencies

#### Install Requirements
```bash
# Activate virtual environment
source greenai/bin/activate

# Install all dependencies
pip install -r requirements_multi_user.txt

# If you get errors, install individually:
pip install streamlit streamlit-authenticator psycopg2-binary sqlalchemy
pip install plotly pandas numpy weasyprint reportlab
pip install python-dotenv bcrypt cryptography
```

#### Fix Common Installation Issues
```bash
# If psycopg2 fails:
pip install psycopg2-binary

# If weasyprint fails (macOS):
brew install cairo pango gdk-pixbuf libffi

# If weasyprint fails (Ubuntu):
sudo apt install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev

# If reportlab fails:
pip install reportlab --upgrade
```

### Step 5: Start the Application

#### Method 1: Docker (Easiest)
```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f app

# Access application
open http://localhost:8501
```

#### Method 2: Local Development
```bash
# Start database services only
docker-compose up -d db redis

# Start the application
source greenai/bin/activate
streamlit run multi_user_platform.py
```

### Step 6: Verify Installation

#### Check Application Status
```bash
# Check if application is running
curl http://localhost:8501/_stcore/health

# Check database connection
python3 -c "
from multi_user_platform import get_db_session
session = get_db_session()
print('Database connection: OK')
"

# Check Redis connection
redis-cli ping
```

#### Test Features
1. **Open the application**: http://localhost:8501
2. **Create an account**: Click "Register" tab
3. **Login**: Use your credentials
4. **Create an organization**: Go to Organizations page
5. **Start carbon tracking**: Go to Carbon Tracking page

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Module not found" errors
```bash
# Solution: Install missing dependencies
pip install -r requirements_multi_user.txt

# Or install individually:
pip install streamlit streamlit-authenticator psycopg2-binary sqlalchemy
```

#### Issue 2: Database connection failed
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

#### Issue 3: Redis connection failed
```bash
# Check if Redis is running
docker-compose ps

# Restart Redis
docker-compose restart redis

# Check Redis logs
docker-compose logs redis
```

#### Issue 4: Port 8501 already in use
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use different port
streamlit run multi_user_platform.py --server.port 8502
```

#### Issue 5: Permission denied errors
```bash
# Fix file permissions
chmod +x *.py
chmod 755 .

# Fix Docker permissions (if using Docker)
sudo chown -R $USER:$USER .
```

### Database Issues

#### Reset Database
```bash
# Stop services
docker-compose down

# Remove database volume
docker volume rm greenai_postgres_data

# Start services again
docker-compose up -d

# Reinitialize database
docker-compose exec app python3 -c "
from multi_user_platform import get_db_engine, Base
engine = get_db_engine()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print('Database reset successfully!')
"
```

#### Check Database Schema
```bash
# Connect to database
docker-compose exec db psql -U postgres -d greenai

# List tables
\dt

# Check users table
SELECT * FROM users;

# Exit
\q
```

### Application Issues

#### Check Application Logs
```bash
# Docker logs
docker-compose logs -f app

# Local logs (if running locally)
# Check terminal output where you ran streamlit
```

#### Restart Application
```bash
# Docker restart
docker-compose restart app

# Local restart
# Stop with Ctrl+C, then restart:
streamlit run multi_user_platform.py
```

---

## 🧪 Testing the Platform

### Test User Registration
1. Open http://localhost:8501
2. Click "Register" tab
3. Fill in the form:
   - Full Name: Test User
   - Username: testuser
   - Email: test@example.com
   - Password: password123
4. Click "Create Account"
5. You should see "Account created successfully!"

### Test User Login
1. Click "Login" tab
2. Enter credentials:
   - Email: test@example.com
   - Password: password123
3. Click "Sign In"
4. You should see the dashboard

### Test Organization Creation
1. After login, go to "Organizations" page
2. Click "Create New Organization"
3. Fill in:
   - Organization Name: Test Organization
   - Description: Test organization for GreenAI
4. Click "Create Organization"
5. You should see the organization listed

### Test Carbon Tracking
1. Go to "Projects" page
2. Create a new project
3. Go to "Carbon Tracking" page
4. Select your project
5. Click "Start Tracking"
6. Wait a few seconds
7. Click "Stop Tracking"
8. You should see emission results

### Test Export Features
1. Go to "Export & Notifications" page
2. Try exporting data in different formats
3. Test notification settings

---

## 🚀 Production Deployment

### Heroku Deployment
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create greenai-multi-user

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set SMTP_USER=your-email@gmail.com
heroku config:set SMTP_PASSWORD=your-app-password

# Deploy
git add .
git commit -m "Deploy multi-user platform"
git push heroku main

# Run database migrations
heroku run python3 -c "
from multi_user_platform import get_db_engine, Base
engine = get_db_engine()
Base.metadata.create_all(engine)
"
```

### AWS Deployment
```bash
# Install AWS CLI
# Configure AWS credentials

# Create ECS cluster
aws ecs create-cluster --cluster-name greenai-cluster

# Create RDS database
aws rds create-db-instance \
    --db-instance-identifier greenai-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password your-password \
    --allocated-storage 20

# Deploy to ECS
# (Follow AWS ECS deployment guide)
```

---

## 📞 Getting Help

### If You're Stuck
1. **Check the logs**: `docker-compose logs -f`
2. **Verify environment**: Check `.env` file
3. **Test database**: `docker-compose exec db psql -U postgres -d greenai`
4. **Restart services**: `docker-compose restart`

### Common Commands
```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart app

# Access database
docker-compose exec db psql -U postgres -d greenai

# Access application shell
docker-compose exec app bash
```

### Support Resources
- **Documentation**: Check all `.md` files in the project
- **Issues**: Create GitHub issues for bugs
- **Community**: Join our Discord server
- **Email**: support@greenai.com

---

## ✅ Success Checklist

After following these steps, you should have:
- [ ] Application running on http://localhost:8501
- [ ] Database connected and initialized
- [ ] User registration working
- [ ] User login working
- [ ] Organization creation working
- [ ] Carbon tracking working
- [ ] Export features working
- [ ] All services healthy

---

**🌿 Ready to make AI development sustainable!**

*If you encounter any issues, check the troubleshooting section or create a GitHub issue.*
