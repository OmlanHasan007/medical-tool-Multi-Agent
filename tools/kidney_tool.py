from tools.base_db_tool import BaseDBTool

class KidneyDBTool(BaseDBTool):
    name: str = "KidneyDBTool"
    description: str = "Use this tool to answer questions about the chronic kidney disease dataset."
    db_path: str = "kidney.db"
    table_name: str = "kidney"
