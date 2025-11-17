# llm_integration_helper.py
# This file shows how to prepare context for an LLM and a safe prompt template.
def build_context_rows(records):
    lines = []
    for r in records:
        lines.append(f"{r['Company']} {r['Fiscal Year']}: Revenue {r['Total Revenue (USD mn)']}, NetIncome {r['Net Income (USD mn)']}, CashOps {r['Cash from Ops (USD mn)']}")
    return "\n".join(lines)

PROMPT_TEMPLATE = """
System: You are a financial assistant. Use ONLY the facts below. When calculating, show your work and cite the row(s) used.
Context:
{context_rows}

User question:
{user_question}

Assistant:"""

# Replace the LLM_CALL function with your provider's SDK call, e.g. OpenAI, Anthropic, etc.
def llm_call_stub(prompt):
    # In production, call the model with the prompt and return the generated answer.
    return "LLM (stub) — please replace llm_call_stub with a real API call."
