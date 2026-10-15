"""
Antigravity Token Monitor - CLI Interface
终端命令行工具：查看反重力Agent平台的会话Token统计、最新一轮与累计用量。
"""

import os
import sys
import time
import json
import argparse
from typing import Optional

# 确保在 Windows 控制台支持 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from antigravity_token_monitor.core import TokenAnalyzer, PlatformSummary, ConversationStats


class Colors:
    """ANSI 终端颜色（自动降级）"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    RED = "\033[31m"
    WHITE = "\033[37m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"


def format_num(val: int) -> str:
    """格式化数字为千分位"""
    return f"{val:,}"


def format_short_num(val: int) -> str:
    """紧凑显示大数字 (例如 12.5k, 1.2M)"""
    if val >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    if val >= 10_000:
        return f"{val / 1_000:.1f}k"
    return f"{val:,}"


def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
  ╔═════════════════════════════════════════════════════════════════════════════╗
  ║                ⚡ ANTIGRAVITY AGENT TOKEN MONITOR ⚡                        ║
  ║                   反重力平台 对话 Token 统计系统                           ║
  ╚═════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}"""
    print(banner)


def render_summary_table(summary: PlatformSummary):
    """渲染全平台会话统计表格"""
    print_banner()
    c = Colors

    # 全局 KPI 概览卡片
    p_cum = summary.platform_cumulative_tokens
    l_sum = summary.latest_turns_total_tokens
    
    print(f"\n{c.BOLD}📊 【全平台概览】{c.RESET} 扫描时间: {c.DIM}{summary.scan_time[:19].replace('T', ' ')}{c.RESET}")
    print(f"  ├─ 监控对话总数: {c.BOLD}{summary.total_conversations}{c.RESET} 个 (活跃: {c.GREEN}{summary.active_conversations_count}{c.RESET})")
    print(f"  ├─ 历史交互轮次: {c.BOLD}{summary.total_turns}{c.RESET} 轮 (LLM 调用共 {summary.total_model_calls} 次)")
    print(f"  ├─ 全平台历史累计 Token : {c.BOLD}{c.YELLOW}{format_num(p_cum.total_tokens)}{c.RESET} "
          f"[新输入: {format_num(p_cum.input_tokens)} | 缓存命中: {format_num(p_cum.cache_read_tokens)} | 生成输出: {format_num(p_cum.output_tokens)}]")
    print(f"  ├─ 缓存优化节省率 : {c.BOLD}{c.GREEN}{p_cum.cache_hit_rate}%{c.RESET} (大幅降低 API 计费成本与推理时延)")
    print(f"  └─ 各对话最新一轮 Token 合计 : {c.BOLD}{c.CYAN}{format_num(l_sum.total_tokens)}{c.RESET} "
          f"[新输入: {format_num(l_sum.input_tokens)} | 缓存命中: {format_num(l_sum.cache_read_tokens)} | 输出: {format_num(l_sum.output_tokens)}]")

    # 表格头部
    print(f"\n{c.BOLD}📑 【各对话 Token 统计明细】{c.RESET}")
    header = (
        f"{'#':<3} | "
        f"{'会话标题 (ID)':<32} | "
        f"{'轮数':<4} | "
        f"{'最新一轮 (新输入/缓存/输出/当前上下文)':<35} | "
        f"{'历史累计 (新输入/缓存/输出/总计)':<36} | "
        f"{'缓存率':<6}"
    )
    sep_len = 125
    print("─" * sep_len)
    print(f"{c.BOLD}{header}{c.RESET}")
    print("─" * sep_len)

    for idx, conv in enumerate(summary.conversations, start=1):
        # 标题处理
        title_str = conv.title
        if len(title_str) > 20:
            title_str = title_str[:18] + ".."
        title_with_id = f"{title_str} ({conv.conversation_id[:6]})"
        if conv.is_subagent:
            title_with_id = f"↳ [Sub] {title_with_id}"

        # 最新一轮
        if conv.latest_turn:
            lt = conv.latest_turn.tokens
            lt_str = (
                f"{c.CYAN}{format_short_num(lt.input_tokens)}{c.RESET}/"
                f"{c.GREEN}{format_short_num(lt.cache_read_tokens)}{c.RESET}/"
                f"{c.YELLOW}{format_short_num(lt.output_tokens)}{c.RESET} "
                f"(ctx:{c.BOLD}{format_short_num(conv.latest_turn.latest_context_size)}{c.RESET})"
            )
        else:
            lt_str = f"{c.DIM}无模型记录{c.RESET}"

        # 累计
        ct = conv.cumulative_tokens
        cum_str = (
            f"{c.CYAN}{format_short_num(ct.input_tokens)}{c.RESET}/"
            f"{c.GREEN}{format_short_num(ct.cache_read_tokens)}{c.RESET}/"
            f"{c.YELLOW}{format_short_num(ct.output_tokens)}{c.RESET} "
            f"Σ:{c.BOLD}{c.YELLOW}{format_short_num(ct.total_tokens)}{c.RESET}"
        )

        hit_rate_str = f"{ct.cache_hit_rate:>5.1f}%"
        if ct.cache_hit_rate >= 80:
            hit_rate_str = f"{c.GREEN}{hit_rate_str}{c.RESET}"
        elif ct.cache_hit_rate >= 50:
            hit_rate_str = f"{c.YELLOW}{hit_rate_str}{c.RESET}"
        else:
            hit_rate_str = f"{c.DIM}{hit_rate_str}{c.RESET}"

        row = (
            f"{idx:<3} | "
            f"{title_with_id:<32} | "
            f"{conv.total_turns:<4} | "
            f"{lt_str:<44} | "
            f"{cum_str:<48} | "
            f"{hit_rate_str}"
        )
        print(row)

    print("─" * sep_len)
    print(f"{c.DIM}提示: 输入 / 缓存 / 输出 / 上下文深度 (ctx) 均为 Token 量。使用 'python -m antigravity_token_monitor detail <ID>' 查看单会话每轮明细。{c.RESET}\n")


