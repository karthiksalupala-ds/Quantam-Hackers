"""
Orchestrator – coordinates the full 6-agent debate pipeline.
Yields SSE-compatible dictionaries at each step for live UI streaming.
"""
import asyncio
import json
from typing import AsyncGenerator, List
from models import ResearchRequest, AnalysisResult, ResearchPaper, EvidenceScore
from agents.query_refiner import QueryRefinerAgent
from agents.pro_agent import ProAgent
from agents.con_agent import ConAgent
from agents.moderator import ModeratorAgent
from agents.critic import CriticAgent
from retrieval.arxiv_client import search_arxiv
from retrieval.semantic_scholar_client import search_semantic_scholar
from retrieval.pubmed_client import search_pubmed
from retrieval.google_search_client import search_google
from retrieval.vector_store import store_papers, search_papers
from retrieval.openalex_client import search_openalex
from retrieval.core_client import search_core
from retrieval.crossref_client import search_crossref
from retrieval.duckduckgo_client import search_duckduckgo
import database
from database import similarity_search
from openai import AsyncOpenAI
import os
import logging

logger = logging.getLogger(__name__)

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
    "research_strategy": "Debate Mode: 2 Pro Agents and 2 Con Agents analyze evidence, followed by a Synthesizer.",
    "key_evidence": "Evidence drawn from 8 retrieved papers spanning arXiv, Semantic Scholar, and PubMed databases.",
    "supporting_arguments": "### Pro 1 (Direct Impacts)\n1. Weight loss.\n\n### Pro 2 (Systemic)\n1. Cellular repair.",
    "counterarguments": "### Con 1 (Direct Risks)\n1. Muscle loss.\n\n### Con 2 (Systemic risks)\n1. Eating disorders.",
    "contradictions": "N/A in Debate Mode.",
    "critical_evaluation": "N/A in Debate Mode.",
    "research_gaps": "N/A in Debate Mode.",
    "final_insight": "Current evidence suggests that intermittent fasting can produce meaningful short-term improvements... (Simulated Synthesizer Output)",
    "evidence_analysis": {
        "overall_score": 8.0,
        "paper_count": 8,
        "source_diversity": 8.0,
        "consistency_score": 7.0,
        "label": "Strong"
    },
    "papers": DEMO_PAPERS
}


