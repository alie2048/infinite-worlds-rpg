"""
Antigravity Token Monitor - Web Dashboard Server
零依赖内置 Web 可视化仪表盘，提供实时 REST API 与现代化单页监控界面。
"""

import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional

from antigravity_token_monitor.core import TokenAnalyzer


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>反重力 Agent 平台 Token 实时监控系统</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f0f9ff',
              500: '#0284c7',
              600: '#0369a1',
              900: '#0c4a6e',
            }
          }
        }
      }
    }
  </script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
    .custom-scroll::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scroll::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
    .custom-scroll::-webkit-scrollbar-thumb:hover { background: #4b5563; }
  </style>
</head>
<body class="bg-gray-950 text-gray-100 min-h-screen custom-scroll">

  <!-- 顶部导航栏 -->
  <header class="border-b border-gray-800 bg-gray-900/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-lg bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20 font-black text-xl text-white">
          ⚡
        </div>
        <div>
          <h1 class="text-lg font-bold tracking-tight text-white flex items-center gap-2">
            反重力 Agent Token 监控系统
            <span class="text-xs px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-mono">Realtime</span>
          </h1>
          <p class="text-xs text-gray-400">Antigravity Platform Token Usage & Cost Analytics</p>
        </div>
      </div>
      <div class="flex items-center space-x-4">
        <div class="flex items-center space-x-2 text-xs text-gray-400">
          <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse" id="statusDot"></span>
          <span id="lastUpdated">正在同步...</span>
        </div>
        <button id="btnAutoRefresh" onclick="toggleAutoRefresh()" class="px-3 py-1.5 rounded-md text-xs font-medium bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 transition flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          <span id="refreshLabel">自动刷新 (3s)</span>
        </button>
        <button onclick="refreshData()" class="p-1.5 rounded-md text-gray-400 hover:text-white hover:bg-gray-800 transition" title="手动刷新">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
        </button>
        <a href="/api/export/csv" class="px-3 py-1.5 rounded-md text-xs font-medium bg-sky-600 hover:bg-sky-500 text-white shadow transition flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          导出 CSV
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

    <!-- KPI 核心指标卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- 累计流通总量 -->
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-sm relative overflow-hidden group">
        <div class="absolute -right-2 -bottom-2 opacity-5 text-gray-100 text-8xl font-black select-none pointer-events-none">Σ</div>
        <div class="text-xs font-semibold text-gray-400 tracking-wider uppercase mb-1">平台历史累计 Token</div>
        <div class="text-2xl font-bold text-white tracking-tight flex items-baseline gap-2">
          <span id="kpiTotalTokens">0</span>
          <span class="text-xs text-sky-400 font-normal">Tokens</span>
        </div>
        <div class="mt-3 pt-3 border-t border-gray-800/80 text-xs flex justify-between text-gray-400">
          <span>未缓存输入: <b id="kpiInputTokens" class="text-gray-200">0</b></span>
          <span>生成输出: <b id="kpiOutputTokens" class="text-amber-400">0</b></span>
        </div>
      </div>

      <!-- 缓存命中优化 -->
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-sm relative overflow-hidden">
        <div class="text-xs font-semibold text-gray-400 tracking-wider uppercase mb-1">Prompt 缓存节省率</div>
        <div class="text-2xl font-bold text-emerald-400 tracking-tight flex items-baseline gap-2">
          <span id="kpiCacheRate">0.0%</span>
          <span class="text-xs text-emerald-500/80 font-normal">高命中</span>
        </div>
        <div class="mt-3 pt-3 border-t border-gray-800/80 text-xs flex justify-between text-gray-400">
          <span>缓存命中 Tokens:</span>
          <b id="kpiCacheTokens" class="text-emerald-300">0</b>
        </div>
      </div>

      <!-- 各对话最新一轮汇总 -->
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-sm relative overflow-hidden">
        <div class="text-xs font-semibold text-gray-400 tracking-wider uppercase mb-1">各对话最新一轮合计</div>
        <div class="text-2xl font-bold text-sky-400 tracking-tight flex items-baseline gap-2">
          <span id="kpiLatestTotal">0</span>
          <span class="text-xs text-sky-300 font-normal">Tokens</span>
        </div>
        <div class="mt-3 pt-3 border-t border-gray-800/80 text-xs flex justify-between text-gray-400">
          <span>最新轮新输入: <b id="kpiLatestInp" class="text-gray-200">0</b></span>
          <span>输出: <b id="kpiLatestOut" class="text-amber-400">0</b></span>
        </div>
      </div>

      <!-- 会话与轮次统计 -->
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-sm relative overflow-hidden">
        <div class="text-xs font-semibold text-gray-400 tracking-wider uppercase mb-1">对话与交互总览</div>
        <div class="text-2xl font-bold text-white tracking-tight flex items-baseline gap-2">
          <span id="kpiConvCount">0</span>
          <span class="text-xs text-gray-400 font-normal">个对话</span>
        </div>
        <div class="mt-3 pt-3 border-t border-gray-800/80 text-xs flex justify-between text-gray-400">
          <span>总轮次: <b id="kpiTurnsCount" class="text-gray-200">0</b> 轮</span>
          <span>模型调用: <b id="kpiModelCalls" class="text-sky-400">0</b> 次</span>
        </div>
      </div>
    </div>

    <!-- 图表区 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 各会话 Token 分布对比图 (柱状) -->
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 lg:col-span-2">
        <h3 class="text-sm font-semibold text-gray-200 mb-4 flex items-center justify-between">
          <span>📊 各对话 Token 构成对比 (最新一轮 vs 历史累计)</span>
          <span class="text-xs text-gray-500 font-normal">单位: Token</span>
        </h3>
        <div class="h-64">
          <canvas id="convBarChart"></canvas>
        </div>
      </div>

      <!-- 全局 Token 结构占比 (环形图) -->
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 class="text-sm font-semibold text-gray-200 mb-4">🍩 全平台 Token 构成占比</h3>
        <div class="h-64 flex items-center justify-center">
          <canvas id="tokenPieChart"></canvas>
        </div>
      </div>
    </div>

    <!-- 对话列表与明细表格 -->
    <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden shadow">
      <div class="p-5 border-b border-gray-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-base font-bold text-white">📑 对话列表及实时用量统计</h2>
          <p class="text-xs text-gray-400 mt-0.5">点击任意行可展开查看该会话从第一轮到最新一轮的演进走势及步骤详情</p>
        </div>
        <div class="flex items-center gap-3">
          <input type="text" id="searchInput" oninput="filterConversations()" placeholder="搜索会话标题或 ID..." 
                 class="px-3 py-1.5 bg-gray-950 border border-gray-700 rounded-lg text-xs text-gray-200 focus:outline-none focus:border-sky-500 w-64" />
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-gray-800 bg-gray-950/60 text-gray-400 font-medium uppercase tracking-wider">
              <th class="py-3 px-4">对话名称 / ID</th>
              <th class="py-3 px-3 text-center">轮数</th>
              <th class="py-3 px-4 bg-sky-950/20 text-sky-300 border-l border-sky-900/30">
                ⭐ 当前最新一轮 (Token)
                <div class="text-[10px] font-normal text-sky-400/70">新输入 / 缓存命中 / 生成输出 / 当前上下文深度</div>
              </th>
              <th class="py-3 px-4 bg-indigo-950/20 text-indigo-300 border-l border-indigo-900/30">
                📈 历史累计 (Token)
                <div class="text-[10px] font-normal text-indigo-400/70">新输入 / 缓存读取 / 生成输出 / 累计总量</div>
              </th>
              <th class="py-3 px-3 text-center">缓存率</th>
              <th class="py-3 px-3">状态 / 最后更新</th>
              <th class="py-3 px-3 text-right">操作</th>
            </tr>
          </thead>
          <tbody id="conversationTableBody" class="divide-y divide-gray-800/60 font-mono">
            <!-- 动态填充 -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- 详情抽屉/弹窗 (Modal) -->
  <div id="detailModal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-gray-900 border border-gray-700 rounded-2xl w-full max-w-5xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
      <!-- 模态框头部 -->
      <div class="p-5 border-b border-gray-800 flex items-center justify-between bg-gray-950/80">
        <div>
          <div class="flex items-center gap-3">
            <h3 class="text-base font-bold text-white" id="modalTitle">对话详情</h3>
            <span class="text-xs font-mono px-2 py-0.5 rounded bg-gray-800 text-gray-400" id="modalConvId">ID</span>
          </div>
          <p class="text-xs text-gray-400 mt-1" id="modalMeta">更新时间: -</p>
        </div>
        <button onclick="closeModal()" class="text-gray-400 hover:text-white p-1 rounded-lg hover:bg-gray-800 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <!-- 模态框主体内容 -->
      <div class="p-6 overflow-y-auto space-y-6 custom-scroll">
        <!-- 弹窗内 KPI 卡片 -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4" id="modalKpis">
          <!-- 动态填充 -->
        </div>

        <!-- 轮次上下文演进折线图 -->
        <div class="bg-gray-950 border border-gray-800 rounded-xl p-4">
          <h4 class="text-xs font-semibold text-gray-300 mb-3 flex items-center justify-between">
            <span>📈 逐轮 Token 消耗与 Prompt 上下文增长曲线</span>
            <span class="text-[10px] text-gray-500">横轴: 轮次 (Turn)</span>
          </h4>
          <div class="h-56">
            <canvas id="turnTrendChart"></canvas>
          </div>
        </div>

        <!-- 各轮次表格 -->
        <div class="space-y-3">
          <h4 class="text-sm font-semibold text-gray-200">📜 轮次明细清单 (Turn 1 ~ N)</h4>
          <div class="space-y-3" id="modalTurnsList">
            <!-- 动态填充 -->
          </div>
        </div>
      </div>

      <!-- 模态框底部 -->
      <div class="p-4 border-t border-gray-800 bg-gray-950 flex justify-end">
        <button onclick="closeModal()" class="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-lg text-xs font-medium transition">
          关闭窗口
        </button>
      </div>
    </div>
  </div>

  <script>
    let rawData = null;
    let autoRefreshTimer = null;
    let isAutoRefreshing = true;
    let barChartInstance = null;
    let pieChartInstance = null;
    let trendChartInstance = null;

    function formatNumber(num) {
      if (num === null || num === undefined) return '0';
      return Number(num).toLocaleString('en-US');
    }

    function formatShort(num) {
      if (!num) return '0';
      if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M';
      if (num >= 10000) return (num / 1000).toFixed(1) + 'k';
      return Number(num).toLocaleString('en-US');
    }

    async function fetchData() {
      try {
        const res = await fetch('/api/summary');
        if (!res.ok) throw new Error('Network error');
        const data = await res.json();
        rawData = data;
        renderDashboard(data);
        document.getElementById('lastUpdated').innerText = '最后同步: ' + new Date().toLocaleTimeString();
        document.getElementById('statusDot').className = 'inline-block w-2 h-2 rounded-full bg-emerald-400';
      } catch (err) {
        console.error(err);
        document.getElementById('statusDot').className = 'inline-block w-2 h-2 rounded-full bg-red-500';
        document.getElementById('lastUpdated').innerText = '同步异常';
      }
    }

    function renderDashboard(data) {
      const pCum = data.platform_cumulative_tokens;
      const lTot = data.latest_turns_total_tokens;

      // KPI 卡片
      document.getElementById('kpiTotalTokens').innerText = formatNumber(pCum.total_tokens);
      document.getElementById('kpiInputTokens').innerText = formatNumber(pCum.input_tokens);
      document.getElementById('kpiOutputTokens').innerText = formatNumber(pCum.output_tokens);

      document.getElementById('kpiCacheRate').innerText = (pCum.cache_hit_rate || 0) + '%';
      document.getElementById('kpiCacheTokens').innerText = formatNumber(pCum.cache_read_tokens);

      document.getElementById('kpiLatestTotal').innerText = formatNumber(lTot.total_tokens);
      document.getElementById('kpiLatestInp').innerText = formatNumber(lTot.input_tokens);
      document.getElementById('kpiLatestOut').innerText = formatNumber(lTot.output_tokens);

      document.getElementById('kpiConvCount').innerText = data.total_conversations;
      document.getElementById('kpiTurnsCount').innerText = data.total_turns;
      document.getElementById('kpiModelCalls').innerText = data.total_model_calls;

      // 渲染图表
      renderCharts(data);

      // 渲染表格
      renderTable(data.conversations);
    }

    function renderCharts(data) {
      const convs = data.conversations.slice(0, 8); // 取前8个
      const labels = convs.map(c => c.title.length > 12 ? c.title.slice(0, 10) + '..' : c.title);
      
      const latestData = convs.map(c => c.latest_turn ? c.latest_turn.tokens.total_tokens : 0);
      const cumulativeData = convs.map(c => c.cumulative_tokens.total_tokens);

      // 柱状图
      const barCtx = document.getElementById('convBarChart').getContext('2d');
      if (barChartInstance) barChartInstance.destroy();
      barChartInstance = new Chart(barCtx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: '当前最新一轮 Token',
              data: latestData,
              backgroundColor: 'rgba(56, 189, 248, 0.8)',
              borderRadius: 4
            },
            {
              label: '历史累计总 Token',
              data: cumulativeData,
              backgroundColor: 'rgba(99, 102, 241, 0.4)',
              borderColor: 'rgba(99, 102, 241, 0.9)',
              borderWidth: 1,
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#9ca3af', font: { size: 11 } } },
            tooltip: {
              callbacks: {
                label: ctx => `${ctx.dataset.label}: ${formatNumber(ctx.raw)} tokens`
              }
            }
          },
          scales: {
            x: { ticks: { color: '#9ca3af' }, grid: { display: false } },
            y: { ticks: { color: '#9ca3af', callback: v => formatShort(v) }, grid: { color: '#1f2937' } }
          }
        }
      });

      // 环形图 (Input, Cache, Output)
      const pieCtx = document.getElementById('tokenPieChart').getContext('2d');
      if (pieChartInstance) pieChartInstance.destroy();
      const p = data.platform_cumulative_tokens;
      pieChartInstance = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
          labels: ['未缓存输入 (Input)', 'Prompt 缓存命中 (Cache)', '生成输出 (Output)'],
          datasets: [{
            data: [p.input_tokens, p.cache_read_tokens, p.output_tokens],
            backgroundColor: [
              'rgba(14, 165, 233, 0.85)',
              'rgba(16, 185, 129, 0.85)',
              'rgba(245, 158, 11, 0.85)'
            ],
            borderColor: '#111827',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { color: '#9ca3af', font: { size: 11 } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.label}: ${formatNumber(ctx.raw)} tokens (${((ctx.raw / (p.total_tokens || 1)) * 100).toFixed(1)}%)`
              }
            }
          },
          cutout: '65%'
        }
      });
    }

    function renderTable(convs) {
      const tbody = document.getElementById('conversationTableBody');
      tbody.innerHTML = '';

      convs.forEach(c => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-gray-800/40 transition group cursor-pointer';
        tr.onclick = (e) => {
          if (e.target.tagName !== 'BUTTON') showDetail(c.conversation_id);
        };

        const lt = c.latest_turn ? c.latest_turn.tokens : null;
        const ct = c.cumulative_tokens;

        let ltCell = `<span class="text-gray-500 font-sans italic">无模型交互</span>`;
        if (lt) {
          ltCell = `
            <div class="flex items-center gap-2">
              <span class="text-sky-400" title="未缓存输入">${formatShort(lt.input_tokens)}</span> /
              <span class="text-emerald-400" title="缓存读取">${formatShort(lt.cache_read_tokens)}</span> /
              <span class="text-amber-400" title="生成输出">${formatShort(lt.output_tokens)}</span>
              <span class="ml-2 px-1.5 py-0.5 rounded text-[11px] bg-sky-950/80 text-sky-300 border border-sky-800/50" title="单次请求上下文深度">
                ctx: ${formatShort(c.latest_turn.latest_context_size)}
              </span>
            </div>
          `;
        }

        const cumCell = `
          <div class="flex items-center gap-2">
            <span class="text-sky-300" title="累计输入">${formatShort(ct.input_tokens)}</span> /
            <span class="text-emerald-300" title="累计缓存">${formatShort(ct.cache_read_tokens)}</span> /
            <span class="text-amber-300" title="累计输出">${formatShort(ct.output_tokens)}</span>
            <span class="ml-2 font-bold text-gray-100" title="累计流通总量">
              Σ ${formatShort(ct.total_tokens)}
            </span>
          </div>
        `;

        const hitRate = ct.cache_hit_rate;
        let hitRateBadge = `<span class="text-gray-400">${hitRate}%</span>`;
        if (hitRate >= 80) hitRateBadge = `<span class="text-emerald-400 font-semibold">${hitRate}%</span>`;
        else if (hitRate >= 50) hitRateBadge = `<span class="text-amber-400">${hitRate}%</span>`;

        tr.innerHTML = `
          <td class="py-3 px-4 font-sans">
            <div class="font-medium text-gray-200 group-hover:text-sky-300 flex items-center gap-1.5">
              ${c.is_subagent ? '<span class="text-[10px] px-1 py-0.2 rounded bg-purple-900/60 text-purple-300 border border-purple-700/50">Subagent</span>' : ''}
              ${c.title}
            </div>
            <div class="text-[11px] text-gray-500 font-mono mt-0.5">${c.conversation_id}</div>
          </td>
          <td class="py-3 px-3 text-center text-gray-300 font-sans font-semibold">${c.total_turns}</td>
          <td class="py-3 px-4 bg-sky-950/10 border-l border-sky-900/20">${ltCell}</td>
          <td class="py-3 px-4 bg-indigo-950/10 border-l border-indigo-900/20">${cumCell}</td>
          <td class="py-3 px-3 text-center">${hitRateBadge}</td>
          <td class="py-3 px-3 font-sans text-gray-400 text-[11px]">
            <div class="flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full ${c.status.includes('IDLE') ? 'bg-emerald-400' : 'bg-gray-400'}"></span>
              <span>${c.status.replace('CASCADE_RUN_STATUS_', '')}</span>
            </div>
            <div class="text-gray-500 text-[10px] mt-0.5">${c.last_modified_time.slice(0, 19).replace('T', ' ')}</div>
          </td>
          <td class="py-3 px-3 text-right">
            <button onclick="showDetail('${c.conversation_id}')" class="px-2.5 py-1 rounded bg-gray-800 hover:bg-sky-600 text-gray-300 hover:text-white transition text-xs font-sans">
              查看各轮详情
            </button>
          </td>
        `;

        tbody.appendChild(tr);
      });
    }

    function filterConversations() {
      if (!rawData) return;
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const filtered = rawData.conversations.filter(c => 
        c.title.toLowerCase().includes(q) || c.conversation_id.toLowerCase().includes(q)
      );
      renderTable(filtered);
    }

    function showDetail(convId) {
      if (!rawData) return;
      const conv = rawData.conversations.find(c => c.conversation_id === convId);
      if (!conv) return;

      document.getElementById('modalTitle').innerText = conv.title;
      document.getElementById('modalConvId').innerText = conv.conversation_id;
      document.getElementById('modalMeta').innerText = `最后活动: ${conv.last_modified_time.replace('T', ' ')} | 状态: ${conv.status}`;

      // 模态框 KPI
      const ct = conv.cumulative_tokens;
      const lt = conv.latest_turn ? conv.latest_turn.tokens : null;
      document.getElementById('modalKpis').innerHTML = `
        <div class="bg-gray-950 border border-gray-800 rounded-lg p-3">
          <div class="text-[11px] text-gray-400">历史累计总量</div>
          <div class="text-lg font-bold text-sky-400">${formatNumber(ct.total_tokens)}</div>
          <div class="text-[10px] text-gray-500 mt-1">净计费: ${formatNumber(ct.net_tokens)}</div>
        </div>
        <div class="bg-gray-950 border border-gray-800 rounded-lg p-3">
          <div class="text-[11px] text-gray-400">整体缓存节省率</div>
          <div class="text-lg font-bold text-emerald-400">${ct.cache_hit_rate}%</div>
          <div class="text-[10px] text-gray-500 mt-1">命中: ${formatShort(ct.cache_read_tokens)}</div>
        </div>
        <div class="bg-gray-950 border border-gray-800 rounded-lg p-3">
          <div class="text-[11px] text-gray-400">最新一轮流通 Token</div>
          <div class="text-lg font-bold text-amber-400">${lt ? formatNumber(lt.total_tokens) : '0'}</div>
          <div class="text-[10px] text-gray-500 mt-1">输出: ${lt ? formatNumber(lt.output_tokens) : '0'}</div>
        </div>
        <div class="bg-gray-950 border border-gray-800 rounded-lg p-3">
          <div class="text-[11px] text-gray-400">最新上下文占用深度</div>
          <div class="text-lg font-bold text-purple-400">${conv.latest_turn ? formatNumber(conv.latest_turn.latest_context_size) : '0'}</div>
          <div class="text-[10px] text-gray-500 mt-1">最大上下文深度</div>
        </div>
      `;

      // 趋势折线图
      const turnLabels = conv.turns.map(t => `T${t.turn_index}`);
      const ctxSizes = conv.turns.map(t => t.latest_context_size);
      const turnTotals = conv.turns.map(t => t.tokens.total_tokens);

      const trendCtx = document.getElementById('turnTrendChart').getContext('2d');
      if (trendChartInstance) trendChartInstance.destroy();
      trendChartInstance = new Chart(trendCtx, {
        type: 'line',
        data: {
          labels: turnLabels,
          datasets: [
            {
              label: '该轮最新上下文深度 (Context Size)',
              data: ctxSizes,
              borderColor: '#c084fc',
              backgroundColor: 'rgba(192, 132, 252, 0.1)',
              fill: true,
              tension: 0.3,
              borderWidth: 2
            },
            {
              label: '该轮消耗流通 Token (Turn Total)',
              data: turnTotals,
              borderColor: '#38bdf8',
              backgroundColor: 'transparent',
              borderDash: [4, 4],
              tension: 0.2,
              borderWidth: 2
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#9ca3af', font: { size: 11 } } },
            tooltip: {
              callbacks: {
                label: ctx => `${ctx.dataset.label}: ${formatNumber(ctx.raw)} tokens`
              }
            }
          },
          scales: {
            x: { ticks: { color: '#9ca3af' }, grid: { color: '#1f2937' } },
            y: { ticks: { color: '#9ca3af', callback: v => formatShort(v) }, grid: { color: '#1f2937' } }
          }
        }
      });

      // 轮次列表
      const listEl = document.getElementById('modalTurnsList');
      listEl.innerHTML = '';
      conv.turns.forEach((t, idx) => {
        const isLatest = (idx === conv.turns.length - 1);
        const card = document.createElement('div');
        card.className = `p-4 rounded-xl border ${isLatest ? 'bg-sky-950/20 border-sky-500/50 shadow-lg shadow-sky-500/10' : 'bg-gray-950 border-gray-800'}`;

        const tok = t.tokens;
        card.innerHTML = `
          <div class="flex items-start justify-between gap-4">
            <div class="flex-1">
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded text-xs font-mono font-bold ${isLatest ? 'bg-sky-500 text-white' : 'bg-gray-800 text-gray-300'}">
                  Turn #${t.turn_index} ${isLatest ? '★ 当前最新轮' : ''}
                </span>
                <span class="text-xs text-gray-500">${t.start_time.slice(0, 19).replace('T', ' ')}</span>
                <span class="text-xs text-gray-400">(${t.model_call_count} 次模型调用 / ${t.step_count} 个步骤)</span>
              </div>
              <div class="mt-2 text-xs text-gray-200 font-sans line-clamp-2">
                <span class="text-sky-400 font-medium">用户指令:</span> ${t.user_prompt_full || t.user_prompt}
              </div>
            </div>
            <div class="text-right font-mono text-xs">
              <div class="text-sm font-bold ${isLatest ? 'text-sky-300' : 'text-gray-200'}">
                本轮总计: ${formatNumber(tok.total_tokens)}
              </div>
              <div class="text-[11px] text-gray-400 mt-1 flex justify-end gap-2">
                <span>新输入: <b class="text-gray-300">${formatShort(tok.input_tokens)}</b></span>
                <span>缓存: <b class="text-emerald-400">${formatShort(tok.cache_read_tokens)}</b></span>
                <span>输出: <b class="text-amber-400">${formatShort(tok.output_tokens)}</b></span>
              </div>
              <div class="text-[11px] text-purple-400 mt-0.5">
                最新上下文: ${formatNumber(t.latest_context_size)}
              </div>
            </div>
          </div>
        `;
        listEl.appendChild(card);
      });

      document.getElementById('detailModal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('detailModal').classList.add('hidden');
    }

    function toggleAutoRefresh() {
      isAutoRefreshing = !isAutoRefreshing;
      const label = document.getElementById('refreshLabel');
      if (isAutoRefreshing) {
        label.innerText = '自动刷新 (3s)';
        autoRefreshTimer = setInterval(fetchData, 3000);
      } else {
        label.innerText = '已暂停刷新';
        if (autoRefreshTimer) clearInterval(autoRefreshTimer);
      }
    }

    function refreshData() {
      fetchData();
    }

    // 初始化运行
    fetchData();
    autoRefreshTimer = setInterval(fetchData, 3000);
  </script>
</body>
</html>
"""


class TokenHttpHandler(BaseHTTPRequestHandler):
    """内置轻量 HTTP 请求处理器"""

    analyzer: TokenAnalyzer = None

    def _send_response(self, content: bytes, content_type: str = "text/html; charset=utf-8", status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        if path in ("/", "/index.html"):
            content = HTML_TEMPLATE.encode("utf-8")
            self._send_response(content, "text/html; charset=utf-8")
            return

        if path == "/api/summary":
            summary = self.analyzer.get_summary()
            payload = json.dumps(summary.to_dict(), ensure_ascii=False).encode("utf-8")
            self._send_response(payload, "application/json; charset=utf-8")
            return

        if path.startswith("/api/conversation/"):
            conv_id = path.replace("/api/conversation/", "").strip()
            summary = self.analyzer.get_summary()
            target = next((c for c in summary.conversations if c.conversation_id == conv_id), None)
            if target:
                payload = json.dumps(target.to_dict(), ensure_ascii=False).encode("utf-8")
                self._send_response(payload, "application/json; charset=utf-8")
            else:
                self._send_response(b'{"error": "Not Found"}', "application/json; charset=utf-8", 404)
            return

        if path == "/api/export/csv":
            import io, csv
            summary = self.analyzer.get_summary()
            out = io.StringIO()
            writer = csv.writer(out)
            writer.writerow([
                "Conversation ID", "Title", "Status", "Is Subagent", "Total Turns", "Total Steps",
                "Latest Turn Index", "Latest Turn Input Tokens", "Latest Turn Cache Tokens", "Latest Turn Output Tokens",
                "Latest Turn Total Tokens", "Latest Context Size",
                "Cumulative Input Tokens", "Cumulative Cache Tokens", "Cumulative Output Tokens",
                "Cumulative Total Tokens", "Cumulative Net Tokens", "Cache Hit Rate (%)", "Last Modified"
            ])
            for c in summary.conversations:
                lt = c.latest_turn
                writer.writerow([
                    c.conversation_id, c.title, c.status, c.is_subagent, c.total_turns, c.step_count,
                    lt.turn_index if lt else 0,
                    lt.tokens.input_tokens if lt else 0,
                    lt.tokens.cache_read_tokens if lt else 0,
                    lt.tokens.output_tokens if lt else 0,
                    lt.tokens.total_tokens if lt else 0,
                    lt.latest_context_size if lt else 0,
                    c.cumulative_tokens.input_tokens,
                    c.cumulative_tokens.cache_read_tokens,
                    c.cumulative_tokens.output_tokens,
                    c.cumulative_tokens.total_tokens,
                    c.cumulative_tokens.net_tokens,
                    c.cumulative_tokens.cache_hit_rate,
                    c.last_modified_time
                ])
            csv_bytes = out.getvalue().encode("utf-8-sig")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=\"antigravity_token_summary.csv\"")
            self.send_header("Content-Length", str(len(csv_bytes)))
            self.end_headers()
            self.wfile.write(csv_bytes)
            return

        self._send_response(b'{"error": "Endpoint not found"}', "application/json; charset=utf-8", 404)

    def log_message(self, format, *args):
        # 静默常规日志，避免刷屏
        pass


def start_server(port: int = 8765, app_data_dir: Optional[str] = None):
    """启动轻量 HTTP 服务"""
    TokenHttpHandler.analyzer = TokenAnalyzer(app_data_dir=app_data_dir)
    server_address = ("127.0.0.1", port)
    try:
        httpd = HTTPServer(server_address, TokenHttpHandler)
    except OSError:
        # 如果端口被占用，尝试下一个端口
        port = port + 1
        server_address = ("127.0.0.1", port)
        httpd = HTTPServer(server_address, TokenHttpHandler)

    url = f"http://127.0.0.1:{port}"
    print(f"\n========================================================")
    print(f"🚀 反重力 Token 监控仪表盘已成功启动!")
    print(f"👉 仪表盘访问地址: {url}")
    print(f"👉 REST API 接口 : {url}/api/summary")
    print(f"👉 CSV 数据导出  : {url}/api/export/csv")
    print(f"========================================================\n")
    print(f"按 Ctrl+C 停止服务...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已平稳关闭。")
        httpd.server_close()
