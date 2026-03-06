import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { AnalysisResult } from '../lib/types';
import PaperCard from './PaperCard';
import EvidenceStrengthMeter from './EvidenceStrengthMeter';
import {
    HelpCircle, Map, BookOpen, ThumbsUp, ThumbsDown,
    Zap, AlertTriangle, Shield, Search, Lightbulb, FileText
} from 'lucide-react';

interface ResultsPanelProps {
    result: AnalysisResult;
}

const TABS = [
    { id: 'overview', icon: FileText, label: 'Final Insight' },
    { id: 'arguments', icon: Zap, label: 'Arguments' },
    { id: 'evidence', icon: Shield, label: 'Evidence' },
    { id: 'gaps', icon: Search, label: 'Research Gaps' },
    { id: 'papers', icon: BookOpen, label: 'Papers' },
];

function Section({ icon: Icon, title, color, children }: {
    icon: React.ElementType; title: string; color: string; children: React.ReactNode
}) {
    return (
        <div className="glass rounded-xl p-5 animate-slide-up">
            <div className={`flex items-center gap-2 mb-3 ${color}`}>
                <Icon className="w-4 h-4" />
                <h4 className="font-semibold text-sm">{title}</h4>
            </div>
            <div className="text-sm text-slate-300 leading-relaxed prose prose-invert prose-sm max-w-none">
                {children}
            </div>
        </div>
    );
}

function MarkdownContent({ text }: { text: string }) {
    return (
        <ReactMarkdown
            components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                li: ({ children }) => <li className="ml-4 mb-1">{children}</li>,
                strong: ({ children }) => <strong className="text-slate-100 font-semibold">{children}</strong>,
            }}
        >
            {text}
        </ReactMarkdown>
    );
}

export default function ResultsPanel({ result }: ResultsPanelProps) {
    const [activeTab, setActiveTab] = useState('overview');

    return (
        <div className="space-y-4 animate-fade-in">
            {/* Refined question banner */}
            <div className="glass-bright rounded-2xl p-5 border border-brand-500/20 glow-border">
                <div className="flex items-start gap-3">
                    <HelpCircle className="w-5 h-5 text-brand-400 flex-shrink-0 mt-0.5" />
                    <div>
                        <p className="text-[11px] uppercase tracking-widest text-brand-400 font-semibold mb-1">Refined Research Question</p>
                        <h3 className="text-lg font-semibold text-white leading-snug">{result.refined_question}</h3>
                    </div>
                </div>
            </div>

            {/* Tab bar */}
            <div className="flex items-center gap-1 p-1 glass rounded-xl overflow-x-auto">
                {TABS.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium whitespace-nowrap transition-all duration-200 ${activeTab === tab.id
                                ? 'bg-brand-500/20 text-brand-300 border border-brand-500/30'
                                : 'text-slate-500 hover:text-slate-300 hover:bg-white/5'
                            }`}
                    >
                        <tab.icon className="w-3.5 h-3.5" />
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Tab content */}
            <div className="space-y-3">
                {activeTab === 'overview' && (
                    <>
                        <Section icon={Map} title="Research Strategy" color="text-brand-400">
                            <MarkdownContent text={result.research_strategy} />
                        </Section>
                        <Section icon={BookOpen} title="Key Evidence" color="text-purple-400">
                            <MarkdownContent text={result.key_evidence} />
                        </Section>
                        <Section icon={Lightbulb} title="Final Balanced Research Insight" color="text-amber-400">
                            <div className="rounded-xl bg-amber-500/5 border border-amber-500/20 p-4">
                                <MarkdownContent text={result.final_insight} />
                            </div>
                        </Section>
                    </>
                )}

                {activeTab === 'arguments' && (
                    <>
                        <Section icon={ThumbsUp} title="Supporting Arguments" color="text-emerald-400">
                            <MarkdownContent text={result.supporting_arguments} />
                        </Section>
                        <Section icon={ThumbsDown} title="Counterarguments" color="text-red-400">
                            <MarkdownContent text={result.counterarguments} />
                        </Section>
                        <Section icon={AlertTriangle} title="Points of Contention" color="text-amber-400">
                            <MarkdownContent text={result.contradictions} />
                        </Section>
                        <Section icon={Shield} title="Critical Evaluation" color="text-purple-400">
                            <MarkdownContent text={result.critical_evaluation} />
                        </Section>
                    </>
                )}

                {activeTab === 'evidence' && (
                    <EvidenceStrengthMeter score={result.evidence_analysis} />
                )}

                {activeTab === 'gaps' && (
                    <Section icon={Search} title="Research Gaps & Future Directions" color="text-teal-400">
                        <MarkdownContent text={result.research_gaps} />
                    </Section>
                )}

                {activeTab === 'papers' && (
                    <div>
                        <p className="text-xs text-slate-500 mb-3">
                            {result.papers.length} papers retrieved from arXiv, Semantic Scholar, and PubMed
                        </p>
                        <div className="space-y-2">
                            {result.papers.length === 0 && (
                                <p className="text-sm text-slate-500 text-center py-8">No papers stored for this query.</p>
                            )}
                            {result.papers.map((paper, i) => (
                                <PaperCard key={paper.id ?? i} paper={paper} index={i} />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
