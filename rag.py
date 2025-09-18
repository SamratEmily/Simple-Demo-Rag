from rag_core import rag_answer  # reuse core logic and index

# =========
# Setup
# =========
"""CLI entry that reuses rag_core.rag_answer and existing index."""

if __name__ == "__main__":
    print("RAG chat ready. Type 'exit' to quit.")
    try:
        while True:
            user_q = input("You: ").strip()
            if not user_q:
                continue
            if user_q.lower() in {"exit", "quit", "q"}:
                break
            answer = rag_answer(user_q)
            print(f"Assistant: {answer}")
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")