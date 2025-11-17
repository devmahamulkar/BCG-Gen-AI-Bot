
GFC Enhanced Chatbot Package

Files:
- streamlit_enhanced_chatbot.py : Enhanced Streamlit app with ratios, plots, rule-based QA, and CSV export.
- llm_integration_helper.py      : Helper to format context and prompt for LLM calls.
- 10K_Extracted_Financials.csv  : Dataset
- 10K_Extracted_Financials.xlsx : Excel version

How to run:
pip install streamlit pandas matplotlib openpyxl
streamlit run streamlit_enhanced_chatbot.py

Notes:
- Plots use matplotlib (one plot per figure). Do not set colors unless desired.
- The app computes Profit Margin, Debt-to-Assets, Cash Conversion, and ROA.
- To integrate an LLM, use llm_integration_helper.build_context_rows to prepare facts and then call your model with PROMPT_TEMPLATE.
