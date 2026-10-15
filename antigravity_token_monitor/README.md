# 反重力平台 Token 统计与监控系统 (Antigravity Token Monitor)

专为 **Google Antigravity（反重力）Agent 平台** 设计的 Token 监控与计量系统。
全面支持统计每个对话的 **当前最新一轮（最新轮次消耗 & 上下文占用深度）** 与 **全量历史累计 Token**，并提供全平台全局汇总、实时终端盯盘、REST API 与现代可视化 Web 仪表盘。

---

## 🌟 核心特性

1. **精准区分“最新一轮”与“累计总量”**：
   - **当前最新一轮 (Latest Turn)**：精准界定从用户最新一次提问至该轮次结束的所有模型交互，展示本轮新输入 Token、Prompt 缓存命中 Token、模型生成输出 Token，以及**当前最后一次调用的上下文窗口深度 (Latest Context Size)**。
   - **历史累计总量 (Cumulative Total)**：统计该对话从创建至今全生命周期的流通 Token、净计费 Token 与总轮数。
2. **Gemini 提示词缓存（Prompt Cache）深度分析**：
   - 准确区分 `input_tokens`（未缓存输入）与 `cache_read_tokens`（缓存命中读取），直观呈现平台节省的成本与缓存命中率。
3. **主对话与子代理（Subagent）关联追踪**：
   - 自动解析 `conversation_summaries.db` 中的 `parent_conversation_id`，标识子代理对话。
4. **多端交互界面**：
   - **终端命令行 (CLI)**：支持彩色报表、紧凑千分位显示、实时轮询盯盘 (`watch` 模式)。
   - **Web 可视化仪表盘 (Dashboard)**：零依赖纯 Python 标准库内置 HTTP 服务 + 现代化深色质感前端，提供图表、时序演进曲线、轮次展开面板与数据导出。
   - **程序化集成**：提供 Python 核心 API、JSON 输出与 CSV 报表导出。
5. **零外部依赖（Zero Dependencies）**：
   - 100% 采用 Python 原生标准库（`http.server`, `sqlite3`, `json`, `dataclasses`, `urllib`），无需额外安装第三方 Python 包，解压即用。

---

## 🚀 快速开始

### 方式一：一键双击启动

- **启动 Web 仪表盘**：双击运行 [`启动Token监控仪表盘.bat`](file:///j:/gemini/%E5%90%AF%E5%8A%A8Token%E7%9B%91%E6%8E%A7%E4%BB%AA%E8%A1%A8%E7%9B%98.bat)，浏览器访问 `http://127.0.0.1:8765`。
- **查看终端报表**：双击运行 [`查看Token统计.bat`](file:///j:/gemini/%E6%9F%A5%E7%9C%8BToken%E7%BB%9F%E8%AE%A1.bat)。

### 方式二：命令行使用

在终端中切换到项目目录或任意能引用到该模块的路径：

```bash
# 1. 查看全平台各对话汇总表格（显示最新一轮与累计）
python -m antigravity_token_monitor summary

# 2. 查看当前最新活跃对话的详情
python -m antigravity_token_monitor current

# 3. 查看指定对话逐轮（Turn 1 ~ N）明细演进表
python -m antigravity_token_monitor detail <CONVERSATION_ID>

# 4. 实时动态盯盘模式 (每 3 秒自动刷新终端)
python -m antigravity_token_monitor watch --interval 3

# 5. 启动本地 Web 可视化仪表盘
python -m antigravity_token_monitor web --port 8765

# 6. 输出结构化 JSON 数据
python -m antigravity_token_monitor --json

# 7. 导出 CSV 报表文件
python -m antigravity_token_monitor --csv token_summary.csv
```

---

## 📊 指标口径说明

| 指标字段 | 说明 | 业务意义 |
| :--- | :--- | :--- |
| **最新一轮 (Latest Turn)** | 本对话最后一次用户输入所触发的交互周期 | 衡量最新交互的单次成本与复杂度 |
| **最新上下文深度 (Ctx Size)** | 本轮最后一次模型请求时的总 Prompt 长度（`input + cache`） | 监控是否接近模型上下文窗口上限 |
| **新输入 Token (Input)** | 本次模型推理重新编码的未缓存 Token | 计费的主要权重项之一 |
| **缓存读取 (Cache Read)** | 命中 Gemini Prompt 缓存的 Token 数量 | 享受高额折扣与低推理延迟的 Token |
| **生成输出 (Output)** | 模型回复生成的 Token 数量 | 模型生成内容的体量 |
| **累计流通总 Token (Gross)** | `Input + Cache + Output` 的历史全量总和 | 衡量对话整体的模型信息处理总量 |
| **缓存优化节省率** | `Cache Read / (Input + Cache Read) * 100%` | 反映 Prompt 缓存机制带来的经济效益 |

---

## 🛠️ 项目目录结构

```text
antigravity_token_monitor/
├── __init__.py           # 包初始化入口
├── __main__.py           # 命令行启动入口
├── core.py               # 核心解析引擎 (SQLite + JSONL 流式分析)
├── cli.py                # 终端命令行渲染界面与报表工具
├── server.py             # 零依赖 Web 仪表盘服务与 REST API
└── README.md             # 说明文档
```
