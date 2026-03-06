"""
Orchestrator – coordinates the full 9-agent research pipeline.
Yields SSE-compatible dictionaries at each step for live UI streaming.
"""
import asyncio
import json
from typing import AsyncGenerator, List
from models import ResearchRequest, AnalysisResult, ResearchPaper
from agents.query_refiner import QueryRefinerAgent
from agents.planner import PlannerAgent
from agents.pro_agent import ProAgent
from agents.con_agent import ConAgent
from agents.evidence_analyzer import EvidenceAnalyzerAgent
from agents.contradiction_detector import ContradictionDetectorAgent
from agents.critic_agent import CriticAgent
from agents.gap_detector import GapDetectorAgent
from agents.moderator import ModeratorAgent
from retrieval.arxiv_client import search_arxiv
from retrieval.semantic_scholar_client import search_semantic_scholar
from retrieval.pubmed_client import search_pubmed
from retrieval.vector_store import store_papers, search_papers
import database

DEMO_PAPERS = [
    {
        "id": "demo-1", "title": "Effects of Intermittent Fasting on Health, Aging, and Disease",
        "abstract": "Intermittent fasting (IF) could be a promising approach to improving public health...",
        "authors": ["de Cabo, R.", "Mattson, M. P."], "year": 2019, "source": "PubMed",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMra1905136"
    },
    {
        "id": "demo-2", "title": "Calorie Restriction with or without Time-Restricted Eating in Weight Loss",
        "abstract": "In this randomized controlled trial involving 139 patients with obesity, we found that...",
        "authors": ["Liu, D.", "Huang, Y.", "et al."], "year": 2022, "source": "Semantic Scholar",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMoa2114833"
    }
]

DEMO_RESULT = {
    "query_id": "demo-query-123",
    "original_query": "Does intermittent fasting improve metabolic health?",
    "refined_question": "What is the empirical evidence for the relationship between intermittent fasting and metabolic health outcomes in adult humans?",
    "research_strategy": "This analysis examines multiple RCTs, systematic reviews, and observational cohort studies investigating intermittent fasting protocols (16:8, 5:2, ADF) and their effects on BMI, insulin sensitivity, lipid profiles, and inflammatory markers across diverse adult populations.",
    "key_evidence": "Evidence drawn from 8 retrieved papers spanning arXiv, Semantic Scholar, and PubMed databases, covering short-term (4-12 week) and medium-term (6-12 month) trials.",
    "supporting_arguments": "1. Multiple RCTs demonstrate significant reductions in body weight (3-8%) and BMI with 16:8 IF protocols over 8-12 weeks.\n2. Insulin sensitivity improvements have been reported in pre-diabetic populations, with fasting insulin levels declining 20-30%.\n3. Meta-analyses confirm consistent reductions in LDL cholesterol and triglycerides across diverse IF modalities.",
    "counterarguments": "1. Most studies have short follow-up periods (< 12 months), limiting conclusions about long-term sustainability.\n2. Adherence rates vary widely (40-80%), raising questions about real-world effectiveness.\n3. Many trials have small sample sizes and lack active dietary comparison arms.",
    "contradictions": "1. Contradiction: Some studies report equivalent weight loss between IF and continuous caloric restriction, suggesting the fasting window itself may not be uniquely beneficial.\n2. Sex-based differences: Several studies show greater metabolic benefits in men than women, with some female-participant trials showing no significant hormonal improvements.",
    "critical_evaluation": "The supporting arguments rely heavily on short-term RCTs with high dropout rates. Many pro-IF claims extrapolate from weight loss data to broader metabolic benefits without direct biomarker measurement. The evidence base, while growing, remains insufficient for strong causal claims.",
    "research_gaps": "Gap: Long-term (>2 year) RCTs comparing IF to isocaloric continuous restriction are absent.\nGap: Mechanistic studies on circadian biology and metabolic regulation during IF are limited.\nGap: IF effects in populations with type 2 diabetes require more rigorous investigation.\nGap: Research on psychological and behavioral effects of fasting protocols is underrepresented.",
    "final_insight": "Current evidence suggests that intermittent fasting can produce meaningful short-term improvements in metabolic health markers including body weight, insulin sensitivity, and lipid profiles in otherwise healthy adults. However, these benefits appear comparable to those achieved through equivalent caloric restriction without fasting, suggesting the fasting mechanism per se may not be uniquely advantageous. Given the methodological limitations of existing trials—including short durations, small samples, and variable adherence—strong clinical recommendations cannot yet be made. Future research should prioritize long-term comparative trials with rigorous biomarker assessment.",
    "evidence_analysis": {
        "overall_score": 6.5,
        "paper_count": 8,
        "source_diversity": 8.0,
        "consistency_score": 5.5,
        "label": "Moderate"
    },
    "papers": DEMO_PAPERS
}


