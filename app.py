import uuid
import streamlit as st
from dotenv import load_dotenv
from agent import build_agent

load_dotenv()

st.set_page_config(page_title="Complaint Resolution Agent", page_icon="🏦", layout="wide")

st.title("🏦 Complaint Resolution Agent")
st.caption("Powered by LangChain Deep Agents + GPT-4o")


def parse_trace(messages: list) -> dict:
    """Extract activated skills and tool calls from agent message history."""
    skills, tools = [], []
    for msg in messages:
        content = msg.content
        # read_file calls appear as dicts in AIMessage content list
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("name") == "read_file":
                    path = block.get("arguments", "")
                    if "SKILL.md" in str(path):
                        skill = str(path).split("skills/")[-1].split("/")[0]
                        if skill and skill not in skills:
                            skills.append(skill)
                elif isinstance(block, dict) and block.get("type") == "function_call":
                    name = block.get("name", "")
                    if name and name != "read_file" and name not in [t["name"] for t in tools]:
                        tools.append({"name": name, "args": block.get("arguments", "")})
        # Also check tool_calls attribute
        if hasattr(msg, "tool_calls"):
            for tc in (msg.tool_calls or []):
                name = tc.get("name", "")
                if name == "read_file":
                    path = str(tc.get("args", {}).get("file_path", ""))
                    if "SKILL.md" in path:
                        skill = path.split("skills/")[-1].split("/")[0]
                        if skill and skill not in skills:
                            skills.append(skill)
                elif name and name not in [t["name"] for t in tools]:
                    tools.append({"name": name, "args": str(tc.get("args", ""))})
    return {"skills": skills, "tools": tools}


# Sidebar
with st.sidebar:
    st.header("Sample Complaints")
    samples = {
        "💳 Unauthorized Charge": (
            "I noticed a charge of $247.50 on May 28th from some merchant I don't recognize. "
            "Transaction ID is TXN001 on my checking account ending in 4821. "
            "I never made this purchase. Please investigate and refund me."
        ),
        "🏦 Missing Wire Transfer": (
            "I sent a wire transfer of $15,000 to ACME Corp on June 1st (TXN002) "
            "and the funds never arrived. The reference was IMAD 20260601MMQFMPQR000427. "
            "I need this resolved immediately."
        ),
        "🏠 Escrow Fee Dispute": (
            "My mortgage statement shows an escrow shortage of $800 that I don't understand. "
            "My insurance hasn't changed and my taxes are the same as last year. "
            "I think there's an error in my escrow analysis."
        ),
    }
    for label, text in samples.items():
        if st.button(label, use_container_width=True):
            st.session_state.prefill = text

    st.divider()
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.caption(f"Thread: `{st.session_state.get('thread_id', '')[:8]}...`")

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "agent" not in st.session_state:
    with st.spinner("Loading agent and skills..."):
        st.session_state.agent = build_agent()

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
    if msg["role"] == "assistant" and msg.get("trace"):
        trace = msg["trace"]
        with st.expander("🔍 Agent trace", expanded=False):
            if trace["skills"]:
                st.markdown("**Skills activated**")
                for s in trace["skills"]:
                    st.success(f"📘 {s}")
            if trace["tools"]:
                st.markdown("**Tools called**")
                for t in trace["tools"]:
                    st.info(f"🔧 `{t['name']}`  {t['args'][:80]}")

# Pre-fill from sidebar
prefill = st.session_state.pop("prefill", "")
user_input = st.chat_input("Describe your complaint...", key="chat_input")
if prefill and not user_input:
    user_input = prefill

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing complaint..."):
            result = st.session_state.agent.invoke(
                {
                    "messages": [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                },
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )

        raw = result["messages"][-1].content
        if isinstance(raw, list):
            response = "\n".join(
                block["text"] for block in raw if block.get("type") == "text"
            )
        else:
            response = raw

        trace = parse_trace(result["messages"])
        st.markdown(response)

        with st.expander("🔍 Agent trace", expanded=True):
            if trace["skills"]:
                st.markdown("**Skills activated**")
                for s in trace["skills"]:
                    st.success(f"📘 {s}")
            else:
                st.warning("No skill activated")
            if trace["tools"]:
                st.markdown("**Tools called**")
                for t in trace["tools"]:
                    st.info(f"🔧 `{t['name']}`  {t['args'][:80]}")

    st.session_state.messages.append({"role": "assistant", "content": response, "trace": trace})
