import { useNavigate } from 'react-router-dom';
import { FlaskConical, Zap, BookOpen, Shield, Search, ArrowRight, Star } from 'lucide-react';
import SearchBar from '../components/SearchBar';

const FEATURES = [
    { icon: BookOpen, title: 'Multi-Source Retrieval', desc: 'Pulls papers from arXiv, Semantic Scholar, and PubMed simultaneously.', color: 'text-brand-400', bg: 'bg-brand-500/10' },
    { icon: Zap, title: '9-Agent Pipeline', desc: 'Refiner → Planner → Debate → Evidence → Critic → Gaps → Moderator.', color: 'text-purple-400', bg: 'bg-purple-500/10' },
    { icon: Shield, title: 'Evidence Analysis', desc: 'Scores evidence quality across source diversity and finding consistency.', color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
    { icon: Search, title: 'Research Gap Detection', desc: 'Surfaces unexplored areas and future research directions automatically.', color: 'text-amber-400', bg: 'bg-amber-500/10' },
];

const STATS = [
    { value: '9', label: 'AI Reasoning Agents' },
    { value: '3', label: 'Academic Data Sources' },
    { value: '10', label: 'Analysis Dimensions' },
    { value: '∞', label: 'Research Questions' },
];

export default function HomePage() {
    const navigate = useNavigate();

    const handleSearch = (query: string) => {
        navigate('/analysis', { state: { query } });
    };

    return (
        <div className="hero-bg min-h-screen">
            {/* Hero */}
            <div className="max-w-5xl mx-auto px-4 sm:px-6 pt-20 pb-16 text-center">
                {/* Badge */}
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-brand-500/30 bg-brand-500/10 mb-8">
                    <Star className="w-3.5 h-3.5 text-brand-400 fill-brand-400" />
                    <span className="text-xs text-brand-300 font-medium">Agentic AI · Multi-Perspective Research Analysis</span>
                </div>

                {/* Headline */}
                <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black tracking-tight mb-6 leading-none">
                    <span className="text-white">Research</span>
                    <br />
                    <span className="gradient-text">Intelligence</span>
                    <br />
                    <span className="text-white">Engine</span>
                </h1>

                <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed">
                    ResearchPilot deploys a 9-agent AI pipeline to retrieve academic papers,
                    analyze evidence, debate perspectives, detect contradictions, and surface
                    research gaps — in seconds.
                </p>

                {/* Search bar */}
                <SearchBar onSubmit={handleSearch} isLoading={false} />

                {/* Stats */}
                <div className="mt-16 grid grid-cols-4 gap-4 max-w-xl mx-auto">
                    {STATS.map((stat, i) => (
                        <div key={i} className="text-center">
                            <div className="text-3xl font-black gradient-text-blue">{stat.value}</div>
                            <div className="text-[11px] text-slate-500 mt-1">{stat.label}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Features */}
            <div className="max-w-5xl mx-auto px-4 sm:px-6 pb-24">
                <h2 className="text-center text-sm font-semibold uppercase tracking-widest text-slate-500 mb-8">
                    How It Works
                </h2>
                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    {FEATURES.map((f, i) => (
                        <div key={i} className="glass rounded-2xl p-5 group hover:bg-white/5 transition-all duration-200">
                            <div className={`w-10 h-10 rounded-xl ${f.bg} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                                <f.icon className={`w-5 h-5 ${f.color}`} />
                            </div>
                            <h3 className="font-semibold text-slate-200 text-sm mb-2">{f.title}</h3>
                            <p className="text-xs text-slate-500 leading-relaxed">{f.desc}</p>
                        </div>
                    ))}
                </div>

                {/* Pipeline visualization */}
                <div className="mt-12 glass rounded-2xl p-6">
                    <h3 className="text-sm font-semibold text-slate-300 mb-5 text-center">Orchestration Pipeline</h3>
                    <div className="flex flex-wrap items-center justify-center gap-2">
                        {[
                            'User Query', 'Query Refiner', 'Planner', 'RAG Retrieval',
                            'Pro Agent', 'Con Agent', 'Evidence Analyzer',
                            'Contradiction Detector', 'Critic Agent', 'Gap Detector',
                            'Moderator', '✨ Final Insight',
                        ].map((step, i, arr) => (
                            <div key={i} className="flex items-center gap-2">
                                <div className={`px-3 py-1.5 rounded-lg text-xs font-medium ${i === 0 ? 'bg-brand-500/20 text-brand-300 border border-brand-500/30' :
                                        i === arr.length - 1 ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                                            'bg-white/5 text-slate-400 border border-white/8'
                                    }`}>
                                    {step}
                                </div>
                                {i < arr.length - 1 && (
                                    <ArrowRight className="w-3 h-3 text-slate-700 flex-shrink-0" />
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
