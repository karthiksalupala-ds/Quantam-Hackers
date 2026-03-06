// TypeScript interfaces for ResearchPilot

export interface ResearchPaper {
    id?: string;
    title: string;
    abstract: string;
    content?: string;
    source: 'arxiv' | 'semantic_scholar' | 'pubmed' | string;
    url?: string;
    authors?: string[];
    year?: number;
    citations?: number;
}

export interface EvidenceScore {
    overall_score: number;
    paper_count: number;
    source_diversity: number;
    consistency_score: number;
    label: 'Strong' | 'Moderate' | 'Limited' | 'Insufficient';
}

export interface AnalysisResult {
    query_id?: string;
    original_query: string;
    refined_question: string;
    research_strategy: string;
    key_evidence: string;
    supporting_arguments: string;
    counterarguments: string;
    evidence_analysis: EvidenceScore;
    contradictions: string;
    critical_evaluation: string;
    research_gaps: string;
    final_insight: string;
    papers: ResearchPaper[];
    timestamp?: string;
}

export interface PipelineStep {
    step: string;
    status: 'pending' | 'running' | 'done' | 'error';
    message: string;
    data?: Record<string, unknown>;
}

export interface SSEEvent {
    event: 'step' | 'result' | 'error' | 'done';
    data: PipelineStep | AnalysisResult | { message: string } | Record<string, unknown>;
}

export interface ResearchRequest {
    query: string;
    max_papers?: number;
    sources?: string[];
}

// Pipeline step definitions (ordered)
export const PIPELINE_STEPS: Array<{ id: string; icon: string; label: string }> = [
    { id: 'query_refinement', icon: '🔍', label: 'Refining Research Query' },
    { id: 'planning', icon: '⚙️', label: 'Planning Research Strategy' },
    { id: 'retrieval', icon: '📚', label: 'Retrieving Research Papers' },
    { id: 'pro_arguments', icon: '⚖️', label: 'Generating Supporting Arguments' },
    { id: 'con_arguments', icon: '⚖️', label: 'Generating Counterarguments' },
    { id: 'evidence_analysis', icon: '📊', label: 'Evaluating Evidence Strength' },
    { id: 'contradictions', icon: '🧠', label: 'Detecting Contradictions' },
    { id: 'critique', icon: '🔎', label: 'Critical Evaluation' },
    { id: 'gaps', icon: '🔬', label: 'Identifying Research Gaps' },
    { id: 'final_insight', icon: '📄', label: 'Producing Final Research Insight' },
];
