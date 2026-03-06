import { FlaskConical, Github, BookOpen } from 'lucide-react';

export default function Navbar() {
    return (
        <nav className="sticky top-0 z-50 glass border-b border-white/5">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                {/* Logo */}
                <div className="flex items-center gap-3">
                    <div className="relative w-9 h-9">
                        <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center shadow-lg">
                            <FlaskConical className="w-5 h-5 text-white" />
                        </div>
                        <div className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-surface-900 animate-pulse-slow" />
                    </div>
                    <div>
                        <span className="font-bold text-lg tracking-tight gradient-text-blue">ResearchPilot</span>
                        <div className="text-[10px] text-slate-500 -mt-1 tracking-widest uppercase">AI Intelligence Engine</div>
                    </div>
                </div>

                {/* Nav links */}
                <div className="flex items-center gap-2">
                    <a
                        href="https://github.com/your-username/research-pilot" // TODO: Update this link
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-white/5 transition-all"
                    >
                        <Github className="w-4 h-4" />
                        <span className="hidden sm:inline">GitHub</span>
                    </a>
                    <a
                        href="http://localhost:8000/docs"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-white/5 transition-all"
                    >
                        <BookOpen className="w-4 h-4" />
                        <span className="hidden sm:inline">API Docs</span>
                    </a>
                    <div className="flex items-center gap-1.5 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10">
                        <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
                        <span className="text-xs text-emerald-400 font-medium">Live</span>
                    </div>
                </div>
            </div>
        </nav>
    );
}
