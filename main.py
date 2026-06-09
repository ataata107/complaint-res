import os
from dotenv import load_dotenv
from agent import build_agent

load_dotenv()

COMPLAINTS = [
    {
        "id": "thread-001",
        "text": (
            "I noticed a charge of $247.50 on May 28th from some merchant I don't recognize. "
            "Transaction ID is TXN001 on my checking account ending in 4821. "
            "I never made this purchase. Please investigate and refund me."
        ),
    },
    {
        "id": "thread-002",
        "text": (
            "I sent a wire transfer of $15,000 to ACME Corp on June 1st (TXN002) "
            "and the funds never arrived. The reference was IMAD 20260601MMQFMPQR000427. "
            "I need this resolved immediately."
        ),
    },
]


def run():
    agent = build_agent()

    for complaint in COMPLAINTS:
        print(f"\n{'='*60}")
        print(f"COMPLAINT [{complaint['id']}]")
        print(f"{'='*60}")
        print(complaint["text"])
        print("\n--- AGENT RESPONSE ---")

        result = agent.invoke(
            {"messages": [{"role": "user", "content": complaint["text"]}]},
            config={"configurable": {"thread_id": complaint["id"]}},
        )

        print("\n--- ALL MESSAGES (raw) ---")
        for i, msg in enumerate(result["messages"]):
            kind = type(msg).__name__
            content = msg.content
            print(f"\n[{i}] {kind}")
            if isinstance(content, str):
                print(f"     {content[:200]}")
            elif isinstance(content, list):
                for block in content:
                    print(f"     {str(block)[:200]}")

        print("\n--- FINAL RESPONSE ---")
        print(result["messages"][-1].content)


if __name__ == "__main__":
    run()
