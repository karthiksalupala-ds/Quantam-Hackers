import { CheckCircle2, Circle, Loader2, AlertCircle } from 'lucide-react';
import type { PipelineStep } from '../lib/types';
import { PIPELINE_STEPS } from '../lib/types';

interface ReasoningPipelineProps {
    steps: Record<string, PipelineStep>;
    isActive: boolean;
}

type StepStatus = 'pending' | 'running' | 'done' | 'error';

function StepIcon({ status }: { status: StepStatus }) {
    if (status === 'done') return <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />;
    if (status === 'running') return <Loader2 className="w-4 h-4 text-brand-400 flex-shrink-0 animate-spin" />;
    if (status === 'error') return <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />;
    return <Circle className="w-4 h-4 text-slate-600 flex-shrink-0" />;
}

export default function ReasoningPipeline({ steps, isActive }: ReasoningPipelineProps) {
    if (!isActive && Object.keys(steps).length === 0) return null;

    const doneCount = Object.values(steps).filter(s => s.status === 'done').length;
    const total = PIPELINE_STEPS.length;
    const progress = Math.round((doneCount / total) * 100);

    return (
        <div className="glass rounded-2xl p-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-brand-400 animate-pulse" />
                    <h3 className="font-semibold text-slate-200 text-sm">AI Reasoning Pipeline</h3>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500">{doneCount}/{total} steps</span>
                    <div className="w-20 h-1.5 rounded-full bg-white/5 overflow-hidden">
                        <div
                            className="h-full rounded-full bg-gradient-to-r from-brand-500 to-purple-500 transition-all duration-500"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                    <span className="text-xs font-mono text-brand-400">{progress}%</span>
                </div>
            </div>

            {/* Steps */}
            <div className="space-y-2">
                {PIPELINE_STEPS.map((def, idx) => {
                    const step = steps[def.id];
                    const status: StepStatus = step?.status ?? 'pending';
                    const isRunning = status === 'running';
                    const isDone = status === 'done';
                    const isRunnable = status !== 'pending';

                    // Connector line
                    const showConnector = idx < PIPELINE_STEPS.length - 1;

                    return (
                        <div key={def.id} className="relative">
                            <div
                                className={`flex items-start gap-3 p-3 rounded-xl transition-all duration-300 ${isRunning ? 'bg-brand-500/10 glow-border' :
                                        isDone ? 'bg-emerald-500/5' :
                                            isRunnable ? '' : 'opacity-40'
                                    }`}
                            >
                                {/* Step icon */}
                                <StepIcon status={status} />

                                {/* Content */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2">
                                        <span className="text-base leading-none">{def.icon}</span>
                                        <span
                                            className={`text-sm font-medium transition-colors ${isDone ? 'text-emerald-300' :
                                                    isRunning ? 'text-brand-300' :
                                                        isRunnable ? 'text-slate-300' :
                                                            'text-slate-600'
                                                }`}
                                        >
                                            {def.label}
                                        </span>
                                        {isDone && (
                                            <span className="text-[10px] text-emerald-500 font-mono uppercase tracking-wider">
                                                done
                                            </span>
                                        )}
                                        {isRunning && (
                                            <span className="text-[10px] text-brand-400 font-mono uppercase tracking-wider animate-pulse">
                                                running
                                            </span>
                                        )}
                                    </div>

                                    {/* Status message */}
                                    {step?.message && isRunnable && (
                                        <p className="mt-0.5 text-xs text-slate-500 truncate">{step.message}</p>
                                    )}
                                </div>
                            </div>

                            {/* Connector */}
                            {showConnector && (
                                <div className={`ml-[1.4rem] w-px h-1.5 ${isDone ? 'bg-emerald-500/30' : 'bg-white/5'}`} />
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
