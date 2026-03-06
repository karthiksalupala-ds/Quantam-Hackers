import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { AnalysisResult } from '../lib/types';
import PaperCard from './PaperCard';
import EvidenceStrengthMeter from './EvidenceStrengthMeter';
import {
    HelpCircle, Map, BookOpen, ThumbsUp, ThumbsDown,
    Zap, AlertTriangle, Shield, Search, Lightbulb, FileText, Sparkles
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
                    <div className="space-y-6">
                        {/* New Hero Insight Card */}
                        <div className="relative group animate-slide-up">
                            <div className="absolute -inset-0.5 bg-gradient-to-r from-brand-600 via-purple-600 to-emerald-500 rounded-2xl blur opacity-15 group-hover:opacity-25 transition duration-1000"></div>
                            <div className="relative glass-bright rounded-2xl p-6 border border-white/10 shadow-2xl">
                                <div className="flex items-center justify-between mb-4">
                                    <div className="flex items-center gap-2.5">
                                        <div className="p-2 bg-amber-500/10 rounded-lg border border-amber-500/20">
                                            <Sparkles className="w-5 h-5 text-amber-400 animate-pulse" />
                                        </div>
                                        <div>
                                            <h3 className="text-white font-bold text-lg tracking-tight">Executive Research Summary</h3>
                                            <div className="flex items-center gap-1.5 mt-0.5">
                                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                                                <span className="text-[10px] text-emerald-400 font-bold uppercase tracking-widest">Balanced Synthesis</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="hidden sm:flex border border-white/5 bg-white/5 px-2.5 py-1 rounded-full items-center gap-1.5">
                                        <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                                        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-tight">Pilot-IQ 1.0</span>
                                    </div>
                                </div>

                                <div className="text-slate-200 text-base leading-relaxed font-medium prose prose-invert max-w-none">
                                    <MarkdownContent text={result.final_insight} />
                                </div>

                                <div className="mt-6 pt-5 border-t border-white/5 flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="flex -space-x-2">
                                            {[1, 2, 3].map(i => (
                                                <div key={i} className={`w-6 h-6 rounded-full border-2 border-[#0B0F1A] bg-brand-${500 + i * 100} flex items-center justify-center text-[8px] font-bold text-white`}>
                                                    AI
                                                </div>
                                            ))}
                                        </div>
                                        <span className="text-xs text-slate-500 font-medium italic">Multi-consensus analysis verified</span>
                                    </div>
                                    <button className="text-[10px] font-bold text-brand-400 uppercase tracking-widest hover:text-brand-300 transition-colors">
                                        Share Detail
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <Section icon={Map} title="Research Strategy" color="text-brand-400">
                                <MarkdownContent text={result.research_strategy} />
                            </Section>
                            <Section icon={BookOpen} title="Key Evidence Summary" color="text-purple-400">
                                <MarkdownContent text={result.key_evidence} />
                            </Section>
                        </div>
                    </div>
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
