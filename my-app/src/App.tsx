import { useState, useEffect } from 'react';
import ReactDiffViewer from 'react-diff-viewer-continued';

interface AgentSession {
  status: string;
  original_code: string;
  fixed_code: string;
  error: string;
  logs: string[];
}

function App() {
  const [session, setSession] = useState<AgentSession | null>(null);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);

 
  useEffect(() => {
    const checkLatest = async () => {
      try {
        const response = await fetch("http://localhost:8000/latest-session");
        const data = await response.json();
        
        // Only update if we found a new ID that isn't null
        if (data.session_id && data.session_id !== activeSessionId) {
          console.log("🚀 New session discovered:", data.session_id);
          setActiveSessionId(data.session_id);
        }
      } catch (err) {
        console.error("Discovery failed. Is FastAPI running?", err);
      }
    };

    const discoveryInterval = setInterval(checkLatest, 1500);
    return () => clearInterval(discoveryInterval);
  }, [activeSessionId]);


  useEffect(() => {
    let pollInterval: number;

    if (activeSessionId) {
      pollInterval = window.setInterval(async () => {
        try {
          const response = await fetch(`http://localhost:8000/session/${activeSessionId}`);
          const data = await response.json();
          setSession(data);
          
          
          if (data && data.status === "Ready for Review") {
            console.log("✅ Fix ready for review!");
            clearInterval(pollInterval);
          }
        } catch (err) {
          console.error("Polling failed:", err);
        }
      }, 1000);
    }

    return () => clearInterval(pollInterval);
  }, [activeSessionId]);

  return (
    <div style={{ padding: '40px', backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh', fontFamily: 'Inter, system-ui' }}>
      <header style={{ marginBottom: '30px', borderBottom: '1px solid #1e293b', paddingBottom: '20px' }}>
        <h1 style={{ fontSize: '24px', fontWeight: 'bold' }}>🤖 Agent Control Plane</h1>
        <p style={{ color: '#94a3b8' }}>Real-time autonomous debugging dashboard.</p>
      </header>

      {!session ? (
        <div style={{ textAlign: 'center', marginTop: '100px', border: '2px dashed #1e293b', padding: '50px', borderRadius: '15px' }}>
          <p style={{ color: '#64748b', fontSize: '18px' }}>📡 Listening for bug reports from <b>main.py</b>...</p>
          <small style={{ color: '#475569' }}>Save an error in buggy_code.py to trigger the agent.</small>
        </div>
      ) : (
        <main>
          <div style={{ display: 'grid', gridTemplateColumns: '350px 1fr', gap: '25px' }}>
            
            {/* LOGS PANEL */}
            <aside style={{ backgroundColor: '#1e293b', padding: '25px', borderRadius: '12px', border: '1px solid #334155' }}>
              <h3 style={{ fontSize: '14px', textTransform: 'uppercase', color: '#94a3b8', marginBottom: '20px' }}>Agent Activity</h3>
              <div style={{ marginBottom: '20px' }}>
                <span style={{ 
                  padding: '4px 10px', 
                  borderRadius: '20px', 
                  fontSize: '12px', 
                  backgroundColor: session.status === "Ready for Review" ? '#065f46' : '#1e3a8a',
                  color: session.status === "Ready for Review" ? '#34d399' : '#60a5fa'
                }}>
                  {session.status}
                </span>
              </div>
              <div style={{ height: '400px', overflowY: 'auto', backgroundColor: '#0f172a', padding: '15px', borderRadius: '8px', fontSize: '12px', lineHeight: '1.6' }}>
                {session.logs.map((log, i) => (
                  <div key={i} style={{ marginBottom: '10px', borderLeft: '2px solid #334155', paddingLeft: '10px' }}>
                    <span style={{ color: '#64748b' }}>[{new Date().toLocaleTimeString()}]</span><br/>
                    {log}
                  </div>
                ))}
              </div>
            </aside>

            {/* DIFF PANEL */}
            <section style={{ backgroundColor: '#1e293b', borderRadius: '12px', overflow: 'hidden', border: '1px solid #334155' }}>
              {session.fixed_code ? (
                <>
                  <ReactDiffViewer 
                    oldValue={session.original_code} 
                    newValue={session.fixed_code} 
                    splitView={true}
                    useDarkTheme={true}
                    leftTitle="Original (Buggy)"
                    rightTitle="Proposed Fix"
                  />
                  <div style={{ padding: '25px', textAlign: 'right', background: '#0f172a' }}>
                    <button 
                      style={{ 
                        padding: '12px 30px', 
                        backgroundColor: '#2563eb', 
                        color: 'white', 
                        border: 'none', 
                        borderRadius: '8px', 
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: '0.2s'
                      }}
                      onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#1d4ed8')}
                      onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#2563eb')}
                      onClick={() => alert("Deployment triggered to Docker Sandbox!")}
                    >
                      Approve & Deploy Fix
                    </button>
                  </div>
                </>
              ) : (
                <div style={{ padding: '150px', textAlign: 'center' }}>
                  <div className="spinner" style={{ border: '4px solid #1e293b', borderTop: '4px solid #3b82f6', borderRadius: '50%', width: '40px', height: '40px', margin: '0 auto 20px', animation: 'spin 1s linear infinite' }}></div>
                  <p style={{ color: '#94a3b8' }}>Agent is analyzing the error in the Docker sandbox...</p>
                </div>
              )}
            </section>
          </div>
        </main>
      )}

      {/* Basic Spinner Animation */}
      <style>{`
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}

export default App;