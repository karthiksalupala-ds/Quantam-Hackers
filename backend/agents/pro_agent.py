"""
Pro Agent – generates supporting arguments backed by research evidence.
"""
from typing import List
from agents.base_agent import BaseAgent
from models import ResearchPaper

SYSTEM_PROMPT = """You are a scientific advocate tasked with presenting the strongest possible
evidence-based case FOR a given research position.
Using the provided research papers as your primary source:
- Identify the most compelling supporting findings
- Reference specific papers by title or findings where relevant
- Highlight consistent patterns and strong evidence
- Be rigorous but persuasive

Write 3-5 well-structured supporting arguments. Format as numbered points."""


class ProAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.4)

    async def argue(self, refined_question: str, papers: List[ResearchPaper]) -> str:
        context = self._build_context(papers)
        prompt = (
            f"Research Question: {refined_question}\n\n"
            f"Available Research Evidence:\n{context}\n\n"
            f"Generate supporting arguments:"
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
