"""
Antigravity Token Monitor - Core Engine
解析反重力Agent平台的会话与日志，精确统计每个对话的最新一轮及历史累计Token使用量。
"""

import os
import glob
import json
import sqlite3
import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any


def get_default_app_data_dir() -> str:
    """获取反重力平台的默认数据存储目录"""
    env_dir = os.environ.get("ANTIGRAVITY_APP_DATA")
    if env_dir and os.path.exists(env_dir):
        return env_dir

    # Windows 常见路径
    user_home = os.path.expanduser("~")
    win_path = os.path.join(user_home, ".gemini", "antigravity")
    if os.path.exists(win_path):
        return win_path

    # Linux / MacOS 兼容路径
    unix_path = os.path.join(user_home, ".config", "antigravity")
    if os.path.exists(unix_path):
        return unix_path

    return win_path


@dataclass
class TokenUsage:
    """Token 用量细分"""
    input_tokens: int = 0          # 新输入/未命中缓存的 prompt tokens
    cache_read_tokens: int = 0     # 命中 prompt cache 读取的 tokens
    output_tokens: int = 0         # 模型生成的 output tokens
    
    @property
    def prompt_tokens(self) -> int:
        """模型处理的完整 Prompt 规模 (未缓存 + 缓存)"""
        return self.input_tokens + self.cache_read_tokens

    @property
    def total_tokens(self) -> int:
        """总流通 Token (Prompt规模 + 生成输出)"""
        return self.input_tokens + self.cache_read_tokens + self.output_tokens

    @property
    def net_tokens(self) -> int:
        """净消耗 Token (实际未缓存输入 + 输出)"""
        return self.input_tokens + self.output_tokens

    @property
    def cache_hit_rate(self) -> float:
        """缓存命中率 (%)"""
        total_p = self.prompt_tokens
        if total_p == 0:
            return 0.0
        return round((self.cache_read_tokens / total_p) * 100, 1)

    def add(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            input_tokens=self.input_tokens + other.input_tokens,
            cache_read_tokens=self.cache_read_tokens + other.cache_read_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
        )


@dataclass
class StepRecord:
    """单个执行步骤的 Token 与元信息"""
    step_index: int
    step_type: str
    source: str
    created_at: str
    input_tokens: int = 0
    cache_read_tokens: int = 0
    output_tokens: int = 0
    tool_calls: List[str] = field(default_factory=list)


@dataclass
class TurnStats:
    """单轮交互（从用户发送提问到该轮次完成）统计"""
    turn_index: int
    user_step_index: int
    user_prompt: str
    user_prompt_full: str
    start_time: str
    end_time: str
    step_count: int
    model_call_count: int
    tokens: TokenUsage
    latest_context_size: int = 0   # 本轮最后一次请求的 Prompt 上下文深度 (input + cache)
    latest_output_tokens: int = 0  # 本轮最后一次模型输出的 tokens
    steps: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ConversationStats:
    """单个对话的完整 Token 统计"""
    conversation_id: str
    title: str
    preview: str
    status: str
    step_count: int
    last_modified_time: str
    parent_conversation_id: str
    is_subagent: bool
    total_turns: int
    total_model_calls: int
    latest_turn: Optional[TurnStats]
    cumulative_tokens: TokenUsage
    turns: List[TurnStats] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # 补充属性
        data["cumulative_tokens"]["prompt_tokens"] = self.cumulative_tokens.prompt_tokens
        data["cumulative_tokens"]["total_tokens"] = self.cumulative_tokens.total_tokens
        data["cumulative_tokens"]["net_tokens"] = self.cumulative_tokens.net_tokens
        data["cumulative_tokens"]["cache_hit_rate"] = self.cumulative_tokens.cache_hit_rate
        if self.latest_turn:
            data["latest_turn"]["tokens"]["prompt_tokens"] = self.latest_turn.tokens.prompt_tokens
            data["latest_turn"]["tokens"]["total_tokens"] = self.latest_turn.tokens.total_tokens
            data["latest_turn"]["tokens"]["net_tokens"] = self.latest_turn.tokens.net_tokens
            data["latest_turn"]["tokens"]["cache_hit_rate"] = self.latest_turn.tokens.cache_hit_rate
        return data


