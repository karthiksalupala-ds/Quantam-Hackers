// API client – communicates with the FastAPI backend via SSE streaming

import type { AnalysisResult, PipelineStep, ResearchRequest } from './types';

const API_BASE = '/api';

export type OnStep = (step: PipelineStep) => void;
export type OnResult = (result: AnalysisResult) => void;
export type OnError = (message: string) => void;
export type OnDone = () => void;

/**
 * Submit a research query and stream back pipeline step events + final result.
 * Returns a cleanup function that aborts the stream.
 */
export function analyzeResearch(
    request: ResearchRequest,
    onStep: OnStep,
    onResult: OnResult,
    onError: OnError,
    onDone: OnDone,
): () => void {
    const controller = new AbortController();

    (async () => {
        try {
            const response = await fetch(`${API_BASE}/research/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(request),
                signal: controller.signal,
            });

            if (!response.ok) {
                const errText = await response.text();
                onError(`Server error ${response.status}: ${errText}`);
                onDone();
                return;
            }

            const reader = response.body?.getReader();
            if (!reader) { onError('No response stream.'); onDone(); return; }

            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() ?? '';

                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed.startsWith('data:')) continue;

                    const jsonStr = trimmed.slice(5).trim();
                    if (!jsonStr) continue;

                    try {
                        const event = JSON.parse(jsonStr) as { event: string; data: unknown };
                        if (event.event === 'step') onStep(event.data as PipelineStep);
                        if (event.event === 'result') onResult(event.data as AnalysisResult);
                        if (event.event === 'error') onError((event.data as { message: string }).message);
                        if (event.event === 'done') onDone();
                    } catch {
                        // skip malformed event
                    }
                }
            }
        } catch (err: unknown) {
            if (err instanceof Error && err.name === 'AbortError') return;
            onError(err instanceof Error ? err.message : 'Unknown error occurred');
            onDone();
        }
    })();

    return () => controller.abort();
}

/** Fetch recent query history */
export async function fetchQueryHistory(): Promise<unknown[]> {
    const res = await fetch(`${API_BASE}/queries/`);
    if (!res.ok) return [];
    return res.json();
}

/** Fetch stored papers */
export async function fetchPapers(source?: string): Promise<unknown[]> {
    const url = source ? `${API_BASE}/papers/?source=${source}` : `${API_BASE}/papers/`;
    const res = await fetch(url);
    if (!res.ok) return [];
    return res.json();
}
