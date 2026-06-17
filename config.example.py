"""
Local configuration - NOT committed to git.
Copy config.example.py to config.py and fill in your values.
"""
import os

DATABASE_URL = os.environ.get(
    "dataurl",
    "postgresql://user:password@host:port/dbname?sslmode=require"
)