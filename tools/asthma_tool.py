from tools.base_db_tool import BaseDBTool

class AsthmaDBTool(BaseDBTool):
    name: str = "AsthmaDBTool"
    description: str = "Use this tool to answer questions about the asthma dataset."
    db_path: str = "asthma.db"
    table_name: str = "asthma"
