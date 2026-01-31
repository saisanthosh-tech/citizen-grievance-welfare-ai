import React, { useState, useEffect } from 'react';
import api from './api';
import './App.css';
import { LayoutDashboard, FileText, Activity } from 'lucide-react';

function App() {
  const [grievances, setGrievances] = useState([]);
  const [form, setForm] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchGrievances();
  }, []);

  const fetchGrievances = async () => {
    try {
      const response = await api.get('/grievances/');
      setGrievances(response.data);
    } catch (error) {
      console.error('Error fetching grievances:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/grievances/', form);
      setForm({ title: '', description: '' });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      fetchGrievances();
    } catch (error) {
      console.error('Error submitting grievance:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo-section">
          <Activity className="icon-primary" />
          <h1>Citizen Grievance Intel</h1>
        </div>
        <nav className="main-nav">
          <a href="#" className="nav-link active">Dashboard</a>
          <a href="#" className="nav-link">Reports</a>
        </nav>
      </header>

      <main className="main-content">
        <div className="hero-section">
          <h2>Voice Your Concerns, <span className="highlight">We Listen & Act.</span></h2>
          <p>An AI-powered platform to bridge the gap between citizens and the government. Submit your grievance and get instant welfare recommendations.</p>
        </div>

        <div className="layout-grid">

          {/* Left Column: Form */}
          <section className="form-section">
            <div className="card">
              <h2 className="card-title">
                <FileText className="icon-secondary" />
                New Grievance
              </h2>
              <form onSubmit={handleSubmit} className="grievance-form">
                {success && (
                  <div className="success-alert">
                    🎉 Grievance submitted successfully! AI analysis complete.
                  </div>
                )}
                <div className="form-group">
                  <label>Title</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g., Water shortage in Sector 4"
                    value={form.title}
                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    required
                    rows={4}
                    placeholder="Describe the issue in detail..."
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                  />
                </div>
                <button type="submit" disabled={loading} className="btn-primary">
                  {loading ? 'Submitting...' : 'Submit Grievance'}
                </button>
              </form>
            </div>

            <div className="info-card">
              <h3>✨ AI-Powered Insights</h3>
              <p>Our intelligent system automatically analyzes your grievance to:</p>
              <ul style={{ paddingLeft: '1.2rem', marginTop: '0.5rem', fontSize: '0.9rem', color: '#4338ca' }}>
                <li>Classify the issue category.</li>
                <li>Detect urgency and assign priority.</li>
                <li>Recommend relevant government schemes.</li>
              </ul>
            </div>
          </section>

          {/* Right Column: Dashboard & List */}
          <section className="dashboard-section">
            <div className="stats-grid">
              <div className="card stat-card">
                <span className="stat-label">Total Grievances</span>
                <span className="stat-value">{grievances.length}</span>
              </div>
              <div className="card stat-card">
                <span className="stat-label">Clearance Rate</span>
                <span className="stat-value text-success">0%</span>
              </div>
            </div>

            <div className="card list-card">
              <div className="card-header">
                <h2 className="card-title">
                  <LayoutDashboard className="icon-secondary" />
                  Recent Grievances
                </h2>
              </div>
              <div className="grievance-list">
                {grievances.length === 0 ? (
                  <div className="empty-state">No grievances found.</div>
                ) : (
                  grievances.map((g) => (
                    <div key={g.id} className="grievance-item">
                      <div className="grievance-header">
                        <h3 className="grievance-title">{g.title}</h3>
                        <span className={`badge ${g.priority?.toLowerCase() || 'medium'}`}>
                          {g.priority || 'Normal'}
                        </span>
                      </div>
                      <p className="grievance-desc">{g.description}</p>
                      <div className="grievance-meta">
                        <span className="category-tag">{g.category || 'Uncategorized'}</span>
                        <span>{new Date(g.created_at).toLocaleDateString()}</span>
                      </div>
                      {g.suggested_schemes && g.suggested_schemes.length > 0 && (
                        <div className="schemes-list">
                          <strong>Suggested Welfare Schemes:</strong>
                          <ul>
                            {g.suggested_schemes.map((scheme, idx) => (
                              <li key={idx}>{scheme}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          </section>

        </div>
      </main>
    </div>
  );
}

export default App;
