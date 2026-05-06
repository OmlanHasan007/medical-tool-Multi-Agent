import os
from langchain.tools import BaseTool
from langchain_anthropic import ChatAnthropic
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

class BaseDBTool(BaseTool):
    db_path: str = ""
    table_name: str = ""

    def _run(self, query: str) -> str:
        if not os.path.exists(self.db_path):
            return f"Database file '{self.db_path}' not found. Please run the CSV-to-SQLite conversion script first."
        try:
            db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
            llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0,
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            sql_tools = toolkit.get_tools()
            agent = create_react_agent(
                model=llm,
                tools=sql_tools,
                prompt=f"You are a SQL expert. Answer questions about the {self.table_name} table. Always write and execute SQL to get the answer. Be concise.",
            )
            result = agent.invoke({"messages": [{"role": "user", "content": query}]})
            return result["messages"][-1].content
        except Exception as e:
            return f"Error querying {self.db_path}: {e}"

    async def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")