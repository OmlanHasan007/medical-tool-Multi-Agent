"""
Multi-Tool Medical Agent - main entry point (CLI mode).
For the web UI, run: streamlit run app.py
"""

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferWindowMemory

from tools.heart_tool import HeartDiseaseDBTool
from tools.cancer_tool import CancerDBTool
from tools.diabetes_tool import DiabetesDBTool
from tools.asthma_tool import AsthmaDBTool
from tools.kidney_tool import KidneyDBTool
from tools.web_search_tool import MedicalWebSearchTool

load_dotenv()

def build_agent(verbose: bool = True):
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        k=10,
    )

    tools = [
        HeartDiseaseDBTool(),
        CancerDBTool(),
        DiabetesDBTool(),
        AsthmaDBTool(),
        KidneyDBTool(),
        MedicalWebSearchTool(),
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=verbose,
        handle_parsing_errors=True,
    )
    return agent


def main():
    print("\n🧠 Multi-Tool Medical Agent (type 'exit' to quit)\n")
    agent = build_agent()

    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if not query:
            continue
        try:
            response = agent.run(query)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\n[Error] {e}\n")


if __name__ == "__main__":
    main()