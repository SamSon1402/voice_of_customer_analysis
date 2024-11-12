# Voice of Customer Analysis Platform

![voc-dashboard-alerts](https://github.com/user-attachments/assets/28bebafd-5a7a-4cc6-bbec-1b99d4a53f27)
![voc-dashboard-analytics (1)](https://github.com/user-attachments/assets/1f66455c-5271-413d-96eb-1863ffd1b6e9)
![voc-dashboard-analytics](https://github.com/user-attachments/assets/365d30cc-24d8-47a9-960f-37b66557d14c)
![voc-dashboard-customer-feedback](https://github.com/user-attachments/assets/a22e1371-a8af-491e-bb0d-52623f4ba7ea)
![voc-dashboard-main](https://github.com/user-attachments/assets/3961888f-cb3f-4a2d-a02f-63dcdc614861)
![voc-users-dashboard](https://github.com/user-attachments/assets/0a358490-fcbb-4006-b441-464ad08cb610)

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Dashboard Guide](#dashboard-guide)
- [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

A comprehensive Voice of Customer (VOC) Analysis platform that leverages advanced machine learning techniques to analyze customer feedback, provide real-time insights, and enable data-driven decision making.

### Status & Info
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red)
![License](https://img.shields.io/badge/license-MIT-green)

### Core Capabilities
- Real-time sentiment analysis
- Customer feedback processing
- Automated alert system
- Interactive analytics dashboard
- Multi-channel notifications

## Project Structure
```bash
voice_of_customer_analysis/
├── api/                 # FastAPI application
│   ├── routes/         # API endpoints
│   │   ├── alerts.py
│   │   ├── auth.py
│   │   ├── metrics.py
│   │   └── users.py
│   └── main.py
│
├── core/               # Core functionality
│   ├── config.py       # Configuration settings
│   ├── database.py     # Database connections
│   └── security.py     # Security utilities
│
├── models/             # Data models
│   ├── alert.py
│   ├── metric.py
│   └── user.py
│
├── services/           # Business logic
│   ├── alerts/
│   │   ├── channels/
│   │   ├── rules.py
│   │   └── processor.py
│   └── metrics/
│       ├── collector.py
│       └── processor.py
│
├── ui/                 # Streamlit interface
│   ├── pages/
│   │   ├── alerts.py
│   │   ├── metrics.py
│   │   └── users.py
│   └── main.py
│
└── utils/              # Utility functions
    ├── constants.py
    ├── formatters.py
    └── validators.py
```

## Features

### Real-time Analytics
```python
# Example: Real-time sentiment analysis
from services.metrics.processor import MetricsProcessor

processor = MetricsProcessor()
sentiment_score = processor.analyze_sentiment(feedback_text)
print(f"Sentiment Score: {sentiment_score}")
```

### Alert System
```python
# Example: Creating an alert rule
alert_rule = {
    "metric": "response_time",
    "condition": ">",
    "threshold": 500,
    "severity": "high"
}
alert_service.create_rule(alert_rule)
```

### User Management
```python
# Example: User creation
user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "role": "analyst"
}
user_service.create_user(user_data)
```

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Node.js 14+ (optional)

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/yourusername/voice_of_customer_analysis.git
cd voice_of_customer_analysis
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup environment variables
```bash
cp .env.example .env
# Edit .env with your configurations
```

5. Initialize database
```bash
python scripts/init_db.py
```

## Configuration

### Environment Variables
```env
# Application
APP_NAME=VOC Analytics
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/voc_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Services
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
SLACK_WEBHOOK_URL=your-webhook-url
```

## Usage

### Starting the Application

1. Start the API server
```bash
uvicorn api.main:app --reload --port 8000
```

2. Launch the dashboard
```bash
streamlit run ui/main.py
```

3. Start background workers
```bash
celery -A worker.celery worker --loglevel=info
```

### Docker Deployment
```bash
# Build and run all services
docker-compose up -d
```

## API Reference

### Authentication
```bash
POST /api/v1/auth/login
POST /api/v1/auth/refresh
```

### Metrics
```bash
GET  /api/v1/metrics
POST /api/v1/metrics
```

### Alerts
```bash
GET  /api/v1/alerts
POST /api/v1/alerts/rules
```

### Users
```bash
GET  /api/v1/users
POST /api/v1/users
```

## Dashboard Guide

### Metrics Dashboard
- Real-time metrics visualization
- Custom metric creation
- Trend analysis
- Data filtering

### Alert Management
- Active alerts view
- Alert rule configuration
- Alert history tracking
- Notification settings

### User Management
- User administration
- Role management
- Activity monitoring
- Access control

## Advanced Usage

### Custom Metric Creation
```python
from services.metrics import MetricsCollector

collector = MetricsCollector()
collector.create_custom_metric(
    name="customer_satisfaction",
    calculation="avg",
    source="feedback_ratings"
)
```

### Alert Rule Configuration
```python
from services.alerts import AlertProcessor

processor = AlertProcessor()
processor.create_rule({
    "name": "High Response Time",
    "metric": "response_time_ms",
    "condition": ">",
    "threshold": 500,
    "window_minutes": 5,
    "severity": "high",
    "channels": ["email", "slack"]
})
```

### Data Export
```python
from services.metrics import MetricsExporter

exporter = MetricsExporter()
exporter.export_to_csv(
    metric_name="customer_feedback",
    start_date="2024-01-01",
    end_date="2024-01-31",
    format="csv"
)
```

## Contributing

1. Fork the repository
2. Create your feature branch
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes
```bash
git commit -m 'Add some AmazingFeature'
```
4. Push to the branch
```bash
git push origin feature/AmazingFeature
```
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation
- Use type hints
- Keep functions focused and small

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [docs.vocanalytics.com](https://docs.vocanalytics.com)
- Email: support@vocanalytics.com
- Issues: [GitHub Issues](https://github.com/yourusername/voice_of_customer_analysis/issues)

## Acknowledgments

- FastAPI team for the excellent framework
- Streamlit team for the amazing dashboard capabilities
- HuggingFace for transformer models
- Open source community for various tools and libraries


