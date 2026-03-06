"""
Pro Agent – generates supporting arguments backed by research evidence.
"""
from typing import List
from agents.base_agent import BaseAgent
from models import ResearchPaper

class ProAgent(BaseAgent):
    def __init__(self, name: str = "Pro Debater", focus: str = "general supportive evidence"):
        system_prompt = f"""You are a scientific advocate: {name}.
Your focus is to present the strongest evidence-based case FOR a given research position, specifically emphasizing:
{focus}

Using the provided research papers:
- Identify compelling supporting findings related to your focus
- Reference specific papers by title or findings
- Highlight patterns and strong evidence
- Be rigorous but persuasive

Write 3-5 well-structured supporting arguments. Format as numbered points."""
        super().__init__(system_prompt=system_prompt, temperature=0.4)
        self.name = name

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