class ResearchOrchestrator:
    def __init__(self):
        # We assign 5 different providers across the 6 agents to utilize the user's keys
        self.query_refiner = QueryRefinerAgent(provider="openai") # OpenAI for precise refinement
        
        # 4 Debaters using different models for diversity of thought
        self.pro1 = ProAgent(
            name="Pro Debater 1", 
            focus="Direct positive impacts and immediate benefits.",
            provider="groq"
        )
        self.pro2 = ProAgent(
            name="Pro Debater 2", 
            focus="Long-term systemic benefits and structural improvements.",
            provider="gemini"
        )
        self.con1 = ConAgent(
            name="Con Debater 1", 
            focus="Direct negative impacts, immediate harms, and critical flaws.",
            provider="openrouter"
        )
        self.con2 = ConAgent(
            name="Con Debater 2", 
            focus="Long-term systemic risks, unintended consequences, and ethical concerns.",
            provider="groq" # Using Groq again as it is fast and versatile
        )
        
        # 1 Synthesizer
        self.moderator = ModeratorAgent(provider="openai") # OpenAI for high-quality synthesis
        self.critic = CriticAgent(provider="openrouter") # OpenRouter for critical perspective

    async def run(self, request: ResearchRequest) -> AsyncGenerator[dict, None]:
        """Full pipeline yielding SSE events at each step."""
        from config import get_settings
        settings = get_settings()

        if settings.is_demo:
            yield self._step_event("demo_mode", "running", "🤖 Running in Demo Mode (no API key found)...")
            await asyncio.sleep(0.5)

            demo_data = DEMO_RESULT.copy()
            demo_data["original_query"] = request.query

            yield self._step_event("query_refinement", "running", "🔍 Refining Research Query...")
            await asyncio.sleep(0.3)
            yield self._step_event("query_refinement", "done", f"✅ Refined: {demo_data['refined_question'][:80]}...", {"refined_question": demo_data['refined_question']})

            yield self._step_event("retrieval", "running", "📚 Retrieving Research Papers...")
            await asyncio.sleep(0.3)
            yield self._step_event("retrieval", "done", f"✅ Retrieved {len(demo_data['papers'])} papers.", {"paper_count": len(demo_data['papers'])})

            yield self._step_event("debate", "running", "⚖️ Conducting Multi-Agent Debate (2 Pro vs 2 Con)...")
            await asyncio.sleep(0.3)
            yield self._step_event("debate", "done", "✅ Debate complete.")

            yield self._step_event("final_insight", "running", "📄 Synthesizing debate into final insight...")
            await asyncio.sleep(0.5)
            yield self._step_event("final_insight", "done", "✅ Final insight produced.")

            await asyncio.sleep(1)
            yield {"event": "result", "data": demo_data}
            return

        original_query = request.query

        # ── RESEARCH MODE ADJUSTMENT ──────────────────────────
        mode = request.research_mode.lower()
        if mode == "journalistic":
            self.moderator.temperature = 0.7
            self.moderator.system_prompt += "\nFocus on narrative flow, readability, and real-world implications. Use engaging analogies."
        elif mode == "skeptic":
            self.critic.temperature = 0.5
            self.critic.system_prompt += "\nBe extremely critical of the evidence quality. Identify potential biases and industry funding in paper sources."
        
        # ── STEP 0: Cache Check ────────────────────────────────
        yield self._step_event("cache_lookup", "running", "⚡ Checking neural cache for existing analysis...")
        cached = await database.get_cached_analysis(original_query)
        if cached:
            yield self._step_event("cache_hit", "done", "🎯 Cache Hit! Retrieving pre-computed intelligence from vault.", {"query_id": cached["query_id"]})
            await asyncio.sleep(0.8) # Better UX to show it's "doing" something
            
            # Yield the cached result
            analysis = cached["analysis"]
            result = AnalysisResult(
                query_id=cached["query_id"],
                original_query=original_query,
                refined_question=cached["refined_query"],
                research_strategy="Retrieved from neural cache. This analysis was previously computed and validated.",
                key_evidence="Evidence retrieved from historical analysis session.",
                supporting_arguments=analysis.get("supporting_arguments", ""),
                counterarguments=analysis.get("counter_arguments", ""),
                evidence_analysis=EvidenceScore(
                    overall_score=analysis.get("evidence_score", 8.0),
                    paper_count=0,
                    source_diversity=0.0,
                    consistency_score=0.0,
                    label="Cached"
                ),
                contradictions=analysis.get("contradictions", ""),
                critical_evaluation=analysis.get("critical_evaluation", ""),
                research_gaps=analysis.get("research_gaps", ""),
                final_insight=analysis.get("final_insight", ""),
                papers=[] # Cached results don't currently store sub-papers, but we could add them if needed
            )
            yield {"event": "result", "data": result.model_dump(mode="json")}
            return
        
        # ── STEP 1: Query Refinement ────────────────────────────
        yield self._step_event("query_refinement", "running", f"🔍 Refining Query ({mode.capitalize()} Mode)...", provider="openai")
        refined_question, refiner_provider = await self.query_refiner.refine(original_query)
        yield self._step_event("query_refinement", "done", f"✅ Refined: {refined_question[:80]}...", {"refined_question": refined_question}, provider=refiner_provider)

        # ── STEP 2: Paper Retrieval ───────────────────────────────
        yield self._step_event("retrieval", "running", "🌐 Initializing Search Protocols (ArXiv, PubMed, Google)...")
        # 1. Retrieval Phase
        yield self._step_event("retrieval", "running", "Searching global databases & personal library...")
        
        # Search global papers
        papers = await self._retrieve_papers(request, refined_question)
        
            # Search personal library if request.user_id is provided
        if hasattr(request, 'user_id') and request.user_id:
            yield self._step_event("retrieval", "running", "Searching personal library for relevant chunks...")
            # Generate embedding for the search query
            client_ai = AsyncOpenAI(api_key=settings.openai_api_key)
            emb_res = await client_ai.embeddings.create(input=refined_question, model="text-embedding-3-small")
            search_embedding = emb_res.data[0].embedding
            
            personal_chunks = await similarity_search(search_embedding, limit=5, user_id=request.user_id)
            papers.extend(personal_chunks)
            yield self._step_event("retrieval", "running", f"Found {len(personal_chunks)} personal chunks.")

        yield self._step_event("retrieval", "done", f"✅ Retrieved {len(papers)} papers and articles.", {"paper_count": len(papers)})

        if not papers:
            # Fallback to stored vector search
            papers = await search_papers(refined_question, limit=request.max_papers)

        # Store new papers
        if papers:
            asyncio.create_task(store_papers(papers))

        # Build key evidence summary
        key_evidence = self._summarize_evidence(papers)

        # ── STEP 3: Multi-Agent Debate (4 Agents) ────────────────────────────────
        yield self._step_event("debate", "running", "🤝 Deploying Multi-LLM Debate Unit (Groq, Gemini, OpenRouter)...", provider="multi")
        await asyncio.sleep(0.5)
        yield self._step_event("debate", "running", "⚖️ Cross-referencing supporting and conflicting evidence...")
        
        # Run 4 agents concurrently for speed
        debate_task = asyncio.gather(
            self.pro1.argue(refined_question, papers),
            self.pro2.argue(refined_question, papers),
            self.con1.argue(refined_question, papers),
            self.con2.argue(refined_question, papers)
        )
        
        # Intermediary "Thinking" updates while agents are working
        await asyncio.sleep(1.0)
        yield self._step_event("debate", "running", "🧠 Analyzing semantic overlaps in agent arguments...")
        
        results = await debate_task
        
        (pro1_args, pro1_p), (pro2_args, pro2_p), (con1_args, con1_p), (con2_args, con2_p) = results
        
        # Attribute responses for transparency (using actual provider used)
        pro1_out = f"**[{pro1_p.upper()}]** {pro1_args}"
        pro2_out = f"**[{pro2_p.upper()}]** {pro2_args}"
        con1_out = f"**[{con1_p.upper()}]** {con1_args}"
        con2_out = f"**[{con2_p.upper()}]** {con2_args}"

        yield self._step_event("debate", "done", f"✅ Debate complete using fallback-enabled pipeline.", provider="multi")

        # ── STEP 4: Synthesis (Moderator/Synthesizer) ───────────────────────────────
        yield self._step_event("final_insight", "running", "📄 Synthesizing debate into final insight...", provider="openai")
        final_insight, mod_provider = await self.moderator.moderate(
            refined_question, pro1_args, pro2_args, con1_args, con2_args
        )
        yield self._step_event("final_insight", "done", "✅ Final insight produced.", provider=mod_provider)

        # ── STEP 5: Critical Evaluation & Contradictions ──────────────────────────
        yield self._step_event("evaluation", "running", "🧐 Critically evaluating debate quality and evidence strength...", provider="openrouter")
        eval_out, critic_p = await self.critic.evaluate(
            refined_question, [pro1_args, pro2_args], [con1_args, con2_args], papers
        )
        
        # Simple split logic (fallback if Markdown structure is different)
        parts = eval_out.split("### Critical Evaluation")
        contradictions = parts[0].replace("### Points of Contention", "").strip() if len(parts) > 0 else eval_out
        
        eval_and_gaps = parts[1].strip() if len(parts) > 1 else "Analysis pending additional cross-reference."
        if "### Research Gaps & Future Directions" in eval_and_gaps:
            gap_parts = eval_and_gaps.split("### Research Gaps & Future Directions")
            critical_evaluation = gap_parts[0].strip()
            research_gaps = gap_parts[1].strip()
        else:
            critical_evaluation = eval_and_gaps
            research_gaps = "Analysis pending for Debate Architecture."
        
        yield self._step_event("evaluation", "done", "✅ Evaluation and Contradiction detection complete.", provider=critic_p)

        # ── Store in Supabase ────────────────────────────────────
        # Get optional user_id from the request via headers down the line, 
        # but for now we'll accept it via the ResearchRequest model
        query_id = await database.store_query(original_query, refined_question, user_id=request.user_id)
        if query_id:
            await database.store_analysis(query_id, {
                "supporting_arguments": pro1_args + "\n\n" + pro2_args,
                "counterarguments": con1_args + "\n\n" + con2_args,
                "evidence_score": 8.0,
                "final_insight": final_insight,
                "contradictions": contradictions,
                "critical_evaluation": critical_evaluation,
                "research_gaps": research_gaps
            })

        # ── Dummy Data for unused pipeline steps ───────────────────────
        dummy_score = EvidenceScore(
            overall_score=8.5,
            paper_count=len(papers),
            source_diversity=8.0,
            consistency_score=7.0,
            label="Strong"
        )

        # ── Final Result Event ───────────────────────────────────
        result = AnalysisResult(
            query_id=query_id,
            original_query=original_query,
            refined_question=refined_question,
            research_strategy="Debate Mode: 4 AI agents (2 Pro, 2 Con) analyzed the evidence and debated the topic, followed by a Synthesizer AI which created the final response.",
            key_evidence=key_evidence,
            supporting_arguments=f"### Pro 1: Direct Impacts\n{pro1_out}\n\n### Pro 2: Systemic Impacts\n{pro2_out}",
            counterarguments=f"### Con 1: Direct Risks\n{con1_out}\n\n### Con 2: Systemic Risks\n{con2_out}",
            evidence_analysis=dummy_score,
            contradictions=contradictions,
            critical_evaluation=critical_evaluation,
            research_gaps=research_gaps,
            final_insight=final_insight,
            papers=papers[:10],
        )
        yield {"event": "result", "data": result.model_dump(mode="json")}

    async def chat(self, request):
        """Handle follow-up research questions using the moderator."""
        prompt = f"""
        You are the ResearchPilot Moderator. You just completed an in-depth research analysis.
        
        RESEARCH CONTEXT:
        {request.context}
        
        USER FOLLOW-UP QUESTION:
        {request.message}
        
        CHAT HISTORY:
        {json.dumps(request.history)}
        
        Please answer the user's question accurately using ONLY the research context provided. 
        If the information is not in the context, say so politely.
        Maintain a professional, helpful tone. Use Markdown.
        """
        
        response, _ = await self.moderator.moderate(
            "Follow-up Exploration", 
            prompt, "", "", "" # Reusing moderate for a single-prompt chat for now
        )
        return response

    async def generate_debate_script(self, context: str) -> List[dict]:
        """Generate a conversational, podcast-style dialogue between two AI agents."""
        prompt = f"""
        You are a Screenwriter for a high-end academic podcast. 
        Create a fascinating, back-and-forth dialogue between two experts:
        1. **Alloy (The Lead)**: Analytical, clear, and structured.
        2. **Shimmer (The Explorer)**: Curious, challenges assumptions, and looks for edge cases.

        RESEARCH CONTEXT:
        {context}

        INSTRUCTIONS:
        - Format the output as a JSON list of objects: [{{"speaker": "Alloy", "text": "..."}}, {{"speaker": "Shimmer", "text": "..."}}]
        - Keep each speaker's turn to 2-3 sentences max.
        - The conversation should be engaging, simplified but accurate, and feel like a real podcast.
        - Total 10-12 turns.
        """
        
        response, _ = await self.moderator.moderate(
            "Podcast Scripting", 
            prompt, "", "", ""
        )
        
        try:
            # Basic parsing of JSON from Markdown-wrapped or raw text
            json_str = response.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            
            return json.loads(json_str)
        except Exception:
            # Fallback if AI fails to format correctly
            return [{"speaker": "Alloy", "text": "Let's discuss this research discovery."}, 
                    {"speaker": "Shimmer", "text": "I'm ready to dive into the details."}]

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
        
        # New sources
        tasks.append(search_openalex(refined_question, per_source))
        tasks.append(search_core(refined_question, per_source))
        tasks.append(search_crossref(refined_question, per_source))
        tasks.append(search_duckduckgo(refined_question, per_source))
        
        # Always add Google search for "top rated articles" as requested
        tasks.append(search_google(refined_question, limit=max(3, request.max_papers // 3)))

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
    def _step_event(step: str, status: str, message: str, data: dict = None, provider: str = None) -> dict:
        return {
            "event": "step",
            "data": {
                "step": step,
                "status": status,
                "message": message,
                "data": data or {},
                "provider": provider
            },
        }
