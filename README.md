# ðŸ§  Multi-Tool Medical Agent

An AI-driven medical assistant built with **OpenAI GPT-4o**, **LangChain**, and **SQLite**, featuring a **Streamlit web UI**, **conversation memory**, **PDF report export**, and support for **5 medical datasets**.

---

## ðŸ†• What's New (v2.0)

| Feature | Description |
|---|---|
| ðŸ–¥ï¸ **Streamlit Web UI** | Full chat interface with example queries and live responses |
| ðŸ§  **Conversation Memory** | Remembers the last 10 turns â€” ask follow-up questions naturally |
| ðŸ“„ **PDF Report Export** | Export the full session as a formatted PDF with one click |
| ðŸŒ¬ï¸ **Asthma Dataset** | New `AsthmaDBTool` for asthma diagnosis queries |
| ðŸ«˜ **Kidney Disease Dataset** | New `KidneyDBTool` for chronic kidney disease queries |

---

## ðŸŽ¯ Objective: Intelligent Medical Query Router

This project creates a **Multi-Tool OpenAI Agent** that automatically routes questions to the correct source:

1. ðŸ©º **Structured medical data (SQL):** Statistical questions about 5 medical datasets.
2. ðŸŒ **General medical web search:** Definitions, symptoms, treatments, and more.

---

## ðŸ§© Tools Overview

| Tool | Dataset | Access |
|---|---|---|
| `HeartDiseaseDBTool` | Heart Disease | SQLite |
| `CancerDBTool` | Cancer Prediction | SQLite |
| `DiabetesDBTool` | Diabetes | SQLite |
| `AsthmaDBTool` | â­ Asthma | SQLite |
| `KidneyDBTool` | â­ Chronic Kidney Disease | SQLite |
| `MedicalWebSearchTool` | Web (DuckDuckGo) | HTTP |

---

## ðŸ§° Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Agent Framework | LangChain |
| LLM | OpenAI GPT-4o |
| Database | SQLite |
| Web UI | Streamlit |
| PDF Generation | ReportLab |
| Memory | LangChain `ConversationBufferWindowMemory` |

---

## ðŸ“Š Datasets

| Dataset | Source |
|---|---|
| Heart Disease | [Kaggle](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset) |
| Cancer Prediction | [Kaggle](https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset) |
| Diabetes | [Kaggle](https://www.kaggle.com/datasets/mathchi/diabetes-data-set) |
| Asthma | [Kaggle](https://www.kaggle.com/datasets/rabieelkharoua/asthma-disease-dataset) |
| Chronic Kidney Disease | [Kaggle](https://www.kaggle.com/datasets/mansoordaku/ckdisease) |

---

## âš™ï¸ Setup Instructions

### 1ï¸âƒ£ Clone the Repository

```bash
git clone https://github.com/OmlanHasan007/medical-tool-Multi-Agent.git
cd medical-tool-Multi-Agent
```

### 2ï¸âƒ£ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3ï¸âƒ£ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4ï¸âƒ£ Add OpenAI API Key

```bash
cp .env.example .env
# Edit .env and paste your OPENAI_API_KEY
```

### 5ï¸âƒ£ Prepare Databases

Download the CSV files from Kaggle into the `data/` folder, then run:

```bash
python scripts/convert_csv_to_sqlite.py data/heart.csv heart_disease.db --table-name heart
python scripts/convert_csv_to_sqlite.py data/cancer.csv cancer.db --table-name cancer
python scripts/convert_csv_to_sqlite.py data/diabetes.csv diabetes.db --table-name diabetes
python scripts/convert_csv_to_sqlite.py data/asthma.csv asthma.db --table-name asthma
python scripts/convert_csv_to_sqlite.py data/kidney.csv kidney.db --table-name kidney
```

---

## ðŸš€ Running the Agent

### Web UI (Recommended)

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### CLI Mode

```bash
python main_agent.py
```

---

## ðŸ“ Project Structure

```
multi-tool-med-agent/
â”œâ”€â”€ app.py                        # â­ Streamlit Web UI
â”œâ”€â”€ main_agent.py                 # Agent builder + CLI entry point
â”œâ”€â”€ tools/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ base_db_tool.py           # Shared SQL agent base class
â”‚   â”œâ”€â”€ heart_tool.py
â”‚   â”œâ”€â”€ cancer_tool.py
â”‚   â”œâ”€â”€ diabetes_tool.py
â”‚   â”œâ”€â”€ asthma_tool.py            # â­ New
â”‚   â”œâ”€â”€ kidney_tool.py            # â­ New
â”‚   â””â”€â”€ web_search_tool.py
â”œâ”€â”€ utils/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â””â”€â”€ pdf_report.py             # â­ PDF export (ReportLab)
â”œâ”€â”€ scripts/
â”‚   â””â”€â”€ convert_csv_to_sqlite.py
â”œâ”€â”€ data/                         # Raw CSVs (not committed)
â”œâ”€â”€ exports/                      # Generated PDFs (not committed)
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md
```

---

## ðŸ’¡ Example Queries

| Query | Routed To |
|---|---|
| "Show average age of heart patients." | `HeartDiseaseDBTool` |
| "What causes heart disease?" | `MedicalWebSearchTool` |
| "What % of cancer patients are female?" | `CancerDBTool` |
| "How many asthma patients have severe symptoms?" | `AsthmaDBTool` |
| "What is the average creatinine level in kidney patients?" | `KidneyDBTool` |
| "How is diabetes treated?" | `MedicalWebSearchTool` |

---

## âš ï¸ Safety Note

LLM-generated SQL queries are used against **read-only** SQLite files. Never connect this agent to a writable or production database.

This tool is for **research and learning purposes only** and is not a substitute for professional medical advice.

---

## ðŸ§‘â€ðŸ’» Author

**Omlan Hasan** 🔗 [GitHub Profile](https://github.com/OmlanHasan007)

## ðŸ“œ License

Open-source for research and educational use only.

