# 🌱 GreenAI Multi-User Platform - Deployment Guide

**Complete deployment guide for cloud platforms with multi-user support**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Platform Deployment](#cloud-platform-deployment)
5. [Database Setup](#database-setup)
6. [Security Configuration](#security-configuration)
7. [Monitoring & Logging](#monitoring--logging)
8. [Troubleshooting](#troubleshooting)
9. [Deployment Checklist](#deployment-checklist)

---

## 🚀 Prerequisites

### System Requirements
- **Python**: 3.9 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **PostgreSQL**: 13 or higher
- **Redis**: 6.0 or higher

### Cloud Platform Requirements
- **Heroku**: Account with PostgreSQL addon
- **AWS**: Account with RDS and ElastiCache
- **Google Cloud**: Account with Cloud SQL and Memorystore
- **Azure**: Account with Azure Database and Redis Cache

---

## 🏠 Local Development Setup

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd GreenAI

# Create virtual environment
python3 -m venv greenai
source greenai/bin/activate  # On Windows: greenai\Scripts\activate

# Install dependencies
pip install -r requirements_multi_user.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp env.production .env

# Edit environment variables
nano .env
```

### 3. Database Setup
```bash
# Start PostgreSQL and Redis with Docker
docker-compose up -d db redis

# Wait for services to be ready
docker-compose logs -f db

# Initialize database
python3 -c "
from multi_user_platform import get_db_engine, Base
engine = get_db_engine()
Base.metadata.create_all(engine)
print('Database initialized successfully!')
"
```

### 4. Run Application
```bash
# Start the multi-user platform
streamlit run multi_user_platform.py

# Or use Docker Compose
docker-compose up app
```

---

## 🐳 Docker Deployment

### 1. Build and Run
```bash
# Build the Docker image
docker build -t greenai-multi-user .

# Run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f app
```

### 2. Production Configuration
```bash
# Use production environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale the application
docker-compose up -d --scale app=3
```

### 3. Health Checks
```bash
# Check application health
curl http://localhost:8501/_stcore/health

# Check database connection
docker-compose exec app python3 -c "
from multi_user_platform import get_db_session
session = get_db_session()
print('Database connection: OK')
"
```

---

## ☁️ Cloud Platform Deployment

### 🟠 Heroku Deployment

#### 1. Prepare for Heroku
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create greenai-multi-user

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis addon
heroku addons:create heroku-redis:hobby-dev
```

#### 2. Configure Environment Variables
```bash
# Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set SMTP_HOST=smtp.gmail.com
heroku config:set SMTP_USER=your-email@gmail.com
heroku config:set SMTP_PASSWORD=your-app-password
```

#### 3. Deploy to Heroku
```bash
# Add Heroku remote
git remote add heroku https://git.heroku.com/greenai-multi-user.git

# Deploy
git push heroku main

# Run database migrations
heroku run python3 -c "
from multi_user_platform import get_db_engine, Base
engine = get_db_engine()
Base.metadata.create_all(engine)
"
```

### 🔵 AWS Deployment

#### 1. AWS Infrastructure
```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier greenai-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password your-password \
    --allocated-storage 20

# Create ElastiCache Redis cluster
aws elasticache create-cache-cluster \
    --cache-cluster-id greenai-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

#### 2. ECS Deployment
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name greenai-cluster

# Create task definition
aws ecs register-task-definition \
    --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
    --cluster greenai-cluster \
    --service-name greenai-service \
    --task-definition greenai-task \
    --desired-count 2
```

#### 3. Application Load Balancer
```bash
# Create ALB
aws elbv2 create-load-balancer \
    --name greenai-alb \
    --subnets subnet-12345 subnet-67890 \
    --security-groups sg-12345
```

### 🟢 Google Cloud Deployment

#### 1. Google Cloud Setup
```bash
# Set project
gcloud config set project your-project-id

# Enable required APIs
gcloud services enable cloudsql.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable run.googleapis.com
```

#### 2. Cloud SQL Setup
```bash
# Create Cloud SQL instance
gcloud sql instances create greenai-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create greenai --instance=greenai-db
```

#### 3. Cloud Run Deployment
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/greenai-multi-user

# Deploy to Cloud Run
gcloud run deploy greenai-multi-user \
    --image gcr.io/your-project/greenai-multi-user \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### 🔷 Azure Deployment

#### 1. Azure Resources
```bash
# Create resource group
az group create --name greenai-rg --location eastus

# Create PostgreSQL server
az postgres server create \
    --resource-group greenai-rg \
    --name greenai-db \
    --location eastus \
    --admin-user postgres \
    --admin-password your-password \
    --sku-name GP_Gen5_2

# Create Redis cache
az redis create \
    --resource-group greenai-rg \
    --name greenai-redis \
    --location eastus \
    --sku Basic \
    --vm-size c0
```

#### 2. Container Instances
```bash
# Deploy to Azure Container Instances
az container create \
    --resource-group greenai-rg \
    --name greenai-app \
    --image your-registry/greenai-multi-user \
    --ports 8501 \
    --environment-variables \
        DATABASE_URL=postgresql://postgres:password@greenai-db.postgres.database.azure.com:5432/greenai
```

---

## 🗄️ Database Setup

### PostgreSQL Configuration
```sql
-- Create database
CREATE DATABASE greenai;

-- Create user
CREATE USER greenai_user WITH PASSWORD 'your_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE greenai TO greenai_user;

-- Connect to database
\c greenai;

-- Run initialization script
\i init.sql;
```

### Redis Configuration
```bash
# Redis configuration for production
redis-cli CONFIG SET requirepass your_redis_password
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

---

## 🔒 Security Configuration

### 1. Environment Variables Security
```bash
# Generate secure keys
python3 -c "
import secrets
print('SECRET_KEY=' + secrets.token_urlsafe(32))
print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))
print('ENCRYPTION_KEY=' + secrets.token_urlsafe(32))
"
```

### 2. Database Security
```sql
-- Enable SSL for PostgreSQL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/path/to/server.crt';
ALTER SYSTEM SET ssl_key_file = '/path/to/server.key';

-- Restart PostgreSQL
SELECT pg_reload_conf();
```

### 3. Application Security
```python
# Add to your application
import ssl

# SSL configuration
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

# CORS configuration
CORS_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com"
]
```

---

## 📊 Monitoring & Logging

### 1. Application Monitoring
```python
# Add to multi_user_platform.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Initialize Sentry
sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### 2. Database Monitoring
```sql
-- Enable PostgreSQL logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';
```

### 3. Health Checks
```bash
# Application health check
curl -f http://localhost:8501/_stcore/health || exit 1

# Database health check
pg_isready -h localhost -p 5432 -U postgres

# Redis health check
redis-cli ping
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check database connectivity
python3 -c "
from multi_user_platform import get_db_session
try:
    session = get_db_session()
    print('Database connection: OK')
except Exception as e:
    print(f'Database connection failed: {e}')
"
```

#### 2. Redis Connection Issues
```bash
# Test Redis connection
redis-cli ping
# Should return: PONG
```

#### 3. Authentication Issues
```bash
# Check user creation
python3 -c "
from multi_user_platform import UserManager
um = UserManager()
user = um.create_user('test@example.com', 'testuser', 'password123', 'Test User')
print(f'User created: {user is not None}')
"
```

#### 4. Docker Issues
```bash
# Check Docker logs
docker-compose logs -f app

# Restart services
docker-compose restart

# Rebuild containers
docker-compose build --no-cache
```

### Performance Issues

#### 1. Database Performance
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Add indexes for performance
CREATE INDEX CONCURRENTLY idx_carbon_runs_user_time 
ON carbon_runs(user_id, start_time);
```

#### 2. Application Performance
```python
# Add caching
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_projects(user_id):
    # Cached function
    pass
```

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Database schema created
- [ ] Security keys generated
- [ ] SSL certificates installed
- [ ] Monitoring configured
- [ ] Backup strategy implemented

### Deployment
- [ ] Application deployed
- [ ] Database migrations run
- [ ] Health checks passing
- [ ] Load balancer configured
- [ ] SSL/TLS enabled
- [ ] Domain configured

### Post-Deployment
- [ ] User registration working
- [ ] Authentication working
- [ ] Carbon tracking functional
- [ ] Export features working
- [ ] Notifications working
- [ ] Performance acceptable

### Security Checklist
- [ ] Passwords hashed securely
- [ ] API keys secured
- [ ] Database access restricted
- [ ] HTTPS enabled
- [ ] CORS configured
- [ ] Rate limiting enabled

### Monitoring Checklist
- [ ] Application logs configured
- [ ] Database monitoring enabled
- [ ] Error tracking configured
- [ ] Performance metrics collected
- [ ] Alerting configured
- [ ] Backup verification

---

## 🚀 Quick Start Commands

### Local Development
```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### Production Deployment
```bash
# Deploy to Heroku
git push heroku main

# Deploy to AWS
aws ecs update-service --cluster greenai-cluster --service greenai-service --force-new-deployment

# Deploy to Google Cloud
gcloud run deploy greenai-multi-user --image gcr.io/your-project/greenai-multi-user

# Deploy to Azure
az container create --resource-group greenai-rg --name greenai-app --image your-registry/greenai-multi-user
```

---

## 📞 Support

### Getting Help
- **Documentation**: Check this guide and inline comments
- **Issues**: Create GitHub issues for bugs
- **Community**: Join our Discord server
- **Email**: support@greenai.com

### Useful Commands
```bash
# Check application status
docker-compose ps

# View application logs
docker-compose logs app

# Access application shell
docker-compose exec app bash

# Database shell
docker-compose exec db psql -U postgres -d greenai

# Redis shell
docker-compose exec redis redis-cli
```

---

**🌿 Built with ❤️ for the environment • Making AI Development Sustainable**

*Happy deploying! 🚀*
