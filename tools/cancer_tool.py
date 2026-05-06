from tools.base_db_tool import BaseDBTool

class CancerDBTool(BaseDBTool):
    name: str = "CancerDBTool"
    description: str = "Use this tool to answer questions about the cancer prediction dataset."
    db_path: str = "cancer.db"
    table_name: str = "cancer"
