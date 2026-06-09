# Complaint Resolution Agent

An agentic AI system that resolves banking complaints end-to-end using LangChain Deep Agents, progressive skill disclosure, and GPT-4o.

![Demo](demo.gif)

## What it does

Inbound complaints (unauthorized charges, wire transfers, mortgage fees) are routed to specialized skills that contain the exact regulatory rules — Regulation E, RESPA, wire recall procedures. The agent reads only the relevant skill, calls the right tools, and produces a compliant response.

**Key behaviors demonstrated:**
- Reg E unauthorized charge → 10-day provisional credit rule, correct liability cap ($500 for 3–60 day reporting window)
- Wire transfer customer error → same-day recall before 6pm ET Fed cutoff, best-effort recovery framing
- IRS wire fraud → social engineering detection, wire fraud unit escalation
- Mortgage escrow dispute → RESPA QWR 5-day acknowledgment + 30-day resolution
- Multi-turn memory — follow-up questions reference prior context without re-explaining

## Architecture

```
complaint_agent/
  skills/
    complaint-triage/     # classifies complaint type + regulatory flags
    reg-e-disputes/       # Regulation E rules, liability caps, provisional credit
      assets/             # response letter templates
    wire-transfers/       # same-day recall, SWIFT gpi, fraud vs. customer error
    mortgage-fees/        # RESPA Section 10, QWR timelines, force-placed insurance
  agent.py               # create_deep_agent with FilesystemBackend
  tools.py               # lookup_transaction, lookup_customer, create_case, escalate_case
  app.py                 # Streamlit UI with agent trace panel
  main.py                # CLI demo runner
```

### Progressive skill disclosure

Skills load in three layers — the agent sees only name + description at startup, reads the full `SKILL.md` only when a complaint matches, and loads assets on demand:

```
Startup     →  skill name + description injected into system prompt
Activation  →  full SKILL.md loaded via read_file (regulations, rules, templates)
Execution   →  assets/ loaded on demand (response letter templates)
```

This prevents context bloat across 4 banking domains without sacrificing accuracy.

## Stack

- **[LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents)** — skills middleware + agent orchestration
- **OpenAI GPT-4o** — LLM backend
- **LangGraph** — stateful multi-turn memory via `MemorySaver`
- **Streamlit** — chat UI with live agent trace panel
- **uv** — dependency management

## Setup

```bash
git clone https://github.com/ataata107/complaint-res.git
cd complaint-res
uv sync
cp .env.example .env
# add your OPENAI_API_KEY to .env
```

## Run

**Streamlit UI:**
```bash
uv run streamlit run app.py
```

**CLI demo:**
```bash
uv run python main.py
```

## Skills

Each skill is a directory with a `SKILL.md` file following the [Agent Skills specification](https://docs.langchain.com/oss/python/deepagents/skills):

```markdown
---
name: reg-e-disputes
description: Handle debit card fraud and unauthorized ACH transfers under Regulation E
---

# Reg E Dispute Skill
...10-day provisional credit rule, liability caps, escalation triggers...
```

The agent trace panel in the UI shows which skill activated and which tools were called for every response.

## Demo prompts

| Prompt | Skill activated |
|--------|----------------|
| Unauthorized charge — exact liability question | `reg-e-disputes` |
| Follow-up on 90-day late reporting | `reg-e-disputes` (memory) |
| Wrong-account wire — same-day recall | `wire-transfers` |
| IRS scam wire fraud | `wire-transfers` (fraud escalation) |
| Mortgage escrow dispute — RESPA rights | `mortgage-fees` |
| "Money keeps disappearing" (ambiguous) | `complaint-triage` |
