"""
Con Agent – generates counterarguments, limitations, and opposing viewpoints.
"""
from typing import List
from agents.base_agent import BaseAgent
from models import ResearchPaper

SYSTEM_PROMPT = """You are a rigorous scientific critic tasked with presenting the strongest
counterarguments, limitations, and opposing evidence for a research position.
Using the provided research papers:
- Identify methodological weaknesses and confounders
- Highlight conflicting findings or null results
- Point out generalizability issues
- Acknowledge what the evidence fails to establish

Write 3-5 well-structured counterarguments. Format as numbered points."""


class ConAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.4)

    async def argue(self, refined_question: str, papers: List[ResearchPaper]) -> str:
        context = self._build_context(papers)
        prompt = (
            f"Research Question: {refined_question}\n\n"
            f"Available Research Evidence:\n{context}\n\n"
            f"Generate counterarguments and limitations:"
        )
        return await self._call_llm(prompt, max_tokens=1500)

    def _build_context(self, papers: List[ResearchPaper]) -> str:
        snippets = []
        for i, p in enumerate(papers[:8], 1):
            authors = ", ".join(p.authors[:2]) if p.authors else "Unknown"
            year = f"({p.year})" if p.year else ""
            snippets.append(
                f"[{i}] {p.title} — {authors} {year} [{p.source}]\n{p.abstract[:400]}"
            )
        return "\n\n".join(snippets)
