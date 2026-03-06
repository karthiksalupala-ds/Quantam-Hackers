import { useState, useRef, useCallback } from 'react';
import { Search, Sparkles, ChevronRight } from 'lucide-react';

const EXAMPLE_QUERIES = [
    'Does intermittent fasting improve metabolic health?',
    'What is the effect of sleep deprivation on cognitive performance?',
    'How effective is CRISPR-Cas9 in treating genetic disorders?',
    'Does social media use cause depression in adolescents?',
    'What are the long-term effects of mindfulness meditation on brain structure?',
];

interface SearchBarProps {
    onSubmit: (query: string) => void;
    isLoading: boolean;
}

export default function SearchBar({ onSubmit, isLoading }: SearchBarProps) {
    const [query, setQuery] = useState('');
    const [focused, setFocused] = useState(false);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = useCallback(() => {
        const trimmed = query.trim();
        if (!trimmed || isLoading) return;
        onSubmit(trimmed);
    }, [query, isLoading, onSubmit]);

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const handleExample = (q: string) => {
        setQuery(q);
        textareaRef.current?.focus();
    };

    return (
        <div className="w-full max-w-3xl mx-auto">
            {/* Main input */}
            <div
                className={`relative rounded-2xl transition-all duration-300 ${focused
                        ? 'glow-border ring-1 ring-brand-500/40'
                        : 'ring-1 ring-white/8'
                    } glass-bright`}
            >
                <div className="flex items-start gap-3 p-4">
                    <Search className={`mt-1 w-5 h-5 flex-shrink-0 transition-colors ${focused ? 'text-brand-400' : 'text-slate-500'}`} />
                    <textarea
                        ref={textareaRef}
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={handleKeyDown}
                        onFocus={() => setFocused(true)}
                        onBlur={() => setFocused(false)}
                        placeholder="Ask a research question... e.g. 'Does intermittent fasting improve metabolic health?'"
                        className="flex-1 bg-transparent resize-none outline-none text-slate-100 placeholder-slate-500 text-base leading-relaxed min-h-[60px] max-h-[160px]"
                        rows={2}
                        disabled={isLoading}
                    />
                </div>

                {/* Bottom bar */}
                <div className="flex items-center justify-between px-4 pb-3 pt-0">
                    <div className="flex items-center gap-2 text-xs text-slate-600">
                        <kbd className="px-1.5 py-0.5 rounded bg-white/5 border border-white/10 text-slate-500">Enter</kbd>
                        <span>to analyze</span>
                        <span className="mx-1">·</span>
                        <kbd className="px-1.5 py-0.5 rounded bg-white/5 border border-white/10 text-slate-500">Shift+Enter</kbd>
                        <span>for newline</span>
                    </div>

                    <button
                        onClick={handleSubmit}
                        disabled={!query.trim() || isLoading}
                        className="btn-primary px-5 py-2 text-sm"
                    >
                        {isLoading ? (
                            <span className="flex items-center gap-2">
                                <span className="flex gap-1">
                                    {[0, 1, 2].map(i => (
                                        <span
                                            key={i}
                                            className="w-1.5 h-1.5 bg-white rounded-full animate-bounce-dot"
                                            style={{ animationDelay: `${i * 0.16}s` }}
                                        />
                                    ))}
                                </span>
                                Analyzing…
                            </span>
                        ) : (
                            <span className="flex items-center gap-1.5">
                                <Sparkles className="w-4 h-4" />
                                Analyze
                            </span>
                        )}
                    </button>
                </div>
            </div>

            {/* Example queries */}
            <div className="mt-4">
                <p className="text-xs text-slate-600 mb-2 text-center">Try an example:</p>
                <div className="flex flex-wrap justify-center gap-2">
                    {EXAMPLE_QUERIES.slice(0, 3).map((q, i) => (
                        <button
                            key={i}
                            onClick={() => handleExample(q)}
                            disabled={isLoading}
                            className="flex items-center gap-1 px-3 py-1.5 rounded-full text-xs text-slate-400 hover:text-slate-200
                         border border-white/8 hover:border-brand-500/40 hover:bg-brand-500/10
                         transition-all duration-200 disabled:opacity-50"
                        >
                            <ChevronRight className="w-3 h-3 text-brand-500" />
                            {q.length > 45 ? q.slice(0, 45) + '…' : q}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
