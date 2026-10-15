@echo off
chcp 65001 >nul
title 反重力 Agent Token 监控系统 - 网页仪表盘
echo ========================================================
echo    正在启动 反重力 Agent Token 监控系统 (Web Dashboard)...
echo ========================================================
cd /d "%~dp0"
python -m antigravity_token_monitor web --port 8765
pause
