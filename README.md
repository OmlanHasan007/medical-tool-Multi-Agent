# 🧠 Multi-Tool Medical Agent

An AI-driven medical assistant built with **OpenAI GPT-4o**, **LangChain**, and **SQLite**, featuring a **Streamlit web UI**, **conversation memory**, **PDF report export**, and support for **5 medical datasets**.

---

## 🆕 What's New (v2.0)

| Feature | Description |
|---|---|
| 🖥️ Streamlit Web UI | Full chat interface with example queries and live responses |
| 🧠 Conversation Memory | Remembers the last 10 turns — ask follow-up questions naturally |
| 📄 PDF Report Export | Export the full session as a formatted PDF with one click |
| 🌬️ Asthma Dataset | New AsthmaDBTool for asthma diagnosis queries |
| 🫘 Kidney Disease Dataset | New KidneyDBTool for chronic kidney disease queries |

---

## 🎯 Objective: Intelligent Medical Query Router

This project creates a **Multi-Tool OpenAI Agent** that automatically routes questions to the correct source:

1. 🩺 **Structured medical data (SQL):** Statistical questions about 5 medical datasets.
2. 🌐 **General medical web search:** Definitions, symptoms, treatments, and more.

---

## 🧩 Tools Overview

| Tool | Dataset | Access |
|---|---|---|
| HeartDiseaseDBTool | Heart Disease | SQLite |
| CancerDBTool | Cancer Prediction | SQLite |
| DiabetesDBTool | Diabetes | SQLite |
| AsthmaDBTool | Asthma | SQLite |
| KidneyDBTool | Chronic Kidney Disease | SQLite |
| MedicalWebSearchTool | Web (DuckDuckGo) | HTTP |

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Agent Framework | LangChain |
| LLM | OpenAI GPT-4o |
| Database | SQLite |
| Web UI | Streamlit |
| PDF Generation | ReportLab |
| Memory | LangChain ConversationBufferWindowMemory |

---

## 📊 Datasets

| Dataset | Source |
|---|---|
| Heart Disease | https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset |
| Cancer Prediction | https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset |
| Diabetes | https://www.kaggle.com/datasets/mathchi/diabetes-data-set |
| Asthma | https://www.kaggle.com/datasets/rabieelkharoua/asthma-disease-dataset |
| Chronic Kidney Disease | https://www.kaggle.com/datasets/mansoordaku/ckdisease |

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

    git clone https://github.com/OmlanHasan007/medical-tool-Multi-Agent.git
    cd medical-tool-Multi-Agent

### 2. Create Virtual Environment

    python -m venv venv
    source venv/bin/activate        # macOS/Linux
    venv\Scripts\activate           # Windows

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Add OpenAI API Key

    cp .env.example .env
    # Edit .env and paste your OPENAI_API_KEY

### 5. Prepare Databases

Download the CSV files from Kaggle into the data/ folder, then run:

    python scripts/convert_csv_to_sqlite.py data/csv_xlsx/heart.csv heart_disease.db --table-name heart
    python scripts/convert_csv_to_sqlite.py data/csv_xlsx/diabetes.csv diabetes.db --table-name diabetes
    python scripts/convert_csv_to_sqlite.py "data/csv_xlsx/The_Cancer_data_1500_V2.csv" cancer.db --table-name cancer
    python scripts/convert_csv_to_sqlite.py data/asthma.csv asthma.db --table-name asthma
    python scripts/convert_csv_to_sqlite.py data/kidney.csv kidney.db --table-name kidney

---

## 🚀 Running the Agent

### Web UI (Recommended)

    streamlit run app.py

Open http://localhost:8501 in your browser.

### CLI Mode

    python main_agent.py

---

## 📁 Project Structure

    medical-tool-Multi-Agent/
    ├── app.py                        # Streamlit Web UI
    ├── main_agent.py                 # Agent builder + CLI entry point
    ├── tools/
    │   ├── __init__.py
    │   ├── base_db_tool.py           # Shared SQL agent base class
    │   ├── heart_tool.py
    │   ├── cancer_tool.py
    │   ├── diabetes_tool.py
    │   ├── asthma_tool.py
    │   ├── kidney_tool.py
    │   └── web_search_tool.py
    ├── utils/
    │   ├── __init__.py
    │   └── pdf_report.py             # PDF export (ReportLab)
    ├── scripts/
    │   └── convert_csv_to_sqlite.py
    ├── src/                          # Original chatbot with RAG + ChromaDB
    ├── data/                         # CSV datasets
    ├── exports/                      # Generated PDFs
    ├── configs/
    │   └── app_config.yml
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md

---

## 💡 Example Queries

| Query | Routed To |
|---|---|
| "Show average age of heart patients." | HeartDiseaseDBTool |
| "What causes heart disease?" | MedicalWebSearchTool |
| "What percentage of cancer patients are female?" | CancerDBTool |
| "How many asthma patients have severe symptoms?" | AsthmaDBTool |
| "What is the average creatinine level in kidney patients?" | KidneyDBTool |
| "How is diabetes treated?" | MedicalWebSearchTool |

---

## ⚠️ Safety Note

LLM-generated SQL queries are used against **read-only** SQLite files. Never connect this agent to a writable or production database.

This tool is for **research and learning purposes only** and is not a substitute for professional medical advice.

---

## 🧑‍💻 Author

**Omlan Hasan** — [GitHub Profile](https://github.com/OmlanHasan007)

Built as a personal learning project to develop skills in AI agents, LangChain, and medical data analysis.

## 📜 License

Open-source for research and educational use only.