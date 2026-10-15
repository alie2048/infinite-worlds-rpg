---
name: token-stats
description: 反重力平台 Token 统计与监控系统。可精准统计每个对话当前最新一轮（输入/缓存读取/输出/最新上下文深度）以及历史累计的 Token 消耗量，支持终端报表、JSON API 与 Web 可视化仪表盘。
---

# 反重力 Token 监控系统 (Antigravity Token Monitor)

为反重力（Antigravity）Agent 平台量身打造的 Token 统计分析系统。通过实时解析 `conversation_summaries.db` 与 `transcript.jsonl`，精确计算每轮交互（Turn）的模型调用量、未缓存新输入（Input）、Prompt 缓存命中读取（Cache Read）、模型生成输出（Output）以及累计流通总量。

## 快速使用

### 1. 终端命令行查看

- **查看全平台所有对话概览（最新一轮 + 累计）**：
  ```bash
  python -m antigravity_token_monitor summary
  ```
- **查看当前活跃会话的最新一轮与累计情况**：
  ```bash
  python -m antigravity_token_monitor current
  ```
- **查看指定对话各轮次详细演进历史（Turn 1 ~ N）**：
  ```bash
  python -m antigravity_token_monitor detail <CONVERSATION_ID>
  ```
- **进入实时盯盘模式（动态监控每秒/每轮变化）**：
  ```bash
  python -m antigravity_token_monitor watch --interval 3
  ```
- **输出 JSON 数据（方便程序集成）**：
  ```bash
  python -m antigravity_token_monitor --json
  ```
- **导出 CSV 报表**：
  ```bash
  python -m antigravity_token_monitor --csv token_report.csv
  ```

### 2. 启动 Web 可视化仪表盘

- 双击工作区根目录的 [`启动Token监控仪表盘.bat`](file:///j:/gemini/%E5%90%AF%E5%8A%A8Token%E7%9B%91%E6%8E%A7%E4%BB%AA%E8%A1%A8%E7%9B%98.bat)，或运行：
  ```bash
  python -m antigravity_token_monitor web --port 8765
  ```
- 打开浏览器访问 `http://127.0.0.1:8765`，可享受：
  - 实时自动刷新（支持 3 秒自动轮询）
  - 全平台 Token 构成占比环形图
  - 最新一轮 vs 累计柱状对比图
  - 点击会话查看其每轮 Prompt 上下文深度增长曲线与单轮详细数据

## 核心指标含义

1. **最新一轮 Token (Latest Turn Tokens)**：
   - 从用户最近一次发送提问到该轮完成期间，所触发的所有模型 API 请求累积消耗。
   - **新输入 (Input Tokens)**：未命中缓存重新处理的 Prompt 部分。
   - **缓存命中 (Cache Read Tokens)**：Gemini 自动命中的 Prompt Cache 部分（大幅降低费用与延迟）。
   - **输出 (Output Tokens)**：模型生成的思考与回答 Token。
   - **最新上下文 (Latest Context Size)**：本轮最后一次模型请求时的实际上下文窗口总深度（`input + cache`）。
2. **历史累计 Token (Cumulative Tokens)**：
   - 该对话自创建起，所有轮次累加的总流通 Token。
3. **缓存节省率 (Cache Hit Rate)**：
   - 缓存读取量占全部 Prompt 处理量的百分比，通常在 80%~95% 之间。
