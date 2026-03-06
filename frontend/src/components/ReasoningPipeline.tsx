import { CheckCircle2, Loader2, AlertCircle, Sparkles, MessageSquareQuote } from 'lucide-react';
import type { PipelineStep } from '../lib/types';
import { PIPELINE_STEPS } from '../lib/types';

interface ReasoningPipelineProps {
    steps: Record<string, PipelineStep>;
    isActive: boolean;
}

type StepStatus = 'pending' | 'running' | 'done' | 'error';

function StepStatusIndicator({ status }: { status: StepStatus }) {
    if (status === 'done') {
        return (
            <div className="relative flex items-center justify-center w-5 h-5 transition-all duration-500 scale-110">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            </div>
        );
    }
    if (status === 'running') {
        return (
            <div className="relative flex items-center justify-center w-5 h-5">
                <div className="absolute inset-0 bg-brand-500/20 rounded-full pulse-ring" />
                <div className="w-2 h-2 bg-brand-400 rounded-full animate-pulse shadow-[0_0_8px_rgba(76,110,245,0.6)]" />
            </div>
        );
    }
    if (status === 'error') {
        return <AlertCircle className="w-5 h-5 text-red-400 animate-bounce" />;
    }
    return (
        <div className="flex items-center justify-center w-5 h-5">
            <div className="w-1.5 h-1.5 bg-slate-700 rounded-full" />
        </div>
    );
}

export default function ReasoningPipeline({ steps, isActive }: ReasoningPipelineProps) {
    if (!isActive && Object.keys(steps).length === 0) return null;

    const doneCount = Object.values(steps).filter(s => s.status === 'done').length;
    const total = PIPELINE_STEPS.length;
    const progress = Math.round((doneCount / total) * 100);

    return (
        <div className="glass rounded-2xl overflow-hidden shadow-2xl animate-fade-in border border-white/10 max-w-2xl mx-auto mb-10">
            {/* Animated Header */}
            <div className="bg-white/5 border-b border-white/5 p-5">
                <div className="flex items-center gap-4 mb-4">
                    <div className="logo-container flex items-center justify-center rounded-xl bg-gradient-to-br from-brand-600 to-purple-700 w-10 h-10 shadow-lg">
                        <Sparkles className="w-6 h-6 text-white animate-pulse" />
                    </div>
                    <div>
                        <h3 className="text-white font-bold text-sm tracking-tight leading-none mb-1">Research Intelligence</h3>
                        <p className="text-[11px] text-slate-400 uppercase tracking-widest font-semibold opacity-70">Analysis Engine v1.0</p>
                    </div>
                    {isActive && (
                        <div className="ml-auto flex items-center gap-1.5 px-2.5 py-1 bg-brand-500/10 border border-brand-500/20 rounded-lg">
                            <Loader2 className="w-3 h-3 text-brand-400 animate-spin" />
                            <span className="text-[10px] text-brand-400 font-bold uppercase tracking-tighter">Analyzing</span>
                        </div>
                    )}
                </div>

                {/* Main Progress Bar */}
                <div className="space-y-1.5">
                    <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase tracking-wider px-0.5">
                        <span>Thinking Progress</span>
                        <span className="text-brand-400">{progress}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden border border-white/5 p-[1px]">
                        <div
                            className="h-full rounded-full bg-gradient-to-r from-brand-600 via-purple-500 to-emerald-400 transition-all duration-700 ease-out shadow-[0_0_10px_rgba(76,110,245,0.4)]"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                </div>
            </div>

            {/* List of Steps with Popup Messages */}
            <div className="p-4 space-y-3">
                {PIPELINE_STEPS.filter(def => def.id !== 'query_refinement').map((def, idx) => {
                    const step = steps[def.id];
                    const status: StepStatus = step?.status ?? 'pending';
                    const isRunning = status === 'running';
                    const isDone = status === 'done';
                    const isPending = status === 'pending';

                    const showConnector = idx < PIPELINE_STEPS.length - 1;

                    return (
                        <div key={def.id} className="relative group">
                            <div
                                className={`flex items-start gap-4 transition-all duration-500 ${isPending ? 'grayscale opacity-30' : 'opacity-100'
                                    }`}
                            >
                                {/* Indicator */}
                                <div className="mt-1 flex-shrink-0">
                                    <StepStatusIndicator status={status} />
                                </div>

                                {/* Content */}
                                <div className="flex-1 min-w-0 space-y-2">
                                    <div className="flex items-center gap-2">
                                        <span className={`text-sm font-bold tracking-tight transition-colors duration-300 ${isRunning ? 'text-brand-300' : isDone ? 'text-emerald-400' : 'text-slate-400'
                                            }`}>
                                            {def.label}
                                        </span>
                                    </div>

                                    {/* Popup Message Bubble */}
                                    {step?.message && !isPending && (
                                        <div className="message-popup p-3 rounded-2xl bg-white/5 border border-white/10 shadow-sm relative overflow-hidden group/msg">
                                            <div className="flex gap-2.5">
                                                <MessageSquareQuote className="w-4 h-4 text-brand-400 flex-shrink-0 mt-0.5 opacity-50" />
                                                <p className="text-[12px] leading-relaxed text-slate-300">
                                                    {step.message}
                                                </p>
                                            </div>
                                            {isRunning && (
                                                <div className="absolute bottom-0 left-0 h-[2px] bg-brand-500/30 w-full overflow-hidden">
                                                    <div className="h-full bg-brand-500 shimmer w-1/2" />
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Refined Connector Line */}
                            {showConnector && (
                                <div className={`ml-[9.5px] w-[1px] h-4 my-1 ${isDone ? 'bg-emerald-500/30' : 'bg-white/5'
                                    } transition-colors duration-500`} />
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Subtle Footer */}
            <div className="px-5 py-3 bg-black/20 border-t border-white/5 flex items-center justify-between">
                <span className="text-[9px] text-slate-600 font-medium uppercase tracking-[0.2em]">Research Intelligence Unit</span>
                <div className="flex gap-1">
                    {[1, 2, 3].map(i => (
                        <div key={i} className={`w-1 h-1 rounded-full ${isActive ? 'bg-brand-500/40 animate-pulse' : 'bg-slate-800'}`} style={{ animationDelay: `${i * 0.2}s` }} />
                    ))}
                </div>
            </div>
        </div>
    );
}
