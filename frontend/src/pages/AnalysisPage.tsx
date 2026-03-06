import { useState, useEffect, useCallback, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import type { AnalysisResult, PipelineStep } from '../lib/types';
import { analyzeResearch } from '../lib/api';
import SearchBar from '../components/SearchBar';
import ReasoningPipeline from '../components/ReasoningPipeline';
import ResultsPanel from '../components/ResultsPanel';
import { ArrowLeft, RotateCcw, AlertCircle } from 'lucide-react';

export default function AnalysisPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const { user } = useAuth();
    const initialQuery = (location.state as { query?: string })?.query ?? '';

    const [query, setQuery] = useState(initialQuery);
    const [steps, setSteps] = useState<Record<string, PipelineStep>>({});
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const cleanupRef = useRef<(() => void) | null>(null);

    const runAnalysis = useCallback((q: string) => {
        // Abort any in-flight request
        cleanupRef.current?.();
        setQuery(q);
        setSteps({});
        setResult(null);
        setError(null);
        setIsLoading(true);

        const requestPayload = {
            query: q,
            max_papers: 12,
            ...(user?.id ? { user_id: user.id } : {})
        };

        const cleanup = analyzeResearch(
            requestPayload,
            (step: PipelineStep) => {
                setSteps(prev => ({ ...prev, [step.step]: step }));
            },
            (res: AnalysisResult) => {
                setResult(res);
            },
            (msg: string) => {
                setError(msg);
                setIsLoading(false);
            },
            () => {
                setIsLoading(false);
            },
        );
        cleanupRef.current = cleanup;
    }, []);

    // Auto-start if we have an initial query
    useEffect(() => {
        if (initialQuery) runAnalysis(initialQuery);
        return () => cleanupRef.current?.();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleNewQuery = (q: string) => runAnalysis(q);

    return (
        <div className="min-h-screen">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
                {/* Header */}
                <div className="flex items-center gap-3 mb-8">
                    <button
                        onClick={() => navigate('/')}
                        className="p-2 rounded-xl text-slate-500 hover:text-slate-200 hover:bg-white/5 transition-all"
                    >
                        <ArrowLeft className="w-4 h-4" />
                    </button>
                    <div className="flex-1">
                        <SearchBar onSubmit={handleNewQuery} isLoading={isLoading} />
                    </div>
                </div>

                {/* Error state */}
                {error && (
                    <div className="mb-6 flex items-start gap-3 p-4 rounded-xl bg-red-500/10 border border-red-500/30 animate-fade-in">
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-red-300">Analysis Error</p>
                            <p className="text-xs text-red-400/80 mt-0.5">{error}</p>
                            <button
                                onClick={() => runAnalysis(query)}
                                className="mt-2 flex items-center gap-1 text-xs text-red-300 hover:text-white"
                            >
                                <RotateCcw className="w-3 h-3" /> Retry
                            </button>
                        </div>
                    </div>
                )}

                {/* Main layout */}
                <div className="grid lg:grid-cols-[340px_1fr] gap-6">
                    {/* Left: Pipeline */}
                    <div className="space-y-4">
                        {(isLoading || Object.keys(steps).length > 0) && (
                            <ReasoningPipeline steps={steps} isActive={isLoading} />
                        )}

                        {/* Query info */}
                        {query && !isLoading && result && (
                            <div className="glass rounded-xl p-4 text-xs text-slate-500">
                                <p className="font-medium text-slate-400 mb-1">Query</p>
                                <p className="italic">"{query}"</p>
                                <div className="mt-3 pt-3 border-t border-white/5 flex items-center gap-2">
                                    <span className="text-emerald-400">✓</span>
                                    <span>Analysis complete</span>
                                </div>
                            </div>
                        )}

                        {/* Empty loading state */}
                        {!query && !isLoading && !result && (
                            <div className="glass rounded-xl p-6 text-center text-slate-600">
                                <p className="text-sm">Enter a research question above to begin.</p>
                            </div>
                        )}
                    </div>

                    {/* Right: Results */}
                    <div>
                        {/* Loading skeleton */}
                        {isLoading && !result && (
                            <div className="space-y-3">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="glass rounded-xl h-24 shimmer" />
                                ))}
                            </div>
                        )}

                        {/* Results */}
                        {result && <ResultsPanel result={result} />}
                    </div>
                </div>
            </div>
        </div>
    );
}
