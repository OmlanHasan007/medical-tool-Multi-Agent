from tools.base_db_tool import BaseDBTool

class HeartDiseaseDBTool(BaseDBTool):
    name: str = "HeartDiseaseDBTool"
    description: str = "Use this tool to answer questions about the heart disease dataset."
    db_path: str = "heart_disease.db"
    table_name: str = "heart"
