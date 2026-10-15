@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -m antigravity_token_monitor summary
echo.
echo 可用命令提示:
echo   python -m antigravity_token_monitor detail ^<ID^>  (查看指定对话逐轮明细)
echo   python -m antigravity_token_monitor watch         (实时盯盘监控)
echo   python -m antigravity_token_monitor web           (启动浏览器可视化仪表盘)
echo.
pause
