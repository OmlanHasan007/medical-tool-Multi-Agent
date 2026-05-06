import os
from langchain.tools import BaseTool
from langchain_anthropic import ChatAnthropic
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents import AgentType
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
            agent = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                verbose=False
            )
            return agent.run(query)
        except Exception as e:
            return f"Error querying {self.db_path}: {e}"

    async def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")