@echo off
title 反重力 Agent Token 监控系统 - 网页仪表盘
color 0A
cd /d "%~dp0"

set "PY_EXE=python"
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if exist "C:\Program Files\Python312\python.exe" set "PY_EXE=C:\Program Files\Python312\python.exe"

echo ========================================================
echo    正在启动 反重力 Agent Token 监控系统 (Web Dashboard)...
echo ========================================================
echo.
echo 服务地址: http://127.0.0.1:8765
echo 正在自动为您打开浏览器仪表盘...
echo （按 Ctrl+C 可停止监控服务）
echo.
start "" "http://127.0.0.1:8765"
"%PY_EXE%" -m antigravity_token_monitor web --port 8765
pause
