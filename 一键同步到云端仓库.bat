@echo off
chcp 65001 >nul
title 诸天之旅 · 一键同步到云端仓库 (Git Sync)
color 0A

echo ========================================================
echo        🌌 无限系统·诸天之旅 - 云端 Git 自动同步工具
echo ========================================================
echo.

cd /d "%~dp0"

:: 自动补齐常见 Git 安装路径到当前会话
if exist "C:\Program Files\Git\cmd\git.exe" (
    set "PATH=C:\Program Files\Git\cmd;%PATH%"
) else if exist "C:\Program Files (x86)\Git\cmd\git.exe" (
    set "PATH=C:\Program Files (x86)\Git\cmd;%PATH%"
) else if exist "%LOCALAPPDATA%\Programs\Git\cmd\git.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%"
)

:: 检查是否存在 git
where git >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [错误] 未检测到 Git 环境，请先安装 Git！
    echo 常见路径未检测到 git.exe。
    echo.
    pause
    exit /b
)

:: 检查是否配置了远程仓库
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [提示] 检测到当前尚未绑定云端仓库 (GitHub / Gitee)。
    echo.
    echo 请先在 GitHub 或 Gitee 上新建一个空仓库。
    echo 然后将仓库地址粘贴在下方（支持 HTTPS 或 SSH 链接）：
    echo 例如：https://github.com/alie2048/infinite-worlds-rpg.git
    echo.
    set /p REPO_URL="请输入远程仓库地址: "
    if "%REPO_URL%"=="" (
        echo [取消] 未输入地址，同步终止。
        pause
        exit /b
    )
    git remote add origin %REPO_URL%
    git branch -M main
    echo.
    echo [成功] 已成功绑定远程仓库：%REPO_URL%
    echo.
)

echo [1/3] 正在扫描并暂存变动文件...
git add .

echo [2/3] 正在记录提交信息...
set "COMMIT_MSG=update: 推进章节与同步最新设定"
git commit -m "%COMMIT_MSG%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] 本地版本已更新：%COMMIT_MSG%
) else (
    echo [提示] 本地已是最新版本，无需额外 commit。
)

echo [3/3] 正在推送到云端 (main 分支)...
echo （提示：如首次推送弹出 GitHub 登录窗口，请在浏览器中点击 Authorize 确认授权）
git push -u origin main

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ========================================================
    echo  ✨ 同步成功！所有设定与小说章节已安全备份至云端。
    echo ========================================================
    echo.
    echo [在线阅读站]：https://alie2048.github.io/infinite-worlds-rpg/
    echo.
) else (
    color 0C
    echo.
    echo ========================================================
    echo [警告] 推送遇到问题，可能的原因：
    echo 1. 尚未登录 GitHub 账号或授权失败；
    echo 2. 网络无法连接 GitHub（可尝试开启代理加速）；
    echo 3. 远端有未拉取的更新，可执行: git pull --rebase origin main
    echo ========================================================
)

echo.
pause
