# BCG-Gen-AI-Bot
#short summary
I learned how to extract, clean, and structure key financial data from 10-K filings for Microsoft, Apple, and Tesla. I prepared an AI-readable dataset containing Total Revenue, Net Income, Total Assets, Total Liabilities, and Cash from Operating Activities for the last three fiscal years. I implemented preprocessing (unit standardization and missing-value handling), basic feature engineering (YoY growth, profit margin, debt-to-assets, cash conversion, ROA), and built a rule-based chatbot prototype (command-line and Streamlit versions). I also created a retrieval + context workflow designed for safe LLM integration (RAG pattern) and packaged everything with documentation and examples.

#task description
Objective: Build an AI-powered financial chatbot for GFC that can interpret and present insights from 10-K data.
Step 1: Manually extract key metrics from 10-Ks for Microsoft, Apple, Tesla (last 3 fiscal years): Total Revenue, Net Income, Total Assets, Total Liabilities, Cash from Operating Activities. Save in Excel/CSV.
Step 2: Prepare a Jupyter notebook and use Python (pandas) to compute YoY growth and insights.
Step 3: Build a prototype chatbot that answers predefined queries and can be extended to LLM-based replies.
Deliverable: Dataset, Python scripts, notebook, a working prototype (command line and/or Streamlit), and documentation.

#deliverables you can show on GitHub
10K_Extracted_Financials.csv and 10K_Extracted_Financials.xlsx — cleaned dataset (USD mn).
simple_chatbot.py — command-line, rule-based chatbot for predefined queries.
streamlit_enhanced_chatbot.py — Streamlit web UI with:
Company/year selectors
Ratio computations (Profit Margin, Debt-to-Assets, Cash Conversion, ROA)
Trend plots (Revenue, Net Income, Profit Margin)
Rule-based QA box and CSV export
enhanced_chatbot_with_state.py — state-aware, follow-up-capable prototype.
llm_ready_chatbot.py & llm_integration_helper.py — templates and prompt scaffolding for safe LLM integration (RAG style).
financial_chatbot_notebook.ipynb — Jupyter notebook demonstrating data loading, basic computations, and example queries.
README.txt and README.md (see below) — instructions, run commands, and notes.
test_results.txt — sample sessions demonstrating expected outputs.
LICENSE.txt (MIT) — permissive license.
Packaged ZIP files for quick sharing (gfc_chatbot_full_package.zip, etc.)

gfc-financial-chatbot/
├─ data/
│  ├─ 10K_Extracted_Financials.csv
│  └─ 10K_Extracted_Financials.xlsx
├─ notebooks/
│  └─ financial_chatbot_notebook.ipynb
├─ src/
│  ├─ simple_chatbot.py
│  ├─ enhanced_chatbot_with_state.py
│  ├─ streamlit_enhanced_chatbot.py
│  ├─ llm_ready_chatbot.py
│  └─ llm_integration_helper.py
├─ test_results.txt
├─ README.md
├─ requirements.txt
├─ LICENSE.txt
└─ .gitignore

Generate the README.md, .gitignore, and requirements.txt files in the ZIP or locally for you to copy.
Create a run_chatbot.bat (Windows) to auto-create venv, install deps, and run Streamlit.
Create a GitHub Actions workflow that runs basic tests when you push.
Produce a short commit history & tags ready for submission.
