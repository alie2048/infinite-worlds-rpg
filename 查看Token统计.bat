@echo off
title 反重力 Agent Token 统计系统
color 0A
cd /d "%~dp0"

set "PY_EXE=python"
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if exist "C:\Program Files\Python312\python.exe" set "PY_EXE=C:\Program Files\Python312\python.exe"

"%PY_EXE%" -m antigravity_token_monitor summary
echo.
echo 常用命令说明:
echo   "%PY_EXE%" -m antigravity_token_monitor watch    (实时盯盘动态刷新)
echo   "%PY_EXE%" -m antigravity_token_monitor web      (启动可视化网页仪表盘)
echo.
pause
