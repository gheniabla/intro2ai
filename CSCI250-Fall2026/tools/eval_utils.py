"""
eval_utils.py — shared evaluation helpers for CSCI 250 (Fall 2026).

Evaluation is a *throughline* in this course (Weeks 9, 11, 13, 16, 17), not a
single end-of-term topic. This module gives every week one consistent way to:
  - score model outputs with an **LLM-as-judge** (Claude or Gemini), and
  - print a small **scorecard** (the "report card" pattern students like).

Everything degrades gracefully without API keys so notebooks never hard-crash.

    from eval_utils import llm_judge, exact_match, scorecard
    cases = [{"q": "2+2?", "answer": "4", "expected": "4"}]
    rows = [{**c, **llm_judge(c["q"], c["answer"], "Is it correct and concise?")}
            for c in cases]
    scorecard(rows)
"""
from __future__ import annotations
import os, re, json

JUDGE_RUBRIC_DEFAULT = (
    "Score the ANSWER from 1 (poor) to 5 (excellent) for correctness, relevance, "
    "and clarity. Return ONLY JSON: {\"score\": <int 1-5>, \"reason\": \"<short>\"}."
)


def _claude(prompt: str, model: str = "claude-haiku-4-5-20251001") -> str | None:
    try:
        import anthropic
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
        msg = client.messages.create(
            model=model, max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except Exception:
        return None


def _gemini(prompt: str, model: str = "gemini-2.5-flash") -> str | None:
    try:
        import google.generativeai as genai
        key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not key:
            return None
        genai.configure(api_key=key)
        return genai.GenerativeModel(model).generate_content(prompt).text
    except Exception:
        return None


def _extract_json(text: str) -> dict:
    """Pull the first {...} JSON object out of a model response."""
    if not text:
        return {}
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def llm_judge(question: str, answer: str, rubric: str = JUDGE_RUBRIC_DEFAULT,
              provider: str = "gemini") -> dict:
    """Judge `answer` to `question` with an LLM. Returns {'score','reason','judge'}.

    provider: 'gemini' (default, generous free tier) or 'claude'.
    Falls back to the other provider, then to a keyword heuristic if no key.
    """
    prompt = f"QUESTION:\n{question}\n\nANSWER:\n{answer}\n\n{rubric}"
    order = ["gemini", "claude"] if provider == "gemini" else ["claude", "gemini"]
    for p in order:
        raw = _gemini(prompt) if p == "gemini" else _claude(prompt)
        data = _extract_json(raw or "")
        if "score" in data:
            data["judge"] = p
            return data
    # No keys available — degrade to a transparent heuristic so notebooks still run.
    score = 3 if answer and answer.strip() else 1
    return {"score": score, "reason": "(no API key — heuristic fallback)", "judge": "fallback"}


def exact_match(answer: str, expected: str) -> int:
    """1 if normalized strings match, else 0 (the simplest baseline metric)."""
    norm = lambda s: re.sub(r"\s+", " ", (s or "").strip().lower())
    return int(norm(answer) == norm(expected))


def scorecard(rows, score_key: str = "score") -> dict:
    """Print a small report card from a list of result dicts. Returns summary."""
    n = len(rows) or 1
    scores = [float(r.get(score_key, 0) or 0) for r in rows]
    avg = sum(scores) / n
    print("=" * 52)
    print(f" SCORECARD — {len(rows)} cases")
    print("-" * 52)
    for i, r in enumerate(rows, 1):
        s = r.get(score_key, "?")
        label = (r.get("q") or r.get("question") or r.get("name") or f"case {i}")
        print(f" {i:>2}. {str(label)[:38]:38} score={s}")
    print("-" * 52)
    print(f" AVERAGE {score_key}: {avg:.2f}")
    print("=" * 52)
    return {"n": len(rows), "avg": avg, "scores": scores}


if __name__ == "__main__":
    demo = [
        {"q": "Capital of France?", "answer": "Paris", "expected": "Paris"},
        {"q": "2+2?", "answer": "four", "expected": "4"},
    ]
    rows = []
    for c in demo:
        v = llm_judge(c["q"], c["answer"])
        rows.append({**c, **v, "em": exact_match(c["answer"], c["expected"])})
    scorecard(rows)
