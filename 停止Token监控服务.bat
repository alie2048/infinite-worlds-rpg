@echo off
title 停止 Token 监控后台服务
color 0A
echo 正在检测并停止 Token 监控后台服务...

set "FOUND=0"
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":8765 " ') do (
    if not "%%a"=="0" (
        taskkill /f /pid %%a >nul 2>&1
        set "FOUND=1"
    )
)

if "%FOUND%"=="1" (
    echo [成功] 已关闭 Token 监控后台服务。
) else (
    echo [提示] 当前未检测到正在运行的监控服务。
)
timeout /t 2 >nul
exit
