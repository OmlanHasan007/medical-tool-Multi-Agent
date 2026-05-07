"""
Multi-Tool Medical Agent - main entry point (CLI mode).
For the web UI, run: streamlit run app.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Try multiple ways to load the .env file
env_path = Path(r"D:\Github project\medical-tool-Multi-Agent-main\.env")
load_dotenv(dotenv_path=env_path, override=True)

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent

from tools.heart_tool import HeartDiseaseDBTool
from tools.cancer_tool import CancerDBTool
from tools.diabetes_tool import DiabetesDBTool
from tools.asthma_tool import AsthmaDBTool
from tools.kidney_tool import KidneyDBTool
from tools.web_search_tool import MedicalWebSearchTool

SYSTEM_PROMPT = """You are a helpful medical data assistant. You have access to several tools:
- HeartDiseaseDBTool: for heart disease dataset queries
- CancerDBTool: for cancer dataset queries
- DiabetesDBTool: for diabetes dataset queries
- AsthmaDBTool: for asthma dataset queries
- KidneyDBTool: for kidney disease dataset queries
- MedicalWebSearchTool: for general medical information

Always use the appropriate tool based on the question.
For dataset statistics use the DB tools.
For general medical knowledge use the web search tool.
IMPORTANT: This is for informational purposes only, not medical advice."""


def build_agent(verbose: bool = True):
    # Try environment variable first, then direct load
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        # Try reading the .env file directly as fallback
        try:
            with open(r"D:\Github project\medical-tool-Multi-Agent-main\.env", "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break
        except Exception:
            pass

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found. Please check your .env file.")

    llm = ChatAnthropic(
        model="claude-sonnet-4-5",
        temperature=0,
        anthropic_api_key=api_key
    )

    tools = [
        HeartDiseaseDBTool(),
        CancerDBTool(),
        DiabetesDBTool(),
        AsthmaDBTool(),
        KidneyDBTool(),
        MedicalWebSearchTool(),
    ]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
    )

    return agent


def run_with_memory(agent, query: str, chat_history: list) -> str:
    messages = chat_history + [HumanMessage(content=query)]
    result = agent.invoke({"messages": messages})
    return result["messages"][-1].content


def main():
    print("\n🧠 Multi-Tool Medical Agent (type 'exit' to quit)\n")
    agent = build_agent()
    chat_history = []

    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if not query:
            continue
        try:
            response = run_with_memory(agent, query, chat_history)
            chat_history.append(HumanMessage(content=query))
            chat_history.append(AIMessage(content=response))
            if len(chat_history) > 20:
                chat_history = chat_history[-20:]
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\n[Error] {e}\n")


if __name__ == "__main__":
    main()