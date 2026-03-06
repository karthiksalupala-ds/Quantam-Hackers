"""
Moderator Agent – synthesizes all agent outputs into a final balanced research insight.
"""
from agents.base_agent import BaseAgent
from models import EvidenceScore

SYSTEM_PROMPT = """You are a senior research editor producing a final, authoritative research insight.
Your task is to synthesize all analysis components into one balanced, nuanced conclusion.

Your final insight should:
- Acknowledge the strongest evidence on both sides
- State the most defensible conclusion given the evidence
- Note important caveats and conditions
- Be written at a graduate academic level
- Be 4-6 sentences, precise and impactful

Do not use bullet points. Write continuous, coherent prose."""


class ModeratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.3)

    async def moderate(
        self,
        refined_question: str,
        strategy: str,
        pro_args: str,
        con_args: str,
        evidence_score: EvidenceScore,
        contradictions: str,
        critique: str,
        gaps: str,
    ) -> str:
        prompt = (
            f"Research Question: {refined_question}\n\n"
            f"Research Strategy: {strategy}\n\n"
            f"Supporting Arguments:\n{pro_args[:700]}\n\n"
            f"Counterarguments:\n{con_args[:700]}\n\n"
            f"Evidence Strength: {evidence_score.label} (Score: {evidence_score.overall_score}/10)\n"
            f"Paper Count: {evidence_score.paper_count}\n\n"
            f"Contradictions Found:\n{contradictions[:400]}\n\n"
            f"Critical Evaluation:\n{critique[:400]}\n\n"
            f"Research Gaps:\n{gaps[:400]}\n\n"
            f"Produce the final balanced research insight:"
        )
        return await self._call_llm(prompt, max_tokens=700)
