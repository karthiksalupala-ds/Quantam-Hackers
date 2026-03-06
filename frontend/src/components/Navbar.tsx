import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FlaskConical, BookOpen, LogOut, User, Settings as SettingsIcon } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { AuthModal } from './AuthModal';
import { SettingsModal } from './SettingsModal';

export default function Navbar() {
    const { user, signOut } = useAuth();
    const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
    const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
    const navigate = useNavigate();

    const handleSignOut = async () => {
        await signOut();
        navigate('/');
    };

    return (
        <>
            <nav className="sticky top-0 z-40 glass border-b border-white/5">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    {/* Logo */}
                    <div className="flex items-center gap-3">
                        <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
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
                        </Link>
                    </div>

                    {/* Nav links */}
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => setIsSettingsModalOpen(true)}
                            className="p-2 rounded-xl text-slate-400 hover:text-brand-400 hover:bg-brand-500/10 transition-all border border-transparent hover:border-brand-500/20"
                            title="Settings"
                        >
                            <SettingsIcon className="w-5 h-5" />
                        </button>

                        <div className="flex items-center gap-2">
                            {user ? (
                                <div className="flex items-center gap-2 ml-2 border-l border-white/10 pl-2">
                                    <Link
                                        to="/profile"
                                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 transition-colors"
                                    >
                                        <User className="w-4 h-4" />
                                        <span className="hidden sm:inline">{user.email?.split('@')[0]}</span>
                                    </Link>
                                    <button
                                        onClick={handleSignOut}
                                        className="flex items-center gap-1.5 px-2 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                                        title="Sign Out"
                                    >
                                        <LogOut className="w-4 h-4" />
                                    </button>
                                </div>
                            ) : (
                                <div className="flex items-center ml-2 border-l border-white/10 pl-2">
                                    <button
                                        onClick={() => setIsAuthModalOpen(true)}
                                        className="px-4 py-1.5 rounded-lg text-sm font-medium text-white bg-brand-600 hover:bg-brand-500 shadow-lg shadow-brand-500/20 transition-all border border-brand-500/50 hover:border-brand-400"
                                    >
                                        Sign In
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </nav>

            <SettingsModal
                isOpen={isSettingsModalOpen}
                onClose={() => setIsSettingsModalOpen(false)}
            />

            <AuthModal
                isOpen={isAuthModalOpen}
                onClose={() => setIsAuthModalOpen(false)}
            />
        </>
    );
}