class ResearchOrchestrator:
    def __init__(self):
        self.query_refiner = QueryRefinerAgent()
        self.planner = PlannerAgent()
        self.pro_agent = ProAgent()
        self.con_agent = ConAgent()
        self.evidence_analyzer = EvidenceAnalyzerAgent()
        self.contradiction_detector = ContradictionDetectorAgent()
        self.critic = CriticAgent()
        self.gap_detector = GapDetectorAgent()
        self.moderator = ModeratorAgent()

    async def run(self, request: ResearchRequest) -> AsyncGenerator[dict, None]:
        """Full pipeline yielding SSE events at each step."""
        from config import get_settings
        settings = get_settings()

        if settings.is_demo:
            yield self._step_event("demo_mode", "running", "🤖 Running in Demo Mode (no API key found)...")
            await asyncio.sleep(0.5)

            demo_data = DEMO_RESULT.copy()
            demo_data["original_query"] = request.query

            # Simulate pipeline steps for a better UX
            yield self._step_event("query_refinement", "running", "🔍 Refining Research Query...")
            await asyncio.sleep(0.3)
            yield self._step_event("query_refinement", "done", f"✅ Refined: {demo_data['refined_question'][:80]}...", {"refined_question": demo_data['refined_question']})

            yield self._step_event("planning", "running", "⚙️ Planning Research Strategy...")
            await asyncio.sleep(0.3)
            yield self._step_event("planning", "done", "✅ Research strategy determined.", {"strategy": demo_data['research_strategy']})

            yield self._step_event("retrieval", "running", "📚 Retrieving Research Papers...")
            await asyncio.sleep(0.3)
            yield self._step_event("retrieval", "done", f"✅ Retrieved {len(demo_data['papers'])} papers.", {"paper_count": len(demo_data['papers'])})

            steps = ["pro_arguments", "con_arguments", "evidence_analysis", "contradictions", "critique", "gaps", "final_insight"]
            messages = {
                "pro_arguments": "⚖️ Generating Supporting Arguments...", "con_arguments": "⚖️ Generating Counterarguments...",
                "evidence_analysis": "📊 Evaluating Evidence Strength...", "contradictions": "🧠 Detecting Contradictions...",
                "critique": "🔎 Critical Evaluation of Arguments...", "gaps": "🔬 Identifying Research Gaps...",
                "final_insight": "📄 Producing Final Research Insight..."
            }

            for step in steps:
                yield self._step_event(step, "running", messages[step])
                await asyncio.sleep(0.3)
                done_message = f"✅ {step.replace('_', ' ').capitalize()} complete."
                if step == "evidence_analysis":
                    done_message = f"✅ Evidence: {demo_data['evidence_analysis']['label']} ({demo_data['evidence_analysis']['overall_score']}/10)"
                yield self._step_event(step, "done", done_message)

            await asyncio.sleep(1)
            yield {"event": "result", "data": demo_data}
            return

        original_query = request.query

        # ── STEP 1: Query Refinement ────────────────────────────
        yield self._step_event("query_refinement", "running", "🔍 Refining Research Query...")
        refined_question = await self.query_refiner.refine(original_query)
        yield self._step_event("query_refinement", "done", f"✅ Refined: {refined_question[:80]}...", {"refined_question": refined_question})

        # ── STEP 2: Planning ─────────────────────────────────────
        yield self._step_event("planning", "running", "⚙️ Planning Research Strategy...")
        strategy = await self.planner.plan(refined_question)
        yield self._step_event("planning", "done", "✅ Research strategy determined.", {"strategy": strategy})

        # ── STEP 3: Paper Retrieval ───────────────────────────────
        yield self._step_event("retrieval", "running", "📚 Retrieving Research Papers from arXiv, Semantic Scholar, PubMed...")
        papers = await self._retrieve_papers(request, refined_question)
        yield self._step_event("retrieval", "done", f"✅ Retrieved {len(papers)} papers.", {"paper_count": len(papers)})

        if not papers:
            # Fallback to stored vector search
            papers = await search_papers(refined_question, limit=request.max_papers)

        # Store new papers
        if papers:
            asyncio.create_task(store_papers(papers))

        # Build key evidence summary
        key_evidence = self._summarize_evidence(papers)

        # ── STEP 4: Pro Arguments ────────────────────────────────
        yield self._step_event("pro_arguments", "running", "⚖️ Generating Supporting Arguments...")
        pro_args = await self.pro_agent.argue(refined_question, papers)
        yield self._step_event("pro_arguments", "done", "✅ Supporting arguments generated.")

        # ── STEP 5: Con Arguments ────────────────────────────────
        yield self._step_event("con_arguments", "running", "⚖️ Generating Counterarguments...")
        con_args = await self.con_agent.argue(refined_question, papers)
        yield self._step_event("con_arguments", "done", "✅ Counterarguments generated.")

        # ── STEP 6: Evidence Analysis ────────────────────────────
        yield self._step_event("evidence_analysis", "running", "📊 Evaluating Evidence Strength...")
        evidence_score = await self.evidence_analyzer.analyze(refined_question, papers, pro_args, con_args)
        yield self._step_event("evidence_analysis", "done", f"✅ Evidence: {evidence_score.label} ({evidence_score.overall_score}/10)")

        # ── STEP 7: Contradiction Detection ──────────────────────
        yield self._step_event("contradictions", "running", "🧠 Detecting Contradictions...")
        contradictions = await self.contradiction_detector.detect(refined_question, papers, pro_args, con_args)
        yield self._step_event("contradictions", "done", "✅ Contradiction analysis complete.")

        # ── STEP 8: Critic ───────────────────────────────────────
        yield self._step_event("critique", "running", "🔎 Critical Evaluation of Arguments...")
        critique = await self.critic.critique(refined_question, pro_args, con_args, contradictions)
        yield self._step_event("critique", "done", "✅ Critical review complete.")

        # ── STEP 9: Research Gaps ────────────────────────────────
        yield self._step_event("gaps", "running", "🔬 Identifying Research Gaps...")
        gaps = await self.gap_detector.detect_gaps(refined_question, papers, pro_args, con_args, contradictions)
        yield self._step_event("gaps", "done", "✅ Research gaps identified.")

        # ── STEP 10: Final Insight ───────────────────────────────
        yield self._step_event("final_insight", "running", "📄 Producing Final Research Insight...")
        final_insight = await self.moderator.moderate(
            refined_question, strategy, pro_args, con_args,
            evidence_score, contradictions, critique, gaps,
        )
        yield self._step_event("final_insight", "done", "✅ Final insight produced.")

        # ── Store in Supabase ────────────────────────────────────
        query_id = await database.store_query(original_query, refined_question)
        if query_id:
            await database.store_analysis(query_id, {
                "supporting_arguments": pro_args,
                "counterarguments": con_args,
                "evidence_score": evidence_score.overall_score,
                "final_insight": final_insight,
            })

        # ── Final Result Event ───────────────────────────────────
        result = AnalysisResult(
            query_id=query_id,
            original_query=original_query,
            refined_question=refined_question,
            research_strategy=strategy,
            key_evidence=key_evidence,
            supporting_arguments=pro_args,
            counterarguments=con_args,
            evidence_analysis=evidence_score,
            contradictions=contradictions,
            critical_evaluation=critique,
            research_gaps=gaps,
            final_insight=final_insight,
            papers=papers[:10],
        )
        yield {"event": "result", "data": result.model_dump(mode="json")}

    async def _retrieve_papers(
        self, request: ResearchRequest, refined_question: str
    ) -> List[ResearchPaper]:
        sources = request.sources
        per_source = max(3, request.max_papers // len(sources))

        tasks = []
        if "arxiv" in sources:
            tasks.append(search_arxiv(refined_question, per_source))
        if "semantic_scholar" in sources:
            tasks.append(search_semantic_scholar(refined_question, per_source))
        if "pubmed" in sources:
            tasks.append(search_pubmed(refined_question, per_source))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        papers: List[ResearchPaper] = []
        for res in results:
            if isinstance(res, list):
                papers.extend(res)
        return papers[:request.max_papers]

    def _summarize_evidence(self, papers: List[ResearchPaper]) -> str:
        if not papers:
            return "No papers retrieved."
        lines = [f"Retrieved {len(papers)} papers from academic sources:\n"]
        for i, p in enumerate(papers[:8], 1):
            year = f" ({p.year})" if p.year else ""
            lines.append(f"{i}. [{p.source.upper()}] {p.title}{year}")
        return "\n".join(lines)

    @staticmethod
    def _step_event(step: str, status: str, message: str, data: dict = None) -> dict:
        return {
            "event": "step",
            "data": {
                "step": step,
                "status": status,
                "message": message,
                "data": data or {},
            },
        }