@dataclass
class PlatformSummary:
    """全平台全局汇总"""
    app_data_dir: str
    scan_time: str
    total_conversations: int
    active_conversations_count: int
    total_turns: int
    total_model_calls: int
    platform_cumulative_tokens: TokenUsage
    latest_turns_total_tokens: TokenUsage
    conversations: List[ConversationStats] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "app_data_dir": self.app_data_dir,
            "scan_time": self.scan_time,
            "total_conversations": self.total_conversations,
            "active_conversations_count": self.active_conversations_count,
            "total_turns": self.total_turns,
            "total_model_calls": self.total_model_calls,
            "platform_cumulative_tokens": {
                "input_tokens": self.platform_cumulative_tokens.input_tokens,
                "cache_read_tokens": self.platform_cumulative_tokens.cache_read_tokens,
                "output_tokens": self.platform_cumulative_tokens.output_tokens,
                "prompt_tokens": self.platform_cumulative_tokens.prompt_tokens,
                "total_tokens": self.platform_cumulative_tokens.total_tokens,
                "net_tokens": self.platform_cumulative_tokens.net_tokens,
                "cache_hit_rate": self.platform_cumulative_tokens.cache_hit_rate,
            },
            "latest_turns_total_tokens": {
                "input_tokens": self.latest_turns_total_tokens.input_tokens,
                "cache_read_tokens": self.latest_turns_total_tokens.cache_read_tokens,
                "output_tokens": self.latest_turns_total_tokens.output_tokens,
                "prompt_tokens": self.latest_turns_total_tokens.prompt_tokens,
                "total_tokens": self.latest_turns_total_tokens.total_tokens,
                "net_tokens": self.latest_turns_total_tokens.net_tokens,
                "cache_hit_rate": self.latest_turns_total_tokens.cache_hit_rate,
            },
            "conversations": [c.to_dict() for c in self.conversations]
        }


