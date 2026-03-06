import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import AnalysisPage from './pages/AnalysisPage';

export default function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen">
                <Navbar />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/analysis" element={<AnalysisPage />} />
                </Routes>
            </div>
        </BrowserRouter>
    );
}
