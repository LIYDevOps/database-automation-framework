# Database Automation Framework
#Project Structure 

.
├── README.md
├── backups
├── config
│   └── db_config.yaml
├── cron
├── logs
│   └── automation.log
├── requirements.txt
├── scripts
│   ├── db_connection_test.py
│   ├── db_health_check.py
│   └── slow_query_check.py
└── sql
    └── setup.sql

## Overview
This project demonstrates a production-style database automation framework
for PostgreSQL. It focuses on operational automation such as connectivity
validation, health checks, and slow query detection using Python.

The framework follows DevOps best practices including secure credential
handling, structured logging, and modular scripts.

---

## Tech Stack
- PostgreSQL
- Python 3
- psycopg2
- YAML
- Linux
- Git & GitHub

---

## Features

### 1. Secure Database Connectivity
- Uses a dedicated database user
- Credentials are injected via environment variables
- No secrets are committed to GitHub

### 2. Database Health Checks
- Validates database connectivity
- Verifies existence of critical tables
- Checks row counts for monitoring
- Logs health status

### 3. Slow Query Detection
- Measures query execution time
- Detects slow queries using configurable thresholds
- Logs warnings for performance issues

### 4. Logging
- Centralized file-based logging
- Separate log directory (ignored by Git)
- Production-style FileHandler usage


### USECASE
This framework simulates real-world database automation tasks performed by
DevOps and SRE teams, including monitoring, validation, and performance checks.



### Configuration

Install PostgresSQL and run the SQL DB Creation script
Databse configuration is stored in config/db_config.yaml

Note : Passwords are injected using env variables. 

### Scripts Execution 

Run the .py scripts to view the results for Database Healthchecks and Query Execution time. 

python3 scripts/db_connection_test.py
python3 scripts/db_health_check.py
python3 scripts/slow_query_check.py


### Logs 

Once the Scripts are executed logs are stored in the logs folder locally which is not pushed to git.  
