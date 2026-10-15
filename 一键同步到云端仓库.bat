@echo off
title 无限系统·诸天之旅 - 云端 Git 自动同步工具
color 0A
cd /d "%~dp0"

echo ========================================================
echo        无限系统·诸天之旅 - 云端 Git 自动同步工具
echo ========================================================
echo.

set "GIT_EXE=C:\Program Files\Git\cmd\git.exe"
if not exist "%GIT_EXE%" set "GIT_EXE=git"

echo [1/3] 正在扫描并暂存变动文件...
"%GIT_EXE%" add .

echo [2/3] 正在记录本地提交...
"%GIT_EXE%" commit -m "update: 推进章节与同步最新设定" >nul 2>&1
if errorlevel 1 (
    echo [提示] 本地已是最新，无新改动。
) else (
    echo [成功] 本地版本已更新。
)

echo [3/3] 正在推送到云端仓库 (main 分支)...
echo （提示：若首次推送弹出浏览器登录窗口，请点击 Authorize 确认授权）
echo.
"%GIT_EXE%" push origin main

if errorlevel 1 (
    color 0C
    echo.
    echo ========================================================
    echo [警告] 推送遇到问题：
    echo 1. 若弹出了网页，请确认是否已完成 GitHub 登录与授权；
    echo 2. 检查网络连接（或代理加速）；
    echo 3. 若远端有更新，可先执行: git pull origin main
    echo ========================================================
) else (
    color 0A
    echo.
    echo ========================================================
    echo   同步成功！所有设定与章节已安全备份至云端。
    echo ========================================================
    echo [在线阅读站] https://alie2048.github.io/infinite-worlds-rpg/
)

echo.
pause
