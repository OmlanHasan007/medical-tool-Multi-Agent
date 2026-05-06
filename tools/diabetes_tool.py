from tools.base_db_tool import BaseDBTool

class DiabetesDBTool(BaseDBTool):
    name: str = "DiabetesDBTool"
    description: str = "Use this tool to answer questions about the diabetes dataset."
    db_path: str = "diabetes.db"
    table_name: str = "diabetes"
