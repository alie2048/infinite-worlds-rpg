@echo off
title 启动 Token 监控后台服务
cd /d "%~dp0"

set "PYW_EXE=pythonw.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" set "PYW_EXE=%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python311\pythonw.exe" set "PYW_EXE=%LOCALAPPDATA%\Programs\Python\Python311\pythonw.exe"

:: 检查 8765 端口是否已经启动
netstat -ano | findstr /r ":8765 " >nul 2>&1
if errorlevel 1 (
    start "" "%PYW_EXE%" -m antigravity_token_monitor web --port 8765
)

:: 打开浏览器网页
start "" "http://127.0.0.1:8765"

:: 自动退出当前黑框，后台静默守护
exit
