import os
import time
from typing import Any, Callable
from openai import OpenAI

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"

API_KEY = ""

# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    client = OpenAI(api_key=API_KEY)
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    end_time = time.time()
    
    latency = end_time - start_time
    if latency <= 0:
        latency = 0.001
        
    response_text = response.choices[0].message.content or ""
    return response_text, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt, model=OPENAI_MODEL)
    mini_response, mini_latency = call_openai_mini(prompt)
    
    word_count = len(gpt4o_response.split())
    estimated_tokens = word_count / 0.75
    gpt4o_cost_estimate = (estimated_tokens / 1000) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    
    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    """
    client = OpenAI(api_key=API_KEY)
    history = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
            
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
            
        if not user_input:
            continue
            
        history.append({"role": "user", "content": user_input})
        
        if len(history) > 6:
            history = history[-6:]
            
        print("Assistant: ", end="", flush=True)
        
        stream = client.chat.completions.create(
            model=OPENAI_MINI_MODEL,
            messages=history,
            stream=True
        )
        
        assistant_reply = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_reply += delta
            
        print()
        history.append({"role": "assistant", "content": assistant_reply})


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).
    """
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as e:
            if attempt >= max_retries:
                raise e
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
            attempt += 1


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    for prompt in prompts:
        res = compare_models(prompt)
        res["prompt"] = prompt
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    def truncate(text: str, length: int = 40) -> str:
        clean_text = text.replace("\n", " ")
        if len(clean_text) > length:
            return clean_text[:length-3] + "..."
        return clean_text.ljust(length)

    headers = ["Prompt", "GPT-4o Response", "Mini Response", "GPT-4o Latency", "Mini Latency"]
    
    table_lines = [
        f"{truncate(headers[0], 40)} | {truncate(headers[1], 40)} | {truncate(headers[2], 40)} | {headers[3].ljust(15)} | {headers[4].ljust(15)}"
    ]
    table_lines.append("-" * len(table_lines[0]))
    
    for res in results:
        p = truncate(res["prompt"], 40)
        g4o_res = truncate(res["gpt4o_response"], 40)
        mini_res = truncate(res["mini_response"], 40)
        g4o_lat = f"{res['gpt4o_latency']:.3f}s".ljust(15)
        mini_lat = f"{res['mini_latency']:.3f}s".ljust(15)
        
        table_lines.append(f"{p} | {g4o_res} | {mini_res} | {g4o_lat} | {mini_lat}")
        
    return "\n".join(table_lines)


if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")