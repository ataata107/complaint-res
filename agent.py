from pathlib import Path
from langchain_core.callbacks import BaseCallbackHandler

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver

from tools import create_case, escalate_case, lookup_customer, lookup_transaction


class ToolLogger(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        name = serialized.get("name", "unknown")
        if "read_file" in name or "write_file" in name:
            print(f"\n🎯 [SKILL] {name} called with: {input_str}", flush=True)
        else:
            print(f"\n🔧 [TOOL] {name} called with: {input_str}", flush=True)

    def on_tool_end(self, output, **kwargs):
        preview = str(output)[:80]
        print(f"   ↳ result: {preview}...", flush=True)


def build_agent():
    backend = FilesystemBackend(root_dir=str(Path(__file__).parent), virtual_mode=False)
    checkpointer = MemorySaver()

    agent = create_deep_agent(
        model="openai:gpt-4o",
        backend=backend,
        skills=["skills/"],
        tools=[lookup_transaction, lookup_customer, create_case, escalate_case],
        checkpointer=checkpointer,
        system_prompt=(
            "You are a banking complaint resolution agent. "
            "You have access to skills that contain the exact regulatory procedures and rules you must follow. "
            "IMPORTANT: Before responding to any complaint, you MUST read the relevant skill file first "
            "using the read_file tool. Never answer from memory alone — always load the skill to get "
            "the correct timelines, liability rules, and escalation procedures. "
            "Start with the complaint-triage skill if unsure which skill applies."
        ),
    )
    return agent
