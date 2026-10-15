@echo off
chcp 65001 >nul
title 诸天之旅 · 一键同步到云端仓库 (Git Sync)
color 0A

echo ========================================================
echo        🌌 无限系统·诸天之旅 - 云端 Git 自动同步工具
echo ========================================================
echo.

cd /d "%~dp0"

:: 检查是否存在 git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [错误] 未检测到 Git 环境，请先安装 Git！
    pause
    exit /b
)

:: 检查是否配置了远程仓库
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [提示] 检测到当前尚未绑定云端仓库 (GitHub / Gitee)。
    echo.
    echo 请先在 GitHub 或 Gitee 上新建一个空仓库（建议设为 Private 私有仓库）。
    echo 然后将仓库地址粘贴在下方（支持 HTTPS 或 SSH 链接）：
    echo 例如：https://github.com/your-username/infinite-worlds-rpg.git
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
set COMMIT_MSG=update: 自动同步章节内容与设定 (%date% %time:~0,8%)
git commit -m "%COMMIT_MSG%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] 本地版本已更新：%COMMIT_MSG%
) else (
    echo [提示] 没有检测到新的文件改动。
)

echo [3/3] 正在推送到云端 (main 分支)...
git push -u origin main

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ========================================================
    echo  ✨ 同步成功！所有技能设定与小说章节已安全备份至云端。
    echo ========================================================
    echo.
    echo [温馨提示] 开启在线网页阅读器：
    echo 1. 打开您的 GitHub 仓库页面，点击【Settings】->【Pages】；
    echo 2. 在【Build and deployment】的 Branch 选【main】，文件夹选【/ (root)】并点击 Save；
    echo 3. 稍等 1~2 分钟，您就能获得一个专属的线上阅读器网址！
    echo.
) else (
    color 0C
    echo.
    echo [警告] 推送遇到问题，请检查网络（如 GitHub 访问权限或代理）。
    echo 如果远程仓库已有 README 或冲突，可尝试输入命令：git pull --rebase origin main
)

pause
