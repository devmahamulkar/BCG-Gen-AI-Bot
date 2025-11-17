import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CSV_PATH = "10K_Extracted_Financials.csv"

@st.cache_data
def load_data(path=CSV_PATH):
    df = pd.read_csv(path)
    df['Fiscal Year'] = df['Fiscal Year'].astype(int)
    return df

def compute_ratios(df):
    df2 = df.copy()
    # Profit margin = Net Income / Revenue
    df2['Profit Margin (%)'] = (pd.to_numeric(df2['Net Income (USD mn)'], errors='coerce') / pd.to_numeric(df2['Total Revenue (USD mn)'], errors='coerce')) * 100
    # Debt to Assets = Total Liabilities / Total Assets
    df2['Debt to Assets (%)'] = (pd.to_numeric(df2['Total Liabilities (USD mn)'], errors='coerce') / pd.to_numeric(df2['Total Assets (USD mn)'], errors='coerce')) * 100
    # Cash Conversion = Cash from Ops / Net Income
    df2['Cash Conversion (x)'] = pd.to_numeric(df2['Cash from Ops (USD mn)'], errors='coerce') / pd.to_numeric(df2['Net Income (USD mn)'], errors='coerce')
    # Return on Assets (ROA) = Net Income / Total Assets
    df2['ROA (%)'] = (pd.to_numeric(df2['Net Income (USD mn)'], errors='coerce') / pd.to_numeric(df2['Total Assets (USD mn)'], errors='coerce')) * 100
    return df2

def format_money(v):
    try:
        if np.isnan(v):
            return "N/A"
    except:
        pass
    try:
        v = float(v)
        if abs(v) >= 1000:
            return f"${v/1000:.2f}B"
        else:
            return f"${v:.2f}M"
    except:
        return str(v)

st.set_page_config(layout="wide", page_title="GFC Enhanced Financial Chatbot Prototype")
st.title("GFC Enhanced Financial Chatbot Prototype")

df = load_data()
df_ratios = compute_ratios(df)

with st.sidebar:
    st.header("Controls")
    company = st.selectbox("Company", options=["All"] + sorted(df['Company'].unique().tolist()))
    years = sorted(df['Fiscal Year'].unique().tolist())
    year = st.selectbox("Fiscal Year (optional)", options=["All"] + years)
    show_plot = st.checkbox("Show trend plots", value=True)
    download_csv = st.button("Download filtered data as CSV")

# Filter
if company != "All":
    df_view = df_ratios[df_ratios['Company']==company]
else:
    df_view = df_ratios.copy()

if year != "All":
    df_view = df_view[df_view['Fiscal Year']==int(year)]

st.subheader("Data view")
st.dataframe(df_view.reset_index(drop=True))

# Quick metrics
st.subheader("Quick computed metrics (latest year per company)")
latest = df_ratios.sort_values(['Company','Fiscal Year']).groupby('Company').last().reset_index()
st.table(latest[['Company','Fiscal Year','Total Revenue (USD mn)','Net Income (USD mn)','Profit Margin (%)','Debt to Assets (%)','Cash Conversion (x)']])

if download_csv:
    csv = df_view.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="gfc_filtered_data.csv", mime="text/csv")

# Plots
if show_plot:
    st.subheader("Trend Plots")
    companies = df['Company'].unique().tolist() if company=="All" else [company]
    for comp in companies:
        comp_df = df_ratios[df_ratios['Company']==comp].sort_values('Fiscal Year')
        if comp_df.empty:
            continue
        # Revenue trend
        fig, ax = plt.subplots()
        ax.plot(comp_df['Fiscal Year'], comp_df['Total Revenue (USD mn)'])
        ax.set_title(f"{comp} - Revenue Trend")
        ax.set_xlabel("Year")
        ax.set_ylabel("Revenue (USD mn)")
        st.pyplot(fig)
        # Net income trend
        fig2, ax2 = plt.subplots()
        ax2.plot(comp_df['Fiscal Year'], comp_df['Net Income (USD mn)'])
        ax2.set_title(f"{comp} - Net Income Trend")
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Net Income (USD mn)")
        st.pyplot(fig2)
        # Profit margin trend
        fig3, ax3 = plt.subplots()
        ax3.plot(comp_df['Fiscal Year'], comp_df['Profit Margin (%)'])
        ax3.set_title(f"{comp} - Profit Margin (%) Trend")
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Profit Margin (%)")
        st.pyplot(fig3)

st.markdown("---")
st.subheader("Ask a predefined question (rule-based)")
q = st.text_input("Type your question (examples: 'What was Tesla revenue in 2023?', 'Show Microsoft revenue growth')")

def detect_company(q):
    for c in df['Company'].unique():
        if c.lower() in q.lower():
            return c
    return None

def detect_year(q):
    import re
    m = re.search(r'(20\\d{2})', q)
    return int(m.group(1)) if m else None

def detect_metric(q):
    ql = q.lower()
    if 'revenue' in ql:
        return 'Total Revenue (USD mn)'
    if 'net income' in ql or 'income' in ql or 'profit' in ql:
        return 'Net Income (USD mn)'
    if 'cash' in ql:
        return 'Cash from Ops (USD mn)'
    return None

def answer_query(q):
    if not q or q.strip()=="":
        return "Waiting for a question."
    comp = detect_company(q)
    met = detect_metric(q)
    yr = detect_year(q)
    if not comp:
        return "Please include a company name: Microsoft, Apple, or Tesla."
    dfc = df_ratios[df_ratios['Company']==comp].sort_values('Fiscal Year')
    if 'growth' in q.lower():
        # compute revenue YoY
        s = dfc['Total Revenue (USD mn)'].astype(float)
        pct = s.pct_change()*100
        lines = []
        for y,val,p in zip(dfc['Fiscal Year'], s, pct):
            lines.append(f\"{comp} {y} — Revenue {format_money(val)}, YoY growth: {round(p,2) if not pd.isna(p) else 'N/A'}%\".replace('nan','N/A'))
        return '\\n'.join(lines)
    if met:
        if yr:
            row = dfc[dfc['Fiscal Year']==yr]
            if row.empty:
                return f\"No data for {comp} in {yr}. Available: {', '.join(dfc['Fiscal Year'].astype(str).tolist())}\"
            return f\"{comp} {yr} — {met}: {format_money(row.iloc[0][met])}\"
        else:
            row = dfc.iloc[-1]
            return f\"{comp} {int(row['Fiscal Year'])} — {met}: {format_money(row[met])}\"
    return \"I couldn't parse that question. Try: 'What was Apple net income in 2024?' or 'Show Tesla revenue growth'.\"

if st.button("Ask") and q:
    st.text(answer_query(q))

st.markdown(\"---\")
st.subheader(\"Developer notes & next steps\")
st.markdown(\"- This prototype computes common ratios and plots trends.\\n- To add LLM polishing, pass the retrieved rows and computed ratios to the model as context.\\n- To connect to live data, replace the CSV with a DB or API endpoint.\")