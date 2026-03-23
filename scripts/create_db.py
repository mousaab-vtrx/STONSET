#!/usr/bin/env python3
"""Create MySQL database if it doesn't exist."""
import os
import re
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
os.chdir(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.config import settings

# Parse DATABASE_URL: mysql+pymysql://user:pass@host:port/dbname
url = settings.DATABASE_URL
# Updated regex to handle optional password (empty string allowed)
m = re.match(r"mysql\+pymysql://([^:]+):([^@]*)@([^:]+):(\d+)/([^?\s]+)", url)
if not m:
    print("Could not parse DATABASE_URL:", url)
    sys.exit(1)

user, password, host, port, dbname = m.groups()

try:
    import pymysql
except ImportError:
    print("Installing pymysql for DB creation...")
    os.system(f"{sys.executable} -m pip install pymysql -q")
    import pymysql

try:
    conn = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
    )
    conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
    conn.close()
    print(f"✓ Database '{dbname}' ready")
except Exception as e:
    print(f"⚠ Could not create database: {e}")
    print("  Ensure MySQL is running and credentials are correct.")
    print(f"  DATABASE_URL: {url}")
    sys.exit(1)
