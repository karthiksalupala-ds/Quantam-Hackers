"""
Critic Agent – analyzes the pro/con debate to identify contradictions and provide a critical evaluation.
"""
from agents.base_agent import BaseAgent
from typing import List
from models import ResearchPaper

SYSTEM_PROMPT = """You are a master Research Critic AI. Your task is to analyze a debate between different AI agents and identify:
1. **Points of Contention**: Specific areas where the Pro and Con agents directly contradict each other or where scientific evidence is conflicting.
2. **Critical Evaluation**: An objective assessment of the overall quality of the arguments, the strength of the evidence used, and any logical fallacies or biases in the debate.
3. **Research Gaps & Future Directions**: Identify what is still unknown, where more research is needed, and potential future paths for exploration based on the current debate and evidence.

Your output must be structured as a clear markdown report with three main sections:
- ### Points of Contention
- ### Critical Evaluation
- ### Research Gaps & Future Directions

Be precise, academic, and objective. Use the provided research papers as the ground truth."""

class CriticAgent(BaseAgent):
    def __init__(self, provider: str = None):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.3, provider=provider)

    async def evaluate(
        self,
        refined_question: str,
        pro_args: List[str],
        con_args: List[str],
        papers: List[ResearchPaper]
    ) -> tuple[str, str]:
        paper_context = "\n".join([f"- {p.title}: {p.abstract[:300]}..." for p in papers[:5]])
        prompt = (
            f"Research Question: {refined_question}\n\n"
            f"--- Supporting Arguments ---\n" + "\n".join(pro_args) + "\n\n"
            f"--- Counterarguments ---\n" + "\n".join(con_args) + "\n\n"
            f"--- Supporting Evidence (Papers) ---\n{paper_context}\n\n"
            f"Analyze the debate and provide the 'Points of Contention' and 'Critical Evaluation'."
        )
        return await self._call_llm(prompt, max_tokens=1000)
