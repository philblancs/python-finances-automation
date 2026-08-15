# Python Finances Automation

A Python-based personal finance automation and analytics application that processes bank transaction data, categorizes expenses, and provides an interactive financial dashboard using Streamlit.

The project is being developed as both a practical finance application and a learning project covering Python, data analysis, data engineering, machine learning, NLP, LLMs, and AI engineering.

---

## Project Overview

Managing personal financial data often involves downloading bank statements, cleaning transaction data, categorizing expenses, and manually analyzing spending patterns.

This project aims to automate that workflow.

The current application allows users to:

- Upload transaction data from CSV files
- Process and clean transaction data
- Separate debits and credits
- Categorize transactions
- Create custom expense categories
- Learn transaction categories from user corrections
- Summarize expenses by category
- Visualize expenses using charts
- Convert PDF bank statements into CSV data
- Use OCR as a fallback for PDFs where table extraction fails

The long-term goal is to evolve this into a production-quality financial analytics platform incorporating machine learning, NLP, LLMs, and AI agents.

---

## Current Architecture

The project currently consists of two main Streamlit applications:

```text
python-finances-automation/
│
├── index.py
├── docparser.py
├── requirements.txt
├── sample_bank_statement.csv
├── README.md
├── .gitignore
└── .venv/                 # Local development environment
