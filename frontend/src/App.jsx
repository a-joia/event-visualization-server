import Sidebar from './components/Sidebar';
import TestPage from './pages/TestPage.jsx';
import Topbar from './components/Topbar';
import DashboardWidgetsConfig from './pages/DashboardWidgetsConfig';
import EventWidgetsConfig from './pages/EventWidgetsConfig';
import EventAnalysisPage from './pages/EventAnalysisPage';
import EventAnalyticsPage from './pages/EventAnalyticsPage';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div style={{ display: 'flex', minHeight: '100vh', width: '100vw' }}>
        <Sidebar />
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
          <Topbar />
          <Routes>
            <Route path="/" element={<Navigate to="/events" replace />} />
            <Route path="/dashboard" element={<DashboardWidgetsConfig />} />
            <Route path="/events" element={<EventWidgetsConfig />} />
            <Route path="/analytics" element={<EventAnalyticsPage />} />
            <Route path="/event/:eventId" element={<EventAnalysisPage />} />            <Route path="/test-page" element={<TestPage />} />

          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