class TokenAnalyzer:
    """Token 分析与统计器"""

    def __init__(self, app_data_dir: Optional[str] = None):
        self.app_data_dir = os.path.abspath(app_data_dir or get_default_app_data_dir())
        self.db_path = os.path.join(self.app_data_dir, "conversation_summaries.db")
        self.brain_dir = os.path.join(self.app_data_dir, "brain")

    def _read_meta_from_db(self) -> Dict[str, Dict[str, Any]]:
        """从 conversation_summaries.db 安全读取会话元数据"""
        meta_dict = {}
        if not os.path.exists(self.db_path):
            return meta_dict

        try:
            # 采用只读 URI 模式连接，避免与主程序冲突
            uri_path = f"file:{self.db_path}?mode=ro"
            conn = sqlite3.connect(uri_path, uri=True, timeout=5)
        except Exception:
            try:
                conn = sqlite3.connect(self.db_path, timeout=5)
            except Exception:
                return meta_dict

        try:
            cursor = conn.cursor()
            query = """
            SELECT conversation_id, title, preview, step_count, last_modified_time, 
                   status, parent_conversation_id 
            FROM conversation_summaries
            """
            for row in cursor.execute(query).fetchall():
                meta_dict[row[0]] = {
                    "conversation_id": row[0],
                    "title": row[1] or "未命名对话",
                    "preview": row[2] or "",
                    "step_count": row[3] or 0,
                    "last_modified_time": row[4] or "",
                    "status": row[5] or "UNKNOWN",
                    "parent_conversation_id": row[6] or "",
                }
        except Exception as e:
            pass
        finally:
            conn.close()

        return meta_dict

    def parse_transcript(self, transcript_file: str) -> List[TurnStats]:
        """解析单份 transcript.jsonl，并将其精准归纳为轮次（Turns）"""
        if not os.path.exists(transcript_file):
            return []

        raw_steps = []
        try:
            with open(transcript_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        raw_steps.append(data)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            return []

        if not raw_steps:
            return []

        # 分割轮次：每个 USER_INPUT 或 USER_EXPLICIT 为一轮的起点
        turn_blocks = []
        current_block = []

        for step in raw_steps:
            source = step.get("source", "")
            stype = step.get("type", "")
            is_user = (source == "USER_EXPLICIT" or stype == "USER_INPUT")
            
            if is_user:
                if current_block:
                    turn_blocks.append(current_block)
                current_block = [step]
            else:
                if not current_block:
                    # 如果开头没有用户输入步，先暂存
                    current_block = [step]
                else:
                    current_block.append(step)

        if current_block:
            turn_blocks.append(current_block)

        # 解析各轮
        turns: List[TurnStats] = []
        for idx, block in enumerate(turn_blocks, start=1):
            first_step = block[0]
            user_idx = first_step.get("step_index", 0)
            user_prompt = ""
            start_time = first_step.get("created_at", "")
            end_time = block[-1].get("created_at", start_time)

            if first_step.get("source") == "USER_EXPLICIT" or first_step.get("type") == "USER_INPUT":
                c = first_step.get("content", "")
                if isinstance(c, str):
                    user_prompt = c
                elif isinstance(c, list):
                    user_prompt = " ".join(str(item) for item in c)
                else:
                    user_prompt = str(c)

            # 提取 clean user prompt (去掉系统注入的 USER_REQUEST 标签方便人类阅读)
            clean_prompt = user_prompt
            if "<USER_REQUEST>" in clean_prompt:
                try:
                    parts = clean_prompt.split("<USER_REQUEST>")
                    clean_prompt = parts[1].split("</USER_REQUEST>")[0].strip()
                except Exception:
                    pass
            clean_prompt = clean_prompt.strip()
            prompt_preview = clean_prompt.replace("\r", " ").replace("\n", " ")
            if len(prompt_preview) > 80:
                prompt_preview = prompt_preview[:80] + "..."
            if not prompt_preview:
                prompt_preview = f"第 {idx} 轮交互"

            inp_sum = 0
            cache_sum = 0
            out_sum = 0
            model_calls = 0
            last_context_size = 0
            last_output = 0
            step_details = []

            for s in block:
                s_idx = s.get("step_index")
                stype = s.get("type")
                source = s.get("source")
                inp = s.get("input_tokens")
                out = s.get("output_tokens")
                cache = s.get("cache_read_tokens")

                tool_calls = []
                if "tool_calls" in s and isinstance(s["tool_calls"], list):
                    for tc in s["tool_calls"]:
                        if isinstance(tc, dict) and "name" in tc:
                            tool_calls.append(tc["name"])

                has_tokens = (inp is not None or out is not None)
                if has_tokens:
                    model_calls += 1
                    inp_val = inp or 0
                    cache_val = cache or 0
                    out_val = out or 0
                    inp_sum += inp_val
                    cache_sum += cache_val
                    out_sum += out_val
                    last_context_size = inp_val + cache_val
                    last_output = out_val

                step_details.append({
                    "step_index": s_idx,
                    "type": stype,
                    "source": source,
                    "created_at": s.get("created_at"),
                    "input_tokens": inp or 0,
                    "cache_read_tokens": cache or 0,
                    "output_tokens": out or 0,
                    "total_tokens": (inp or 0) + (cache or 0) + (out or 0),
                    "tool_calls": tool_calls,
                })

            turn_stat = TurnStats(
                turn_index=idx,
                user_step_index=user_idx,
                user_prompt=prompt_preview,
                user_prompt_full=clean_prompt,
                start_time=start_time,
                end_time=end_time,
                step_count=len(block),
                model_call_count=model_calls,
                tokens=TokenUsage(
                    input_tokens=inp_sum,
                    cache_read_tokens=cache_sum,
                    output_tokens=out_sum,
                ),
                latest_context_size=last_context_size,
                latest_output_tokens=last_output,
                steps=step_details
            )
            turns.append(turn_stat)

        return turns

    def analyze_conversation(self, conv_id: str, meta: Optional[Dict[str, Any]] = None) -> Optional[ConversationStats]:
        """统计单个对话的各项指标"""
        transcript_file = os.path.join(self.brain_dir, conv_id, ".system_generated", "logs", "transcript.jsonl")
        if not os.path.exists(transcript_file):
            return None

        turns = self.parse_transcript(transcript_file)
        latest_turn = turns[-1] if turns else None

        cum_inp = sum(t.tokens.input_tokens for t in turns)
        cum_cache = sum(t.tokens.cache_read_tokens for t in turns)
        cum_out = sum(t.tokens.output_tokens for t in turns)
        total_calls = sum(t.model_call_count for t in turns)

        cum_tokens = TokenUsage(
            input_tokens=cum_inp,
            cache_read_tokens=cum_cache,
            output_tokens=cum_out
        )

        title = meta.get("title") if meta else ""
        if not title and turns and turns[0].user_prompt:
            title = turns[0].user_prompt[:30]
        if not title:
            title = f"会话 {conv_id[:8]}"

        status = meta.get("status") if meta else "UNKNOWN"
        step_count = meta.get("step_count") if meta else (sum(t.step_count for t in turns))
        last_modified = meta.get("last_modified_time") if meta else (latest_turn.end_time if latest_turn else "")
        parent_id = meta.get("parent_conversation_id") if meta else ""

        return ConversationStats(
            conversation_id=conv_id,
            title=title,
            preview=meta.get("preview", "") if meta else "",
            status=status,
            step_count=step_count,
            last_modified_time=last_modified,
            parent_conversation_id=parent_id,
            is_subagent=bool(parent_id),
            total_turns=len(turns),
            total_model_calls=total_calls,
            latest_turn=latest_turn,
            cumulative_tokens=cum_tokens,
            turns=turns
        )

    def get_summary(self) -> PlatformSummary:
        """扫描全平台所有对话并汇总统计"""
        meta_dict = self._read_meta_from_db()
        
        # 扫描 brain 下所有目录
        conv_dirs = []
        if os.path.exists(self.brain_dir):
            for entry in os.listdir(self.brain_dir):
                full_path = os.path.join(self.brain_dir, entry)
                if os.path.isdir(full_path):
                    t_path = os.path.join(full_path, ".system_generated", "logs", "transcript.jsonl")
                    if os.path.exists(t_path):
                        conv_dirs.append(entry)

        # 同时也兼顾 meta_dict 中可能存在的
        all_conv_ids = set(conv_dirs).union(set(meta_dict.keys()))

        conversations: List[ConversationStats] = []
        for cid in all_conv_ids:
            meta = meta_dict.get(cid)
            stats = self.analyze_conversation(cid, meta)
            if stats:
                conversations.append(stats)

        # 按最后修改时间倒序排列
        conversations.sort(key=lambda c: c.last_modified_time or "", reverse=True)

        # 聚合全平台数据
        total_inp = sum(c.cumulative_tokens.input_tokens for c in conversations)
        total_cache = sum(c.cumulative_tokens.cache_read_tokens for c in conversations)
        total_out = sum(c.cumulative_tokens.output_tokens for c in conversations)
        total_calls = sum(c.total_model_calls for c in conversations)
        total_turns = sum(c.total_turns for c in conversations)

        latest_inp = sum(c.latest_turn.tokens.input_tokens for c in conversations if c.latest_turn)
        latest_cache = sum(c.latest_turn.tokens.cache_read_tokens for c in conversations if c.latest_turn)
        latest_out = sum(c.latest_turn.tokens.output_tokens for c in conversations if c.latest_turn)

        scan_time = datetime.datetime.now().isoformat()

        return PlatformSummary(
            app_data_dir=self.app_data_dir,
            scan_time=scan_time,
            total_conversations=len(conversations),
            active_conversations_count=len([c for c in conversations if c.status not in ("TERMINATED", "KILLED")]),
            total_turns=total_turns,
            total_model_calls=total_calls,
            platform_cumulative_tokens=TokenUsage(
                input_tokens=total_inp,
                cache_read_tokens=total_cache,
                output_tokens=total_out
            ),
            latest_turns_total_tokens=TokenUsage(
                input_tokens=latest_inp,
                cache_read_tokens=latest_cache,
                output_tokens=latest_out
            ),
            conversations=conversations
        )
