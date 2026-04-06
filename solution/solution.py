"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Solution implemented using Anthropic Claude API (thay thế OpenAI API).

Setup:
    1. Copy .env.example to .env
    2. Fill in your ANTHROPIC_API_KEY in .env
    3. Run: pip install python-dotenv
"""

import os
import time
from typing import Any, Callable
import anthropic

# Load .env file nếu có (dùng khi chạy local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv chưa cài, dùng environment variable thực tế

# ---------------------------------------------------------------------------
# Config — API key được đọc từ environment variable, KHÔNG hardcode
# ---------------------------------------------------------------------------
# Đặt ANTHROPIC_API_KEY trong file .env (xem .env.example)

# Map tên model OpenAI → Claude (để giữ nguyên interface)
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"

# Claude models tương ứng
CLAUDE_MODEL_LARGE = "claude-sonnet-4-6"         # tương đương gpt-4o
CLAUDE_MODEL_SMALL = "claude-haiku-4-5-20251001"   # tương đương gpt-4o-mini

MODEL_MAP = {
    "gpt-4o": CLAUDE_MODEL_LARGE,
    "gpt-4o-mini": CLAUDE_MODEL_SMALL,
}


def _get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY chưa được set. "
            "Hãy tạo file .env với nội dung: ANTHROPIC_API_KEY=sk-ant-..."
        )
    return anthropic.Anthropic(api_key=api_key)


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o  (dùng Claude thay thế)
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi Claude API với interface giống OpenAI.
    Trả về (response_text, latency_seconds).
    """
    client = _get_client()
    claude_model = MODEL_MAP.get(model, CLAUDE_MODEL_LARGE)

    start = time.time()
    response = client.messages.create(
        model=claude_model,
        max_tokens=max_tokens,
        temperature=temperature,
        # Lưu ý: Claude không cho dùng temperature và top_p cùng lúc
        # top_p=top_p,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.time() - start

    text = response.content[0].text
    return text, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini  (dùng Claude Haiku thay thế)
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi Claude Haiku (tương đương gpt-4o-mini).
    Trả về (response_text, latency_seconds).
    """
    return call_openai(
        prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Gọi cả 2 model với cùng prompt, trả về dict so sánh.
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)

    # Ước tính chi phí: (số_từ / 0.75) / 1000 * giá_per_1k
    gpt4o_cost_estimate = (
        (len(gpt4o_response.split()) / 0.75) / 1000
        * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    )

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot với conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Chatbot tương tác trong terminal.
    - Stream token từng chút một khi nhận được.
    - Giữ 3 turn hội thoại gần nhất.
    - Gõ 'quit' hoặc 'exit' để thoát.
    """
    client = _get_client()
    history = []

    print("Chatbot ready! (type 'quit' to exit)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        print("Assistant: ", end="", flush=True)
        full_reply = ""

        # Stream response từng chunk
        with client.messages.stream(
            model=CLAUDE_MODEL_LARGE,
            max_tokens=1024,
            messages=history,
        ) as stream:
            for text_chunk in stream.text_stream:
                print(text_chunk, end="", flush=True)
                full_reply += text_chunk

        print()  # xuống dòng sau khi xong

        history.append({"role": "assistant", "content": full_reply})

        # Giữ lại 3 turn gần nhất (6 messages)
        history = history[-6:]


# ---------------------------------------------------------------------------
# Bonus Task A — Retry với exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Gọi fn(). Nếu thất bại → retry tối đa max_retries lần
    với delay tăng theo luỹ thừa: base_delay * 2^attempt.
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)

    raise last_exception


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Chạy compare_models cho từng prompt trong danh sách.
    Trả về list dict, mỗi dict có thêm key "prompt".
    """
    results = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format kết quả batch_compare thành bảng text dễ đọc.
    Columns: Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency
    """
    headers = ["Prompt", "GPT-4o Response", "Mini Response", "GPT-4o Latency", "Mini Latency"]
    col_width = 44

    def truncate(text: str, length: int = 40) -> str:
        text = str(text)
        return text[:length] + "..." if len(text) > length else text

    separator = "+" + "+".join(["-" * col_width for _ in headers]) + "+"
    header_row = "|" + "|".join(f" {h:<{col_width - 1}}" for h in headers) + "|"

    lines = [separator, header_row, separator]

    for r in results:
        row_values = [
            truncate(r.get("prompt", "")),
            truncate(r.get("gpt4o_response", "")),
            truncate(r.get("mini_response", "")),
            f"{r.get('gpt4o_latency', 0):.3f}s",
            f"{r.get('mini_latency', 0):.3f}s",
        ]
        row = "|" + "|".join(f" {v:<{col_width - 1}}" for v in row_values) + "|"
        lines.append(row)
        lines.append(separator)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."

    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
