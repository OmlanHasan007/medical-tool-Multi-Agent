import requests
from langchain.tools import BaseTool

class MedicalWebSearchTool(BaseTool):
    name: str = "MedicalWebSearchTool"
    description: str = "Use this tool to search the web for general medical information such as disease definitions, symptoms, treatments, or medications. Do NOT use for dataset statistics."

    def _run(self, query: str) -> str:
        try:
            url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            abstract = data.get("AbstractText", "").strip()
            related = [r.get("Text", "") for r in data.get("RelatedTopics", [])[:3] if "Text" in r]
            if abstract:
                result = f"Summary: {abstract}"
                if related:
                    result += "\n\nRelated:\n" + "\n".join(f"- {r}" for r in related)
                return result
            if related:
                return "Related Information:\n" + "\n".join(f"- {r}" for r in related)
            return "No direct answer found. Please consult a medical professional."
        except Exception as e:
            return f"Web search failed: {e}"

    async def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")