def render_conversation_detail(conv: ConversationStats):
    """渲染指定会话的完整轮次详情"""
    c = Colors
    print_banner()

    print(f"\n{c.BOLD}🔍 【对话详情】 {conv.title}{c.RESET}")
    print(f"  ├─ 会话 ID : {c.CYAN}{conv.conversation_id}{c.RESET}")
    print(f"  ├─ 运行状态 : {conv.status}")
    print(f"  ├─ 总轮数 : {conv.total_turns} 轮 (包含 {conv.step_count} 个 Step，{conv.total_model_calls} 次模型调用)")
    print(f"  └─ 最后更新时间 : {conv.last_modified_time}")

    ct = conv.cumulative_tokens
    print(f"\n{c.BOLD}📈 【历史累计 Token 消耗】{c.RESET}")
    print(f"  ├─ 新输入 Token (Input)    : {c.BOLD}{format_num(ct.input_tokens)}{c.RESET}")
    print(f"  ├─ 缓存读取 Token (Cache)  : {c.BOLD}{c.GREEN}{format_num(ct.cache_read_tokens)}{c.RESET}")
    print(f"  ├─ 生成输出 Token (Output) : {c.BOLD}{c.YELLOW}{format_num(ct.output_tokens)}{c.RESET}")
    print(f"  ├─ 累计总流通 Token (Gross): {c.BOLD}{c.CYAN}{format_num(ct.total_tokens)}{c.RESET}")
    print(f"  ├─ 实际计费 Token (Net)    : {format_num(ct.net_tokens)}")
    print(f"  └─ 整体缓存节省率          : {c.BOLD}{c.GREEN}{ct.cache_hit_rate}%{c.RESET}")

    if not conv.turns:
        print(f"\n{c.DIM}暂无轮次交互数据。{c.RESET}")
        return

    latest = conv.latest_turn
    if latest:
        lt = latest.tokens
        print(f"\n{c.BOLD}⭐ 【当前最新一轮 (Turn #{latest.turn_index}) 专项统计】{c.RESET}")
        print(f"  ├─ 用户指令: {c.WHITE}{latest.user_prompt}{c.RESET}")
        print(f"  ├─ 触发时间: {latest.start_time}")
        print(f"  ├─ 本轮模型调用次数: {latest.model_call_count} 次 (共 {latest.step_count} 个执行步骤)")
        print(f"  ├─ 本轮新输入 Token   : {format_num(lt.input_tokens)}")
        print(f"  ├─ 本轮缓存命中 Token : {c.GREEN}{format_num(lt.cache_read_tokens)}{c.RESET}")
        print(f"  ├─ 本轮生成输出 Token : {c.YELLOW}{format_num(lt.output_tokens)}{c.RESET}")
        print(f"  ├─ 本轮流通 Token 合计: {c.CYAN}{format_num(lt.total_tokens)}{c.RESET}")
        print(f"  └─ 最新上下文深度 (Ctx Size): {c.BOLD}{c.MAGENTA}{format_num(latest.latest_context_size)}{c.RESET} tokens (单次模型最大上下文占用)")

    # 历轮明细表格
    print(f"\n{c.BOLD}📜 【各轮次（Turn 1 ~ {conv.total_turns}）演进表】{c.RESET}")
    header = (
        f"{'轮次':<6} | "
        f"{'用户指令摘录':<36} | "
        f"{'调用':<4} | "
        f"{'新输入':<10} | "
        f"{'缓存读取':<10} | "
        f"{'生成输出':<10} | "
        f"{'本轮总计':<10} | "
        f"{'最新上下文 (Ctx)':<14}"
    )
    sep_len = 115
    print("─" * sep_len)
    print(f"{c.BOLD}{header}{c.RESET}")
    print("─" * sep_len)

    for t in conv.turns:
        is_latest = (t.turn_index == conv.total_turns)
        tag = f"{c.GREEN}*T{t.turn_index}{c.RESET}" if is_latest else f" T{t.turn_index}"
        prompt_disp = t.user_prompt
        if len(prompt_disp) > 34:
            prompt_disp = prompt_disp[:32] + ".."
        
        tok = t.tokens
        row = (
            f"{tag:<14} | "
            f"{prompt_disp:<36} | "
            f"{t.model_call_count:<4} | "
            f"{format_num(tok.input_tokens):<10} | "
            f"{format_num(tok.cache_read_tokens):<10} | "
            f"{format_num(tok.output_tokens):<10} | "
            f"{format_num(tok.total_tokens):<10} | "
            f"{format_num(t.latest_context_size):<14}"
        )
        print(row)

    print("─" * sep_len)
    print(f"{c.DIM}(* 标记为当前最新一轮){c.RESET}\n")


