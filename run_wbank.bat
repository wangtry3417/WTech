@echo off
cd /d E:\wbank

REM Set database connection string (SQLAlchemy)
REM Change this to your actual Neon PostgreSQL URL
set dataurl=postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

REM Optional: customize ports
set HTTP_PORT=8080
set HTTPS_PORT=8443

echo [WBank] Starting server...
echo [WBank] HTTP: 0.0.0.0:%HTTP_PORT% ^(portproxy 80 -> %HTTP_PORT%^)
echo [WBank] HTTPS: 0.0.0.0:%HTTPS_PORT% ^(portproxy 443 -> %HTTPS_PORT%^)

python main.py

pause