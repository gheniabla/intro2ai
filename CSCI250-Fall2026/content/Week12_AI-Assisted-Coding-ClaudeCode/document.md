# Week 12 — AI-Assisted Software Development with Claude Code
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of November 9, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Explain what **agentic coding** is and how an AI coding assistant differs from autocomplete and from a chat window.
2. **Install and run Claude Code**, and drive a project from the terminal (plan → edit → run → review).
3. Write effective **coding prompts**: give context, constraints, and acceptance criteria; separate *planning* from *editing*.
4. **Review, test, and secure** AI-generated code — treat the AI as a fast junior developer whose work you must verify.
5. Use a sane **git workflow** with AI: small commits, branches, diffs you actually read.
6. Judge **when AI helps vs. when it hurts**, and disclose AI use honestly.
7. Complete a **tested feature** in a small starter repo with AI help (Lab A6).

> **Time budget:** ~10 hours this week (lecture + slides + notebook + Lab A6).

---

## 1. From autocomplete to agentic coding
You have used three kinds of AI help with code, whether you noticed or not:

- **Autocomplete** (e.g., editor tab-completion): predicts the next few tokens. No project awareness.
- **Chat** (Claude / Gemini in a browser): you paste code in, it answers, you paste code back. *You* are the integration layer.
- **Agentic coding** (Claude Code): the assistant can **read your files, run commands, edit code, and run tests** in a loop, inside your actual project. It acts, observes the result, and adjusts.

That loop — **reason → act → observe → repeat** — is the same agent loop we formalize next week (Week 13). Claude Code is an agent whose tools are your filesystem, your shell, and git.

This is a genuinely new way to work, and it is the biggest new emphasis in this course. The skill is **not** "make the AI write code." The skill is **directing and verifying** an AI that writes code fast.

---

## 2. Installing and running Claude Code
Claude Code is a command-line tool. You need Node.js (v18+) and an Anthropic account.

```bash
# 1. Install (Node 18+ required)
npm install -g @anthropic-ai/claude-code

# 2. Go to your project and start a session
cd my-project
claude

# 3. Useful one-offs
claude --help
claude -p "summarize what this repo does"   # print mode: one answer, no session
```

The first run walks you through signing in. Inside a session you just type requests in natural language. Claude Code shows you the **commands it wants to run** and the **edits it wants to make**, and (by default) asks permission before changing files or running commands. You stay in control.

A few in-session commands worth knowing:
- `/init` — generate a `CLAUDE.md` describing the project (Claude reads this every session).
- `/clear` — reset the conversation context when you start a new task.
- `/review` — ask Claude to review a diff or a pull request.
- Press **Esc** to interrupt; ask it to **stop and plan** instead of editing.

### CLAUDE.md — give the agent a memory
A file named `CLAUDE.md` at the repo root is automatically loaded as context. Put project conventions there: how to run tests, the stack, style rules, "never touch `migrations/`." A good `CLAUDE.md` makes every later prompt shorter and more accurate.

---

## 3. Prompting for code: context, constraints, criteria
Vague prompts get vague code. Strong coding prompts have three parts:

1. **Context** — what the project is, where the relevant file lives, what already works.
2. **Constraints** — the stack, the style, what *not* to change, edge cases to handle.
3. **Acceptance criteria** — how we will both know it is done (usually: "the tests pass").

Compare:

> ❌ "Add caching."

> ✅ "In `pricing.py`, add an in-memory cache to `get_rate(currency)` so repeated calls in the same run don't refetch. Keep the function signature. Add a `pytest` test in `test_pricing.py` proving a second call doesn't hit `fetch_rate`. Don't add new dependencies."

The second prompt names the file, fixes the signature, defines done (a passing test), and forbids scope creep.

### Plan first, then edit
For anything non-trivial, ask for a **plan before code**:

> "Before editing anything, outline how you'd implement this in 4–6 steps and which files you'd touch. Wait for my OK."

Claude Code has a **plan mode** for exactly this — it investigates and proposes without writing. Reading the plan catches wrong assumptions *before* they become 200 lines of wrong code. This "planning vs. editing" split is the single highest-value habit in this week.

---

## 4. Reviewing, testing, and securing AI-generated code
**Never merge code you have not read.** The AI is a fast junior developer: productive, occasionally confidently wrong. Your job moves from *typing* to *reviewing*.

### Read the diff
After Claude edits, look at the actual change (`git diff`). Ask yourself:
- Does it do what I asked — and *only* that?
- Are the edge cases handled (empty input, zero, `None`, negatives)?
- Did it invent an API or import that doesn't exist (a **hallucination**)?