def watch_mode(analyzer: TokenAnalyzer, interval: int = 3):
    """实时监控模式：定时循环刷新终端"""
    print(f"进入实时监控模式 (刷新间隔: {interval} 秒，按 Ctrl+C 退出)...")
    try:
        while True:
            # 清屏
            os.system("cls" if os.name == "nt" else "clear")
            summary = analyzer.get_summary()
            render_summary_table(summary)
            print(f"{Colors.DIM}监控中... 下次刷新: {interval} 秒后 (Ctrl+C 退出){Colors.RESET}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n已退出实时监控模式。")


def export_csv(summary: PlatformSummary, filename: str):
    """导出全平台统计到 CSV 文件"""
    import csv
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
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
                c.conversation_id,
                c.title,
                c.status,
                c.is_subagent,
                c.total_turns,
                c.step_count,
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
    print(f"数据已成功导出至: {filename}")


def main():
    parser = argparse.ArgumentParser(
        prog="antigravity_token_monitor",
        description="反重力 Agent 平台 Token 统计系统"
    )
    parser.add_argument("command", nargs="?", default="summary",
                        choices=["summary", "detail", "current", "watch", "web"],
                        help="命令：summary (汇总列表), detail (单个详情), current (最新活跃会话), watch (实时监控), web (启动仪表盘)")
    parser.add_argument("id", nargs="?", default=None, help="会话 ID（detail 命令使用，可传前缀或全量 UUID）")
    parser.add_argument("--app-data", default=None, help="自定义反重力数据目录路径")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    parser.add_argument("--csv", default=None, help="导出统计数据至指定 CSV 文件")
    parser.add_argument("--interval", type=int, default=3, help="watch 模式刷新间隔秒数 (默认 3)")
    parser.add_argument("--port", type=int, default=8765, help="web 模式 HTTP 端口 (默认 8765)")

    args = parser.parse_args()
    analyzer = TokenAnalyzer(app_data_dir=args.app_data)

    if args.command == "web":
        from antigravity_token_monitor.server import start_server
        start_server(port=args.port, app_data_dir=args.app_data)
        return

    if args.command == "watch":
        watch_mode(analyzer, interval=args.interval)
        return

    summary = analyzer.get_summary()

    if args.csv:
        export_csv(summary, args.csv)
        return

    if args.json:
        print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
        return

    if args.command == "summary":
        render_summary_table(summary)
        return

    if args.command == "current":
        if not summary.conversations:
            print("未找到任何对话。")
            return
        target = summary.conversations[0]
        render_conversation_detail(target)
        return

    if args.command == "detail":
        if not args.id:
            print(f"{Colors.RED}错误: 请指定会话 ID，例如: python -m antigravity_token_monitor detail <ID>{Colors.RESET}")
            return
        
        target = None
        for c in summary.conversations:
            if c.conversation_id.lower().startswith(args.id.lower()):
                target = c
                break
        
        if not target:
            print(f"{Colors.RED}未找到 ID 匹配 '{args.id}' 的会话。{Colors.RESET}")
            return

        render_conversation_detail(target)


if __name__ == "__main__":
    main()
