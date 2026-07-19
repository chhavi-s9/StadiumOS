import { useEffect, useState } from "react";
import "./App.css";

// Dynamic API URL resolution (works on local dev & production Vercel/Render)
const rawEnvUrl = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");
const API = rawEnvUrl
  ? rawEnvUrl.endsWith("/api")
    ? rawEnvUrl
    : `${rawEnvUrl}/api`
  : "/api";

function App() {
  const [state, setState] = useState({});
  const [incidents, setIncidents] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [summary, setSummary] = useState("");
  const [zoneAnalysis, setZoneAnalysis] = useState(null);
  const [selectedZone, setSelectedZone] = useState("Z1");
  const [plan, setPlan] = useState([]);
  const [demoResult, setDemoResult] = useState(null);
  const [isOnline, setIsOnline] = useState(true);
  const [lastSync, setLastSync] = useState(new Date());
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);

  const zones = state.zones || [];
  const totalPopulation = zones.reduce((sum, z) => sum + (z.current_occupancy || 0), 0);

  async function fetchAPI(endpoint, setter) {
    try {
      const res = await fetch(API + endpoint);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setter(data);
      setIsOnline(true);
      setLastSync(new Date());
    } catch (err) {
      console.warn(`Fetch error for ${endpoint}:`, err);
      setIsOnline(false);
    }
  }

  useEffect(() => {
    fetchAPI("/state", setState);
    fetchAPI("/incidents", setIncidents);
    fetchAPI("/predictions", setPredictions);
    fetchPlan();

    const timer = setInterval(() => {
      fetchAPI("/state", setState);
      fetchAPI("/incidents", setIncidents);
    }, 4000);

    return () => clearInterval(timer);
  }, []);

  async function generateSummary() {
    setLoadingSummary(true);
    try {
      const res = await fetch(API + "/summary");
      const data = await res.json();
      setSummary(data.summary || "Summary generated successfully.");
    } catch (err) {
      setSummary("Failed to generate summary. Verify backend server.");
    } finally {
      setLoadingSummary(false);
    }
  }

  async function analyzeSelectedZone(zoneId = selectedZone) {
    setLoadingAnalysis(true);
    try {
      const res = await fetch(`${API}/zones/${zoneId}/analysis`);
      const data = await res.json();
      setZoneAnalysis(data);
    } catch (err) {
      setZoneAnalysis({ error: err.message });
    } finally {
      setLoadingAnalysis(false);
    }
  }

  async function fetchPlan() {
    try {
      const res = await fetch(API + "/plan");
      const data = await res.json();
      setPlan(data.actions || []);
    } catch (e) {
      setPlan([]);
    }
  }

  async function executeAction(action) {
    try {
      await fetch(API + "/actions/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(action),
      });
      fetchPlan();
      fetchAPI("/incidents", setIncidents);
    } catch (e) {
      console.error("Execute action failed:", e);
    }
  }

  async function runDemo() {
    try {
      const res = await fetch(API + "/demo/run", { method: "POST" });
      const data = await res.json();
      setDemoResult(data.timeline || []);
      fetchAPI("/state", setState);
      fetchPlan();
    } catch (e) {
      setDemoResult([{ error: e.message }]);
    }
  }

  const getCrowdLevelClass = (level = "LOW") => {
    switch (level.toUpperCase()) {
      case "CRITICAL": return "level-CRITICAL";
      case "HIGH": return "level-HIGH";
      case "MEDIUM": return "level-MEDIUM";
      default: return "level-LOW";
    }
  };

  const getProgressColor = (occupancy, capacity = 5000) => {
    const ratio = occupancy / capacity;
    if (ratio > 0.9) return "#ef4444";
    if (ratio > 0.7) return "#f43f5e";
    if (ratio > 0.4) return "#f59e0b";
    return "#10b981";
  };

  return (
    <div className="app-container">
      {/* Top Navigation / Brand Header */}
      <header className="app-header">
        <div className="brand">
          <div className="brand-icon">🏟️</div>
          <div className="brand-text">
            <h1>StadiumOS AI</h1>
            <p>Generative AI Stadium Operations Platform • FIFA 2026</p>
          </div>
        </div>

        <div className="header-status">
          <div className={`status-badge ${!isOnline ? "offline" : ""}`}>
            <span className="pulse-dot"></span>
            <span>{isOnline ? "SYSTEM ONLINE" : "RECONNECTING"}</span>
          </div>
          <div className="sync-time">
            Sync: {lastSync.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
          </div>
        </div>
      </header>

      {/* Top Metric Highlights */}
      <section className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon blue">👥</div>
          <div className="metric-info">
            <h4>Total Crowd Count</h4>
            <div className="value">{totalPopulation ? totalPopulation.toLocaleString() : "—"}</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon red">🚨</div>
          <div className="metric-info">
            <h4>Active Incidents</h4>
            <div className="value">{incidents.length}</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon purple">🔮</div>
          <div className="metric-info">
            <h4>Active Predictions</h4>
            <div className="value">{predictions.length}</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon green">⚡</div>
          <div className="metric-info">
            <h4>Active Zones</h4>
            <div className="value">{zones.length || 8}</div>
          </div>
        </div>
      </section>

      {/* Main Dashboard Layout */}
      <div className="dashboard-grid">
        {/* Left Primary Column */}
        <div className="main-column">
          {/* Interactive Zone Map / Grid */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <span>📍</span>
                <span>Stadium Zones & Real-Time Density</span>
              </div>
              <button className="btn-secondary" onClick={() => fetchAPI("/state", setState)}>
                Refresh Map
              </button>
            </div>

            <div className="zones-grid">
              {zones.length === 0 && (
                <div className="empty-state">Loading live zone metrics...</div>
              )}
              {zones.map((z) => {
                const occupancy = z.current_occupancy || 0;
                const capacity = z.capacity || 5000;
                const percent = Math.min(100, Math.round((occupancy / capacity) * 100));
                const level = z.crowd_level || "LOW";

                return (
                  <div
                    key={z.id}
                    className={`zone-card ${selectedZone === z.id ? "selected" : ""}`}
                    onClick={() => {
                      setSelectedZone(z.id);
                      analyzeSelectedZone(z.id);
                    }}
                  >
                    <div className="zone-header">
                      <span className="zone-name">{z.name || z.id}</span>
                      <span className={`zone-badge ${getCrowdLevelClass(level)}`}>
                        {level}
                      </span>
                    </div>

                    <div className="occupancy-info">
                      <span>{occupancy.toLocaleString()} / {capacity.toLocaleString()}</span>
                      <span>{percent}%</span>
                    </div>

                    <div className="progress-bar-bg">
                      <div
                        className="progress-bar-fill"
                        style={{
                          width: `${percent}%`,
                          backgroundColor: getProgressColor(occupancy, capacity),
                        }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* AI Planner Actions */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <span>🧭</span>
                <span>AI Live Operational Planner</span>
              </div>
              <div style={{ display: "flex", gap: "8px" }}>
                <button className="btn-secondary" onClick={fetchPlan}>
                  Fetch Plan
                </button>
                <button className="btn-primary" onClick={runDemo}>
                  ⚡ Run Crowd Surge Demo
                </button>
              </div>
            </div>

            <div className="plan-list">
              {plan.length === 0 && (
                <div className="empty-state">No automated safety actions needed at this time.</div>
              )}
              {plan.map((action, i) => (
                <div key={i} className={`plan-card ${action.priority || "info"}`}>
                  <div className="plan-content">
                    <div className="plan-meta">
                      <span className="priority-badge">{action.priority || "info"}</span>
                      {action.zone_id && <span className="priority-badge">{action.zone_id}</span>}
                    </div>
                    <div className="plan-message">{action.message}</div>
                  </div>
                  <button className="btn-action" onClick={() => executeAction(action)}>
                    Execute Action
                  </button>
                </div>
              ))}
            </div>

            {demoResult && (
              <div style={{ marginTop: "16px" }}>
                <h4 style={{ fontSize: "0.88rem", marginBottom: "8px", color: "var(--accent-blue)" }}>
                  Surge Simulation Timeline Log
                </h4>
                <pre style={{ fontSize: "0.78rem", maxHeight: "180px", overflow: "auto" }}>
                  {JSON.stringify(demoResult, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        {/* Right Side Column */}
        <div className="side-column">
          {/* AI Executive Summary */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <span>🤖</span>
                <span>AI Executive Summary</span>
              </div>
              <button className="btn-primary" onClick={generateSummary} disabled={loadingSummary}>
                {loadingSummary ? "Analyzing..." : "Generate Summary"}
              </button>
            </div>

            <div className="summary-box">
              {summary || "Click 'Generate Summary' for an AI analysis of stadium operations."}
            </div>
          </div>

          {/* Crowd Analysis Inspector */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <span>🔬</span>
                <span>Zone Inspector ({selectedZone})</span>
              </div>
              <button
                className="btn-secondary"
                onClick={() => analyzeSelectedZone(selectedZone)}
                disabled={loadingAnalysis}
              >
                {loadingAnalysis ? "Analyzing..." : "Analyze Zone"}
              </button>
            </div>

            {zoneAnalysis ? (
              zoneAnalysis.error ? (
                <div className="summary-box" style={{ color: "var(--accent-red)" }}>
                  Error: {zoneAnalysis.error}
                </div>
              ) : (
                <div className="analysis-box">
                  <div className="analysis-row">
                    <span className="muted">Target Zone:</span>
                    <strong>{zoneAnalysis.zone || selectedZone}</strong>
                  </div>
                  <div className="analysis-row">
                    <span className="muted">Crowd Density:</span>
                    <strong>
                      {zoneAnalysis.density != null
                        ? `${Math.round(zoneAnalysis.density * 100)}%`
                        : zoneAnalysis.predicted_crowd_density ?? "—"}
                    </strong>
                  </div>
                  <div className="analysis-row">
                    <span className="muted">Congestion Risk:</span>
                    <strong style={{ color: "var(--accent-amber)" }}>
                      {zoneAnalysis.congestion_risk || zoneAnalysis.congestion_probability || "Low"}
                    </strong>
                  </div>
                  <div className="analysis-row" style={{ flexDirection: "column", gap: "4px" }}>
                    <span className="muted">Recommendation:</span>
                    <span style={{ fontSize: "0.85rem", color: "#e2e8f0" }}>
                      {zoneAnalysis.recommendation || zoneAnalysis.reasoning || "Normal operations."}
                    </span>
                  </div>
                </div>
              )
            ) : (
              <div className="empty-state">Select a zone from the map to view deep crowd insights.</div>
            )}
          </div>

          {/* Live Incidents Feed */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <span>🚨</span>
                <span>Live Incidents Feed ({incidents.length})</span>
              </div>
            </div>

            <div className="incident-list">
              {incidents.length === 0 && (
                <div className="empty-state">No critical incidents reported.</div>
              )}
              {incidents.map((inc, i) => (
                <div key={i} className="incident-card">
                  <div className="incident-header">
                    <span className="incident-type">
                      {inc.type || inc.note || "Incident Alert"}
                    </span>
                    <span className="incident-zone">{inc.zone_id || "Zone Z1"}</span>
                  </div>
                  <div className="incident-desc">
                    {inc.description || inc.note || "Crowd surge / telemetry notice"}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;