### Test it
Tests are how you make "it works" objective. The workflow we use this week:

```text
1. Write or ask for a failing test that captures the requirement.
2. Ask Claude to make the test pass.
3. Run the tests yourself. Green ≠ done; read the code too.
```

This is **test-driven** AI coding. The test is a contract the AI cannot talk its way out of.

### Secure it
AI-generated code can introduce real vulnerabilities. Watch for:
- **Secrets in code** — keys hard-coded instead of read from the environment.
- **Injection** — unsanitized input into SQL, shell commands, or `eval`.
- **Unsafe deserialization** — `pickle.load` / `eval` on untrusted data.
- **Over-broad permissions** or dependencies you didn't vet.

Claude Code can help here too: `/security-review` and `/review` ask it to audit a diff. But the human signs off.

---

## 5. When AI helps vs. when it hurts
| AI tends to **help** | AI tends to **hurt** |
|---|---|
| Boilerplate, scaffolding, tests | Novel algorithms with no examples online |
| Explaining unfamiliar code | Subtle concurrency / numerical bugs |
| Refactors with tests as a safety net | Anything you can't verify |
| "How do I do X in library Y?" | Security-critical code you skim instead of read |
| Repetitive edits across many files | Decisions that need product/context judgment |

Rule of thumb: **the more easily you can verify the output, the more you can trust the AI to produce it.** Tests, types, and small diffs make verification cheap — that is *why* we lean on them.

---

## 6. A sane git workflow with AI
AI makes it easy to generate a lot of code fast, which makes good git hygiene *more* important, not less.

```bash
git checkout -b feature/discount-codes   # branch per feature
# ... AI helps you implement + test ...
git add -p                               # stage in small, reviewed chunks
git commit -m "Add discount-code validation with tests"
git diff main                            # read everything before merging
```

Principles:
- **Small commits** with honest messages — easy to review and to revert.
- **Branch per feature** — keep `main` working.
- **Read every diff** before it lands.
- **Disclose** AI involvement per the course policy (and many real workplaces' policies).

---

## 7. This week's lab — the starter repo
In `code/starter_repo/` you get a tiny Python package, `mathkit`, with:
- `mathkit/discounts.py` — a working `apply_discount(...)` plus an **incomplete** `best_price(...)`.
- `tests/test_discounts.py` — **failing tests** describing what `best_price(...)` must do.
- `mathkit/SOLUTION_NOTES.md` — a reference solution (for the instructor / your self-check).

Your job: use an AI assistant (ideally Claude Code) to **make the failing tests pass** without breaking the passing ones — and to be able to explain every line. See Section 8.

```bash
cd code/starter_repo
python -m pytest -q          # see the failing tests first
# ... work with the AI to implement best_price ...
python -m pytest -q          # all green when you're done
```

---

## 8. Lab — Assignment A6 (due Sunday 11:59 PM PT)
**Goal:** complete a *tested* feature using an AI coding assistant, and reflect on the process.

1. Clone/open `code/starter_repo/`. Run `python -m pytest -q` and confirm the `best_price` tests **fail**.
2. Start Claude Code in that folder (`claude`). First ask it to **explain the repo and propose a plan** for `best_price` — do **not** let it edit yet.
3. Approve a plan, then have it implement `best_price` and make the tests pass. **Read the diff.**
4. Run the tests yourself. If green, add one more test of your own (an edge case the AI missed) and make it pass too.
5. Commit your work on a feature branch with a clear message.
6. Write a 200-word reflection: Where did the AI help most? Did it hallucinate or over-reach? What did you have to fix or verify yourself? Include a one-line **AI Use** note.

**Submit:** your completed `starter_repo` (or a repo link) with green tests + the reflection.

*A6 is graded on working tests, evidence of review, and the quality of your reflection (see syllabus).*

> If you can't install Claude Code, you may do A6 with Claude or Gemini in the browser — but you must still produce the same green tests and reflection. The notebook `code/01_ai_assisted_coding.ipynb` shows the AI-as-coder loop without needing the CLI.

---

## Reading & videos
- **Anthropic — Claude Code overview & quickstart** (docs.anthropic.com/claude-code) — required skim.
- **Anthropic — "Claude Code best practices"** blog post.
- Video: "Plan mode and reviewing diffs in Claude Code" (linked in Canvas).
- Optional: a short read on **test-driven development** (any reputable intro).

---

## Key terms
**agentic coding**, **Claude Code**, **CLAUDE.md**, **plan mode**, **diff review**, **acceptance criteria**, **test-driven development (TDD)**, **hallucination**, **prompt injection / code injection**, **feature branch**, **AI disclosure**.
